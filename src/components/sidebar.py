import streamlit as st

_SPACER = '<div style="margin-top:28px;"></div>'


# ── 공개 컴포넌트 ─────────────────────────────────────────────
def render_sidebar(is_open: bool, status_label: str) -> None:
    """사이드바: 병원명 + 상태 배지 + 응급실 + 설정 (진료 시간은 메인 expander로 이동)"""

    # 병원명 + 진료 상태 배지
    st.markdown("#### 🏥 평택성모병원")
    st.markdown(
        f'<div class="status-badge">'
        f'<div class="status-dot"></div>{status_label}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(_SPACER, unsafe_allow_html=True)

    # 핵심 연락처 카드
    st.markdown(
        '<div class="sidebar-info-card">'
        '<div class="info-label">대표전화</div>'
        '<div class="info-value info-highlight">031-1800-8800</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(_SPACER, unsafe_allow_html=True)

    # 응급실
    st.markdown('<p class="sb-section-title">응급실</p>', unsafe_allow_html=True)
    st.markdown(
        '<div class="emergency-strip">🚨 &nbsp;24시간 · 연중무휴 365일</div>',
        unsafe_allow_html=True,
    )

    st.markdown(_SPACER, unsafe_allow_html=True)

    # 설정
    st.markdown('<p class="sb-section-title">설정</p>', unsafe_allow_html=True)
    if st.button("↺  대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("© 2026 평택성모병원 의료정보팀")
