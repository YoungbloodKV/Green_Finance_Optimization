import React from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';

const ChartComponent = ({ chartType, data, options }) => {
    // Select chart type dynamically
    const ChartType = {
        bar: Bar,
        line: Line,
        pie: Pie,
    }[chartType.toLowerCase()] || Bar;

    return (
        <div className="chart-container">
            <h3>{`${chartType} Chart`}</h3>
            <ChartType data={data} options={options} />
        </div>
    );
};

export default ChartComponent;
