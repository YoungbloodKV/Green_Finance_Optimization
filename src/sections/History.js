import React, { useState } from "react";
import "./History.css";
import { Bar, Pie } from "react-chartjs-2";

const mockHistory = [
    {
        datasetName: "Project_Data_1.csv",
        status: "Completed",
        dateProcessed: "2025-01-05",
        fundingAmount: 1000000,
        description: "Renewable energy project funding.",
        successRate: 85,
    },
    {
        datasetName: "Region_Analysis.csv",
        status: "Pending",
        dateProcessed: "2025-01-06",
        fundingAmount: 500000,
        description: "Regional impact analysis for sustainability.",
        successRate: 0,
    },
    {
        datasetName: "Climate_Study_2025.csv",
        status: "Completed",
        dateProcessed: "2025-01-04",
        fundingAmount: 750000,
        description: "Climate change adaptation study.",
        successRate: 92,
    },
    {
        datasetName: "ESG_Scores_Q4.csv",
        status: "Completed",
        dateProcessed: "2025-01-02",
        fundingAmount: 1250000,
        description: "Quarterly ESG evaluation for green bonds.",
        successRate: 95,
    },
];

const History = () => {
    const [history] = useState(mockHistory);
    const [showCharts, setShowCharts] = useState(false);

    // Data for Bar Chart: Funding Trend
    const barData = {
        labels: history.map((entry) => entry.dateProcessed),
        datasets: [
            {
                label: "Funding Amount ($)",
                data: history.map((entry) => entry.fundingAmount),
                backgroundColor: "rgba(75, 192, 192, 0.6)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1,
            },
        ],
    };

    // Data for Pie Chart: Status Proportion
    const pieData = {
        labels: ["Completed", "Pending"],
        datasets: [
            {
                data: [
                    history.filter((entry) => entry.status === "Completed").length,
                    history.filter((entry) => entry.status === "Pending").length,
                ],
                backgroundColor: ["#4caf50", "#f44336"],
                borderColor: ["#388e3c", "#d32f2f"],
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="history-container">
            <h2>History</h2>
            <p>Track processed datasets and gain valuable insights into ESG evaluations.</p>

            {/* Button to Toggle Chart View */}
            <div className="chart-toggle">
                <button onClick={() => setShowCharts(!showCharts)}>
                    {showCharts ? "Hide Insight Charts" : "View Insight Charts"}
                </button>
            </div>

            {/* Fixed Chart Section */}
            {showCharts && (
                <div className="charts-fixed">
                    <div className="chart-section">
                        <h3>Funding Trend</h3>
                        <Bar 
                            data={barData} 
                            options={{
                                responsive: true,
                                maintainAspectRatio: true,
                            }}
                            height={200} // Adjusted height for a smaller size
                            width={400} // Adjusted width for a smaller size
                        />
                    </div>
                    <div className="chart-section">
                        <h3>Dataset Status</h3>
                        <Pie 
                            data={pieData} 
                            options={{
                                responsive: true,
                                maintainAspectRatio: true,
                            }}
                            height={200}
                            width={200}
                        />
                    </div>
                </div>
            )}

            {/* History Table */}
            {!showCharts && (
                <table className="history-table">
                    <thead>
                        <tr>
                            <th>Dataset Name</th>
                            <th>Status</th>
                            <th>Date Processed</th>
                            <th>Funding Amount ($)</th>
                            <th>Success Rate (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.map((entry, index) => (
                            <tr key={index}>
                                <td>{entry.datasetName}</td>
                                <td>{entry.status}</td>
                                <td>{entry.dateProcessed}</td>
                                <td>${entry.fundingAmount.toLocaleString()}</td>
                                <td>{entry.successRate || "N/A"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default History;
