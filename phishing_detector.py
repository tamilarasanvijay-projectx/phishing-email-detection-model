import argparse, re
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

DATA_PATH = Path("emails.csv")
MODEL_PATH = Path("phishing_model.joblib")
SUSPICIOUS = ("urgent", "verify", "password", "suspended", "click", "confirm",
              "winner", "prize", "login", "update", "limited", "bank",
              "security alert", "unusual activity")

def url_features(series):
    rows = []
    for item in series:
        text = str(item).lower()
        urls = re.findall(r"https?://\\S+|www\\.\\S+", text)
        rows.append([len(urls), int(any(w in text for w in SUSPICIOUS)),
                     int("@" in text),
                     int(any(x in text for x in ("bit.ly", "tinyurl", "t.co"))),
                     int(bool(re.search(r"\\b(urgent|immediately|within 24 hours)\\b", text)))])
    return pd.DataFrame(rows, columns=["url_count", "suspicious_keyword",
        "at_symbol", "short_url", "urgency"], index=series.index)

def load_data(path):
    data = pd.read_csv(path).dropna(subset=["email_text", "label"]).copy()
    if not {"email_text", "label"}.issubset(data.columns):
        raise ValueError("CSV must contain email_text and label columns.")
    data["label"] = data["label"].astype(str).str.lower().str.strip()
    data = data[data["label"].isin(["phishing", "safe"])]
    if data["label"].nunique() != 2:
        raise ValueError("Dataset must contain phishing and safe labels.")
    return data

def build_model():
    features = ColumnTransformer([
        ("text", TfidfVectorizer(ngram_range=(1, 2), stop_words="english",
                                 max_features=3000), "email_text"),
        ("indicators", FunctionTransformer(url_features, validate=False), "email_text")
    ])
    return Pipeline([("features", features),
                     ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])

def main():
    parser = argparse.ArgumentParser(description="Train and use an educational phishing email classifier.")
    parser.add_argument("--dataset", default=str(DATA_PATH))
    parser.add_argument("--predict", help="Email text to classify after training")
    args = parser.parse_args()

    data = load_data(args.dataset)
    X, y = data[["email_text"]], data["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)
    model = build_model()
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    labels = ["phishing", "safe"]
    matrix = confusion_matrix(y_test, predicted, labels=labels)

    print("\n=== PHISHING EMAIL DETECTION MODEL ===")
    print("Dataset samples :", len(data))
    print("Training samples:", len(X_train))
    print("Testing samples :", len(X_test))
    print(f"Accuracy        : {accuracy_score(y_test, predicted) * 100:.2f}%")
    print("\nClassification report:")
    print(classification_report(y_test, predicted, labels=labels, zero_division=0))
    print("Confusion matrix (rows=actual, columns=predicted):")
    print("                 Predicted phishing | Predicted safe")
    print(f"Actual phishing       {matrix[0][0]:3d}       |      {matrix[0][1]:3d}")
    print(f"Actual safe           {matrix[1][0]:3d}       |      {matrix[1][1]:3d}")

    joblib.dump(model, MODEL_PATH)
    print("\nSaved trained model:", MODEL_PATH)

    if args.predict:
        sample = pd.DataFrame({"email_text": [args.predict]})
        result = model.predict(sample)[0]
        confidence = max(model.predict_proba(sample)[0]) * 100
        print("\nPrediction:", result.upper())
        print(f"Model confidence: {confidence:.1f}%")
        print("A prediction is not proof that an email is safe or malicious.")
    print("\nNote: included sample data is for learning only, not real-world accuracy.")

if __name__ == "__main__":
    main()
