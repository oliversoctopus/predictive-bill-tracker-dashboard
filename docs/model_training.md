# Model Training Documentation

## Overview
- Notebook: `models/model.ipynb`
- Trains dual-stage models: Viability (traction prediction), then Passage (success among viable).
- Time-aware: Models for new (<1 day), early (1-30 days), progressive (>30 days) bills.
- Handles imbalance (1.7% passage rate) with ensembles, calibration, adaptive thresholds.

## Features
- Base (new bills): Sponsors, title length, policy area, bipartisan score.
- Extended (early): + Cosponsors, support velocity.
- Progressive: + Activity rate, committee density, momentum.
- Selection: Mutual info; top 14-20 per stage.

## Training Process
- Split: 80/20 stratified.
- Scaling: StandardScaler.
- Models: RF (balanced), GB, LR; Voting ensemble (soft, weights 0.4/0.4/0.2).
- Calibration: Isotonic for probabilities (imbalanced data).
- Evaluation: ROC-AUC, precision/recall/F1; CV (5-fold stratified).
- Threshold: Adaptive (e.g., 0.5 for viability).
- Saved: PKL files per stage/model type (e.g., `viability_new_bill.pkl` – includes all components).

## Evaluation
- Viability: ROC-AUC ~0.77-0.82; F1 ~0.29-0.35.
- Passage: Similar; higher recall for positives.
- By Stage: Progressive best (more features); new bills have conservative predictions (less passage rate, more uncertainty).