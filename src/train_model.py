from __future__ import annotations

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split

from src.config import MODEL_PATH
from src.data_prep import FEATURE_COLUMNS, load_or_create_dataset


def train_and_save_model() -> dict:
    bundle = load_or_create_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        bundle.X, bundle.y, test_size=0.2, random_state=42, stratify=bundle.y
    )

    model = RandomForestClassifier(n_estimators=250, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    artifact = {"model": model, "features": FEATURE_COLUMNS}
    joblib.dump(artifact, MODEL_PATH)
    return metrics


if __name__ == "__main__":
    result = train_and_save_model()
    print("Treino concluido.")
    print(result)

