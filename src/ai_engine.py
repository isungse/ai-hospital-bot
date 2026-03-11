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
_FEES_INFO = ""
_MRI_FEES_INFO = ""

def prepare_engine():
    """데이터와 모델을 미리 로드하여 응답 속도를 높이는 함수"""
    global _CACHED_MODEL, _HOSPITAL_INFO, _DOCTORS_INFO, _FEES_INFO, _MRI_FEES_INFO

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

        # 4. CT 보험수가 데이터(정형) 읽기
        try:
            fees_df = pd.read_csv("data/mri_ct_fees.csv", encoding="utf-8", skipinitialspace=True)
            _FEES_INFO = fees_df.to_string(index=False)
        except Exception as e:
            logging.error(f"mri_ct_fees.csv 로드 실패: {e}")
            _FEES_INFO = "현재 CT 수가 정보 업데이트 중입니다."

        # 5. MRI 보험수가 데이터(정형) 읽기
        try:
            mri_df = pd.read_csv("data/mri_fees.csv", encoding="utf-8", skipinitialspace=True)
            # 보험수가 0인 항목(비급여 전용) 제외하지 않고 전체 포함
            _MRI_FEES_INFO = mri_df[["수가코드", "한글명칭", "보험수가", "일반수가"]].to_string(index=False)
        except Exception as e:
            logging.error(f"mri_fees.csv 로드 실패: {e}")
            _MRI_FEES_INFO = "현재 MRI 수가 정보 업데이트 중입니다."

        # 6. 시스템 프롬프트 구성
        system_prompt = f"""
        당신은 평택성모병원의 로비에 설치된 친절하고 전문적인 AI 안내 직원입니다.
        아래 제공된 [병원 정보], [의료진 명단], [CT/MRI 보험수가]를 바탕으로 환자의 질문에 답변하세요.

        [병원 정보 (위치 및 시간)]
        {_HOSPITAL_INFO}

        [의료진 명단 (진료과 및 전문분야)]
        {_DOCTORS_INFO}

        [CT 보험수가 (수가코드, 한글명칭, 보험수가)]
        - 본 데이터는 보험 기본 단가 기준이며, 야간·응급·연령·난이도 등 세부 가산 및 3T 장비 가산은 반영되지 않을 수 있습니다.
        - 조영제(CE: with Contrast Enhancement) 사용 시 조영제 검사임을 안내하세요.
        {_FEES_INFO}

        [MRI 보험수가 (수가코드, 한글명칭, 보험수가, 일반수가)]
        - 본 데이터는 보험 기본 단가 기준이며, 야간·응급·연령·난이도 등 세부 가산 및 3T 장비 가산은 반영되지 않을 수 있습니다.
        - 보험수가: 건강보험 적용 기준 금액 / 일반수가: 비급여(건강보험 미적용) 금액
        - 보험수가가 0인 항목은 비급여 항목으로 일반수가로 안내하세요.
        - [3T]는 3테슬라 MRI 장비 사용을 의미합니다.
        {_MRI_FEES_INFO}

        지시사항 (반드시 준수할 것):
        1. **병원 무관 질문 차단**: 병원 이용, 위치 안내, 진료과 추천과 전혀 상관없는 질문(예: 뉴스, 연예인, 음식 레시피, 일반 상식 등)에는 반드시 다음과 같이 정중히 거절하세요:
           "죄송합니다. 저는 병원 안내를 돕는 AI입니다. 병원 이용 관련 질문을 해주세요."

        2. **의료 상담 제한**: 환자가 특정 질병의 진단이나 구체적인 치료 방법을 요구하는 민감한 질문을 할 경우 다음과 같이 안내하세요:
           "자세한 진료는 반드시 전문의와의 상담이 필요합니다. 증상을 이야기 해 주시면 진료과를 추천 해 드릴 수 있습니다."

        3. **진료과 및 의료진 안내**:
           - 환자가 아픈 부위나 증상을 말하면 [의료진 명단]에서 가장 적합한 진료과와 전문의 성함을 찾아 추천하세요.
           - 진료 시간 및 층별 위치는 [병원 정보]를 기준으로 정확히 안내하세요.
           - 환자가 진료 시간, 운영 시간, 진료 일정을 직접적으로 묻는 질문에만 답변 마지막에 다음 문구를 포함하세요:
             "수술이나 응급 상황에 따라 진료 일정이 변경될 수 있으니 상세 일정은 안내 데스크에서 확인이 필요합니다."
           - 위치 안내, 의료진 추천, 주차 안내 등 진료 시간과 무관한 질문에는 위 문구를 절대 포함하지 마세요.

        4. **CT/MRI 수가 안내**:
           - 환자가 CT 비용을 물으면 [CT 보험수가]에서, MRI 비용을 물으면 [MRI 보험수가]에서 해당 항목을 찾아 안내하세요.
           - MRI의 경우 보험수가(급여)와 일반수가(비급여)를 구분하여 안내하세요.
           - 보험수가가 0인 MRI 항목은 비급여임을 명시하고 일반수가로 안내하세요.
           - 조영제(CE) 검사는 조영제 사용 사실을 함께 안내하세요.
           - 금액 안내 시 반드시 다음 고지 문구를 답변 마지막에 포함하세요:
             "⚠️ 안내된 금액은 보험 기본 단가 기준의 추정 범위입니다.
             야간·응급·연령·가산 등 세부 조건 및 촬영 장비(3T 등)에 따라 실제 금액이 달라질 수 있습니다.
             정확한 금액은 원무팀 또는 수납 창구에서 확인하시기 바랍니다."

        5. **공통 준수 사항**:
           - 모든 답변은 환자를 배려하는 따뜻한 '해요체'를 사용하세요.

        6. **답변 형식 규칙 (반드시 준수)**:

           [문장 구조]
           - 한 문장은 40자 이내로 작성하세요.
           - 하나의 문장에는 하나의 정보만 담으세요.
           - 불필요한 조사·접속사·중복 표현은 생략하세요.

           [단락 구성]
           - 관련 내용은 2~3문장으로 묶어 하나의 단락으로 구성하세요.
           - 단락과 단락 사이는 한 줄을 띄우세요.
           - 핵심 내용은 단락의 첫 문장에 배치하세요.

           [강조]
           - 금액, 날짜, 핵심 단어는 **굵게** 표시하세요.
           - 주의사항은 > 인용 블록으로 구분하세요.

           [목록 사용]
           - 항목이 3개 이상이면 bullet(•) 또는 번호 목록으로 정리하세요.
           - 순서가 중요하면 번호 목록을 사용하세요.
           - bullet 항목은 각 항목 사이에 빈 줄을 넣어 간격을 띄우세요.

           [줄바꿈 규칙]
           - 마침표(.) 뒤에는 반드시 줄바꿈(\\n)을 삽입하세요. 두 문장을 한 줄에 이어 쓰지 마세요.
           - 각 bullet 항목 뒤에는 반드시 빈 줄(\\n\\n)을 삽입하세요.
           - 단락 제목(예: **복부 CT 비용**) 다음 줄도 빈 줄을 넣으세요.
           - 문장이 연속으로 이어지지 않도록 항상 줄바꿈으로 구분하세요.

           [기호 사용 규칙]
           - 일반 안내 문장 앞에는 ▶ 기호를 붙이세요.
           - 금액·비용 정보 앞에는 💰 기호를 붙이세요.
           - 위치 안내 문장 앞에는 📍 기호를 붙이세요.
           - 시간 안내 문장 앞에는 🕐 기호를 붙이세요.
           - 주의·유의 사항 앞에는 ⚠️ 기호를 붙이세요.
           - bullet 목록 항목에는 • 대신 ✔ 기호를 사용하세요.

           [금지 표현]
           - "~라고 할 수 있습니다" → "~입니다"로 대체하세요.
           - "~의 경우에는" → "~이면"으로 대체하세요.
           - 동일한 단어를 한 단락 내에서 2회 이상 반복하지 마세요.
        """

        # 6. 모델 동적 설정 (시스템 프롬프트를 모델에 내장)
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
