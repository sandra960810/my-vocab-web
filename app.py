import streamlit as st
import random

# 設定網頁標題與排版
st.set_page_config(page_title="我的專屬單字庫", page_icon="📖", layout="centered")

# --- 1. 完整單字庫 (由照片提取並校對) ---
if "words" not in st.session_state:
    st.session_state.words = [
        # 第一張照片內容
        {"en": "Ambivert", "zh": "中性性格者 (50% 50%)"},
        {"en": "Rational", "zh": "理性的"},
        {"en": "Delusional", "zh": "幻想的/妄想的"},
        {"en": "Complexion", "zh": "膚色/面色"},
        {"en": "Disciplined", "zh": "紀律的/自律的"},
        {"en": "Character", "zh": "特點/性格"},
        {"en": "Ludicrous", "zh": "可笑的/荒唐的"},
        {"en": "Rigid", "zh": "死板的/堅硬的"},
        {"en": "Versatile", "zh": "多才多藝的"},
        {"en": "Zodiac", "zh": "十二生肖/黃道帶"},
        {"en": "Nurture", "zh": "培育/養育"},
        {"en": "Offend", "zh": "得罪/冒犯"},
        {"en": "Put up with", "zh": "忍受"},
        {"en": "To pay the price", "zh": "付出代價"},
        {"en": "Bragging", "zh": "吹牛/自誇"},
        {"en": "Obnoxious", "zh": "令人討厭的"},
        {"en": "Profanity", "zh": "髒話/褻瀆"},
        {"en": "Irk", "zh": "使厭煩/惱火"},
        {"en": "Predict", "zh": "預測"},
        {"en": "Obligation", "zh": "義務/責任"},
        {"en": "Conduct", "zh": "執行/行為"},
        {"en": "Masculine", "zh": "男性的/陽剛的"},
        # 第二張照片內容
        {"en": "Panoramic", "zh": "全景的/全景畫"},
        {"en": "Financial commitment", "zh": "財務承諾"},
        {"en": "Enthusiast", "zh": "愛好者/熱衷者"},
        {"en": "Trial", "zh": "審判/試驗"},
        {"en": "Backpacking", "zh": "自助旅行/背包旅行"},
        {"en": "Devour", "zh": "吞食/狼吞虎嚥"},
        {"en": "Braised", "zh": "燉的/滷的"},
        {"en": "Consumption", "zh": "消耗/消費"},
        {"en": "Determine", "zh": "決定/確定"},
        {"en": "Involve", "zh": "涉及/包含"},
        {"en": "Compulsory", "zh": "強制的/義務的"},
        {"en": "Particular", "zh": "挑剔的/獨特的"},
        {"en": "Monetary relief", "zh": "貨幣救助/資金援助"},
        {"en": "Superstition", "zh": "迷信"},
        {"en": "Merchant", "zh": "商人"},
        {"en": "Unworthy", "zh": "不值得的"},
        {"en": "Netherworld", "zh": "冥界/地府"},
        {"en": "Prevalent", "zh": "流行的/普遍的"},
        {"en": "Mandatory", "zh": "強制的/指令的"},
        {"en": "Bride", "zh": "新娘"},
        {"en": "Despite", "zh": "儘管/雖然"},
        {"en": "Ruling", "zh": "裁決/判決"},
        {"en": "Cremation", "zh": "火葬"},
        {"en": "Urging", "zh": "催促/力勸"},
        {"en": "Ancestors", "zh": "祖先"}
    ]

# --- 2. 初始化 Session 狀態 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(st.session_state.words)
if "user_feedback" not in st.session_state:
    st.session_state.user_feedback = ""

# --- 3. 語音功能 (優化音質與語速) ---
def speak(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = 'en-US';
    msg.rate = 0.85;  // 稍慢語速，聽得更清楚
    msg.pitch = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 4. 側邊欄導覽 ---
st.sidebar.title("🛠️ 單字學習選單")
mode = st.sidebar.radio("請切換模式：", ["全單字庫複習", "單字拼寫練習", "造句練習模式", "自行新增單字"])

st.sidebar.divider()
st.sidebar.write(f"📊 目前共有 {len(st.session_state.words)} 個單字")

# --- 模式 A：全單字庫複習 ---
if mode == "全單字庫複習":
    st.title("📚 全單字庫複習")
    st.write("在練習之前，先快速瀏覽一遍你的筆記單字：")
    
    # 建立一個美觀的表格
    st.table(st.session_state.words)
    
    if st.button("🔊 隨機聽一個單字發音"):
        word = random.choice(st.session_state.words)
        st.write(f"正在朗讀：**{word['en']}**")
        speak(word['en'])

# --- 模式 B：單字拼寫練習 ---
elif mode == "單字拼寫練習":
    st.title("✍️ 拼寫測驗")
    q = st.session_state.current_q
    
    st.subheader(f"意思：:blue[{q['zh']}]")
    
    user_input = st.text_input("請拼出英文：", key="input_text").strip()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("檢查"):
            if user_input.lower() == q['en'].lower():
                st.session_state.user_feedback = "✅ 正確！你太棒了！"
                st.balloons()
                speak(q['en'])
            else:
                st.session_state.user_feedback = f"❌ 拼錯了，正確是：**{q['en']}**"
    
    with col2:
        if st.button("🔊 聽發音"):
            speak(q['en'])
            
    with col3:
        if st.button("下一題 ➡️"):
            st.session_state.current_q = random.choice(st.session_state.words)
            st.session_state.user_feedback = ""
            st.rerun()
            
    if st.session_state.user_feedback:
        st.markdown(st.session_state.user_feedback)

# --- 模式 C：造句練習模式 ---
elif mode == "造句練習模式":
    st.title("💡 造句練習")
    q = st.session_state.current_q
    st.write(f"請嘗試用單字 **{q['en']}** ({q['zh']}) 造一個句子：")
    
    sentence = st.text_area("在下方輸入句子：", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 朗讀我的句子"):
            if sentence:
                speak(sentence)
            else:
                st.warning("請先輸入內容喔！")
    with col2:
        if st.button("更換單字"):
            st.session_state.current_q = random.choice(st.session_state.words)
            st.
