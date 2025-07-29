\# Dashboard Usage Guide



\## Overview

\- File: `src/app.py` (Streamlit app).

\- Fetches bill data via `src/data\_fetch.py` (Congress API).

\- Predicts using loaded models from `models/`.



\## Running the App

1\. Install deps: `pip install streamlit pandas numpy scikit-learn joblib requests plotly`.

2\. Run: `streamlit run src/app.py`.

3\. Input: Bill number (e.g., 1234), type (HR/S), Congress (118).

4\. Output: Details, metrics, timeline, predictions with confidence.



\## Features

\- Bill Verification: Title, sponsor, status.

\- Metrics: Days active, actions, cosponsors, bipartisan.

\- Timeline: Action table (paginated for long histories).

\- Predictions: Viability/Passage scores with gauges, confidence intervals.

\- Breakdown: Model agreement, feature importance (optional).

\- Recommendations: Strategic tips based on scores.



Deploy: Use Streamlit Sharing for public access.

