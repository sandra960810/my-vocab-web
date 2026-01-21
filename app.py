import streamlit as st
import random
import requests # 改用這個發送網路請求

# --- 設定網頁 ---
st.set_page_config(page_title="我的專屬單字教練", page_icon="🎓", layout="wide")

# --- 關鍵修正：改用直接 API 連線 (完全不需要 Java) ---
def check_grammar_api(text):
    """直接呼叫 LanguageTool 官方 API，不依賴不穩定的 Python 套件"""
    url = "https://api.languagetool.org/v2/check"
    data = {
        'text': text,
        'language': 'en-US'
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json().get('matches', [])
        else:
            print(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

# --- 1. 完整單字庫 (已分類) ---
if "words" not in st.session_state:
    st.session_state.words = [
        # --- 🧠 性格與心理 ---
        {"en": "Ambivert", "zh": "中性性格者 (50% 50%)", "cat": "🧠 性格與心理"},
        {"en": "Rational", "zh": "理性的", "cat": "🧠 性格與心理"},
        {"en": "Delusional", "zh": "幻想的/妄想的", "cat": "🧠 性格與心理"},
        {"en": "Disciplined", "zh": "紀律的/自律的", "cat": "🧠 性格與心理"},
        {"en": "Character", "zh": "特點/性格", "cat": "🧠 性格與心理"},
        {"en": "Versatile", "zh": "多才多藝的", "cat": "🧠 性格與心理"},
        {"en": "Obnoxious", "zh": "令人討厭的", "cat": "🧠 性格與心理"},
        {"en": "Enthusiast", "zh": "愛好者", "cat": "🧠 性格與心理"},
        {"en": "Masculine", "zh": "男性的/陽剛的", "cat": "🧠 性格與心理"},
        {"en": "Superstition", "zh": "迷信", "cat": "🧠 性格與心理"},

        # --- ⚖️ 法律與義務 ---
        {"en": "Obligation", "zh": "義務/責任", "cat": "⚖️ 法律與義務"},
        {"en": "Conduct", "zh": "執行/行為", "cat": "⚖️ 法律與義務"},
        {"en": "Trial", "zh": "審判/試驗", "cat": "⚖️ 法律與義務"},
        {"en": "Compulsory", "zh": "強制的", "cat": "⚖️ 法律與義務"},
        {"en": "Mandatory", "zh": "強制的/指令的", "cat": "⚖️ 法律與義務"},
        {"en": "Ruling", "zh": "裁決", "cat": "⚖️ 法律與義務"},
        {"en": "Financial commitment", "zh": "財務承諾", "cat": "⚖️ 法律與義務"},
        {"en": "Monetary relief", "zh": "貨幣救助", "cat": "⚖️ 法律與義務"},

        # --- 🥘 生活與行為 ---
        {"en": "Nurture", "zh": "培育/養育", "cat": "🥘 生活與行為"},
        {"en": "Offend", "zh": "得罪/冒犯", "cat": "🥘 生活與行為"},
        {"en": "Put up with", "zh": "忍受", "cat": "🥘 生活與行為"},
        {"en": "To pay the price", "zh": "付出代價", "cat": "🥘 生活與行為"},
        {"en": "Bragging", "zh": "吹牛", "cat": "🥘 生活與行為"},
        {"en": "Profanity", "zh": "髒話", "cat": "🥘 生活與行為"},
        {"en": "Irk", "zh": "使厭煩", "cat": "🥘 生活與行為"},
        {"en": "Devour", "zh": "吞食", "cat": "🥘 生活與行為"},
        {"en": "Braised", "zh": "燉/滷的", "cat": "🥘 生活與行為"},
        {"en": "Consumption", "zh": "消耗/消費", "cat": "🥘 生活與行為"},
        {"en": "Backpacking", "zh": "自助旅行", "cat": "🥘 生活與行為"},
        {"en": "Cremation", "zh": "火葬", "cat": "🥘 生活與行為"},
        {"en": "Bride", "zh": "新娘", "cat": "🥘 生活與行為"},
        {"en": "Ancestors", "zh": "祖先", "cat": "🥘 生活與行為"},
        {"en": "Zodiac", "zh": "十二生肖", "cat": "🥘 生活與行為"},

        # --- 🖼️ 抽象與其他 ---
        {"en": "Ludicrous", "zh": "可笑的/荒唐的", "cat": "🖼️ 抽象與其他"},
        {"en": "Rigid", "zh": "死板的/堅硬的", "cat": "🖼️ 抽象與其他"},
        {"en": "Predict", "zh": "預測", "cat": "🖼️ 抽象與其他"},
        {"en": "Panoramic", "zh": "全景的", "cat": "🖼️ 抽象與其他"},
        {"en": "Determine", "zh": "決定", "cat": "🖼️ 抽象與其他"},
        {"en": "Involve", "zh": "涉及", "cat": "🖼️ 抽象與其他"},
        {"en": "Particular", "zh": "獨特的/挑剔的", "cat": "🖼️ 抽象與其他"},
        {"en": "Merchant", "zh": "商人", "cat": "🖼️ 抽象與其他"},
        {"en": "Unworthy", "zh": "不值得的", "cat": "🖼️ 抽象與其他"},
        {"en": "Netherworld", "zh": "冥界", "cat": "🖼️ 抽象與其他"},
        {"en": "Prevalent", "zh": "流行的/普遍的", "cat": "🖼️ 抽象與其他"},
        {"en": "Despite", "zh": "儘管", "cat": "🖼️ 抽象與其他"},
        {"en": "Urging", "zh": "催促", "cat": "🖼️ 抽象與其他"},
        {"en": "Complexion", "zh": "膚色/面色", "cat": "🖼️ 抽象與其他"}
    ]

# --- 2. 狀態初始化 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(st.session_state.words)

# --- 3. 語音功能 (HTML5) ---
def speak(text):
    clean_text = text.replace('"', '').replace("'", "")
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{clean_text}');
    msg.lang = 'en-US';
    msg.rate = 0.85; 
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 4. 側邊欄 ---
st.sidebar.title("功能選單")
mode = st.sidebar.radio("請選擇學習模式：", ["📚 分類複習 (Review)", "✍️ 拼寫測驗 (Quiz)", "👨‍🏫 AI 造句糾錯 (Grammar)"])
st.sidebar.divider()
st.sidebar.caption(f"目前單字量：{len(st.session_state.words)} 個")

# --- 模式 A: 分類複習 ---
if mode == "📚 分類複習 (Review)":
    st.title("📚 分類單字複習")
    st.info("點擊分類展開單字，勾選「顯示意思」來測試記憶力。")

    categories = sorted(list(set([w['cat'] for w in st.session_state.words])))
    
    for cat in categories:
        with st.expander(f"{cat}", expanded=False):
            cat_words = [w for w in st.session_state.words if w['cat'] == cat]
            for w in cat_words:
                c1, c2, c3 = st.columns([2, 1, 2])
                with c1:
                    st.markdown(f"### {w['en']}")
                with c2:
                    if st.button("🔊", key=f"speak_{w['en']}"):
                        speak(w['en'])
                with c3:
                    if st.checkbox("顯示意思", key=f"check_{w['en']}"):
                        st.write(f":blue[{w['zh']}]")
                st.divider()

# --- 模式 B: 拼寫測驗 ---
elif mode == "✍️ 拼寫測驗 (Quiz)":
    st.title("✍️ 拼寫測驗")
    q = st.session_state.current_q
    
    st.subheader(f"中文意思：:blue[{q['zh']}]")
    ans = st.text_input("請拼出英文：", key="quiz_input").strip()
    
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("檢查答案"):
            if ans.lower() == q['en'].lower():
                st.success("✅ 正確！")
                st.balloons()
                speak(q['en'])
            else:
                st.error(f"❌ 錯誤，正確答案是：{q['en']}")
    with c2:
        if st.button("🔊 聽發音"):
            speak(q['en'])
    with c3:
        if st.button("下一題 ➡️"):
            st.session_state.current_q = random.choice(st.session_state.words)
            st.rerun()

# --- 模式 C: 造句糾錯 (API 版本) ---
elif mode == "👨‍🏫 AI 造句糾錯 (Grammar)":
    st.title("👨‍🏫 AI 造句糾錯教練")
    
    q = st.session_state.current_q
    st.info(f"目標單字：**{q['en']}** ({q['zh']})")
    
    user_sentence = st.text_area("請造一個句子：", height=100, placeholder=f"例如：He is a very {q['en'].lower()} person.")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        if st.button("🔍 檢查文法"):
            if user_sentence:
                # 1. 關鍵字檢查
                if q['en'].lower() not in user_sentence.lower():
                    st.warning(f"⚠️ 句子裡好像沒用到單字：{q['en']}")
                
                # 2. 文法檢查 (呼叫 API)
                with st.spinner("AI 老師正在批改中..."):
                    matches = check_grammar_api(user_sentence)
                
                if matches is None:
                    st.error("連線不穩定，請稍後再試。")
                elif len(matches) == 0:
                    st.success("🎉 完美！沒有發現文法錯誤。")
                    st.balloons()
                    speak(user_sentence)
                else:
                    st.error(f"發現 {len(matches)} 個建議：")
                    for match in matches:
                        err_text = user_sentence[match['offset']:match['offset']+match['length']]
                        replacements = [r['value'] for r in match['replacements']]
                        suggestion = replacements[0] if replacements else "刪除"
                        st.write(f"❌ **{err_text}** -> ✅ **{suggestion}**")
                        st.caption(f"原因：{match['message']}")
            else:
                st.warning("請先輸入句子")
    
    with c2:
        if st.button("🔊 朗讀句子"):
            if user_sentence: speak(user_sentence)
            
    with c3:
        if st.button("換一題"):
            st.session_state.current_q = random.choice(st.session_state.words)
            st.rerun()

st.sidebar.divider()
st.sidebar.caption("由 Streamlit 與 LanguageTool API 驅動")
