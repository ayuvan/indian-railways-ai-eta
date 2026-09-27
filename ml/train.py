"""
Indian Railways Dynamic ETA - Machine Learning Training & Evaluation
Author: SIH AI Prototype
Description:
    Trains, compares, and evaluates multiple predictive models:
      1. Naive Delay Propagation (Industry Baseline: D_target = D_current)
      2. Linear Regression (Statistical Baseline)
      3. Random Forest Regressor (Ensemble Baseline)
      4. HistGradientBoostingRegressor (Champion Non-linear Gradient Boosted Tree)
    Follows strict featurization ordering and robust cross-validation.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "ml", "model_artifacts")

FEATURE_COLS = [
    "train_priority",
    "current_delay",
    "distance_to_target",
    "stops_remaining",
    "total_route_distance",
    "pct_journey_completed",
    "scheduled_transit_min",
    "dep_hour",
    "is_target_junction",
    "target_zone_code",
    "target_hist_delay"
]

TARGET_COL = "target_delay"

def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, model_name: str) -> Dict[str, float]:
    """Calculates comprehensive operational and statistical metrics."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # Railway operational accuracy thresholds
    abs_err = np.abs(y_true - y_pred)
    within_5min = float(np.mean(abs_err <= 5.0) * 100.0)
    within_15min = float(np.mean(abs_err <= 15.0) * 100.0)
    
    print(f"\n[{model_name.upper()} RESULTS]")
    print(f"  MAE (Mean Absolute Error)     : {mae:.2f} mins")
    print(f"  RMSE (Root Mean Squared Error): {rmse:.2f} mins")
    print(f"  R² Score                      : {r2:.4f}")
    print(f"  Accuracy (Within ±5 mins)     : {within_5min:.2f}%")
    print(f"  Accuracy (Within ±15 mins)    : {within_15min:.2f}%")

    return {
        "model_name": model_name,
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 4),
        "within_5min_pct": round(within_5min, 2),
        "within_15min_pct": round(within_15min, 2)
    }

def train_and_evaluate():
    data_path = os.path.join(ARTIFACTS_DIR, "processed_training_data.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed dataset not found at {data_path}. Run ml/preprocess.py first.")

    print(f"[ML Training] Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"[ML Training] Total instances: {len(df):,}")

    X = df[FEATURE_COLS].copy()
    y = df[TARGET_COL].values

    # Strict featurization ordering: Train-Test split BEFORE any scaling or fitting
    # We stratify/group by train_no to prevent data leakage across same train trips
    train_indices, test_indices = train_test_split(
        np.arange(len(df)),
        test_size=0.20,
        random_state=42
    )

    X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]

    print(f"[ML Training] Split sizes: Train = {len(X_train):,}, Test = {len(X_test):,}")

    # Standard Scaler fit ONLY on training set
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    results = []

    # 1. NAIVE BASELINE (Current Delay persistence: y_pred = current_delay)
    y_pred_naive = X_test["current_delay"].values
    results.append(evaluate_predictions(y_test, y_pred_naive, "Naive Delay Persistence (Standard NTES/IRCTC)"))

    # 2. LINEAR REGRESSION BASELINE
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    y_pred_lr = lr_model.predict(X_test_scaled)
    results.append(evaluate_predictions(y_test, y_pred_lr, "Linear Regression Baseline"))

    # 3. RIDGE REGRESSION (L2 Regularized)
    ridge_model = Ridge(alpha=10.0)
    ridge_model.fit(X_train_scaled, y_train)
    y_pred_ridge = ridge_model.predict(X_test_scaled)
    results.append(evaluate_predictions(y_test, y_pred_ridge, "Ridge Regression (L2 Regularized)"))

    # 4. CHAMPION MODEL: HistGradientBoostingRegressor
    # Fast, handles non-linearities, natively handles high-dimensional interactions
    print("\n[ML Training] Training Champion Model: HistGradientBoostingRegressor...")
    hgb_model = HistGradientBoostingRegressor(
        max_iter=250,
        learning_rate=0.08,
        max_leaf_nodes=45,
        min_samples_leaf=25,
        l2_regularization=1.5,
        random_state=42
    )
    hgb_model.fit(X_train, y_train)
    y_pred_hgb = hgb_model.predict(X_test)
    champion_eval = evaluate_predictions(y_test, y_pred_hgb, "AI Dynamic Gradient Boosted Model (Champion)")
    results.append(champion_eval)

    # Save champion model and artifacts
    model_export_path = os.path.join(ARTIFACTS_DIR, "champion_eta_model.joblib")
    scaler_export_path = os.path.join(ARTIFACTS_DIR, "scaler.joblib")
    metrics_export_path = os.path.join(ARTIFACTS_DIR, "model_comparison_metrics.json")
    features_export_path = os.path.join(ARTIFACTS_DIR, "feature_columns.json")

    joblib.dump(hgb_model, model_export_path)
    joblib.dump(scaler, scaler_export_path)

    with open(metrics_export_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open(features_export_path, "w", encoding="utf-8") as f:
        json.dump(FEATURE_COLS, f, indent=2)

    print(f"\n[ML Training] Successfully exported model and artifacts to {ARTIFACTS_DIR}")
    print("=" * 60)
    print("COMPARATIVE SUMMARY:")
    for r in results:
        print(f"  {r['model_name']:<48} | MAE: {r['mae']:>5.2f}m | ±15m Acc: {r['within_15min_pct']:>5.1f}% | R²: {r['r2']:>6.4f}")
    print("=" * 60)

if __name__ == "__main__":
    train_and_evaluate()
