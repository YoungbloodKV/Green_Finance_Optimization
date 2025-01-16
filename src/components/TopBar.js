import React from 'react';
import './TopBar.css';

const TopBar = () => {
    return (
        <header className="topbar">
            <div className="logo-container">
                {/* Add logo image */}
                <img src="/logo.png" alt="Site Logo" className="site-logo" />
                <h1 className="site-name">Green Finance Optimization</h1>
            </div>
            <nav className="navigation">
                <ul>
                    <li><a href="/about" className="nav-link">About</a></li>
                    <li><a href="/workspace" className="nav-link">Workspace</a></li>
                    <li><a href="/history" className="nav-link">History</a></li>
                    <li><a href="/Test yourself" className="nav-link">Test Yourself</a></li>
                </ul>
            </nav>
        </header>
    );
};

export default TopBar;
