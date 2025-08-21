# ml_model.py
# Machine Learning Model Implementation (Example: Spam Email Detection)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Sample dataset (emails and labels: 1 = spam, 0 = not spam)
data = {
    "text": [
        "Congratulations! You won a lottery worth $1,000,000. Claim now!",
        "Reminder: Your appointment is scheduled for tomorrow at 10 AM.",
        "Win free prizes!!! Click the link below to claim your reward.",
        "Meeting at 3 PM with the sales team. Don’t be late.",
        "Earn money from home easily by signing up today.",
        "Can we reschedule our call to next week?",
    ],
    "label": [1, 0, 1, 0, 1, 0]  # 1 = spam, 0 = not spam
}

# Load data into a DataFrame
df = pd.DataFrame(data)

# Features (text) and labels (target)
X = df["text"]
y = df["label"]

# Convert text into numerical vectors
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.3, random_state=42
)

# Train model (Naive Bayes classifier)
model = MultinomialNB()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
