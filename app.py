import streamlit as st
import random
import language_tool_python # 引入文法檢查工具

# 設定網頁
st.set_page_config(page_title="高階單字教練", page_icon="👨‍🏫", layout="centered")

# --- 0. 初始化文法檢查工具 (使用快取避免重複載入) ---
@st.cache_resource
def get_grammar_tool():
    # 使用公共API，不需要Java環境
    return language_tool_python.LanguageTool('en-US')

tool = get_grammar_tool()

# --- 1. 完整單字庫 ---
if "words" not in st.session_state:
    st.session_state.words = [
        # 第一張照片
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
        # 第二張照片
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

# --- 2. 狀態初始化 ---
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(st.session_state.words)
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# --- 3. 語音功能 ---
def speak(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text.replace('"', '')}");
    msg.lang = 'en-US';
    msg.rate = 0.85; 
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 4. 側邊欄 ---
st.sidebar.title("功能選單")
mode = st.sidebar.radio("請選擇：", ["全單字庫複習", "拼寫測驗", "造句糾錯教練"])
st.sidebar.divider()
st.sidebar.info(f"單字庫總量：{len(st.session_state.words)} 個")

# --- 模式 A: 複習 ---
if mode == "全單字庫複習":
    st.title("📚 單字總表")
    st.table(st.session_state.words)

# --- 模式 B: 拼寫 ---
elif mode == "拼寫測驗":
    st.title("✍️ 拼寫測驗")
    q = st.session_state.current_q
    st.subheader(f"意思：:blue[{q['zh']}]")
    
    ans = st.text_input("請拼出英文：").strip()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("檢查"):
            if ans.lower() == q['en'].lower():
                st.success("✅ 正確！")
                st.balloons()
                speak(q['en'])
            else:
                st.error(f"❌ 錯誤，正確是：{q['en']}")
    with col2:
        if st.button("🔊 發音"):
            speak(q['en'])
    with col3:
        if st.button("下一題 ➡️"):
            st.session_state.current_q = random.choice(st.session_state.words)
            st.rerun()

# --- 模式 C: 造句糾錯 (核心升級功能) ---
elif mode == "造句糾錯教練":
    st.title("👨‍🏫 AI 造句糾錯")
    q = st.session_state.current_q
    
    st.info(f"請用單字 **「{q['en']}」 ({q['zh']})** 造一個句子：")
    
    user_sentence = st.text_area("在此輸入你的句子：", height=100, placeholder="例如：He is a very rational person.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 這是升級的核心：檢查文法
        if st.button("🔍 檢查文法"):
            if user_sentence:
                # 1. 檢查是否有用到目標單字
                if q['en'].lower() not in user_sentence.lower():
                    st.warning(f"⚠️ 你的句子好像沒有用到目標單字：{q['en']}")
                
                # 2. 使用工具檢查文法
                matches = tool.check(user_sentence)
                
                if len(matches) == 0:
                    st.success("🎉 太棒了！沒有發現明顯的文法錯誤。")
                    st.balloons()
                    speak(user_sentence) # 只有正確時才朗讀
                else:
                    st.error(f"發現 {len(matches)} 個潛在錯誤：")
                    for match in matches:
                        st.write(f"❌ **錯誤**: {user_sentence[match.offset:match.offset+match.errorLength]}")
                        st.write(f"💡 **建議**: {', '.join(match.replacements[:3])}")
                        st.divider()
            else:
                st.warning("請先輸入句子喔！")
                
    with col2:
        # 單純朗讀功能
        if st.button("🔊 朗讀句子"):
            if user_sentence:
                speak(user_sentence)
            else:
                st.warning("請先輸入句子")

    with col3:
        if st.button("換一個單字"):
            st.session_state.current_q = random.choice(st.session_state.words)
            st.rerun()
            
    st.caption("註：文法檢查由 LanguageTool 提供，能修正大部分拼寫與基礎文法錯誤。")
