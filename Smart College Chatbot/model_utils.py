"""
SmartCollegeBot - NLP Preprocessing & ML Model
Custom implementation (no NLTK downloads required)
"""

import re
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import os

from dataset import INTENTS

# ─── CUSTOM NLP PREPROCESSING ────────────────────────────────────────────────

STOPWORDS = {
    'a', 'an', 'the', 'is', 'it', 'in', 'on', 'at', 'to', 'for', 'of',
    'and', 'or', 'but', 'not', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought', 'used',
    'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'they', 'them',
    'this', 'that', 'these', 'those', 'there', 'their', 'what', 'which',
    'who', 'when', 'where', 'why', 'how', 'about', 'with', 'from', 'into',
    'through', 'during', 'so', 'just', 'as', 'if', 'then', 'than', 'too',
    'very', 'up', 'out', 'no', 'its', 'am', 'also', 'by', 'get', 'got'
}

# Basic suffix rules for stemming (without NLTK)
SUFFIXES = ['ing', 'tion', 'ness', 'ment', 'able', 'ible', 'ful', 'less',
            'ity', 'ies', 'ed', 'er', 'est', 'ly', 'al', 'ial', 'ical']


def simple_stem(word: str) -> str:
    """Lightweight stemmer using suffix stripping."""
    if len(word) <= 3:
        return word
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    # Handle plurals
    if word.endswith('ies') and len(word) > 4:
        return word[:-3] + 'y'
    if word.endswith('es') and len(word) > 4:
        return word[:-2]
    if word.endswith('s') and not word.endswith('ss') and len(word) > 3:
        return word[:-1]
    return word


def preprocess(text: str, stemming: bool = True) -> str:
    """
    Full NLP preprocessing pipeline:
    1. Lowercase
    2. Remove special characters
    3. Tokenize
    4. Remove stopwords
    5. Stemming (optional)
    """
    # Lowercase
    text = text.lower()
    # Remove special chars, keep letters, digits, spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Tokenize (split on whitespace)
    tokens = text.split()
    # Remove stopwords & short tokens
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    # Stemming
    if stemming:
        tokens = [simple_stem(t) for t in tokens]
    return ' '.join(tokens)


# ─── BUILD TRAINING DATA ─────────────────────────────────────────────────────

def build_training_data(augment: bool = True):
    """
    Build X (processed text) and y (intent labels) from INTENTS dataset.
    Includes data augmentation to boost smaller classes.
    """
    X, y = [], []
    for intent in INTENTS:
        tag = intent["tag"]
        if tag == "unknown":
            continue
        for pattern in intent["patterns"]:
            X.append(preprocess(pattern))
            y.append(tag)
            if augment:
                # Augment: add slight variations
                # 1. original without stemming
                X.append(preprocess(pattern, stemming=False))
                y.append(tag)
                # 2. add "tell me about X" / "I want to know X" prefix variations
                for prefix in ["tell me about ", "what about ", "explain ", "info on "]:
                    X.append(preprocess(prefix + pattern))
                    y.append(tag)
    return X, y


# ─── TRAIN MODEL ─────────────────────────────────────────────────────────────

def train_model(verbose: bool = True):
    """Train a TF-IDF + Logistic Regression pipeline with cross-validation."""
    X, y = build_training_data(augment=True)
    
    if verbose:
        print(f"Training data: {len(X)} samples across {len(set(y))} intents")

    # Pipeline: TF-IDF -> Logistic Regression (best for text classification)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 3),        # unigrams, bigrams, trigrams
            max_features=8000,
            sublinear_tf=True,         # apply log normalization
            analyzer='word',
            min_df=1
        )),
        ('clf', LogisticRegression(
            max_iter=1000,
            C=5.0,
            solver='lbfgs',
        ))
    ])
    
    pipeline.fit(X, y)

    # Cross-validation score
    if verbose:
        try:
            cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
            print(f"Cross-validation accuracy: {cv_scores.mean():.2%} +/- {cv_scores.std():.2%}")
        except Exception:
            pass

    return pipeline


# ─── RESPONSE SELECTOR ────────────────────────────────────────────────────────

import random

def get_response(tag: str, confidence: float) -> str:
    """Get a response for the predicted intent tag."""
    # Low confidence → fallback to unknown
    if confidence < 0.25:
        tag = "unknown"
    
    for intent in INTENTS:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    
    # Default fallback
    for intent in INTENTS:
        if intent["tag"] == "unknown":
            return random.choice(intent["responses"])
    
    return "I'm not sure about that. Please contact the college administration for assistance."


def predict_intent(text: str, model) -> tuple[str, float]:
    """Return (predicted_tag, confidence_score) for input text."""
    processed = preprocess(text)
    try:
        probas = model.predict_proba([processed])[0]
    except ValueError:
        # If the loaded object is an old classifier instead of the pipeline,
        # retrain/load the correct pipeline and retry.
        model = load_or_train_model()
        probas = model.predict_proba([processed])[0]
    classes = model.classes_
    top_idx = np.argmax(probas)
    return classes[top_idx], probas[top_idx]


# ─── SAVE / LOAD MODEL ───────────────────────────────────────────────────────

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def save_model(model):
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_PATH}")


def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        # Ensure the loaded model is the expected TF-IDF + classifier pipeline.
        if not isinstance(model, Pipeline) or "tfidf" not in model.named_steps:
            print("Incompatible model detected; retraining a fresh pipeline.")
            model = train_model(verbose=True)
            save_model(model)
        return model
    model = train_model(verbose=True)
    save_model(model)
    return model


if __name__ == "__main__":
    print("Training SmartCollegeBot model...")
    model = train_model(verbose=True)
    save_model(model)
    
    # Quick smoke test
    tests = [
        "How to apply for admission?",
        "What is the fee structure?",
        "Tell me about hostel facilities",
        "When are the exams?",
        "How to clear backlogs?",
        "What scholarships are available?"
    ]
    print("\nQuick Predictions:")
    for t in tests:
        tag, conf = predict_intent(t, model)
        resp = get_response(tag, conf)
        print(f"  Q: {t}")
        print(f"  Intent: {tag} (conf: {conf:.2%})")
        print()
