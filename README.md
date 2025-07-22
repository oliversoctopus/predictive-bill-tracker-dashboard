# Predictive Bill Tracker Dashboard
AI4Legislation 2025 project: an AI-powered web app that monitors US state and federal bills in real-time, using machine learning to predict passage likelihood.

## Overview
An AI-powered web app for monitoring U.S. federal bills in real-time, predicting passage likelihood using ML (e.g., logistic regression on historical votes), visualizations (heatmaps for amendments), and alerts. Built for AI4Legislation 2025 in Legislative Tracking category.

## Features
- Bill search and status fetch via Congress.gov API.
- Passage prediction (e.g., >70% accuracy target).
- Visuals: Heatmaps, timelines.
- Alerts: Email on updates.
- Ethical: Bias audits on models (e.g., party skew in data).

## Installation
1. Clone repo: `git clone https://github.com/oliversoctopus/predictive-bill-tracker-dashboard.git`
2. Activate env: `.\env\Scripts\Activate.ps1`
3. Install deps: `pip install -r requirements.txt`

## Setup
- Get API keys: Congress.gov (api.congress.gov), store in `.env` as `CONGRESS_API_KEY=yourkey`.
- Run: `streamlit run src/app.py`

## Usage
Enter bill ID (e.g., HR1234) in the dashboard for predictions and visuals.

## Timeline
- Day 1: Setup (July 22, 2025)
- Days 2-3: Data
- Days 4-5: Models
- Days 6-7: Dashboard
- Days 8-9: Test & Docs

## Ethics
Document biases (e.g., historical data may favor major parties); mitigate with SMOTE balancing.