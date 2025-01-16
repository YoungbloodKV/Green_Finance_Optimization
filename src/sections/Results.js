import React, { useState } from "react";
import "./Results.css"; // Create a CSS file for custom styling

const Results = ({ title, data }) => {
    const [currentPage, setCurrentPage] = useState(1);
    const rowsPerPage = 10;

    if (!data || data.length === 0) {
        return (
            <div className="empty-results">
                <p>No {title.toLowerCase()} available.</p>
                {/* Optional illustration */}
            </div>
        );
    }

    // Pagination logic
    const totalPages = Math.ceil(data.length / rowsPerPage);
    const paginatedData = data.slice(
        (currentPage - 1) * rowsPerPage,
        currentPage * rowsPerPage
    );

    const handleExportCSV = () => {
        const csvContent =
            "data:text/csv;charset=utf-8," +
            [Object.keys(data[0]).join(","), ...data.map((row) => Object.values(row).join(","))].join("\n");
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `${title.toLowerCase().replace(/\s/g, "_")}_results.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="results-container">
            <h3>{title}</h3>
            <button className="export-button" onClick={handleExportCSV}>
                Export to CSV
            </button>
            <table className="results-table">
                <thead>
                    <tr>
                        {Object.keys(data[0]).map((key, index) => (
                            <th key={index}>{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {paginatedData.map((item, rowIndex) => (
                        <tr key={rowIndex}>
                            {Object.values(item).map((value, colIndex) => (
                                <td key={colIndex}>{value}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Pagination Controls */}
            <div className="pagination">
                <button
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <span>
                    Page {currentPage} of {totalPages}
                </span>
                <button
                    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    );
};

export default Results;