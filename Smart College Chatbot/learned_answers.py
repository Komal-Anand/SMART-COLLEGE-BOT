"""
SmartCollegeBot - Admin-reviewed learned answers.
"""

import json
import os
import re
from datetime import datetime
from difflib import SequenceMatcher
from uuid import uuid4

LEARNED_ANSWERS_FILE = os.path.join(os.path.dirname(__file__), "learned_answers.json")


def _load_answers():
    if os.path.exists(LEARNED_ANSWERS_FILE):
        with open(LEARNED_ANSWERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def _save_answers(answers):
    with open(LEARNED_ANSWERS_FILE, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2, ensure_ascii=False)


def normalize_question(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def _similarity(left: str, right: str) -> float:
    left_norm = normalize_question(left)
    right_norm = normalize_question(right)
    if not left_norm or not right_norm:
        return 0.0

    left_tokens = set(left_norm.split())
    right_tokens = set(right_norm.split())
    overlap = len(left_tokens & right_tokens) / max(len(left_tokens | right_tokens), 1)
    sequence = SequenceMatcher(None, left_norm, right_norm).ratio()
    return max(overlap, sequence)


def add_learned_answer(question: str, answer: str, created_by: str):
    answers = _load_answers()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normalized = normalize_question(question)

    for item in answers:
        if item.get("normalized_question") == normalized:
            item["question"] = question.strip()
            item["answer"] = answer.strip()
            item["updated_by"] = created_by
            item["updated_at"] = now
            _save_answers(answers)
            return item

    item = {
        "id": str(uuid4()),
        "question": question.strip(),
        "normalized_question": normalized,
        "answer": answer.strip(),
        "created_by": created_by,
        "created_at": now,
        "updated_at": now,
    }
    answers.append(item)
    _save_answers(answers)
    return item


def delete_learned_answer(answer_id: str):
    answers = _load_answers()
    updated = [item for item in answers if item.get("id") != answer_id]
    _save_answers(updated)
    return len(updated) != len(answers)


def get_all_learned_answers():
    return sorted(_load_answers(), key=lambda item: item.get("updated_at", ""), reverse=True)


def find_learned_answer(question: str, threshold: float = 0.72):
    best_item = None
    best_score = 0.0
    for item in _load_answers():
        score = _similarity(question, item.get("question", ""))
        if score > best_score:
            best_item = item
            best_score = score

    if best_item and best_score >= threshold:
        return best_item, best_score
    return None, best_score
