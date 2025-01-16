import React, { useState, useEffect } from "react";
import { Bar, Pie } from "react-chartjs-2";
import { Chart, registerables } from "chart.js";
import axios from "axios";
import "./Workspace.css";
import Summary from "../components/Summary";
import FileUpload from "../components/FileUpload";

// Register Chart.js components
Chart.register(...registerables);

const Workspace = () => {
    const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

    const [budget, setBudget] = useState(1000);
    const [projectSeries, setProjectSeries] = useState("All Projects");
    const [predictions, setPredictions] = useState(null);
    const [allocation, setAllocation] = useState(null);
    const [loading, setLoading] = useState({ prediction: false, allocation: false, series: false });
    const [error, setError] = useState("");
    const [projectSeriesOptions, setProjectSeriesOptions] = useState(["All Projects"]);

    // Fetch dynamic project series options from backend
    useEffect(() => {
        const fetchProjectSeries = async () => {
            setLoading((prev) => ({ ...prev, series: true }));
            try {
                const response = await axios.get(`${API_URL}/project-series`);
                if (response.data.series) {
                    setProjectSeriesOptions(["All Projects", ...response.data.series]);
                } else {
                    setError("No project series data found.");
                }
            } catch (error) {
                console.error("Error fetching project series:", error);
                setError("Failed to fetch project series. Please ensure the backend is running.");
            } finally {
                setLoading((prev) => ({ ...prev, series: false }));
            }
        };
        fetchProjectSeries();
    }, [API_URL]);

    const handlePrediction = async () => {
        setLoading((prev) => ({ ...prev, prediction: true }));
        setPredictions(null);
        setError("");
        try {
            const response = await axios.post(`${API_URL}/predict-esg`, {
                project_series: projectSeries, // Pass selected series
            });
            if (response.data.predictions) {
                setPredictions(response.data.predictions);
            } else {
                setError("No predictions returned from the backend.");
            }
        } catch (error) {
            console.error("Error predicting ESG:", error);
            setError(error.response?.data?.error || "Failed to fetch ESG predictions. Please try again.");
        } finally {
            setLoading((prev) => ({ ...prev, prediction: false }));
        }
    };

    const handleBudgetAllocation = async () => {
        if (!predictions || predictions.length === 0) {
            setError("No predictions found. Please run ESG predictions first.");
            return;
        }

        const preparedPredictions = predictions.map((pred) => ({
            ...pred,
            "Series Name": pred["Series Name"] || "Unknown", // Default to "Unknown" if missing
            Cost: pred.Cost || 0, // Default to 0 if missing
            "Predicted ESG Score": pred["Predicted ESG Score"] || 0, // Default to 0 if missing
            RiskFactor: pred.RiskFactor || "Unknown", // Default to "Unknown" if missing
        }));

        setLoading((prev) => ({ ...prev, allocation: true }));
        setAllocation(null);
        setError("");
        try {
            const response = await axios.post(`${API_URL}/allocate-budget`, {
                budget, // Value from slider
                project_series: projectSeries, // Dropdown value
                predictions: preparedPredictions, // Pass cleaned predictions
            });

            if (response.data.allocated_projects) {
                setAllocation(response.data.allocated_projects);
            } else {
                setError("No allocation data returned from the backend.");
            }
        } catch (error) {
            console.error("Error allocating budget:", error);
            setError(error.response?.data?.error || "Failed to allocate budget. Please try again.");
        } finally {
            setLoading((prev) => ({ ...prev, allocation: false }));
        }
    };

    // Generate dynamic colors for charts
    const generateColors = (count) =>
        Array.from({ length: count }, () => `#${Math.floor(Math.random() * 16777215).toString(16)}`);

    // Chart data for predictions
    const predictionChartData = predictions && {
        labels: predictions.map((pred) => pred["Series Name"] || "Unknown"),
        datasets: [
            {
                label: "Predicted ESG Score",
                data: predictions.map((pred) => pred["Predicted ESG Score"] || 0),
                backgroundColor: "rgba(75, 192, 192, 0.6)",
            },
        ],
    };

    // Chart data for budget allocation
    const allocationChartData = allocation && {
        labels: allocation.map((alloc) => alloc.Project || "Unknown"),
        datasets: [
            {
                data: allocation.map((alloc) => alloc.Cost || 0),
                backgroundColor: generateColors(allocation.length),
            },
        ],
    };

    // Summarized data for predictions
    const predictionSummary = predictions?.map((pred) => ({
        Project: pred["Series Name"],
        ESGScore: pred["Predicted ESG Score"],
    }));

    // Summarized data for budget allocation
    const allocationSummary = allocation?.map((alloc) => ({
        Project: alloc.Project,
        Cost: `$${alloc.Cost}`,
        ESGScore: alloc.ESGScore,
        RiskFactor: alloc.RiskFactor,
    }));

    return (
        <div className="workspace-container">
            <h2>Green Finance Optimization</h2>
            <p>Upload your datasets and explore ESG evaluations and visual insights.</p>

            {/* Include the FileUpload Component */}
            <FileUpload />

            {/* Input Section */}
            <div className="input-section">
                <label htmlFor="budget">Budget:</label>
                <input
                    id="budget"
                    type="range"
                    min="100"
                    max="5000"
                    step="100"
                    value={budget}
                    onChange={(e) => setBudget(Number(e.target.value))}
                />
                <span>${budget}</span>
                <label htmlFor="project-series">Project Series:</label>
                {loading.series ? (
                    <p>Loading project series...</p>
                ) : (
                    <select
                        id="project-series"
                        value={projectSeries}
                        onChange={(e) => setProjectSeries(e.target.value)}
                    >
                        {projectSeriesOptions.map((series, index) => (
                            <option key={index} value={series}>
                                {series}
                            </option>
                        ))}
                    </select>
                )}
            </div>

            {/* Action Buttons */}
            <div className="action-buttons">
                <button
                    onClick={handlePrediction}
                    disabled={loading.prediction}
                    className="action-button"
                >
                    {loading.prediction ? "Predicting ESG..." : "Run ESG Predictions"}
                </button>
                <button
                    onClick={handleBudgetAllocation}
                    disabled={loading.allocation}
                    className="action-button"
                >
                    {loading.allocation ? "Allocating Budget..." : "Allocate Budget"}
                </button>
            </div>

            {/* Error Message */}
            {error && <p className="error-message">{error}</p>}

            {/* Prediction Summary */}
            {predictions && <Summary title="Predictions Summary" data={predictionSummary} />}

            {/* Prediction Chart */}
            {predictions && (
                <div className="predictions-section">
                    <h3>Predictions</h3>
                    <div className="chart-container">
                        <Bar
                            data={predictionChartData}
                            options={{
                                maintainAspectRatio: true,
                                responsive: true,
                                plugins: {
                                    tooltip: {
                                        callbacks: {
                                            label: function (context) {
                                                return `ESG Score: ${context.raw}`;
                                            },
                                        },
                                    },
                                },
                            }}
                        />
                    </div>
                </div>
            )}

            {/* Allocation Summary */}
            {allocation && <Summary title="Allocation Summary" data={allocationSummary} />}

            {/* Allocation Chart */}
            {allocation && (
                <div className="allocation-section">
                    <h3>Budget Allocation</h3>
                    <div className="chart-container">
                        <Pie
                            data={allocationChartData}
                            options={{
                                maintainAspectRatio: true,
                                responsive: true,
                                plugins: {
                                    tooltip: {
                                        callbacks: {
                                            label: function (context) {
                                                const alloc = allocation[context.dataIndex];
                                                return `Cost: $${alloc.Cost}, ESG: ${alloc.ESGScore}, Risk: ${alloc.RiskFactor}`;
                                            },
                                        },
                                    },
                                },
                            }}
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default Workspace;
