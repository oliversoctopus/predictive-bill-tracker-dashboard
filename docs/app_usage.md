# Dashboard Usage Guide

## Overview
The Congressional Bill Tracker provides real-time AI predictions for legislative success through an interactive web dashboard.

- **Main Application**: `src/app.py` (Streamlit dashboard)
- **Data Source**: Congress.gov API via `src/data_fetch.py`
- **ML Models**: Pre-trained models in `models/` directory

## Access Options

### Option 1: Use the Deployed App (Recommended)
Visit the live dashboard at: https://predictivebilltracker.streamlit.app
- No installation required
- Always up-to-date
- Instant access with full functionality

### Option 2: Run Locally
1. **Install dependencies**: 
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up API key** (optional for enhanced features):
   ```bash
   echo "CONGRESS_API_KEY=your_key_here" > .env
   ```
3. **Launch the app**:
   ```bash
   streamlit run src/app.py
   ```
4. **Open browser**: Navigate to `http://localhost:8501`

## How to Use

### Input Parameters
- **Bill Number**: Enter the numeric identifier (e.g., 1234)
- **Type**: Select HR (House) or S (Senate)
- **Congress**: Default is 118th (2023-2024)

### Understanding the Output

#### 1. Bill Verification Section
- Confirms bill title, sponsor, and current status
- Shows policy area and committee assignments
- Helps verify you're analyzing the correct bill

#### 2. Key Metrics Dashboard
- **Days Active**: Time since introduction
- **Total Actions**: Legislative activity count
- **Committees**: Number of committee referrals
- **Cosponsors**: Support level indicator
- **Bipartisan**: Cross-party support status
- **Activity Rate**: Actions per day metric

#### 3. Legislative Timeline
- Complete chronological action history
- Paginated display for bills with extensive histories
- Download option for CSV export
- Shows action text, date, and days ago

#### 4. AI Predictions
- **Viability Score**: Likelihood of gaining traction (0-100%)
- **Passage Score**: Chance of becoming law (for viable bills)
- **Confidence Intervals**: Model uncertainty ranges
- **Visual Gauges**: Color-coded prediction displays
  - Green (>70%): High likelihood
  - Yellow (30-70%): Moderate chance
  - Red (<30%): Low probability

#### 5. Advanced Features (Optional)
- **Model Breakdown**: Individual algorithm predictions
- **Feature Analysis**: Top factors influencing prediction
- **Similar Bills**: Historical comparison data

#### 6. Strategic Recommendations
- Personalized action items based on current status
- Focus areas for improving bill success
- Timing considerations

## Display Options
Toggle these features via the expandable menu:
- Show/hide confidence intervals
- Display individual model predictions
- View feature importance analysis
- Compare with similar historical bills

## Tips for Best Results
- Bills with 30+ days of activity provide most accurate predictions
- Check confidence intervals for prediction reliability
- Use CSV export for detailed analysis
- Refresh page to analyze multiple bills

## Troubleshooting
- **"Model not found"**: Ensure `models/` directory contains all .pkl files
- **Slow loading**: First prediction may take 10-15 seconds to load models
- **No data found**: Verify bill number and congress session
- **API limits**: Consider using local deployment with API key

## Deployment
For your own instance:
1. Fork the repository
2. Deploy via [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Set secrets in Streamlit dashboard for API keys
```

This improved version:
1. Fixes the pip install command to use requirements.txt
2. Adds the deployed website option prominently
3. Provides much clearer structure and formatting
4. Includes troubleshooting section
5. Adds color-coding explanation for gauges
6. Includes API key setup instructions
7. Provides deployment guidance
8. Uses better markdown formatting for readability