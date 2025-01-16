import React, { useEffect } from 'react';
import './About.css';
import AOS from 'aos';
import 'aos/dist/aos.css';

const About = () => {
    useEffect(() => {
        AOS.init({ duration: 1200 });
    }, []);

    return (
        <div className="about-container">
            <div className="content-wrapper">
                <h1 className="about-heading">Green Finance Optimization Platform</h1>
                <p className="about-description">
                    Welcome to the <strong>Green Finance Optimization Platform</strong>, designed to revolutionize the way financial institutions evaluate sustainable projects. By leveraging AI and ESG (Environmental, Social, and Governance) scoring, this platform empowers users to make informed, impactful investment decisions.
                </p>
                <p className="about-description">
                    Explore the platform to upload datasets, predict ESG scores, allocate budgets, and visualize data dynamically. Together, we can contribute to a sustainable future.
                </p>
            </div>

            {/* Why ESG Matters Section */}
            <div className="why-esg-section">
                <h2 data-aos="fade-up">Why ESG Matters</h2>
                <p className="why-esg-intro" data-aos="fade-up">
                    ESG (Environmental, Social, and Governance) investing is more than just a trend; it’s a critical approach for addressing global challenges like climate change, social inequality, and corporate accountability. Companies with strong ESG performance often show better long-term stability and reduced risks.
                </p>
                <div className="why-esg-cards">
                    <div className="why-esg-card" data-aos="fade-up">
                        <h3>Environmental Impact</h3>
                        <p>Protect natural resources, reduce emissions, and support renewable energy initiatives.</p>
                    </div>
                    <div className="why-esg-card" data-aos="fade-up" data-aos-delay="200">
                        <h3>Social Responsibility</h3>
                        <p>Promote diversity, improve employee well-being, and contribute to societal growth.</p>
                    </div>
                    <div className="why-esg-card" data-aos="fade-up" data-aos-delay="400">
                        <h3>Strong Governance</h3>
                        <p>Encourage transparency, reduce corruption, and ensure accountability in leadership.</p>
                    </div>
                </div>
            </div>

            {/* ESG Cards Section */}
            <div className="esg-cards">
                {/* Environmental (E) Card */}
                <div className="esg-card">
                    <img src="/environment.png" alt="Environmental" className="esg-card-image" />
                    <div className="esg-card-content">
                        <h2>Environmental (E)</h2>
                        <p>
                            The environmental component of ESG focuses on a company’s impact on the planet. It includes
                            considerations like energy efficiency, waste management, carbon emissions, and sustainability
                            initiatives. Organizations are encouraged to adopt green practices to mitigate climate change.
                        </p>
                    </div>
                </div>

                {/* Social (S) Card */}
                <div className="esg-card">
                    <img src="/social.png" alt="Social" className="esg-card-image" />
                    <div className="esg-card-content">
                        <h2>Social (S)</h2>
                        <p>
                            The social component evaluates how an organization manages relationships with employees,
                            suppliers, customers, and the communities where it operates. This includes labor practices,
                            diversity, workplace safety, and contributions to societal well-being.
                        </p>
                    </div>
                </div>

                {/* Governance (G) Card */}
                <div className="esg-card">
                    <img src="/governance.png" alt="Governance" className="esg-card-image" />
                    <div className="esg-card-content">
                        <h2>Governance (G)</h2>
                        <p>
                            Governance refers to how an organization is led and managed. It examines leadership,
                            executive pay, audits, internal controls, shareholder rights, and ethical business practices.
                            Strong governance promotes accountability and transparency in corporate operations.
                        </p>
                    </div>
                </div>
            </div>

            <footer className="about-footer">
                <p>Contact us at: <strong>contact@greenfinance.com</strong></p>
                <p>Source of data: <strong>World Bank</strong>, <strong>UNEP</strong></p>
                <p>&copy; 2025 Green Finance Platform. All rights reserved.</p>
                <div className="team-credits">
                    <h4>Meet the Team</h4>
                    <ul>
                        <li>KEERTHIVASAN S</li>
                        <li>CRB KAMESH</li>
                        <li>SELVIBALA</li>
                        <li>QUEEN JERRY</li>
                    </ul>
                </div>
            </footer>
        </div>
    );
};

export default About;