import streamlit as st
from pathlib import Path

from ai_engine import get_hospital_response
from utils.clinic_status import get_clinic_status, get_status_theme
from components.sidebar import render_sidebar
from components.header import render_header, render_schedule

# ── 자주 묻는 질문 목록 (추가 시 이곳만 수정) ────────────────
QUICK_QUESTIONS: list[str] = [
    "진료 시간이 어떻게 되나요?",
    "주차장 이용 안내",
    "입원 절차 안내",
]

# ── 페이지 설정 ───────────────────────────────────────────────
st.set_page_config(
    page_title="평택성모병원 AI 안내",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto",
)

# ── 진료 상태 계산 ────────────────────────────────────────────
is_open, status_label = get_clinic_status()
theme = get_status_theme(is_open)

# ── CSS 로드 (정적 파일 + 동적 CSS 변수 주입) ─────────────────
css = (Path(__file__).parent / "styles" / "main.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown(
    f"<style>:root {{"
    f"--status-color: {theme['color']};"
    f"--status-bg: {theme['bg']};"
    f"--status-animation: {theme['animation']};"
    f"}}</style>",
    unsafe_allow_html=True,
)

# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    render_sidebar(is_open, status_label)

# ── 메인 레이아웃 ─────────────────────────────────────────────
render_header()
render_schedule()

# ── 자주 묻는 질문 ─────────────────────────────────────────────
st.markdown('<p class="faq-label">자주 묻는 질문</p>', unsafe_allow_html=True)

def _text_width(text: str) -> int:
    return sum(2 if ord(c) > 127 else 1 for c in text)

weights = [_text_width(q) for q in QUICK_QUESTIONS]
column_weights = weights + [max(weights)]
cols = st.columns(column_weights, gap="small")

for i, question in enumerate(QUICK_QUESTIONS):
    with cols[i]:
        if st.button(question, key=f"quick_q_{i}", use_container_width=True):
            st.session_state["quick_question"] = question

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 세션 초기화 ───────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_question" not in st.session_state:
    st.session_state.quick_question = None

# ── 대화 내역 출력 ────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── 입력 처리 ─────────────────────────────────────────────────
prompt = None

if st.session_state.quick_question:
    prompt = st.session_state.quick_question
    st.session_state.quick_question = None

if user_input := st.chat_input("질문을 입력하세요…"):
    prompt = user_input

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = get_hospital_response(prompt, st.session_state.messages[:-1])
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
