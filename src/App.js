import React from "react";
import Dashboard from "./Dashboard"; // Import the Dashboard component
import { BrowserRouter as Router } from "react-router-dom";

function App() {
    return (
        <Router> {/* Wrap the Dashboard in Router */}
            <div className="App">
                <Dashboard /> {/* Render the Dashboard component */}
            </div>
        </Router>
    );
}

export default App;