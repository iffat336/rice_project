from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


@dataclass
class ClassifierResult:
    accuracy: float
    confusion: np.ndarray
    classes: list[str]
    importance: pd.Series
    fpr: np.ndarray
    tpr: np.ndarray
    roc_auc: float


def build_feature_matrix(expr: pd.DataFrame, metadata: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Transpose the gene x sample matrix into a sample x gene feature table."""
    sample_cols = metadata["sample_id"].tolist()
    features = expr.set_index("gene_name")[sample_cols].T
    features.index.name = "sample_id"
    return features.astype(float), list(expr["gene_name"])


def train_classifier(features: pd.DataFrame, labels: pd.Series, random_state: int = 7) -> ClassifierResult:
    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)

    x_train, x_test, y_train, y_test = train_test_split(
        features, y, test_size=0.3, random_state=random_state, stratify=y
    )
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = RandomForestClassifier(n_estimators=200, max_depth=4, random_state=random_state)
    model.fit(x_train_scaled, y_train)
    predictions = model.predict(x_test_scaled)
    probabilities = model.predict_proba(x_test_scaled)[:, 1]

    fpr, tpr, _ = roc_curve(y_test, probabilities)
    importance = pd.Series(model.feature_importances_, index=features.columns).sort_values(ascending=False)

    return ClassifierResult(
        accuracy=accuracy_score(y_test, predictions),
        confusion=confusion_matrix(y_test, predictions),
        classes=list(encoder.classes_),
        importance=importance,
        fpr=fpr,
        tpr=tpr,
        roc_auc=auc(fpr, tpr),
    )
