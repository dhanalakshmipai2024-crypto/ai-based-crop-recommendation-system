import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


def train_crop_model(data_path="Crop_recommendation.csv", model_path="crop_model.pkl", meta_path="model_metadata.json"):
    print("=" * 60)
    print("[AI-Based Crop Recommendation] Model Training Pipeline")
    print("=" * 60)

    # 1. Load dataset
    df = pd.read_csv(data_path)
    print(f"Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Data Quality & Pre-flight Checks
    missing = df.isnull().sum().to_dict()
    duplicates = int(df.duplicated().sum())
    numeric_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    negatives = {col: int((df[col] < 0).sum()) for col in numeric_cols}

    print("\nData Quality Report:")
    print(f" - Missing values: {sum(missing.values())}")
    print(f" - Duplicate rows: {duplicates}")
    print(f" - Negative / invalid values: {sum(negatives.values())}")

    if sum(missing.values()) > 0:
        df = df.dropna()
    if duplicates > 0:
        df = df.drop_duplicates()

    # 3. Features & Target
    X = df[numeric_cols]
    y = df["label"]
    unique_crops = sorted(list(y.unique()))
    print(f" - Unique crop classes ({len(unique_crops)}): {', '.join(unique_crops[:8])}...")

    # 4. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

    # 5. Model Training (Random Forest)
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=None,
        min_samples_split=2,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # 6. Evaluation
    y_pred = model.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, average="weighted"))
    rec = float(recall_score(y_test, y_pred, average="weighted"))
    f1 = float(f1_score(y_test, y_pred, average="weighted"))

    print("\n" + "=" * 60)
    print(">> Model Performance Metrics on Holdout Test Set (20%):")
    print(f" - Accuracy:  {acc * 100:.2f}% ({acc:.4f})")
    print(f" - Precision: {prec * 100:.2f}% ({prec:.4f})")
    print(f" - Recall:    {rec * 100:.2f}% ({rec:.4f})")
    print(f" - F1-Score:  {f1 * 100:.2f}% ({f1:.4f})")
    print("=" * 60)

    # 7. Feature Importances
    importances = {
        col: round(float(imp), 4)
        for col, imp in zip(numeric_cols, model.feature_importances_)
    }
    # Sort descending
    sorted_importances = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))
    print("\nFeature Importances:")
    for feat, imp in sorted_importances.items():
        print(f" - {feat:12s}: {imp * 100:5.2f}%")

    # 8. Per-Crop Statistical Profiles (for UI guides and agronomic advice)
    crop_profiles = {}
    for crop in unique_crops:
        subset = df[df["label"] == crop]
        crop_profiles[crop] = {
            "samples": int(len(subset)),
            "N": {"min": float(subset["N"].min()), "max": float(subset["N"].max()), "mean": round(float(subset["N"].mean()), 1)},
            "P": {"min": float(subset["P"].min()), "max": float(subset["P"].max()), "mean": round(float(subset["P"].mean()), 1)},
            "K": {"min": float(subset["K"].min()), "max": float(subset["K"].max()), "mean": round(float(subset["K"].mean()), 1)},
            "temperature": {"min": round(float(subset["temperature"].min()), 1), "max": round(float(subset["temperature"].max()), 1), "mean": round(float(subset["temperature"].mean()), 1)},
            "humidity": {"min": round(float(subset["humidity"].min()), 1), "max": round(float(subset["humidity"].max()), 1), "mean": round(float(subset["humidity"].mean()), 1)},
            "ph": {"min": round(float(subset["ph"].min()), 2), "max": round(float(subset["ph"].max()), 2), "mean": round(float(subset["ph"].mean()), 2)},
            "rainfall": {"min": round(float(subset["rainfall"].min()), 1), "max": round(float(subset["rainfall"].max()), 1), "mean": round(float(subset["rainfall"].mean()), 1)},
        }

    # 9. Save Model and Metadata
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"\nSaved trained model to {model_path}")

    metadata = {
        "model_type": "RandomForestClassifier",
        "n_estimators": 100,
        "features": numeric_cols,
        "classes": unique_crops,
        "total_classes": len(unique_crops),
        "total_samples": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
        },
        "feature_importances": sorted_importances,
        "crop_profiles": crop_profiles,
        "evaluation_summary": classification_report(y_test, y_pred, output_dict=True),
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved model metadata & crop profiles to {meta_path}")

    return model, metadata


if __name__ == "__main__":
    train_crop_model()