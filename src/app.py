import streamlit as st
from ai_engine import get_hospital_response

# 1. 웹 페이지 레이아웃 및 브라우저 탭 설정
st.set_page_config(
    page_title="스마트 병원 AI 안내",
    page_icon="🏥",
    layout="wide"  # 화면을 넓게 사용하여 키오스크 느낌을 줍니다.
)

# 2. 사이드바 디자인 (병원 운영 시간 및 중요 정보 고정)
with st.sidebar:
    # 병원 로고 대용 아이콘
    st.image("https://cdn-icons-png.flaticon.com/512/883/883407.png", width=80)
    st.title("병원 안내 정보")
    st.markdown("---")

    # 진료 시간 안내 (기존 디자인 유지 + 검진팀 정보 추가)
    st.subheader("⏱ 진료 시간")

    st.write("📅 **평일**")
    st.info("08:30 ~ 17:30")

    st.write("📅 **토요일**")
    st.info("08:30 ~ 13:00")

    st.write("📅 **공휴일**")
    st.info("08:30 ~ 13:00")

    st.write("🔴 **일요일**")
    st.write("휴진")

    st.markdown("---")

    # 추가된 검진 센터 정보 (기존 박스 디자인 유지)
    st.subheader("🔍 검진 센터")

    st.write("🏥 **종합검진팀**")
    st.info("평일: 07:30 ~ 17:00\n\n토요일: 07:30 ~ 12:30")

    st.write("🏢 **기업체검진팀**")
    st.info("평일: 08:00 ~ 17:00\n\n토요일: 08:00 ~ 12:30")

    st.markdown("---")

    st.markdown("---")

    # 응급실 강조 (빨간색 박스)
    st.error("🚨 **응급실(24시간)**\n\n연중무휴 365일 운영")

    st.markdown("---")
    st.caption("© 2026 평택성모병원 의료정보팀")

# 3. 메인 화면 디자인 (채팅 영역)
st.title("🏥 병원 AI 안내 데스크")
st.markdown("##### 무엇을 도와드릴까요? 시설 위치나 진료 시간에 대해 물어보세요.")
st.write("---")

# 대화 내용 저장용 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 내역 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. 사용자 입력 및 AI 응답 로직
if prompt := st.chat_input("질문을 여기에 입력하세요 (예: 2층에 무엇이 있나요?)"):
    # 환자 질문 표시 및 저장
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 응답 가져오기 및 표시
    with st.chat_message("assistant"):
        with st.spinner("정보를 찾는 중입니다..."):
            # ai_engine.py의 함수를 호출하여 제미나이 답변 수신
            response = get_hospital_response(prompt)
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
