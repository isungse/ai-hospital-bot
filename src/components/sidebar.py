import streamlit as st

# ── 데이터 정의 (변경 시 이곳만 수정) ────────────────────────
CLINIC_HOURS: list[tuple[str, str, bool]] = [
    ("평일",   "08:30 – 17:30", False),
    ("토요일", "08:30 – 13:00", False),
    ("공휴일", "08:30 – 13:00", False),
    ("일요일", "휴진",           True),
]

CHECKUP_HOURS: list[tuple[str, str, bool]] = [
    ("종합검진 평일",   "07:30 – 17:00", False),
    ("종합검진 토요일", "07:30 – 12:30", False),
    ("기업검진 평일",   "08:00 – 17:00", False),
    ("기업검진 토요일", "08:00 – 12:30", False),
]


# ── 내부 헬퍼 ────────────────────────────────────────────────
def _hours_html(rows: list[tuple[str, str, bool]]) -> str:
    """시간표 데이터를 HTML 문자열로 변환합니다."""
    items = []
    for label, value, is_closed in rows:
        cls = "hour-closed" if is_closed else "hour-value"
        items.append(
            f'<div class="hour-row">'
            f'<span class="hour-label">{label}</span>'
            f'<span class="{cls}">{value}</span>'
            f'</div>'
        )
    return f'<div>{"".join(items)}</div>'


# ── 공개 컴포넌트 ─────────────────────────────────────────────
def render_sidebar(is_open: bool, status_label: str) -> None:
    """사이드바 전체를 렌더링합니다."""

    # 병원명 + 진료 상태 배지
    st.markdown("#### 🏥 평택성모병원")
    st.markdown(
        f'<div class="status-badge">'
        f'<div class="status-dot"></div>{status_label}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 진료 시간
    st.markdown('<p class="sb-section-title">진료 시간</p>', unsafe_allow_html=True)
    st.markdown(_hours_html(CLINIC_HOURS), unsafe_allow_html=True)

    # 검진 센터
    st.markdown('<p class="sb-section-title">검진 센터</p>', unsafe_allow_html=True)
    st.markdown(_hours_html(CHECKUP_HOURS), unsafe_allow_html=True)

    # 응급실
    st.markdown('<p class="sb-section-title">응급실</p>', unsafe_allow_html=True)
    st.markdown(
        '<div class="emergency-strip">🚨 &nbsp;24시간 · 연중무휴 365일</div>',
        unsafe_allow_html=True,
    )

    # 설정
    st.markdown('<p class="sb-section-title">설정</p>', unsafe_allow_html=True)
    if st.button("↺  대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("© 2026 평택성모병원 의료정보팀")
