"""
SmartCollegeBot - Chat History & Analytics Module
"""

import json
import os
from datetime import datetime

CHAT_LOG_FILE = os.path.join(os.path.dirname(__file__), "chat_history.json")

def _load_history():
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def _save_history(history):
    with open(CHAT_LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)

def log_message(username: str, user_message: str, bot_response: str,
                intent: str, confidence: float):
    """Log a chat interaction."""
    history = _load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "user_message": user_message,
        "bot_response": bot_response,
        "intent": intent,
        "confidence": round(confidence, 4)
    })
    _save_history(history)

def get_all_logs():
    """Return all chat logs."""
    return _load_history()

def get_user_logs(username: str):
    """Return logs for a specific user."""
    history = _load_history()
    return [h for h in history if h.get("username") == username]

def get_intent_stats():
    """Return intent frequency statistics."""
    history = _load_history()
    stats = {}
    for log in history:
        intent = log.get("intent", "unknown")
        stats[intent] = stats.get(intent, 0) + 1
    return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

def get_daily_stats():
    """Return messages per day."""
    history = _load_history()
    stats = {}
    for log in history:
        date = log.get("timestamp", "")[:10]
        stats[date] = stats.get(date, 0) + 1
    return dict(sorted(stats.items()))

def get_low_confidence_logs(threshold: float = 0.4):
    """Return logs where bot wasn't confident — useful for improving dataset."""
    history = _load_history()
    return [h for h in history if h.get("confidence", 1.0) < threshold]

def clear_all_logs():
    _save_history([])
