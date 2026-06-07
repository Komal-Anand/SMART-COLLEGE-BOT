"""
SmartCollegeBot - Notice Board Storage
"""

import json
import os
from datetime import datetime
from uuid import uuid4

NOTICE_FILE = os.path.join(os.path.dirname(__file__), "notices.json")


def _load_notices():
    if os.path.exists(NOTICE_FILE):
        with open(NOTICE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def _save_notices(notices):
    with open(NOTICE_FILE, "w", encoding="utf-8") as f:
        json.dump(notices, f, indent=2)


def get_notices(include_inactive: bool = False):
    notices = _load_notices()
    if not include_inactive:
        notices = [n for n in notices if n.get("active", True)]
    return sorted(notices, key=lambda n: n.get("created_at", ""), reverse=True)


def add_notice(title: str, body: str, category: str, posted_by: str):
    notices = _load_notices()
    notice = {
        "id": str(uuid4()),
        "title": title.strip(),
        "body": body.strip(),
        "category": category,
        "posted_by": posted_by,
        "active": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    notices.append(notice)
    _save_notices(notices)
    return notice


def delete_notice(notice_id: str):
    notices = _load_notices()
    updated = [n for n in notices if n.get("id") != notice_id]
    if len(updated) == len(notices):
        return False, "Notice not found."
    _save_notices(updated)
    return True, "Notice deleted."


def set_notice_active(notice_id: str, active: bool):
    notices = _load_notices()
    for notice in notices:
        if notice.get("id") == notice_id:
            notice["active"] = active
            _save_notices(notices)
            return True, "Notice updated."
    return False, "Notice not found."
