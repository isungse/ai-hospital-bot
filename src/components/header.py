import streamlit as st


def render_header() -> None:
    """메인 페이지 헤더를 렌더링합니다."""
    st.markdown(
        '<div class="page-header">'
        "<h2>AI 안내 데스크</h2>"
        "<p>진료과 위치, 의료진, 운영 시간 등 궁금한 점을 자유롭게 질문하세요.</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_quick_questions(questions: list[str]) -> None:
    """자주 묻는 질문 버튼을 렌더링합니다."""
    st.markdown('<p class="faq-label">자주 묻는 질문</p>', unsafe_allow_html=True)

    cols = st.columns([1.2, 1.2, 2.6])
    for i, question in enumerate(questions):
        if cols[i].button(question, key=f"qq_{i}"):
            st.session_state["quick_question"] = question

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
