import React from "react";
import PropTypes from "prop-types";
import "./Summary.css";

const Summary = ({ title, data }) => {
    if (!data || data.length === 0) {
        return (
            <div className="summary-container">
                <h3>{title}</h3>
                <p>No data available to summarize.</p>
            </div>
        );
    }

    return (
        <div className="summary-container">
            <h3>{title}</h3>
            <ul className="summary-list">
                {data.map((item, index) => (
                    <li key={index} className="summary-item">
                        {Object.entries(item).map(([key, value]) => (
                            <p key={key}>
                                <strong>{key}:</strong> {value}
                            </p>
                        ))}
                    </li>
                ))}
            </ul>
        </div>
    );
};

Summary.propTypes = {
    title: PropTypes.string.isRequired,
    data: PropTypes.arrayOf(PropTypes.object).isRequired,
};

export default Summary;