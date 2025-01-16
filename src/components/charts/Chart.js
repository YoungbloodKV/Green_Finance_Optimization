import React from 'react';
import { Bar } from 'react-chartjs-2';

const Chart = ({ data }) => {
    const chartData = {
        labels: Object.keys(data['mean']), // Example: Column names
        datasets: [
            {
                label: 'Mean Values',
                data: Object.values(data['mean']), // Example: Mean values
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
        ],
    };

    return (
        <div>
            <h3>Visualization</h3>
            <Bar data={chartData} />
        </div>
    );
};

export default Chart;
