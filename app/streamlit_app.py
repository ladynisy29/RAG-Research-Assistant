import streamlit as st
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# ⚙️ PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="RAG Research Assistant",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# 🧠 SESSION STATE
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# 🎨 CSS (FIXED)
# ---------------------------
st.markdown("""
<style>

/* Main background */
.main {
    background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
}

/* Sidebar text visibility */
[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* Chat bubbles */
.user-msg {
    background: linear-gradient(135deg, #10a37f 0%, #0d8659 100%);
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    max-width: 75%;
    margin-left: auto;
    margin-bottom: 8px;
}

.bot-msg {
    background-color: #2a2a2a;
    color: #e0e0e0;
    padding: 10px 14px;
    border-radius: 12px;
    max-width: 75%;
    margin-bottom: 6px;
    border-left: 3px solid #10a37f;
}

/* Sources */
.source {
    color: #888;
    font-size: 12px;
    margin-left: 10px;
}

/* Fixed signature under chat input */
.made-by {
    position: fixed;
    bottom: 8px;
    left: 50%;
    transform: translateX(-50%);
    color: #10a37f;
    font-size: 12px;
    font-weight: 600;
    z-index: 999;
    pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 📌 SIDEBAR
# ---------------------------
API_URL = "http://localhost:8000"

with st.sidebar:
    st.markdown("## Nisy's RAG Assistant")

    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Settings")
    retrieval_count = st.slider("Sources", 1, 10, 3)

    st.markdown("### API Status")
    try:
        res = requests.get(f"{API_URL}/health", timeout=2)
        if res.status_code == 200:
            st.success("Connected")
        else:
            st.error("Error")
    except:
        st.error("Disconnected")

    st.markdown("---")
    st.caption("Powered by GPT-4.1 Mini + FAISS")

# ---------------------------
# 🧠 HEADER
# ---------------------------
st.markdown("### What's on your research agenda?")
st.caption("Ask questions about your research documents")

# ---------------------------
# 💬 CHAT DISPLAY
# ---------------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='user-msg'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='bot-msg'>{msg['content']}</div>",
                unsafe_allow_html=True
            )

            if "sources" in msg and msg["sources"]:
                st.markdown("<div class='source'><b>Sources:</b></div>", unsafe_allow_html=True)
                for s in msg["sources"]:
                    st.markdown(f"<div class='source'>• {s}</div>", unsafe_allow_html=True)

# ---------------------------
# 🔽 AUTO-SCROLL (KEY PART)
# ---------------------------
st.markdown("""
<script>
const scrollToBottom = () => {
    window.scrollTo(0, document.body.scrollHeight);
};
setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)

# ---------------------------
# 🧾 CHAT INPUT
# ---------------------------
query = st.chat_input("Ask your question...")

# 👇 SIGNATURE
st.markdown("""
<div class="made-by">
    Made by Lady Nisy 💚
</div>
""", unsafe_allow_html=True)

# ---------------------------
# 🚀 HANDLE QUERY
# ---------------------------
if query:
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    try:
        with st.spinner("Searching documents..."):
            res = requests.post(
                f"{API_URL}/query",
                json={"question": query},
                timeout=30
            )

        if res.status_code == 200:
            result = res.json()

            st.session_state.messages.append({
                "role": "assistant",
                "content": result.get("answer", "No answer"),
                "sources": result.get("sources", [])
            })

            st.rerun()

        else:
            st.error("API error")

    except requests.exceptions.Timeout:
        st.error("Request timed out")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API")

    except Exception as e:
        st.error(f"Error: {str(e)}")
        logger.error(str(e), exc_info=True)