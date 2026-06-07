"""
SmartCollegeBot - Response Feedback Storage
"""

import json
import os
from datetime import datetime
from uuid import uuid4

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback.json")


def _load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def _save_feedback(feedback):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=2)


def add_feedback(message_id: str, username: str, rating: str, comment: str = ""):
    feedback = _load_feedback()
    feedback = [f for f in feedback if f.get("message_id") != message_id]
    entry = {
        "id": str(uuid4()),
        "message_id": message_id,
        "username": username,
        "rating": rating,
        "comment": comment.strip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    feedback.append(entry)
    _save_feedback(feedback)
    return entry


def get_all_feedback():
    return sorted(_load_feedback(), key=lambda f: f.get("timestamp", ""), reverse=True)


def get_feedback_summary():
    summary = {"helpful": 0, "not_helpful": 0}
    for entry in _load_feedback():
        rating = entry.get("rating")
        if rating in summary:
            summary[rating] += 1
    return summary
