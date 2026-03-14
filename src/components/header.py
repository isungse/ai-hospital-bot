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


# ── 진료 시간 데이터 ──────────────────────────────────────────
SCHEDULE_HTML = """
<table class="schedule-table">
<thead>
    <tr>
        <th>구분</th>
        <th>평일</th>
        <th>토요일</th>
        <th>공휴일</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>일반 진료</td>
        <td>08:30 – 17:30</td>
        <td>08:30 – 13:00</td>
        <td>08:30 – 13:00</td>
    </tr>
    <tr>
        <td>종합검진</td>
        <td>07:30 – 17:00</td>
        <td>07:30 – 12:30</td>
        <td class="closed">휴진</td>
    </tr>
    <tr>
        <td>기업검진</td>
        <td>08:00 – 17:00</td>
        <td>08:00 – 12:30</td>
        <td class="closed">휴진</td>
    </tr>
    <tr>
        <td>일요일</td>
        <td class="closed" colspan="3" style="text-align:center;">휴진</td>
    </tr>
</tbody>
</table>
"""


def render_schedule() -> None:
    """진료 시간표를 expander로 렌더링합니다."""
    st.markdown('<div class="schedule-expander-wrap">', unsafe_allow_html=True)
    with st.expander("👉 진료 시간 안내", expanded=False):
        st.markdown(SCHEDULE_HTML, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_quick_questions(questions: list[str]) -> None:
    """자주 묻는 질문 버튼을 렌더링합니다. (flexbox 기반 자동 너비)"""
    st.markdown('<p class="faq-label">자주 묻는 질문</p>', unsafe_allow_html=True)

    # CSS 마커 → 바로 다음 stHorizontalBlock을 flexbox로 변환
    st.markdown('<div class="faq-flex-marker"></div>', unsafe_allow_html=True)
    cols = st.columns(len(questions))
    for i, question in enumerate(questions):
        with cols[i]:
            if st.button(question, key=f"quick_q_{i}"):
                st.session_state["quick_question"] = question

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
