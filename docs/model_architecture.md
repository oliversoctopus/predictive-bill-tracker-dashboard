# Model Architecture and Training

## Two-Phase Prediction System

### Phase 1: Viability Prediction
Determines if a bill will gain traction (20.3% of bills are viable)

### Phase 2: Passage Prediction
For viable bills only, predicts likelihood of becoming law

## Time-Aware Model Stages

### 1. New Bill Model (Day 1)
**Features**: 15 base features
- Sponsor party and characteristics
- Title complexity
- Policy area
- Initial bipartisan support
- Introduction timing

**Performance**:
- ROC-AUC: 0.768
- Accuracy: 80.7%

### 2. Early Stage Model (2-30 days)
**Features**: 22 extended features (base + 7 additional)
- Cosponsor growth rate
- Early momentum indicators
- Support velocity
- Initial activity patterns

**Performance**:
- ROC-AUC: 0.775
- Accuracy: 81.7%

### 3. Progressive Model (30+ days)
**Features**: 38 comprehensive features
- Full legislative history
- Committee engagement metrics
- Activity rate normalization
- Momentum indicators

**Performance**:
- ROC-AUC: 0.782
- Accuracy: 82.5%

## Ensemble Architecture
Each stage uses a calibrated ensemble of:
- **Random Forest** (40% weight): 300 trees, balanced sampling
- **Gradient Boosting** (40% weight): 200 trees, learning rate 0.05
- **Logistic Regression** (20% weight): For stability

## Key Innovations
1. **Isotonic Calibration**: Adjusts probabilities for realistic predictions
2. **Mutual Information Feature Selection**: Identifies most predictive features
3. **Conservative Thresholds**: Prevents overfitting on imbalanced data
4. **Confidence Intervals**: Shows prediction uncertainty

## Training Process
- **Cross-validation**: 5-fold stratified CV
- **Class balancing**: Addresses 1.7% positive class imbalance
- **Feature scaling**: StandardScaler normalization
- **Model persistence**: Saved as separate .pkl files under 100MB each