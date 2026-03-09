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


def _text_width(text: str) -> int:
    """한글/CJK 문자는 2, 나머지는 1로 계산하여 픽셀 너비를 추정합니다."""
    return sum(2 if ord(c) > 127 else 1 for c in text)


def render_quick_questions(questions: list[str]) -> None:
    """자주 묻는 질문 버튼을 렌더링합니다."""
    st.markdown('<p class="faq-label">자주 묻는 질문</p>', unsafe_allow_html=True)

    # 한글 문자 너비를 2로 환산한 가중치로 컬럼 배분 (여백 컬럼은 최대 버튼 너비와 동일)
    weights = [_text_width(q) for q in questions]
    column_weights = weights + [max(weights)]
    cols = st.columns(column_weights, gap="small")

    for i, question in enumerate(questions):
        with cols[i]:
            if st.button(question, key=f"quick_q_{i}", use_container_width=True):
                st.session_state["quick_question"] = question

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
