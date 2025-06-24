# Green_Finance_Optimization
ESG-Driven Fund Allocation and Engagement Platform
![License: Proprietary](https://img.shields.io/badge/license-Proprietary-red)

Gree Finance Optimization e is a machine learning–powered platform that enables investors and institutions to make data-driven, ESG-aligned capital allocation decisions. It combines predictive modeling, optimization algorithms, and interactive engagement tools to support sustainable finance with transparency and impact.

---

## Overview

Green Finance Optimization  evaluates the Environmental, Social, and Governance (ESG) performance of sustainability-related projects using time-series indicators, predicts future ESG scores and risk factors, and optimally allocates investment funds based on budget and impact potential.

This platform also features educational and interactive components, making it accessible and engaging for both institutional users and ESG-curious individuals.


## Key Features

### 1. ESG Score & Risk Prediction
- Uses Random Forest models to forecast ESG scores and risk factors based on historical data.
- Supports multi-year, multi-project forecasting across countries and sectors.

### 2. Optimization Engine
- Applies MILP (Mixed Integer Linear Programming) using PuLP to determine optimal fund distribution.
- Objective: Maximize ESG-adjusted impact under a budget constraint.
- Supports filtering by project type or category.

### 3. NLP Insights (optional modules)
- Leverages FinBERT-ESG for project sentiment analysis by ESG pillar.
- Generates natural-language summaries using a T5-based model for interpretability.

### 4. User Dashboard (Frontend)
- Clean and responsive React UI with multiple functional sections:
  - **Home**: Platform mission, ESG awareness, and introductory walkthrough
  - **Work**: Upload CSV data, enter budget, run models, and receive results
  - **History**: View previously executed allocations and outcomes
  - **Quiz**: Interactive ESG quiz with gamified rewards (Xbox-style badge system)

---

## How It Works

1. Upload a structured CSV file containing ESG indicators by year, country, and series.
2. The backend:
   - Cleans and transforms the data
   - Predicts ESG scores and project-specific risk
   - Allocates budget using MILP optimization
3. Results include a ranked list of projects selected for funding along with ESG and risk metrics.

---

## Backend Stack

| Component     | Technologies Used                                  |
|---------------|----------------------------------------------------|
| Data Handling | Pandas, NumPy                                      |
| ML Models     | scikit-learn (RandomForestRegressor), Transformers |
| Optimization  | PuLP (MILP solver for allocation)                  |
| NLP Modules   | FinBERT-ESG, T5-small                              |
| Framework     | Flask (REST endpoints)                             |

---

## Frontend Stack

| Component     | Technologies Used      |
|---------------|------------------------|
| Framework     | React.js               |
| Design        | Responsive CSS, Flexbox/Grid |
| UI Structure  | Page-based (Home, Work, History, Quiz) |

---

## Demo & Media

Visual previews and walkthrough video are available in the main directory as image files :
eg: HOMEpage.png
ESGinfoCard1.pnh


> These assets demonstrate the full user flow — from uploading data to viewing optimized fund allocations.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However, we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify
This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
