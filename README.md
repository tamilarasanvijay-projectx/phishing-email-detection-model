# Phishing Email Detection Model (Mini Project)

A beginner-friendly machine-learning project using Python and Scikit-learn. It classifies email text as **Phishing** or **Safe**, and displays accuracy, a classification report, and a confusion matrix.

## Assignment features
1. Trains on labelled phishing and legitimate email examples.
2. Uses TF-IDF text features and simple indicators for URLs, suspicious keywords, and urgency language.
3. Classifies email text as `phishing` or `safe`.
4. Displays accuracy and a confusion matrix.

## Files
- `phishing_detector.py` — training, evaluation and prediction program.
- `emails.csv` — small labelled teaching dataset.
- `requirements.txt` — required Python packages.
- `README.md` — project documentation.
- `.gitignore` — files Git should ignore.

## Install
```bash
python -m pip install -r requirements.txt
```

## Train and evaluate
```bash
python phishing_detector.py
```

The model prints accuracy, a classification report and a confusion matrix, then saves `phishing_model.joblib`.

## Classify an email
```bash
python phishing_detector.py --predict "Urgent: verify your account password immediately using this link"
```

The program trains the model first, then prints a prediction and confidence estimate.

## Dataset format
The CSV must contain `email_text` and `label` columns. Labels must be `phishing` or `safe`. You can replace `emails.csv` with a larger trusted labelled dataset while keeping these column names and labels.

## How it works
1. Load labelled email examples.
2. Convert words and phrases into TF-IDF features.
3. Extract simple URL and suspicious-language indicators.
4. Train a Logistic Regression classifier.
5. Evaluate on a held-out test set.
6. Predict the class of new email text.

## Limitations
**The included dataset is small and illustrative only. Its accuracy is not a real-world benchmark.** For meaningful evaluation, use a larger, diverse, verified dataset and keep duplicate or near-duplicate messages out of both training and test sets.

The model only analyses the text supplied. It does not inspect real email attachments, sender authentication, mail-server headers, or live websites. A `safe` prediction is not a guarantee that an email is safe.

## Responsible use
Use this project for education and defensive awareness. Do not use it to impersonate senders, harvest credentials, or send phishing messages.

## Conclusion
This mini project demonstrates a basic machine-learning workflow for email classification, including feature extraction, training, prediction and evaluation.
