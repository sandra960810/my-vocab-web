import streamlit as st
import random
import requests

# --- 設定網頁 ---
st.set_page_config(page_title="我的專屬單字教練", page_icon="🎓", layout="wide")

# --- 文法檢查 API (免安裝 Java) ---
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
        # --- 🖼️ 抽象與其他 ---
        {"en": "Ludicrous", "zh": "荒唐的", "cat": "🖼️ 抽象與其他"},
        {"en": "Rigid", "zh": "死板的", "cat": "🖼️ 抽象與其他"},
        {"en": "Predict", "zh": "預測", "cat": "🖼️ 抽象與其他"},
        {"en": "Panoramic", "zh": "全景的", "cat": "🖼️ 抽象與其他"},
        {"en": "Determine", "zh": "決定", "cat": "🖼️ 抽象與其他"},
        {"en": "Involve", "zh": "涉及", "cat": "🖼️ 抽象與其他"},
        {"en": "Particular", "zh": "獨特的", "cat": "🖼️ 抽象與其他"},
        {"en": "Merchant", "zh": "商人", "cat": "🖼️ 抽象與其他"},
        {"en": "Unworthy", "zh": "不值得的", "cat": "🖼️ 抽象與其他"},
        {"en": "Netherworld", "zh": "冥界", "cat": "🖼️ 抽象與其他"},
        {"en": "Prevalent", "zh": "流行的", "cat": "🖼️ 抽象與其他"},
        {"en": "Despite", "zh": "儘管", "cat": "🖼️ 抽象與其他"},
        {"en": "Urging", "zh": "催促", "cat": "🖼️ 抽象與其他"},
        {"en": "Complexion", "zh": "膚色", "cat": "🖼️ 抽象與其他"}
    ]

# --- 2. 初始化 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(st.session_state.words)

def speak(text):
    clean_text = text.replace('"', '').replace("'", "")
    js_code = f"""<script>
    var msg = new SpeechSynthesisUtterance('{clean_text}');
    msg.lang = 'en-US'; msg.rate = 0.85; window.speechSynthesis.speak(msg);
    </script>"""
    st.components.v1.html(js_code, height=0)

# --- 3. 側邊欄 ---
st.sidebar.title("功能選單")
mode = st.sidebar.radio("請選擇：", ["📚 分類複習", "✍️ 拼寫測驗", "👨‍🏫 AI 造句糾錯", "➕ 新增單字"])
st.sidebar.divider()
st.sidebar.caption(f"目前單字量：{len(st.session_state.words)} 個")

# --- 模式 A: 複習 ---
if mode == "📚 分類複習":
    st.title("📚 分類單字複習")
    categories = sorted(list(set([w['cat'] for w in st.session_state.words])))
    for cat in categories:
        with st.expander(f"{cat}", expanded=False):
            for w in [x for x in st.session_state.words if x['cat'] == cat]:
                c1, c2, c3 = st.columns([2, 1, 2])
                c1.markdown(f"### {w['en']}")
                if c2.button("🔊", key=f"s_{w['en']}"): speak(w['en'])
                if c3.checkbox("意思", key=f"c_{w['en']}"): st.write(f":blue[{w['zh']}]")
                st.divider()

# --- 模式 B: 拼寫 ---
elif mode == "✍️ 拼寫測驗":
    st.title("✍️ 拼寫測驗")
    q = st.session_state.current_q
    st.subheader(f"中文：:blue[{q['zh']}]")
    ans = st.text_input("英文：", key="quiz").strip()
    c1, c2, c3 = st.columns([1, 1, 2])
    if c1.button("檢查"):
        if ans.lower() == q['en'].lower():
            st.success("✅ 正確！"); st.balloons(); speak(q['en'])
        else: st.error(f"❌ 錯誤，是：{q['en']}")
    if c2.button("發音"): speak(q['en'])
    if c3.button("下一題"):
        st.session_state.current_q = random.choice(st.session_state.words); st.rerun()

# --- 模式 C: 造句 (API版) ---
elif mode == "👨‍🏫 AI 造句糾錯":
    st.title("👨‍🏫 AI 造句糾錯")
    q = st.session_state.current_q
    st.info(f"目標：**{q['en']}** ({q['zh']})")
    sent = st.text_area("造句：", height=100)
    c1, c2, c3 = st.columns([1, 1, 1])
    if c1.button("🔍 檢查"):
        if sent:
            if q['en'].lower() not in sent.lower(): st.warning(f"⚠️ 沒用到 {q['en']}")
            matches = check_grammar_api(sent)
            if matches is None: st.error("連線錯誤")
            elif not matches: st.success("🎉 完美！"); st.balloons(); speak(sent)
            else:
                st.error(f"發現 {len(matches)} 個錯誤：")
                for m in matches:
                    rep = m['replacements'][0]['value'] if m['replacements'] else "刪除"
                    st.write(f"❌ **{sent[m['offset']:m['offset']+m['length']]}** -> ✅ **{rep}**")
    if c2.button("🔊 朗讀"): 
        if sent: speak(sent)
    if c3.button("換題"):
        st.session_state.current_q = random.choice(st.session_state.words); st.rerun()

# --- 模式 D: 新增單字 (補回功能) ---
elif mode == "➕ 新增單字":
    st.title("➕ 新增單字到庫存")
    with st.form("add_word"):
        new_en = st.text_input("英文單字")
        new_zh = st.text_input("中文意思")
        # 自動抓取目前的分類選項
        cats = sorted(list(set([w['cat'] for w in st.session_state.words])))
        new_cat = st.selectbox("選擇分類", cats)
        
        if st.form_submit_button("儲存"):
            if new_en and new_zh:
                st.session_state.words.append({"en": new_en, "zh": new_zh, "cat": new_cat})
                st.success(f"已新增：{new_en} 到 {new_cat}")
            else:
                st.error("請填寫完整")
