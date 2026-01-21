import streamlit as st
import random

# 設定網頁標題與風格
st.set_page_config(page_title="My Vocab Master", page_icon="📝")

# 1. 這裡是你照片中的所有單字初始庫
initial_vocab = [
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
    {"en": "Obligation", "zh": "義務"},
    {"en": "Conduct", "zh": "執行/行為"},
    {"en": "Masculine", "zh": "男性的/陽剛的"},
    {"en": "Panoramic", "zh": "全景的"},
    {"en": "Financial commitment", "zh": "財務承諾"},
    {"en": "Enthusiast", "zh": "愛好者"},
    {"en": "Trail", "zh": "審判/小徑 (註:筆記中為Trial音近)"},
    {"en": "Devour", "zh": "吞食"},
    {"en": "Braised", "zh": "燉/滷的"},
    {"en": "Consumption", "zh": "消耗/消費"},
    {"en": "Determine", "zh": "決定"},
    {"en": "Involve", "zh": "涉及/包含"},
    {"en": "Compulsory", "zh": "強制的 (註:對應筆記compulsor)"},
    {"en": "Particular", "zh": "獨特的/挑剔的"},
    {"en": "Monetary relief", "zh": "貨幣救助"},
    {"en": "Superstition", "zh": "迷信"},
    {"en": "Merchant", "zh": "商人"},
    {"en": "Unworthy", "zh": "不值得的"},
    {"en": "Netherworld", "zh": "冥界/地府"},
    {"en": "Prevalent", "zh": "流行的/普遍的"},
    {"en": "Mandatory", "zh": "強制的"},
    {"en": "Bride", "zh": "新娘"},
    {"en": "Despite", "zh": "儘管"},
    {"en": "Ruling", "zh": "裁決"},
    {"en": "Cremation", "zh": "火葬"},
    {"en": "Urging", "zh": "催促"},
    {"en": "Ancestors", "zh": "祖先"}
]

# 初始化 session_state
if "words" not in st.session_state:
    st.session_state.words = initial_vocab
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(st.session_state.words)
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# --- 側邊欄：新增與管理 ---
with st.sidebar:
    st.header("⚙️ 單字管理")
    with st.expander("➕ 新增單字"):
        new_en = st.text_input("英文單字")
        new_zh = st.text_input("中文意思")
        if st.button("確認新增"):
            if new_en and new_zh:
                st.session_state.words.append({"en": new_en, "zh": new_zh})
                st.success(f"已新增: {new_en}")
            else:
                st.error("請填寫內容")
    
    st.write(f"目前單字總數：{len(st.session_state.words)}")
    if st.button("🔄 隨機換一題"):
        st.session_state.current_q = random.choice(st.session_state.words)
        st.session_state.feedback = ""
        st.rerun()

# --- 主畫面：測驗區 ---
st.title("📖 我的專屬單字練習站")
st.write("看中文，拼英文！練習完可以聽聽看發音。")

q = st.session_state.current_q

st.divider()
st.subheader(f"目標意思：:blue[{q['zh']}]")

# 輸入框
user_input = st.text_input("在這裡拼出英文...", key="user_ans").strip()

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("檢查"):
        if user_input.lower() == q['en'].lower():
            st.session_state.feedback = "✅ 正確！太棒了！"
            st.balloons()
        else:
            st.session_state.feedback = f"❌ 拼錯囉！正確是：**{q['en']}**"

with col2:
    # 網頁版語音按鈕
    if st.button("🔊 發音"):
        js_code = f'var msg = new SpeechSynthesisUtterance("{q["en"]}"); window.speechSynthesis.speak(msg);'
        st.components.v1.html(f'<script>{js_code}</script>', height=0)

with col3:
    if st.button("下一題 ➡️"):
        st.session_state.current_q = random.choice(st.session_state.words)
        st.session_state.feedback = ""
        st.rerun()

# 顯示回饋
if st.session_state.feedback:
    st.markdown(st.session_state.feedback)

st.divider()
st.caption("提示：在手機上打開這個網址，可以隨時隨地背單字！")
