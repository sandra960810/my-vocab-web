import streamlit as st
import random

# 設定網頁標題
st.set_page_config(page_title="高階單字學習系統", page_icon="🎓", layout="centered")

# 1. 初始單字庫 (包含你照片中的內容)
if "words" not in st.session_state:
    st.session_state.words = [
        {"en": "Ambivert", "zh": "中性性格者 (50% 50%)"},
        {"en": "Rational", "zh": "理性的"},
        {"en": "Delusional", "zh": "幻想的/妄想的"},
        {"en": "Complexion", "zh": "膚色/面色"},
        {"en": "Disciplined", "zh": "紀律的/自律的"},
        {"en": "Ludicrous", "zh": "可笑的/荒唐的"},
        {"en": "Versatile", "zh": "多才多藝的"},
        {"en": "Nurture", "zh": "培育/養育"},
        {"en": "Obnoxious", "zh": "令人討厭的"},
        {"en": "Profanity", "zh": "髒話/褻瀆"},
        {"en": "Mandatory", "zh": "強制的"},
        {"en": "Prevalent", "zh": "流行的/普遍的"},
        {"en": "Ancestors", "zh": "祖先"},
        {"en": "Financial commitment", "zh": "財務承諾"},
        {"en": "Cremation", "zh": "火葬"},
        {"en": "Netherworld", "zh": "冥界/地府"},
        {"en": "Urging", "zh": "催促/主張"},
        {"en": "Hinder", "zh": "阻礙"},
        {"en": "Zodiac", "zh": "十二生肖/黃道帶"}
    ]

# 初始化 Session State
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(st.session_state.words)
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# 自然語音函式 (調整語速與音調)
def speak_js(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = 'en-US';
    msg.rate = 0.9;  // 稍微放慢一點點，聽起來更清晰
    msg.pitch = 1.0; // 音調正常
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 側邊欄導覽 ---
st.sidebar.title("🚀 學習選單")
mode = st.sidebar.radio("請選擇模式：", ["單字拼寫練習", "全單字庫複習", "造句挑戰模式", "新增單字"])

# --- 模式 1：全單字庫複習 ---
if mode == "全單字庫複習":
    st.title("📚 全單字庫複習")
    st.write("在開始練習前，先溫習一下所有的單字吧！")
    
    # 使用表格顯示
    st.table(st.session_state.words)
    
    if st.button("全部準備好了，去練習！"):
        st.info("請從左側選單切換至練習模式")

# --- 模式 2：單字拼寫練習 ---
elif mode == "單字拼寫練習":
    st.title("✍️ 拼寫練習")
    q = st.session_state.current_q
    st.subheader(f"意思：:blue[{q['zh']}]")
    
    ans = st.text_input("請拼出英文單字：", key="quiz_input").strip()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("檢查答案"):
            if ans.lower() == q['en'].lower():
                st.success("✅ 正確！")
                st.balloons()
                speak_js(q['en'])
            else:
                st.error(f"❌ 錯誤，正確是：{q['en']}")
    with c2:
        if st.button("🔊 聽發音"):
            speak_js(q['en'])
    with c3:
        if st.button("下一題 ➡️"):
            st.session_state.current_q = random.choice(st.session_state.words)
            st.rerun()

# --- 模式 3：造句挑戰模式 ---
elif mode == "造句挑戰模式":
    st.title("💡 造句挑戰")
    q = st.session_state.current_q
    st.write(f"請使用單字 **{q['en']}** ({q['zh']}) 造一個句子：")
    
    sentence = st.text_area("在下方輸入你的句子：", placeholder="例如：He is a rational person...")
    
    if st.button("🔊 朗讀我的句子"):
        if sentence:
            speak_js(sentence)
        else:
            st.warning("請先輸入句子")
            
    if st.button("換一個單字造句"):
        st.session_state.current_q = random.choice(st.session_state.words)
        st.rerun()

# --- 模式 4：新增單字 ---
elif mode == "新增單字":
    st.title("➕ 擴充你的庫存")
    new_en = st.text_input("英文單字 (English)")
    new_zh = st.text_input("中文意思 (Chinese)")
    if st.button("儲存單字"):
        if new_en and new_zh:
            st.session_state.words.append({"en": new_en, "zh": new_zh})
            st.success("儲存成功！已加入單字庫。")
        else:
            st.error("請輸入完整資訊")
