# Project Report: Predictive Bill Tracker Dashboard

## 1. Problem Statement and Motivation
The U.S. legislative process is complex and opaque, with thousands of bills introduced each Congress session, but only ~1-2% becoming law. Citizens, advocates, and even policymakers struggle to track bill progress, predict outcomes, and understand influencing factors. This leads to low civic engagement and inefficient advocacy.

This project addresses this by creating an AI-powered dashboard that:
- Tracks bills in real-time.
- Predicts viability (traction potential) and passage probability with confidence intervals.
- Provides actionable insights (e.g., bipartisan support needs).

Motivation: Enhance transparency and participation, aligning with SVCAF's goals for civic education in Chinese-American communities and beyond.

## 2. Approach and Methodologies
### Data Acquisition
- Used Congress.gov API to fetch ~6,000 bills from the 118th Congress (HR, S, HJRES, SJRES).
- Notebooks: `data/extract_118th_congress.ipynb` (API fetching), `data/combine_and_preprocess.ipynb` (merging, failure identification).
- Features extracted: Sponsors, cosponsors, actions, committees, subjects, timelines.
- Outcomes: Labeled bills as passed/failed based on actions; created 'viable' target for bills with traction.

### Data Preprocessing
- Handled missing data, encoded categoricals (e.g., party, policy area).
- Engineered features: Bipartisan score, activity rate, support velocity, etc.
- Datasets: Full (~16K bills post-processing), training with outcomes.
- Ethical note: Used public data; no personal info.

### AI Techniques
- **Dual-Stage Prediction**:
  - Viability: Binary classification (20% positive class) – predicts if bill gains traction.
  - Passage: On viable bills, predicts final success (8% positive).
- **Models**: Ensemble (RF + GB + LR) with isotonic calibration for imbalanced data.
- **Time-Aware**: Separate models for new (<1 day), early (1-30 days), progressive (>30 days) bills, using progressive feature sets.
- Notebook: `models/model.ipynb` – Trains, evaluates, saves models.
- Evaluation: ROC-AUC ~0.77-0.85; CV for robustness.
- Libraries: scikit-learn, pandas, numpy.

### Dashboard
- Streamlit app (`src/app.py`): User inputs bill ID; fetches data via `data_fetch.py`.
- Visuals: Timelines, metrics, predictions with confidence.
- Recommendations: E.g., "Build bipartisan support" if low score.

## 3. Results and Evaluations
- **Model Performance**:
  - Viability: Accuracy 81-83%, ROC-AUC 0.77-0.82 across stages.
  - Passage: Similar, with focus on recall for rare positives.
  - Tested on bill age buckets; progressive models perform best.
- **Impact Metrics**: On test bills, correctly identifies 85% of passed ones as viable early.
- **Usability**: Interactive gauges, tables; confidence intervals show uncertainty.
- Limitations: Relies on historical data; may miss external factors (e.g., elections).

## 4. Ethical Considerations and Fairness
See [ethics.md](ethics.md) for details. Key: Bias checks in party/policy features; transparent predictions; promotes inclusive civic action.

## 5. Future Improvements
- Integrate real-time updates via webhooks.
- Add NLP for bill text sentiment/impact analysis.
- Mobile app version.
- Expand to state legislatures.
- Collaborate with NGOs for real-world testing.

## Appendix
- Data: ~16K bills, 1.7% passed rate.
- Training: Stratified CV; handled imbalance.
- Scalability: API-based; models <100MB.