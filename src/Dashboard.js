import React from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import TopBar from "./components/TopBar";
import About from "./sections/About";
import Workspace from "./sections/Workspace";
import History from "./sections/History";
import Results from "./sections/Results";

const Dashboard = () => {
    const resultsData = []; // Replace with fetched or computed data if available

    return (
        <div className="dashboard-container">
            <TopBar />
            <Routes>
                {/* Redirect default "/" route to About */}
                <Route path="/" element={<Navigate to="/about" />} />
                <Route path="/about" element={<About />} />
                <Route path="/workspace" element={<Workspace />} />
                <Route path="/history" element={<History />} />
                <Route path="/results" element={<Results title="Results" data={resultsData} />} />
                {/* Fallback for unmatched routes */}
                <Route path="*" element={<div>Page Not Found</div>} />
            </Routes>
        </div>
    );
};

export default Dashboard;
