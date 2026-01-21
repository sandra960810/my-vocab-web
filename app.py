import streamlit as st
import random
import requests
import time

# --- 設定網頁 ---
st.set_page_config(page_title="我的專屬單字教練", page_icon="🎓", layout="wide")

# --- 文法檢查 API ---
def check_grammar_api(text):
    url = "https://api.languagetool.org/v2/check"
    data = {'text': text, 'language': 'en-US'}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json().get('matches', [])
        return None
    except:
        return None

# --- 1. 完整單字庫 ---
if "words" not in st.session_state:
    st.session_state.words = [
        # --- 🧠 性格與心理 ---
        {"en": "Ambivert", "zh": "中性性格者", "cat": "🧠 性格與心理"},
        {"en": "Rational", "zh": "理性的", "cat": "🧠 性格與心理"},
        {"en": "Delusional", "zh": "幻想的", "cat": "🧠 性格與心理"},
        {"en": "Disciplined", "zh": "自律的", "cat": "🧠 性格與心理"},
        {"en": "Character", "zh": "性格", "cat": "🧠 性格與心理"},
        {"en": "Versatile", "zh": "多才多藝的", "cat": "🧠 性格與心理"},
        {"en": "Obnoxious", "zh": "令人討厭的", "cat": "🧠 性格與心理"},
        {"en": "Enthusiast", "zh": "愛好者", "cat": "🧠 性格與心理"},
        {"en": "Masculine", "zh": "陽剛的", "cat": "🧠 性格與心理"},
        {"en": "Superstition", "zh": "迷信", "cat": "🧠 性格與心理"},
        # --- ⚖️ 法律與義務 ---
        {"en": "Obligation", "zh": "義務", "cat": "⚖️ 法律與義務"},
        {"en": "Conduct", "zh": "行為/執行", "cat": "⚖️ 法律與義務"},
        {"en": "Trial", "zh": "審判", "cat": "⚖️ 法律與義務"},
        {"en": "Compulsory", "zh": "強制的", "cat": "⚖️ 法律與義務"},
        {"en": "Mandatory", "zh": "強制的", "cat": "⚖️ 法律與義務"},
        {"en": "Ruling", "zh": "裁決", "cat": "⚖️ 法律與義務"},
        {"en": "Financial commitment", "zh": "財務承諾", "cat": "⚖️ 法律與義務"},
        {"en": "Monetary relief", "zh": "貨幣救助", "cat": "⚖️ 法律與義務"},
        # --- 🥘 生活與行為 ---
        {"en": "Nurture", "zh": "培育", "cat": "🥘 生活與行為"},
        {"en": "Offend", "zh": "冒犯", "cat": "🥘 生活與行為"},
        {"en": "Put up with", "zh": "忍受", "cat": "🥘 生活與行為"},
        {"en": "To pay the price", "zh": "付出代價", "cat": "🥘 生活與行為"},
        {"en": "Bragging", "zh": "吹牛", "cat": "🥘 生活與行為"},
        {"en": "Profanity", "zh": "髒話", "cat": "🥘 生活與行為"},
        {"en": "Irk", "zh": "使厭煩", "cat": "🥘 生活與行為"},
        {"en": "Devour", "zh": "吞食", "cat": "🥘 生活與行為"},
        {"en": "Braised", "zh": "燉/滷", "cat": "🥘 生活與行為"},
        {"en": "Consumption", "zh": "消耗", "cat": "🥘 生活與行為"},
        {"en": "Backpacking", "zh": "自助旅行", "cat": "🥘 生活與行為"},
        {"en": "Cremation", "zh": "火葬", "cat": "🥘 生活與行為"},
        {"en": "Bride", "zh": "新娘", "cat": "🥘 生活與行為"},
        {"en": "Ancestors", "zh": "祖先", "cat": "🥘 生活與行為"},
        {"en": "Zodiac", "zh": "十二生肖", "cat": "🥘 生活與行為"},
        #
