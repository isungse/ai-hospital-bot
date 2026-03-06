import os
import logging
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

logging.basicConfig(level=logging.ERROR, format="%(asctime)s [%(levelname)s] %(message)s")

# 1. 환경 설정
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# [로딩 속도 개선] 전역 변수를 사용하여 데이터를 메모리에 캐싱합니다.
_CACHED_MODEL = None
_HOSPITAL_INFO = ""
_DOCTORS_INFO = ""

def prepare_engine():
    """데이터와 모델을 미리 로드하여 응답 속도를 높이는 함수"""
    global _CACHED_MODEL, _HOSPITAL_INFO, _DOCTORS_INFO

    # 데이터가 비어있을 때만 (최초 1회) 실행됩니다.
    if _CACHED_MODEL is None:
        # 2. 병원 안내 데이터(비정형) 읽기
        try:
            with open("data/hospital_info.md", "r", encoding="utf-8") as f:
                _HOSPITAL_INFO = f.read()
        except Exception as e:
            logging.error(f"hospital_info.md 로드 실패: {e}")
            _HOSPITAL_INFO = "병원 정보 로드 실패"

        # 3. 의료진 데이터(정형) 읽기
        try:
            doctors_df = pd.read_csv("data/doctors_list.csv", encoding="utf-8", skipinitialspace=True)
            _DOCTORS_INFO = doctors_df.to_string(index=False)
        except Exception as e:
            logging.error(f"doctors_list.csv 로드 실패: {e}")
            _DOCTORS_INFO = "현재 의료진 정보 업데이트 중입니다."

        # 4. 시스템 프롬프트 구성
        system_prompt = f"""
        당신은 평택성모병원의 로비에 설치된 친절하고 전문적인 AI 안내 직원입니다.
        아래 제공된 [병원 정보]와 [의료진 명단]을 바탕으로 환자의 질문에 답변하세요.

        [병원 정보 (위치 및 시간)]
        {_HOSPITAL_INFO}

        [의료진 명단 (진료과 및 전문분야)]
        {_DOCTORS_INFO}

        지시사항 (반드시 준수할 것):
        1. **병원 무관 질문 차단**: 병원 이용, 위치 안내, 진료과 추천과 전혀 상관없는 질문(예: 뉴스, 연예인, 음식 레시피, 일반 상식 등)에는 반드시 다음과 같이 정중히 거절하세요:
           "죄송합니다. 저는 병원 안내를 돕는 AI입니다. 병원 이용 관련 질문을 해주세요."

        2. **의료 상담 제한**: 환자가 특정 질병의 진단이나 구체적인 치료 방법을 요구하는 민감한 질문을 할 경우 다음과 같이 안내하세요:
           "자세한 진료는 반드시 전문의와의 상담이 필요합니다. 증상을 이야기 해 주시면 진료과를 추천 해 드릴 수 있습니다."

        3. **진료과 및 의료진 안내**:
           - 환자가 아픈 부위나 증상을 말하면 [의료진 명단]에서 가장 적합한 진료과와 전문의 성함을 찾아 추천하세요.
           - 진료 시간 및 층별 위치는 [병원 정보]를 기준으로 정확히 안내하세요.
           - 진료 시간 답변의 마지막에는 반드시 다음 문구를 포함하세요:
             "수술이나 응급 상황에 따라 진료 일정이 변경될 수 있으니 상세 일정은 안내 데스크에서 확인이 필요합니다."

        4. **공통 준수 사항**:
           - 모든 답변은 환자를 배려하는 따뜻한 '해요체'를 사용하세요.
        """

        # 5. 모델 동적 설정 (시스템 프롬프트를 모델에 내장)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

        if available_models:
            selected_model_name = available_models[0]
            for name in available_models:
                if "gemini-1.5-flash" in name:
                    selected_model_name = name
                    break
            _CACHED_MODEL = genai.GenerativeModel(
                selected_model_name,
                system_instruction=system_prompt
            )

    return _CACHED_MODEL, _HOSPITAL_INFO, _DOCTORS_INFO

def get_hospital_response(user_query, chat_history=None):
    try:
        model, _, _ = prepare_engine()

        if model is None:
            return "현재 API 키로 사용할 수 있는 모델이 없습니다."

        # 이전 대화 내역을 Gemini 형식으로 변환
        gemini_history = []
        if chat_history:
            for msg in chat_history:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg["content"]]})

        # 대화 히스토리를 포함한 채팅 세션 생성 후 응답
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(user_query)
        return response.text

    except Exception as e:
        logging.error(f"응답 생성 실패: {e}")
        return f"답변을 생성하는 중 오류가 발생했습니다: {str(e)}"
