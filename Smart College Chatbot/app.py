"""
SmartCollegeBot - Main Streamlit Application
An NLP & ML-Based College Assistant Chatbot
B.Tech Pre-Final Year Project | CSM355
"""

import streamlit as st
import time
import sys
import os
import textwrap
import streamlit.components.v1 as components
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from auth import authenticate, register_user, get_all_users, delete_user, reset_password
from model_utils import load_or_train_model, predict_intent, get_response, preprocess
from chat_logger import (log_message, get_all_logs, get_intent_stats,
                          get_daily_stats, get_low_confidence_logs,
                          get_user_logs, clear_all_logs)
from dataset import INTENTS
from document_qa import add_pdf_document, answer_from_documents, delete_document, get_documents
from feedback_store import add_feedback, get_all_feedback, get_feedback_summary
from learned_answers import (add_learned_answer, delete_learned_answer,
                             find_learned_answer, get_all_learned_answers,
                             normalize_question)
from notice_board import add_notice, delete_notice, get_notices, set_notice_active
from uuid import uuid4

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SmartCollegeBot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────

st.markdown(textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

body, .stApp, .stMarkdown, .stTextInput input, .stTextArea textarea,
.stButton button, .stSelectbox, label, p, div {
    font-family: 'Inter', sans-serif;
}

.material-icons, .material-symbols-rounded, .material-symbols-outlined,
span[class*="material-symbols"], span[class*="material-icons"] {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
}

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 14% 18%, rgba(183,229,205,0.16), transparent 28%),
        radial-gradient(circle at 88% 12%, rgba(183,229,205,0.10), transparent 26%),
        radial-gradient(circle at 58% 92%, rgba(138,190,185,0.10), transparent 34%),
        linear-gradient(135deg, #13252f 0%, #203544 42%, #172935 100%);
    background-attachment: fixed;
    min-height: 100vh;
    color: #B7E5CD;
    display: flex;
    flex-direction: column;
}
div[data-testid="stMainBlockContainer"] {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    max-width: 100%;
    padding: 0;
    margin: 0;
    height: 100%;
}

/* Hide Streamlit branding while keeping the sidebar toggle available */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none !important; }
header[data-testid="stHeader"] {
    display: none !important;
}

/* Remove extra spacing from columns and containers */
div[data-testid="stVerticalBlockContainer"] {
    padding: 0 !important;
    gap: 0 !important;
}
div[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(17, 33, 45, 0.96) 0%, rgba(10, 18, 28, 0.98) 100%) !important;
    border-right: 1px solid rgba(183,229,205,0.12);
    box-shadow: 14px 0 42px rgba(0,0,0,0.22);
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.75rem;
}
section[data-testid="stSidebar"] * { color: #B7E5CD !important; }
section[data-testid="stSidebar"] .stButton button {
    background: rgba(48,86,105,0.58) !important;
    border: 1px solid rgba(183,229,205,0.14) !important;
    color: #B7E5CD !important;
    border-radius: 12px !important;
    transition: all 0.22s ease !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(138,190,185,0.18) !important;
    border-color: rgba(183,229,205,0.22) !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16) !important;
    transform: translateY(-1px) !important;
}
section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(180deg, #8ABEB9 0%, #305669 100%) !important;
    border-color: rgba(183,229,205,0.18) !important;
    color: #ffffff !important;
}

/* Premium in-app top bar */
.app-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    margin: 4px 0 22px;
    padding: 16px 20px;
    border: 1px solid rgba(183,229,205,0.14);
    border-radius: 24px;
    background: linear-gradient(180deg, rgba(15, 28, 44, 0.76), rgba(18, 36, 56, 0.62));
    box-shadow: 0 22px 56px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.03);
    backdrop-filter: blur(20px) saturate(140%);
    animation: fadeInUp 0.45s ease both;
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    color: #B7E5CD;
    letter-spacing: -0.02em;
}
.topbar-brand-text {
    display: flex;
    flex-direction: column;
    gap: 1px;
}
.topbar-brand-text small {
    color: rgba(226,247,255,0.48);
    font-size: 0.72rem;
    font-weight: 600;
}
.topbar-logo {
    display: grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 11px;
    background: linear-gradient(135deg, rgba(138,190,185,0.20), rgba(48,86,105,0.24));
    border: 1px solid rgba(183,229,205,0.18);
}
.topbar-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: rgba(226, 247, 255, 0.74);
    font-size: 0.82rem;
    font-weight: 650;
}
.topbar-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}
.topbar-icon {
    display: grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 12px;
    border: 1px solid rgba(183,229,205,0.14);
    background: rgba(12, 20, 36, 0.60);
    color: rgba(226,247,255,0.82);
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
}
.topbar-icon:hover {
    background: rgba(14, 24, 42, 0.84);
    border-color: rgba(183,229,205,0.38);
    box-shadow: 0 8px 22px rgba(0,0,0,0.20);
    transform: translateY(-1px);
}
.topbar-icon:active {
    transform: translateY(0);
}
.deploy-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 34px;
    padding: 0 15px;
    border-radius: 12px;
    background: linear-gradient(135deg, #8ABEB9, #305669);
    color: white;
    font-size: 0.82rem;
    font-weight: 800;
    box-shadow: 0 12px 26px rgba(0,0,0,0.22);
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    user-select: none;
}
.deploy-pill:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 32px rgba(0,0,0,0.28);
    background: linear-gradient(135deg, #C1785A, #305669);
}
.deploy-pill:active {
    transform: translateY(0);
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #C1785A;
    box-shadow: 0 0 0 4px rgba(193,120,90,0.12);
}

/* Chat input bar */
.st-key-chat_input_shell {
    position: sticky;
    bottom: 0;
    z-index: 10;
    border: 1px solid rgba(183,229,205,0.18) !important;
    border-radius: 28px !important;
    padding: 14px 26px !important;
    background: rgba(14, 26, 42, 0.82) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 -10px 32px rgba(0,0,0,0.24) !important;
    backdrop-filter: blur(18px);
    transition: border-color 0.22s ease, box-shadow 0.22s ease, transform 0.22s ease;
    margin: 0 !important;
}
.st-key-chat_input_shell:hover,
.st-key-chat_input_shell:focus-within {
    border-color: rgba(183,229,205,0.26) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 -12px 36px rgba(138,190,185,0.16) !important;
}
.st-key-chat_input_shell [data-testid="stHorizontalBlock"] {
    align-items: center !important;
    gap: 0 !important;
}
.st-key-chat_input_shell div[data-testid="stTextInput"] {
    margin-bottom: 0 !important;
}
.st-key-chat_input_shell div[data-testid="stTextInput"] input {
    border: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
    min-height: 46px !important;
    font-size: 0.98rem !important;
}
.st-key-chat_input_shell .stButton button,
.st-key-chat_input_shell button {
    border: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
    min-height: 44px !important;
    color: #B7E5CD !important;
    border-radius: 14px !important;
}
.st-key-chat_input_shell .stButton button {
    font-weight: 850 !important;
    font-size: 1rem !important;
}
.st-key-chat_input_shell [data-testid="column"]:nth-of-type(2) .stButton button {
    background: linear-gradient(135deg, #8ABEB9, #305669) !important;
    box-shadow: 0 10px 24px rgba(0,0,0,0.18) !important;
}
.st-key-chat_input_shell .stButton button:hover,
.st-key-chat_input_shell button:hover {
    background: rgba(138,190,185,0.12) !important;
    transform: translateY(-1px) !important;
}

/* Chat messages */
.user-bubble {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
    animation: slideInRight 0.3s ease;
}
.user-bubble-inner {
    background: linear-gradient(135deg, rgba(40,68,85,0.96), rgba(24,42,55,0.98));
    border: 1px solid rgba(138,190,185,0.15);
    color: #B7E5CD;
    padding: 14px 20px;
    border-radius: 20px 20px 4px 20px;
    max-width: 70%;
    font-size: 0.95rem;
    line-height: 1.55;
    box-shadow: 0 14px 32px rgba(0,0,0,0.22);
}
.bot-bubble {
    display: flex;
    justify-content: flex-start;
    margin: 10px 0;
    animation: slideInLeft 0.3s ease;
}
.bot-avatar {
    width: 36px; height: 36px;
    background: rgba(138,190,185,0.18);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-right: 10px;
    margin-top: 4px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
    color: #B7E5CD;
}
.bot-bubble-inner {
    background: linear-gradient(180deg, rgba(48,86,105,0.62), rgba(20,38,56,0.78));
    border: 1px solid rgba(183,229,205,0.18);
    color: rgba(226,247,255,0.92);
    padding: 18px 22px;
    border-radius: 20px 20px 20px 4px;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.75;
    backdrop-filter: blur(14px);
    box-shadow: 0 18px 46px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.03);
}
.bot-bubble-inner strong { color: #B7E5CD; }
.bot-bubble-inner table {
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 0.85rem;
    width: 100%;
}
.bot-bubble-inner th {
    background: rgba(138,190,185,0.16);
    color: #B7E5CD;
    padding: 6px 10px;
    border: 1px solid rgba(183,229,205,0.12);
    text-align: left;
}
.bot-bubble-inner td {
    padding: 5px 10px;
    border: 1px solid rgba(183,229,205,0.12);
    color: rgba(183,229,205,0.82);
}
.bot-bubble-inner code {
    background: rgba(0,0,0,0.3);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem;
    color: #B7E5CD;
}

/* Chat container */
.chat-container {
    background:
        radial-gradient(circle at 10% 10%, rgba(183,229,205,0.10), transparent 26%),
        radial-gradient(circle at 84% 18%, rgba(138,190,185,0.08), transparent 22%),
        linear-gradient(180deg, rgba(12, 22, 38, 0.88), rgba(8, 16, 30, 0.80));
    border: 1px solid rgba(183,229,205,0.12);
    border-radius: 28px;
    padding: 0;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 0 48px rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(18px) saturate(140%);
}

#chat-box {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 24px;
    gap: 8px;
}

.chat-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 0;
    margin-top: 0;
    animation: fadeInUp 0.45s ease both;
    padding: 28px 24px 18px;
    border-bottom: 1px solid rgba(183,229,205,0.12);
    flex-shrink: 0;
    backdrop-filter: blur(16px);
}
.chat-hero h1 {
    margin: 0;
    color: #B7E5CD;
    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: clamp(1.4rem, 3vw, 2rem);
    font-weight: 850;
    letter-spacing: -0.035em;
}
.chat-hero h1 span {
    background: linear-gradient(135deg, #8ABEB9, #C1785A);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.chat-hero p {
    margin: 6px 0 0;
    color: rgba(226,247,255,0.62);
    max-width: 580px;
    line-height: 1.5;
    font-weight: 500;
    font-size: 0.92rem;
}
.chat-hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid rgba(183,229,205,0.22);
    background: rgba(138,190,185,0.08);
    color: rgba(226,247,255,0.84);
    font-size: 0.75rem;
    font-weight: 700;
    white-space: nowrap;
    box-shadow: 0 4px 12px rgba(138,190,185,0.10);
}

/* Confidence badge */
.conf-badge {
    font-size: 0.72rem;
    color: rgba(226, 247, 255, 0.44);
    margin-top: 4px;
    margin-left: 46px;
    font-family: 'JetBrains Mono', monospace !important;
}

.input-disclaimer {
    text-align: center;
    color: rgba(226,247,255,0.34);
    font-size: 0.72rem;
    margin: 8px 0 2px;
}

/* Typing indicator */
.typing-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #8ABEB9;
    margin: 0 2px;
    animation: typing 1.4s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing { 0%,80%,100% { opacity: 0.2; transform: scale(0.8); }
                    40% { opacity: 1; transform: scale(1); } }

/* Premium login page */
.st-key-login_page {
    min-height: 100vh;
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    justify-content: stretch;
    padding: 0;
    margin: 0;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 12% 18%, rgba(138,190,185,0.14), transparent 20%),
        radial-gradient(circle at 84% 12%, rgba(183,229,205,0.10), transparent 18%),
        radial-gradient(circle at 54% 78%, rgba(48,86,105,0.08), transparent 28%),
        linear-gradient(155deg, #04070f 0%, #071229 38%, #050a16 100%);
    color: #eef7ff;
}

.st-key-login_page::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 18% 20%, rgba(138,190,185,0.12), transparent 18%),
        radial-gradient(circle at 82% 14%, rgba(183,229,205,0.09), transparent 18%),
        linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0) 42%);
    animation: glowOrbit 14s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}

@keyframes glowOrbit {
    0%, 100% { transform: translateY(0); filter: drop-shadow(0 16px 46px rgba(183,229,205,0.24)); }
    50% { transform: translateY(-5px); filter: drop-shadow(0 24px 64px rgba(183,229,205,0.36)); }
}

@keyframes logoGlow {
    0%, 100% { transform: translateY(0); filter: drop-shadow(0 16px 46px rgba(183,229,205,0.24)); }
    50% { transform: translateY(-5px); filter: drop-shadow(0 24px 64px rgba(183,229,205,0.36)); }
}

.st-key-login_page::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(circle at 20% 48%, transparent 1px, rgba(138,190,185,0.02) 1px),
        radial-gradient(circle at 60% 72%, transparent 1px, rgba(183,229,205,0.02) 1px),
        radial-gradient(circle at 80% 14%, transparent 1px, rgba(138,190,185,0.02) 1px);
    background-size: 360px 360px;
    animation: gridFloat 26s linear infinite;
    z-index: 0;
    pointer-events: none;
}

@keyframes gridFloat {
    0% { transform: translate(0, 0); }
    100% { transform: translate(400px, 400px); }
}

/* Left hero section */
.login-hero-section {
    flex: 1.2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    padding: 72px 84px;
    position: relative;
    z-index: 1;
    background: linear-gradient(135deg, rgba(11, 17, 33, 0.5) 0%, rgba(12, 16, 38, 0.52) 100%);
    border-right: 1px solid rgba(183,229,205,0.12);
}

.login-hero-section::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 10% 90%, rgba(115,143,156,0.08), transparent 35%),
                radial-gradient(circle at 85% 10%, rgba(183,229,205,0.06), transparent 30%);
    pointer-events: none;
}

.login-hero-content {
    max-width: 680px;
    position: relative;
    z-index: 2;
}

.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 18px;
    border-radius: 999px;
    background: rgba(138,190,185,0.12);
    border: 1px solid rgba(183,229,205,0.22);
    color: #B7E5CD;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(138,190,185,0.08);
}

.login-hero-content h1 {
    font-size: clamp(3rem, 5vw, 4.8rem);
    font-weight: 900;
    margin: 0 0 22px 0;
    line-height: 0.95;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #B7E5CD 0%, #8ABEB9 45%, #C1785A 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 16px 36px rgba(0, 0, 0, 0.18);
    animation: fadeInLeft 0.8s ease both;
}

.login-hero-content p {
    font-size: 1.15rem;
    color: rgba(226, 247, 255, 0.78);
    margin: 0 0 34px 0;
    font-weight: 500;
    max-width: 600px;
    animation: fadeInLeft 0.8s ease both 0.1s;
}

/* Explicit hero title/subtitle selectors to ensure styles apply when used */
.hero-title {
    font-size: clamp(3rem, 5vw, 4.8rem);
    font-weight: 900;
    margin: 0 0 22px 0;
    line-height: 0.95;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #B7E5CD 0%, #8ABEB9 45%, #C1785A 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 16px 36px rgba(0, 0, 0, 0.18);
    animation: fadeInLeft 0.8s ease both;
}

.hero-subtitle {
    font-size: 1.15rem;
    color: rgba(226, 247, 255, 0.78);
    margin: 0 0 34px 0;
    font-weight: 500;
    max-width: 600px;
    animation: fadeInLeft 0.8s ease both 0.1s;
}

/* Feature pills */
.feature-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-bottom: 28px;
    animation: fadeInLeft 0.8s ease both 0.2s;
}

.feature-pill {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    padding: 14px 20px;
    background: rgba(10, 20, 40, 0.74);
    border: 1px solid rgba(183,229,205,0.18);
    border-radius: 18px;
    color: rgba(226, 247, 255, 0.92);
    font-size: 0.95rem;
    font-weight: 700;
    backdrop-filter: blur(16px);
    transition: all 0.28s ease;
    cursor: default;
}

.feature-pill:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 44px rgba(138,190,185,0.12);
    border-color: rgba(183,229,205,0.32);
}

.hero-card-row {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    width: 100%;
    max-width: 720px;
    margin-top: 20px;
    animation: fadeInLeft 0.8s ease both 0.3s;
}

.hero-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 18px 22px;
    border-radius: 24px;
    background: rgba(4, 11, 24, 0.72);
    border: 1px solid rgba(183,229,205,0.14);
    box-shadow: 0 18px 38px rgba(2, 33, 74, 0.28);
    backdrop-filter: blur(18px);
}

.hero-card-icon {
    width: 50px;
    height: 50px;
    border-radius: 18px;
    display: grid;
    place-items: center;
    font-size: 1.4rem;
    background: linear-gradient(135deg, rgba(138,190,185,0.14), rgba(48,86,105,0.22));
    border: 1px solid rgba(183,229,205,0.2);
}

.hero-card strong {
    display: block;
    color: #eef7ff;
    font-size: 0.98rem;
    font-weight: 700;
}

.hero-card span {
    color: rgba(226, 247, 255, 0.7);
    font-size: 0.85rem;
    line-height: 1.5;
}

/* Floating cards */
.floating-cards {
    position: absolute;
    bottom: 58px;
    left: 80px;
    display: flex;
    gap: 20px;
    z-index: 2;
}

.floating-card {
    width: 106px;
    height: 106px;
    background: rgba(33, 58, 79, 0.24);
    border: 1px solid rgba(183,229,205,0.22);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.18);
    animation: float 4.5s ease-in-out infinite;
}

.floating-card:nth-child(2) { animation-delay: 0.4s; }
.floating-card:nth-child(3) { animation-delay: 0.8s; }

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-18px); }
}

/* Right auth section */
.login-auth-section {
    flex: 0.95;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 48px 48px;
    position: relative;
    z-index: 1;
}

.st-key-login_card {
    position: relative;
    z-index: 0;
    width: 100%;
    max-width: 520px;
    padding: 52px 42px 46px;
    border-radius: 34px;
    background: rgba(10, 18, 34, 0.74);
    border: 1px solid rgba(183,229,205,0.20);
    backdrop-filter: blur(20px) saturate(190%);
    box-shadow:
        0 45px 120px rgba(2, 12, 30, 0.44),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
    animation: fadeInUp 0.7s ease both 0.2s;
    overflow: hidden;
}

.st-key-login_card::before {
    content: "";
    position: absolute;
    inset: -1px;
    pointer-events: none;
    z-index: -1;
    border-radius: 32px;
    background: linear-gradient(135deg, rgba(138,190,185,0.30), rgba(48,86,105,0.24), rgba(193,120,90,0.18));
    opacity: 0.9;
    animation: glowPulse 3.8s ease-in-out infinite;
    mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    mask-composite: exclude;
    -webkit-mask-composite: xor;
    padding: 1px;
}

.st-key-login_card::after {
    content: "";
    position: absolute;
    bottom: -36px;
    left: 50%;
    transform: translateX(-50%);
    width: 280px;
    height: 280px;
    pointer-events: none;
    z-index: -1;
    text-align: center;
    padding-bottom: 28px;
    border-bottom: 1px solid rgba(183,229,205,0.14);
    margin-bottom: 28px;
}

.login-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 84px;
    height: 84px;
    margin-bottom: 18px;
    font-size: 3.5rem;
    filter: drop-shadow(0 16px 46px rgba(183,229,205,0.24));
    animation: logoGlow 2.2s ease-in-out infinite;
}

.login-title {
    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    line-height: 1.12;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #B7E5CD 0%, #8ABEB9 45%, #C1785A 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 0 0 10px 0;
}

.login-subtitle {
    margin: 0;
    color: rgba(226, 247, 255, 0.72);
    font-size: 1rem;
    font-weight: 500;
}

.login-helper {
    margin: 22px 0 0 0;
    text-align: center;
    color: rgba(226, 247, 255, 0.6);
    font-size: 0.92rem;
    font-weight: 500;
}

.login-helper b {
    color: #8ABEB9;
    font-weight: 700;
}

/* Premium tabs */
.st-key-login_card .stTabs [data-baseweb="tab-list"] {
    width: 100%;
    padding: 8px !important;
    border-radius: 14px !important;
    background: rgba(15, 14, 46, 0.4) !important;
    border: 1px solid rgba(183,229,205,0.2);
    gap: 6px !important;
    margin-bottom: 24px !important;
}

.st-key-login_card .stTabs [data-baseweb="tab"] {
    flex: 1;
    height: 44px;
    border-radius: 12px !important;
    color: rgba(226, 247, 255, 0.6) !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.st-key-login_card .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(138,190,185,0.92), rgba(48,86,105,0.88)) !important;
    color: white !important;
    box-shadow: 0 12px 32px rgba(138,190,185,0.22);
    transform: scale(1.02);
}

.st-key-login_card .stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* Premium inputs */
.st-key-login_card .stTextInput {
    margin-bottom: 16px;
    position: relative;
}

.st-key-login_card .stTextInput label {
    color: rgba(226, 247, 255, 0.85) !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
    margin-bottom: 8px !important;
    display: block !important;
}

.st-key-login_card .stTextInput input {
    background: rgba(15, 14, 46, 0.5) !important;
    border: 1.5px solid rgba(183,229,205,0.2) !important;
    color: #f0f9ff !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
}

.st-key-login_card .stTextInput input::placeholder {
    color: rgba(226, 247, 255, 0.35) !important;
}

.st-key-login_card .stTextInput input:focus {
    border-color: #8ABEB9 !important;
    background: rgba(15, 14, 46, 0.7) !important;
    box-shadow: 0 0 0 3px rgba(138,190,185,0.16), 0 8px 20px rgba(48,86,105,0.14) !important;
    outline: none !important;
}

/* Premium buttons */
.st-key-login_card .stButton button {
    background: linear-gradient(135deg, #8ABEB9 0%, #305669 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 14px 24px !important;
    margin-top: 8px !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.01em;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 12px 32px rgba(48,86,105,0.18), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.st-key-login_card .stButton button::before {
    content: "";
    position: absolute;
    top: 0;
    left: -120%;
    width: 28%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.24), transparent);
    transition: left 0.6s ease;
}

.st-key-login_card .stButton button:hover::before {
    left: 120%;
}

.st-key-login_card .stButton button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 18px 48px rgba(48,86,105,0.28), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    background: linear-gradient(135deg, #8ABEB9 0%, #305669 100%) !important;
}

.st-key-login_card .stButton button:active {
    transform: translateY(-1px) !important;
}

/* AI Powered badge */
.ai-powered-badge {
    position: absolute;
    top: 22px;
    right: 22px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    background: rgba(7, 11, 26, 0.88);
    border: 1px solid rgba(183,229,205,0.22);
    border-radius: 999px;
    color: rgba(226, 247, 255, 0.92);
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    box-shadow: 0 18px 40px rgba(4, 11, 25, 0.35);
}

.ai-powered-badge::before {
    content: "";
    display: inline-block;
    width: 10px;
    height: 10px;
    background: #C1785A;
    border-radius: 50%;
    box-shadow: 0 0 0 6px rgba(193,120,90,0.14);
    animation: pulse 1.6s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}

/* Responsive */
@media (max-width: 1200px) {
    .st-key-login_page {
        flex-direction: column;
    }
    
    .login-hero-section {
        padding: 40px 60px;
        border-right: none;
        border-bottom: 1px solid rgba(183,229,205,0.12);
        justify-content: flex-start;
        min-height: 50vh;
    }
    
    .login-auth-section {
        min-height: 50vh;
    }
    
    .floating-cards {
        bottom: 40px;
        left: 60px;
    }
    
    .login-hero-content h1 {
        font-size: clamp(2rem, 4vw, 2.5rem);
    }
}
/* Additional input refinements */
.st-key-login_card .stTextInput div[data-baseweb="input"] {
    background: transparent !important;
}
.st-key-login_card .stTextInput button {
    height: 44px !important;
    align-items: center !important;
}

@media (max-width: 720px) {
    .app-topbar {
        align-items: flex-start;
        flex-direction: column;
        gap: 10px;
        margin: 0 0 18px;
    }
    .st-key-login_page {
        min-height: auto;
        padding: 18px 0;
    }
    .st-key-login_card {
        padding: 24px 18px;
        margin: 0 8px;
    }
}

/* Metric cards */
.metric-card {
    background: rgba(8, 18, 38, 0.62);
    border: 1px solid rgba(183,229,205,0.14);
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
    backdrop-filter: blur(14px);
    box-shadow: 0 16px 38px rgba(0,0,0,0.18);
}
.metric-value { font-size: 2rem; font-weight: 800; color: #B7E5CD; }
.metric-label { font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 4px; }

/* Page title */
.page-title {
    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: clamp(2rem, 3vw, 2.75rem);
    font-weight: 850;
    color: #B7E5CD;
    letter-spacing: -0.035em;
    margin-bottom: 10px;
    text-shadow: 0 12px 34px rgba(0,0,0,0.25);
}
.page-subtitle {
    color: rgba(226, 247, 255, 0.58);
    font-size: 0.98rem;
    margin-bottom: 26px;
    font-weight: 520;
}

/* Input styling */
.stExpander {
    margin: 14px 0 20px 0 !important;
}
.stExpander details summary {
    min-height: 44px !important;
    align-items: center !important;
}
.stExpander details summary p {
    margin: 0 !important;
    line-height: 1.4 !important;
}
.stTextInput input, .stTextArea textarea {
    background: rgba(3, 7, 18, 0.52) !important;
    border: 1px solid rgba(183,229,205,0.16) !important;
    color: white !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #8ABEB9 !important;
    box-shadow: 0 0 0 2px rgba(138,190,185,0.18), 0 0 22px rgba(48,86,105,0.12) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: rgba(255,255,255,0.7) !important;
}

/* Primary button */
.stButton button[kind="primary"], .stButton button {
    background: linear-gradient(135deg, #8ABEB9, #305669) !important;
    color: white !important;
    border: 1px solid rgba(183,229,205,0.18) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 12px 28px rgba(48,86,105,0.14);
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 14px 34px rgba(48,86,105,0.22) !important;
    border-color: rgba(183,229,205,0.42) !important;
}

/* Quick action buttons */
.st-key-quick_questions {
    animation: fadeInUp 0.5s ease both;
    margin-top: auto;
    padding-top: 16px;
    border-top: 1px solid rgba(183,229,205,0.1);
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.st-key-quick_questions .stButton button {
    min-height: 44px !important;
    border-radius: 13px !important;
    background: linear-gradient(135deg, #8ABEB9 0%, #305669 100%) !important;
    border: 1px solid rgba(183,229,205,0.28) !important;
    box-shadow: 0 8px 20px rgba(48,86,105,0.18), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    font-weight: 650 !important;
    font-size: 0.92rem !important;
}
.st-key-quick_questions .stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(48,86,105,0.28), inset 0 1px 0 rgba(255,255,255,0.12) !important;
    filter: brightness(1.08);
    background: linear-gradient(135deg, #8ABEB9 0%, #305669 100%) !important;
}

/* Dataframe */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Divider */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* Custom scrollbar */
* {
    scrollbar-width: thin;
    scrollbar-color: rgba(183,229,205,0.38) rgba(2, 6, 23, 0.28);
}
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: rgba(2, 6, 23, 0.28);
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(183,229,205,0.44), rgba(48,86,105,0.36));
    border-radius: 999px;
    border: 2px solid rgba(2, 6, 23, 0.55);
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, rgba(183,229,205,0.62), rgba(48,86,105,0.50));
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(3, 7, 18, 0.42) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(183,229,205,0.12);
}
.stTabs [data-baseweb="tab"] {
    color: rgba(255,255,255,0.6) !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(138,190,185,0.32) !important;
    color: white !important;
}

/* Alerts */
.stAlert { border-radius: 10px !important; }

/* Quick reply chips */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }
.chip {
    background: rgba(138,190,185,0.16);
    border: 1px solid rgba(183,229,205,0.38);
    color: #B7E5CD;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-block;
}
.chip:hover { background: rgba(138,190,185,0.32); }

@keyframes slideInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: none; } }
@keyframes slideInLeft  { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: none; } }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInLeft { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }

/* Premium theme overrides */
body, .stApp, .stMarkdown, .stTextInput input, .stTextArea textarea,
.stButton button, .stSelectbox, label, p, div {
    color: #B7E5CD !important;
}
.stApp {
    background:
        radial-gradient(circle at 14% 18%, rgba(183,229,205,0.16), transparent 28%),
        radial-gradient(circle at 88% 12%, rgba(183,229,205,0.10), transparent 26%),
        radial-gradient(circle at 58% 92%, rgba(138,190,185,0.10), transparent 34%),
        linear-gradient(135deg, #13252f 0%, #203544 42%, #172935 100%) !important;
    background-attachment: fixed;
}
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(17, 33, 45, 0.96) 0%, rgba(10, 18, 28, 0.98) 100%) !important;
    border-right: 1px solid rgba(183,229,205,0.15) !important;
    box-shadow: 14px 0 42px rgba(0,0,0,0.22) !important;
}
section[data-testid="stSidebar"] * { color: #B7E5CD !important; }
section[data-testid="stSidebar"] .stButton button {
    background: rgba(48,86,105,0.64) !important;
    border: 1px solid rgba(183,229,205,0.18) !important;
    color: #B7E5CD !important;
    border-radius: 14px !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(138,190,185,0.18) !important;
    border-color: rgba(183,229,205,0.22) !important;
    transform: translateY(-1px) !important;
}
section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(180deg, #8ABEB9 0%, #305669 100%) !important;
    border-color: rgba(183,229,205,0.18) !important;
    color: #ffffff !important;
}
.app-topbar {
    background: linear-gradient(180deg, rgba(15, 28, 44, 0.78), rgba(18, 36, 56, 0.64)) !important;
    border: 1px solid rgba(183,229,205,0.15) !important;
    box-shadow: 0 16px 42px rgba(0,0,0,0.26) !important;
}
.topbar-brand, .topbar-status, .hero-title, .hero-card strong,
.hero-stat strong, .feature-pill, .hero-card span, .hero-stat span,
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: rgba(183,229,205,0.92) !important;
}
.stButton button[kind="primary"], .stButton button {
    background: linear-gradient(135deg, #8ABEB9 0%, #305669 100%) !important;
    border: 1px solid rgba(183,229,205,0.2) !important;
    color: #ffffff !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18) !important;
}
.stButton button:not([kind="primary"]) {
    background: rgba(48,86,105,0.45) !important;
    border: 1px solid rgba(183,229,205,0.2) !important;
    color: #B7E5CD !important;
}
.stButton button:hover {
    background: rgba(138,190,185,0.12) !important;
    transform: scale(1.02) !important;
    box-shadow: 0 14px 34px rgba(0,0,0,0.24) !important;
}
.stTextInput input, .stTextArea textarea {
    background: rgba(16, 28, 44, 0.72) !important;
    border: 1px solid rgba(183,229,205,0.18) !important;
    color: #B7E5CD !important;
    border-radius: 18px !important;
    box-shadow: inset 0 1px 10px rgba(0,0,0,0.28) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #8ABEB9 !important;
    box-shadow: 0 0 0 3px rgba(138,190,185,0.16) !important;
}
.stDataFrame {
    border-radius: 18px !important;
    border: 1px solid rgba(183,229,205,0.12) !important;
    background: rgba(48,86,105,0.40) !important;
}
.stAlert {
    background: rgba(23,46,61,0.72) !important;
    border: 1px solid rgba(183,229,205,0.15) !important;
    color: #B7E5CD !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(48,86,105,0.45) !important;
    border: 1px solid rgba(183,229,205,0.15) !important;
}
.stTabs [data-baseweb="tab"] {
    color: rgba(183,229,205,0.85) !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(138,190,185,0.22) !important;
    color: #ffffff !important;
}
.chip {
    background: rgba(138,190,185,0.18) !important;
    border: 1px solid rgba(183,229,205,0.22) !important;
    color: #B7E5CD !important;
}
.chip:hover { background: rgba(138,190,185,0.30) !important; }
.badge, .status-indicator, .dot, .notification-dot {
    background: #C1785A !important;
}
hr { border-color: rgba(183,229,205,0.15) !important; }
    </style>
"""), unsafe_allow_html=True)


# ─── SESSION STATE INIT ───────────────────────────────────────────────────────

def init_session():
    defaults = {
        "logged_in": False,
        "user": None,
        "chat_history": [],   # list of {"role": "user"|"bot", "text": ..., "intent": ..., "conf": ...}
        "model": None,
        "page": "chat",       # chat | admin
        "input_key": 0,
        "chat_input_text": "",
        "pending_user_message": "",
        "voice_text": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


def _queue_typed_message():
    text = st.session_state.get("chat_input_text", "").strip()
    if text:
        st.session_state.pending_user_message = text
        st.session_state.chat_input_text = ""


# ─── MODEL LOADING ────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="🤖 Training SmartCollegeBot model…")
def get_model():
    return load_or_train_model()


# ─── QUICK REPLY SUGGESTIONS ─────────────────────────────────────────────────

QUICK_REPLIES = [
    "How to apply for admission?",
    "What is the fee structure?",
    "Tell me about hostel facilities",
    "What scholarships are available?",
    "How to check my result?",
    "What are the placement statistics?",
    "Attendance requirements",
    "How to clear backlogs?",
]

QUICK_REPLY_ICONS = ["📄", "₹", "🏢", "🎁", "📊", "💼", "📅", "✓"]


# ─── LOGIN / REGISTER PAGE ────────────────────────────────────────────────────

def render_login():
    with st.container(key="login_page"):
        col_left, col_right = st.columns([1.55, 1], gap="large")

        with col_left:
            components.html(textwrap.dedent("""
            <html>
            <head>
            <style>
            body{margin:0;padding:0;background:transparent;font-family:Inter,Arial,sans-serif;color:#B7E5CD;}
            .login-hero-section { position: relative; min-height: 860px; padding: 64px 64px 48px; display:flex; flex-direction:column; gap:30px; overflow:hidden; box-sizing:border-box; background: linear-gradient(180deg, rgba(14, 24, 42, 0.88), rgba(10, 18, 32, 0.82)); border:1px solid rgba(183,229,205,0.18); box-shadow: 0 16px 48px rgba(0,0,0,0.28); backdrop-filter: blur(16px); }
            .login-hero-section::before { content: ""; position:absolute; inset:0; background: radial-gradient(circle at 16% 18%, rgba(183,229,205,0.12), transparent 18%), radial-gradient(circle at 86% 14%, rgba(193,120,90,0.10), transparent 18%), linear-gradient(180deg, rgba(29,48,63,0.84), rgba(23,41,54,0.92)); pointer-events:none; }
            .hero-grid { position:absolute; inset:0; background-image: linear-gradient(rgba(183,229,205,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(183,229,205,0.04) 1px, transparent 1px); background-size: 220px 220px; opacity:0.10; pointer-events:none; }
            .hero-light { position:absolute; right:-82px; top: 8px; width: 280px; height: 280px; background: radial-gradient(circle, rgba(138,190,185,0.16), transparent 62%); filter: blur(38px); pointer-events:none; }
            .hero-light.alt { left:-78px; top: 34%; width: 220px; height: 220px; background: radial-gradient(circle, rgba(193,120,90,0.12), transparent 66%); }
            .login-hero-content { position: relative; z-index: 1; max-width: 720px; }
            .hero-tag { display:inline-flex; align-items:center; gap:10px; padding:12px 18px; border-radius:999px; background: rgba(16, 28, 44, 0.72); border:1px solid rgba(183,229,205,0.16); color:rgba(183,229,205,0.95); font-size:0.9rem; font-weight:700; letter-spacing:0.01em; backdrop-filter:blur(14px); box-shadow:0 18px 36px rgba(0,0,0,0.18); }
            .hero-title { font-size: clamp(3rem, 5vw, 4.8rem); font-weight:900; margin:0; line-height:0.96; letter-spacing:-0.04em; background: linear-gradient(135deg, #B7E5CD 0%, #8ABEB9 45%, #C1785A 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
            .hero-subtitle { max-width: 680px; font-size:1.08rem; color: rgba(183,229,205,0.78); margin:0; line-height:1.7; font-weight:500; }
            .feature-pills { display:flex; flex-wrap:wrap; gap:14px; margin-top: 6px; margin-bottom:32px; }
            .feature-pill { display:inline-flex; align-items:center; gap:12px; padding:14px 18px; border-radius:18px; background: rgba(18, 30, 48, 0.72); border:1px solid rgba(183,229,205,0.14); color:#B7E5CD; font-size:0.95rem; font-weight:700; backdrop-filter:blur(16px); box-shadow:0 16px 40px rgba(0,0,0,0.20); }
            .feature-pill:hover { transform: translateY(-1px); }
            .hero-card-row { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:20px; width:100%; max-width:760px; margin-top: 10px; }
            .hero-card { display:flex; align-items:flex-start; gap:16px; padding:24px; border-radius:26px; background: rgba(16, 28, 44, 0.76); border:1px solid rgba(183,229,205,0.16); box-shadow: 0 18px 52px rgba(0, 0, 0, 0.22); backdrop-filter: blur(14px); transition: transform 0.3s ease, box-shadow 0.3s ease; }
            .hero-card:hover { transform: translateY(-2px); box-shadow: 0 20px 56px rgba(0, 0, 0, 0.24); }
            .hero-card-icon { width:52px; height:52px; border-radius:18px; display:grid; place-items:center; font-size:1.35rem; background: linear-gradient(135deg, rgba(138,190,185,0.18), rgba(48,86,105,0.24)); border:1px solid rgba(183,229,205,0.18); color:#B7E5CD; }
            .hero-card strong { display:block; color:#B7E5CD; font-size:1.02rem; font-weight:800; margin-bottom:6px; }
            .hero-card span { color: rgba(183,229,205,0.75); font-size:0.9rem; line-height:1.55; }
            .hero-stats-row { display:grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap:16px; margin-top:40px; width:100%; max-width:760px; }
            .hero-stat { padding:20px 24px; border-radius:24px; background: rgba(48,86,105,0.55); border:1px solid rgba(183,229,205,0.15); box-shadow:0 16px 40px rgba(0,0,0,0.20); backdrop-filter:blur(12px); transition: transform 0.25s ease; }
            .hero-stat:hover { transform: translateY(-1px); }
            .hero-stat strong { display:block; font-size:1.35rem; font-weight:800; color:#B7E5CD; margin-bottom:8px; }
            .hero-stat span { font-size:0.9rem; color: rgba(183,229,205,0.72); }
            @media (max-width: 960px) { .login-hero-section { padding: 34px 28px 30px; min-height: auto; } .hero-card-row { grid-template-columns: 1fr; } .hero-stats-row { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
            @media (max-width: 640px) { .login-hero-section { padding: 24px 18px; } .hero-title { font-size: 2.6rem; } .hero-card-row, .hero-stats-row { grid-template-columns: 1fr; } }
            </style>
            </head>
            <body>
            <div class="login-hero-section">
                <div class="hero-grid"></div>
                <div class="hero-light"></div>
                <div class="hero-light alt"></div>
                <div class="login-hero-content">
                    <div class="hero-tag">AI Campus Intelligence</div>
                    <h1 class="hero-title">SmartCollegeBot</h1>
                    <p class="hero-subtitle">Your AI-powered smart campus assistant for admission, exams, hostels, and placement insights.</p>
                </div>
                <div class="feature-pills">
                    <div class="feature-pill">📄 Admissions Help</div>
                    <div class="feature-pill">📚 Exam Guidance</div>
                    <div class="feature-pill">🏠 Hostel Support</div>
                    <div class="feature-pill">💼 Placement Insights</div>
                </div>
                <div class="hero-card-row">
                    <div class="hero-card">
                        <div class="hero-card-icon">🧠</div>
                        <div><strong>Adaptive Campus AI</strong><span>Instant answers for student life and policy.</span></div>
                    </div>
                    <div class="hero-card">
                        <div class="hero-card-icon">⚡</div>
                        <div><strong>Lightning-fast Guidance</strong><span>Optimized paths for admission, exams, and placements.</span></div>
                    </div>
                    <div class="hero-card">
                        <div class="hero-card-icon">🔒</div>
                        <div><strong>Secure Student Access</strong><span>Protected login and streamlined campus workflows.</span></div>
                    </div>
                    <div class="hero-card">
                        <div class="hero-card-icon">🌐</div>
                        <div><strong>Campus Pulse</strong><span>Real-time insights across departments and schedules.</span></div>
                    </div>
                </div>
                <div class="hero-stats-row">
                    <div class="hero-stat"><strong>24/7</strong><span>AI Assistant</span></div>
                    <div class="hero-stat"><strong>1000+</strong><span>Student Queries Answered</span></div>
                    <div class="hero-stat"><strong>98%</strong><span>Accuracy Rate</span></div>
                    <div class="hero-stat"><strong>10+</strong><span>Campus Services Integrated</span></div>
                </div>
            </div>
            </body>
            </html>
            """), height=860, scrolling=False)

        with col_right:
            st.markdown(textwrap.dedent("""
            <div class="ai-powered-badge">AI Powered</div>
            """), unsafe_allow_html=True)

            with st.container(key="login_card"):
                st.markdown(textwrap.dedent("""
                <div class="login-hero">
                    <div class="login-logo">🤖</div>
                    <div class="login-title">Welcome Back</div>
                    <div class="login-subtitle">Secure access to your campus AI workspace</div>
                </div>
                <div class="login-helper">No account yet? Use <b>Create Account</b> to onboard instantly.</div>
                """), unsafe_allow_html=True)

                tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])

                with tab1:
                    username = st.text_input(
                        "👤 Username",
                        placeholder="Enter your username",
                        key="login_user"
                    )
                    password = st.text_input(
                        "🔒 Password",
                        type="password",
                        placeholder="Enter your password",
                        key="login_pass"
                    )

                    col_rem, col_forgot = st.columns([3, 2])
                    with col_rem:
                        remember_me = st.checkbox("Remember me", key="remember_me")
                    with col_forgot:
                        if st.button("Forgot password?", key="forgot_password"):
                            st.info("Please contact support to reset your password.")

                    login_btn = st.button("Sign In", use_container_width=True, key="do_login")

                    if login_btn:
                        if not username or not password:
                            st.error("❌ Please enter both username and password.")
                        else:
                            user = authenticate(username, password)
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.user = user
                                st.session_state.chat_history = []
                                st.success(f"✨ Welcome back, {user['name']}!")
                                time.sleep(0.8)
                                st.rerun()
                            else:
                                st.error("❌ Invalid credentials. Please register first.")

                with tab2:
                    reg_user = st.text_input(
                        "👤 Username",
                        placeholder="Choose a unique username",
                        key="reg_user"
                    )
                    reg_name = st.text_input(
                        "📝 Full Name",
                        placeholder="Your full name",
                        key="reg_name"
                    )
                    reg_pass = st.text_input(
                        "🔒 Password",
                        type="password",
                        placeholder="Min 6 characters",
                        key="reg_pass"
                    )
                    reg_pass2 = st.text_input(
                        "🔁 Confirm Password",
                        type="password",
                        placeholder="Repeat your password",
                        key="reg_pass2"
                    )

                    register_btn = st.button("Create Account", use_container_width=True, key="do_register")

                    if register_btn:
                        if not reg_user or not reg_name or not reg_pass or not reg_pass2:
                            st.error("❌ All fields are required.")
                        elif len(reg_pass) < 6:
                            st.error("❌ Password must be at least 6 characters.")
                        elif reg_pass != reg_pass2:
                            st.error("❌ Passwords do not match.")
                        else:
                            success, msg = register_user(reg_user, reg_pass, reg_name)
                            if success:
                                st.success("✨ Account created! Now login with your credentials.")
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        user = st.session_state.user

        # User card
        role_badge = "🛡️ Admin" if user["role"] == "admin" else "🎓 Student"
        st.markdown(f"""
        <div style="background:linear-gradient(180deg,rgba(8,145,178,0.18),rgba(15,23,42,0.64));
             border:1px solid rgba(103,232,249,0.18);border-radius:18px;padding:18px 14px;margin-bottom:24px;
             box-shadow:0 18px 36px rgba(0,0,0,0.20);backdrop-filter:blur(16px);">
            <div style="font-size:1.9rem;text-align:center;margin-bottom:8px;filter:drop-shadow(0 8px 14px rgba(14,165,233,0.20));">👤</div>
            <div style="font-weight:800;font-size:1rem;text-align:center;color:#B7E5CD;">{user['name']}</div>
            <div style="font-size:0.75rem;text-align:center;opacity:0.8;margin-top:4px;color:rgba(183,229,205,0.76);">{role_badge}</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown("**Navigation**")
        if st.button("💬  Chat", use_container_width=True,
                     type="primary" if st.session_state.page == "chat" else "secondary"):
            st.session_state.page = "chat"
            st.rerun()

        if st.button("📜  My Chat History", use_container_width=True,
                     type="primary" if st.session_state.page == "history" else "secondary"):
            st.session_state.page = "history"
            st.rerun()

        if user["role"] == "admin":
            st.markdown("---")
            st.markdown("**Admin Tools**")
            if st.button("📊  Analytics Dashboard", use_container_width=True,
                         type="primary" if st.session_state.page == "admin_analytics" else "secondary"):
                st.session_state.page = "admin_analytics"
                st.rerun()
            if st.button("Manage Notices", use_container_width=True,
                         type="primary" if st.session_state.page == "admin_notices" else "secondary"):
                st.session_state.page = "admin_notices"
                st.rerun()

        st.markdown("---")
        if st.button("🚪  Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.chat_history = []
            st.rerun()


def render_topbar():
    user = st.session_state.user
    role = user.get("role", "student").title()
    st.markdown(textwrap.dedent(f"""
    <div class="app-topbar">
        <div class="topbar-brand">
            <span class="topbar-logo">🎓</span>
            <span class="topbar-brand-text">
                <span>SmartCollegeBot</span>
                <small>AI-powered college assistant</small>
            </span>
        </div>
        <div class="topbar-actions">
            <div class="topbar-status">
                <span class="status-dot"></span>
                <span>AI Online</span>
                <span style="opacity:0.38;">•</span>
                <span>{role}</span>
            </div>
            <span class="topbar-icon" title="Toggle theme" onclick="document.dispatchEvent(new CustomEvent('theme_toggle'))">☾</span>
            <span class="topbar-icon" title="View notifications" onclick="document.dispatchEvent(new CustomEvent('show_notifications'))">🔔</span>
            <span class="deploy-pill" title="Deploy to Streamlit Cloud" onclick="document.dispatchEvent(new CustomEvent('deploy_app'))">🚀 Deploy</span>
        </div>
    </div>
    <script>
        document.addEventListener('theme_toggle', function() {{
            alert('🌙 Theme toggle clicked!');
        }});
        document.addEventListener('show_notifications', function() {{
            alert('📢 No new notifications');
        }});
        document.addEventListener('deploy_app', function() {{
            alert('🚀 Deployment initiated! Building and deploying to Streamlit Cloud...');
        }});
    </script>
    """), unsafe_allow_html=True)



# ─── CHAT PAGE ────────────────────────────────────────────────────────────────

def render_chat():
    model = get_model()

    # Container wrapper
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown(textwrap.dedent("""
    <div class="chat-hero">
        <div>
            <h1>👋 Hello, I'm <span>SmartCollegeBot</span></h1>
            <p>Ask me about admissions, fees, courses, exams, hostel, placements, scholarships, and much more.</p>
        </div>
        <div class="chat-hero-badge">✦ Smart answers</div>
    </div>
    """), unsafe_allow_html=True)

    st.info("✅ SmartCollegeBot uses intent-based responses only.")

    # Chat messages area
    chat_html = '<div id="chat-box">'
    if not st.session_state.chat_history:
        chat_html += """
        <div style="flex: 1; display: flex; align-items: center; justify-content: center; text-align: center; color: rgba(255,255,255,0.3); padding: 40px 20px;">
            <div>
                <div style="font-size: 3rem; margin-bottom: 12px;">🎓</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: rgba(255,255,255,0.5);">
                    Hello! I'm SmartCollegeBot
                </div>
                <div style="font-size: 0.85rem; margin-top: 6px;">
                    Ask me about admissions, fees, courses, exams, hostel,<br>
                    placements, scholarships, and much more!
                </div>
            </div>
        </div>
        """
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="user-bubble">
                    <div class="user-bubble-inner">{msg["text"]}</div>
                </div>"""
            else:
                import markdown as md_lib
                try:
                    rendered = md_lib.markdown(msg["text"], extensions=['tables'])
                except Exception:
                    rendered = msg["text"].replace('\n', '<br>')
                conf_pct = int(msg.get("conf", 0) * 100)
                conf_color = "#4ade80" if conf_pct >= 60 else "#fbbf24" if conf_pct >= 35 else "#f87171"
                chat_html += f"""
                <div class="bot-bubble">
                    <div class="bot-avatar">🤖</div>
                    <div>
                        <div class="bot-bubble-inner">{rendered}</div>
                        <div class="conf-badge">
                            Intent: <b>{msg.get("intent","—")}</b> | 
                            Confidence: <span style="color:{conf_color}">{conf_pct}%</span>
                        </div>
                    </div>
                </div>"""
    chat_html += "</div>"
    
    st.markdown(chat_html, unsafe_allow_html=True)
    
    # Close chat container
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick replies
    with st.container(key="quick_questions"):
        st.markdown("**Quick Questions:**")
        cols = st.columns(4)
        for i, qr in enumerate(QUICK_REPLIES):
            with cols[i % 4]:
                label = f"{QUICK_REPLY_ICONS[i]}  {qr}  ›"
                if st.button(label, key=f"qr_{i}_{st.session_state.input_key}",
                             use_container_width=True):
                    _send_message(qr, model)
                    st.rerun()

    # Input area
    with st.container(key="chat_input_shell", border=True):
        col_inp, col_btn, col_voice = st.columns([7, 1.2, 0.5], vertical_alignment="center")
        with col_inp:
            st.text_input(
                "Your message",
                placeholder="Type your question here… (e.g. 'How do I apply for admission?')",
                key="chat_input_text",
                label_visibility="collapsed",
                on_change=_queue_typed_message,
            )
        with col_btn:
            st.button("➤", use_container_width=True, on_click=_queue_typed_message)
        with col_voice:
            voice_text = _render_voice_button()
    st.markdown(
        '<div class="input-disclaimer">SmartCollegeBot can make mistakes. Please verify important information.</div>',
        unsafe_allow_html=True
    )

    if voice_text:
        st.session_state.pending_user_message = voice_text

    pending_message = st.session_state.get("pending_user_message", "").strip()
    if pending_message:
        st.session_state.pending_user_message = ""
        _send_message(pending_message, model)
        st.session_state.input_key += 1
        st.rerun()


def _send_message(text: str, model):
    """Process a user message and generate bot response."""
    # Add user message
    st.session_state.chat_history.append({"role": "user", "text": text})

    learned, learned_score = find_learned_answer(text)
    if learned:
        tag = "admin_learned"
        conf = round(learned_score, 4)
        response = learned.get("answer", "")
    else:
        # Predict
        tag, conf = predict_intent(text, model)
        response = get_response(tag, conf)

    # Add bot message
    message_id = str(uuid4())
    st.session_state.chat_history.append({
        "id": message_id,
        "role": "bot",
        "text": response,
        "intent": tag,
        "conf": conf
    })
    
    # Log
    log_message(
        username=st.session_state.user["username"],
        user_message=text,
        bot_response=response,
        intent=tag,
        confidence=conf
    )


def _render_feedback_controls():
    last_bot = None
    for msg in reversed(st.session_state.chat_history):
        if msg.get("role") == "bot":
            last_bot = msg
            break

    if not last_bot or last_bot.get("feedback_saved"):
        return

    st.markdown("**Was this answer helpful?**")
    col_yes, col_no, col_comment = st.columns([1, 1, 4])
    comment_key = f"feedback_comment_{last_bot.get('id', 'latest')}"
    with col_comment:
        comment = st.text_input(
            "Optional feedback",
            placeholder="Optional: what should be improved?",
            key=comment_key,
            label_visibility="collapsed"
        )
    with col_yes:
        if st.button("Helpful", use_container_width=True, key=f"helpful_{last_bot.get('id')}"):
            add_feedback(last_bot.get("id", str(uuid4())), st.session_state.user["username"], "helpful", comment)
            last_bot["feedback_saved"] = True
            st.success("Thanks for the feedback.")
            st.rerun()
    with col_no:
        if st.button("Not helpful", use_container_width=True, key=f"not_helpful_{last_bot.get('id')}"):
            add_feedback(last_bot.get("id", str(uuid4())), st.session_state.user["username"], "not_helpful", comment)
            last_bot["feedback_saved"] = True
            st.success("Thanks. Admin can review this to improve answers.")
            st.rerun()


def _render_voice_button():
    try:
        from streamlit_mic_recorder import speech_to_text
    except ImportError:
        st.button("🎙️", use_container_width=True, disabled=True, key=f"voice_missing_{st.session_state.input_key}")
        return None

    voice_text = speech_to_text(
        language="en",
        start_prompt="🎙️",
        stop_prompt="⏹️",
        just_once=True,
        use_container_width=True,
        key=f"voice_{st.session_state.input_key}",
    )
    return voice_text.strip() if voice_text else None


# ─── CHAT HISTORY PAGE ────────────────────────────────────────────────────────

def render_history():
    import pandas as pd

    st.markdown('<div class="page-title">📜 My Chat History</div>', unsafe_allow_html=True)
    
    username = st.session_state.user["username"]
    logs = get_user_logs(username)
    
    if not logs:
        st.info("No chat history yet. Start a conversation!")
        return
    
    st.markdown(f"**Total conversations logged: {len(logs)}**")
    
    df = pd.DataFrame(logs)[["timestamp", "user_message", "intent", "confidence"]]
    df.columns = ["Time", "Your Question", "Intent Detected", "Confidence"]
    df["Confidence"] = df["Confidence"].apply(lambda x: f"{x*100:.1f}%")
    df = df.iloc[::-1].reset_index(drop=True)
    
    st.dataframe(df, use_container_width=True, height=500)
    
    if st.button("🗑️ Clear History", key="clear_my_hist"):
        # Only clear this user's display (actual logs kept for admin analytics)
        st.session_state.chat_history = []
        st.success("Chat session cleared.")
        st.rerun()


# ─── ADMIN: ANALYTICS ─────────────────────────────────────────────────────────

def render_notice_board():
    st.markdown('<div class="page-title">Notice Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Latest college announcements posted by admin.</div>', unsafe_allow_html=True)

    if st.session_state.user["role"] == "admin":
        if st.button("Manage Notices", use_container_width=True):
            st.session_state.page = "admin_notices"
            st.rerun()

    notices = get_notices()
    if not notices:
        st.info("No active notices yet.")
        return

    categories = ["All"] + sorted({n.get("category", "General") for n in notices})
    selected = st.selectbox("Filter by category", categories)
    if selected != "All":
        notices = [n for n in notices if n.get("category") == selected]

    for notice in notices:
        body = notice.get("body", "").replace(chr(10), "<br>")
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
             border-radius:12px;padding:16px 18px;margin:12px 0;">
            <div style="font-size:0.75rem;color:#C1785A;font-weight:700;text-transform:uppercase;">
                {notice.get("category", "General")} | {notice.get("created_at", "")}
            </div>
            <div style="font-size:1.1rem;color:#B7E5CD;font-weight:800;margin-top:4px;">
                {notice.get("title", "")}
            </div>
            <div style="color:rgba(183,229,205,0.88);margin-top:8px;line-height:1.6;">
                {body}
            </div>
            <div style="color:rgba(255,255,255,0.4);font-size:0.75rem;margin-top:10px;">
                Posted by {notice.get("posted_by", "admin")}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_pdf_qa():
    st.markdown('<div class="page-title">PDF Q&A</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Ask questions from PDFs uploaded by admin.</div>', unsafe_allow_html=True)

    documents = get_documents()
    if not documents:
        st.info("No PDFs uploaded yet. Ask admin to upload syllabus, rules, calendars, or notices.")
        return

    options = {"All uploaded PDFs": None}
    options.update({f"{d.get('title')} ({d.get('pages', 0)} pages)": d.get("id") for d in documents})
    selected = st.selectbox("Search in", list(options.keys()))
    question = st.text_input("Question", placeholder="Example: What are the exam rules in the uploaded document?")

    if st.button("Ask PDF", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
            return
        answer = answer_from_documents(question.strip(), options[selected])
        if answer:
            st.markdown(answer)
        else:
            st.warning("I could not find a strong match in the uploaded PDFs.")

    with st.expander("Uploaded PDFs"):
        for doc in documents:
            st.write(f"**{doc.get('title')}** - {doc.get('filename')} - uploaded {doc.get('uploaded_at')}")


def render_admin_notices():
    st.markdown('<div class="page-title">Manage Notices</div>', unsafe_allow_html=True)

    if st.button("View Notice Board", use_container_width=True):
        st.session_state.page = "notices"
        st.rerun()

    with st.form("add_notice_form"):
        title = st.text_input("Title")
        category = st.selectbox("Category", ["General", "Admissions", "Exams", "Fees", "Placements", "Events", "Hostel"])
        body = st.text_area("Notice details", height=140)
        submitted = st.form_submit_button("Publish Notice", use_container_width=True)
        if submitted:
            if not title.strip() or not body.strip():
                st.error("Title and details are required.")
            else:
                add_notice(title, body, category, st.session_state.user["username"])
                st.success("Notice published.")
                st.rerun()

    st.markdown("---")
    notices = get_notices(include_inactive=True)
    if not notices:
        st.info("No notices yet.")
        return

    for notice in notices:
        col_info, col_active, col_delete = st.columns([5, 1, 1])
        with col_info:
            status = "Active" if notice.get("active", True) else "Hidden"
            st.markdown(f"**{notice.get('title')}**  \n{notice.get('category')} | {status} | {notice.get('created_at')}")
        with col_active:
            new_active = not notice.get("active", True)
            label = "Hide" if notice.get("active", True) else "Show"
            if st.button(label, key=f"toggle_notice_{notice.get('id')}"):
                set_notice_active(notice.get("id"), new_active)
                st.rerun()
        with col_delete:
            if st.button("Delete", key=f"delete_notice_{notice.get('id')}"):
                delete_notice(notice.get("id"))
                st.rerun()


def render_admin_documents():
    st.markdown('<div class="page-title">Manage PDFs</div>', unsafe_allow_html=True)

    with st.form("pdf_upload_form"):
        title = st.text_input("Document title")
        uploaded = st.file_uploader("Upload PDF", type=["pdf"])
        submitted = st.form_submit_button("Upload PDF", use_container_width=True)
        if submitted:
            if not uploaded:
                st.error("Choose a PDF file first.")
            else:
                ok, msg = add_pdf_document(uploaded, title or uploaded.name, st.session_state.user["username"])
                st.success(msg) if ok else st.error(msg)
                if ok:
                    st.rerun()

    st.markdown("---")
    documents = get_documents()
    if not documents:
        st.info("No PDFs uploaded yet.")
        return

    for doc in documents:
        col_info, col_delete = st.columns([6, 1])
        with col_info:
            st.markdown(
                f"**{doc.get('title')}**  \n"
                f"{doc.get('filename')} | {doc.get('pages', 0)} pages | "
                f"{len(doc.get('chunks', []))} sections | uploaded {doc.get('uploaded_at')}"
            )
        with col_delete:
            if st.button("Delete", key=f"delete_doc_{doc.get('id')}"):
                delete_document(doc.get("id"))
                st.rerun()


def render_admin_feedback():
    import pandas as pd

    st.markdown('<div class="page-title">Feedback Review</div>', unsafe_allow_html=True)
    summary = get_feedback_summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("Helpful", summary.get("helpful", 0))
    col2.metric("Not Helpful", summary.get("not_helpful", 0))
    total = summary.get("helpful", 0) + summary.get("not_helpful", 0)
    score = (summary.get("helpful", 0) / total * 100) if total else 0
    col3.metric("Helpful Rate", f"{score:.1f}%")

    feedback = get_all_feedback()
    if not feedback:
        st.info("No feedback submitted yet.")
        return

    df = pd.DataFrame(feedback)
    st.dataframe(df, use_container_width=True, height=420)


def render_admin_analytics():
    import pandas as pd

    st.markdown('<div class="page-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    
    logs = get_all_logs()
    
    if not logs:
        st.info("No data yet. Conversations will appear here.")
        return

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    users_set = set(l["username"] for l in logs)
    avg_conf = sum(l.get("confidence", 0) for l in logs) / len(logs) if logs else 0
    
    for col, (val, label) in zip(
        [col1, col2, col3, col4],
        [
            (len(logs), "Total Messages"),
            (len(users_set), "Unique Users"),
            (f"{avg_conf*100:.1f}%", "Avg Confidence"),
            (len(get_intent_stats()), "Intents Used"),
        ]
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🏷️ Top Intents")
        intent_stats = get_intent_stats()
        if intent_stats:
            df_intents = pd.DataFrame(
                list(intent_stats.items())[:15],
                columns=["Intent", "Count"]
            )
            st.bar_chart(df_intents.set_index("Intent"))

    with col_right:
        st.subheader("📅 Daily Activity")
        daily = get_daily_stats()
        if daily:
            df_daily = pd.DataFrame(
                list(daily.items()),
                columns=["Date", "Messages"]
            )
            st.line_chart(df_daily.set_index("Date"))

    st.subheader("📋 Recent Logs")
    df = pd.DataFrame(logs[-50:][::-1])
    if not df.empty:
        show_cols = ["timestamp", "username", "user_message", "intent", "confidence"]
        available = [c for c in show_cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True, height=300)
    
    if st.button("🗑️ Clear All Logs (Admin)", key="clear_all_admin"):
        clear_all_logs()
        st.success("All logs cleared.")
        st.rerun()


# ─── ADMIN: USER MANAGEMENT ───────────────────────────────────────────────────

def render_admin_users():
    import pandas as pd

    st.markdown('<div class="page-title">👥 User Management</div>', unsafe_allow_html=True)
    
    users = get_all_users()
    
    df = pd.DataFrame([
        {"Username": u, "Name": d["name"], "Email": d["email"],
         "Role": d["role"], "Joined": d["created_at"]}
        for u, d in users.items()
    ])
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("➕ Add New User")
        new_name  = st.text_input("Full Name", key="new_name")
        new_user  = st.text_input("Username", key="new_user_admin")
        new_email = st.text_input("Email", key="new_email")
        new_pass  = st.text_input("Password", type="password", key="new_pass")
        new_role  = st.selectbox("Role", ["student", "admin"], key="new_role")
        
        if st.button("Create User", key="create_user_btn"):
            ok, msg = register_user(new_user, new_pass, new_name, new_email, new_role)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    
    with col2:
        st.subheader("🔑 Reset Password")
        target_user = st.selectbox("Select User", list(users.keys()), key="reset_target")
        new_pw = st.text_input("New Password", type="password", key="reset_pw")
        if st.button("Reset Password", key="do_reset"):
            ok, msg = reset_password(target_user, new_pw)
            st.success(msg) if ok else st.error(msg)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("❌ Delete User")
        del_user = st.selectbox("Select User to Delete",
                                [u for u in users if u != "admin"], key="del_user")
        if st.button("Delete User", key="do_delete"):
            ok, msg = delete_user(del_user)
            st.success(msg) if ok else st.error(msg)
            if ok:
                st.rerun()


# ─── ADMIN: LOW CONFIDENCE ────────────────────────────────────────────────────

def render_low_confidence():
    import pandas as pd

    st.markdown('<div class="page-title">Improve Bot Answers</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="page-subtitle">
    Review low-confidence questions and save the correct answer for next time.
    </div>
    """, unsafe_allow_html=True)

    threshold = st.slider("Confidence Threshold", 0.1, 0.8, 0.4, 0.05)
    logs = get_low_confidence_logs(threshold)
    learned_answers = get_all_learned_answers()
    learned_questions = {item.get("normalized_question") for item in learned_answers}

    unresolved = []
    seen_questions = set()
    for log in logs:
        normalized = normalize_question(log.get("user_message", ""))
        if not normalized or normalized in learned_questions or normalized in seen_questions:
            continue
        seen_questions.add(normalized)
        unresolved.append(log)

    col_pending, col_saved = st.columns(2)
    col_pending.metric("Pending Questions", len(unresolved))
    col_saved.metric("Saved Answers", len(learned_answers))

    if unresolved:
        df = pd.DataFrame(unresolved)[["timestamp", "username", "user_message", "intent", "confidence"]]
        df["confidence"] = df["confidence"].apply(lambda x: f"{x*100:.1f}%")
        st.dataframe(df, use_container_width=True)

        options = [
            f"{log.get('user_message')}  ({log.get('confidence', 0) * 100:.1f}%)"
            for log in unresolved
        ]
        selected_label = st.selectbox("Select question to improve", options)
        selected_log = unresolved[options.index(selected_label)]
        selected_question = selected_log.get("user_message", "")

        with st.form("learn_answer_form"):
            st.text_area("Question", value=selected_question, disabled=True)
            answer = st.text_area(
                "Correct Answer",
                placeholder="Write the answer the bot should give when this question is asked again.",
                height=160,
            )
            submitted = st.form_submit_button("Save Answer")
            if submitted:
                if not answer.strip():
                    st.error("Please write an answer before saving.")
                else:
                    add_learned_answer(
                        selected_question,
                        answer,
                        st.session_state.user["username"],
                    )
                    st.success("Saved. The bot will use this answer for similar questions next time.")
                    st.rerun()
    else:
        st.success(f"No unresolved low-confidence questions below {threshold:.0%}.")

    st.markdown("---")
    st.subheader("Saved Admin Answers")
    if not learned_answers:
        st.info("No admin-learned answers yet.")
        return

    for item in learned_answers:
        with st.expander(item.get("question", "Saved question")):
            st.markdown(item.get("answer", ""))
            st.caption(f"Updated: {item.get('updated_at', '')} | Created by: {item.get('created_by', '')}")
            if st.button("Delete Saved Answer", key=f"delete_learned_{item.get('id')}"):
                delete_learned_answer(item.get("id"))
                st.success("Saved answer deleted.")
                st.rerun()


# ─── ADMIN: MODEL INFO ────────────────────────────────────────────────────────

def render_model_info():
    st.markdown('<div class="page-title">🧠 Model Information</div>', unsafe_allow_html=True)
    
    model = get_model()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚙️ Model Architecture")
        st.markdown("""
        | Component | Details |
        |-----------|---------|
        | **Algorithm** | Logistic Regression |
        | **Feature Extraction** | TF-IDF Vectorizer |
        | **N-gram Range** | (1, 3) — uni/bi/trigrams |
        | **Max Features** | 8,000 |
        | **Solver** | LBFGS (multinomial) |
        | **Regularization** | C = 5.0 |
        """)
    
    with col2:
        st.subheader("📊 Dataset Statistics")
        from dataset import INTENTS
        total_patterns = sum(len(i["patterns"]) for i in INTENTS if i["tag"] != "unknown")
        intent_count = len([i for i in INTENTS if i["tag"] != "unknown"])
        
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | **Total Intents** | {intent_count} |
        | **Total Patterns** | {total_patterns} |
        | **Augmented Samples** | ~{total_patterns * 5} |
        | **NLP Preprocessing** | Custom (no NLTK) |
        | **Tokenizer** | Regex word tokenizer |
        | **Stemmer** | Custom suffix stripper |
        | **Stopwords** | 60+ custom stopwords |
        """)
    
    st.subheader("🏷️ Intent Categories")
    cats = {}
    for intent in INTENTS:
        if intent["tag"] == "unknown":
            continue
        tag = intent["tag"]
        patterns = len(intent["patterns"])
        cats[tag] = patterns
    
    import pandas as pd
    df = pd.DataFrame(list(cats.items()), columns=["Intent Tag", "# Patterns"])
    df = df.sort_values("# Patterns", ascending=False).reset_index(drop=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df.head(15), use_container_width=True)
    with col2:
        st.bar_chart(df.set_index("Intent Tag").head(15))
    
    st.subheader("🔬 Test the Model")
    test_input = st.text_input("Enter a test query:", placeholder="e.g. 'How to apply for scholarship?'")
    if test_input:
        from model_utils import predict_intent, preprocess
        processed = preprocess(test_input)
        tag, conf = predict_intent(test_input, model)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Intent", tag)
        col2.metric("Confidence", f"{conf*100:.1f}%")
        col3.metric("Preprocessed Input", processed[:30] + "..." if len(processed) > 30 else processed)
        
        # Show top 5 probabilities
        if not hasattr(model, "named_steps"):
            model = load_or_train_model()
        probs = model.predict_proba([processed])[0]
        classes = model.classes_
        top5_idx = probs.argsort()[-5:][::-1]
        
        st.markdown("**Top 5 Intent Probabilities:**")
        for idx in top5_idx:
            pct = probs[idx] * 100
            bar = "█" * int(pct / 3)
            st.markdown(f"`{classes[idx]:<25}` {bar} **{pct:.1f}%**")


# ─── MAIN ROUTER ─────────────────────────────────────────────────────────────

def main():
    if not st.session_state.logged_in:
        render_login()
        return
    
    render_sidebar()
    
    page = st.session_state.get("page", "chat")
    
    if page == "chat":
        render_chat()
    elif page == "history":
        render_history()
    elif page == "notices":
        render_notice_board()
    elif page == "pdf_qa":
        render_pdf_qa()
    elif page == "admin_analytics":
        if st.session_state.user["role"] == "admin":
            render_admin_analytics()
        else:
            st.error("Access denied. Admin only.")
    elif page == "admin_users":
        if st.session_state.user["role"] == "admin":
            render_admin_users()
        else:
            st.error("Access denied. Admin only.")
    elif page == "admin_lowconf":
        if st.session_state.user["role"] == "admin":
            render_low_confidence()
        else:
            st.error("Access denied. Admin only.")
    elif page == "admin_model":
        if st.session_state.user["role"] == "admin":
            render_model_info()
        else:
            st.error("Access denied. Admin only.")
    elif page == "admin_notices":
        if st.session_state.user["role"] == "admin":
            render_admin_notices()
        else:
            st.error("Access denied. Admin only.")
    elif page == "admin_documents":
        if st.session_state.user["role"] == "admin":
            render_admin_documents()
        else:
            st.error("Access denied. Admin only.")
    elif page == "admin_feedback":
        if st.session_state.user["role"] == "admin":
            render_admin_feedback()
        else:
            st.error("Access denied. Admin only.")


if __name__ == "__main__":
    main()
