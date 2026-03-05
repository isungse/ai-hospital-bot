import os
import pandas as pd  # [추가] CSV 데이터를 다루기 위해 pandas 라이브러리 임포트
import google.generativeai as genai
from dotenv import load_dotenv

# 1. 환경 설정
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_hospital_response(user_query):
    try:
        # 2. 병원 안내 데이터(비정형) 읽기
        with open("data/hospital_info.md", "r", encoding="utf-8") as f:
            hospital_info = f.read()

        # 3. [추가] 의료진 데이터(정형) 읽기
        try:
            # CSV 파일을 읽어와서 텍스트 형태로 변환하여 AI에게 전달할 준비를 합니다.
            # skipinitialspace=True를 넣어 공백 문제를 방지합니다.
            doctors_df = pd.read_csv("data/doctors_list.csv", encoding="utf-8", skipinitialspace=True)
            # AI가 읽기 편하도록 표 형태의 데이터를 문자열로 변환합니다.
            doctors_info = doctors_df.to_string(index=False)
        except Exception as e:
            doctors_info = "현재 의료진 정보 업데이트 중입니다."

        # 4. 모델 동적 설정 (기존 성공 로직 유지)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

        if not available_models:
            return "현재 API 키로 사용할 수 있는 모델이 없습니다."

        selected_model_name = available_models[0]
        for name in available_models:
            if "gemini-1.5-flash" in name:
                selected_model_name = name
                break

        model = genai.GenerativeModel(selected_model_name)

        # 5. AI 페르소나 설정 (프롬프트 확장)
        # [수정] 프롬프트에 의료진 정보를 추가하여 AI가 상담 능력을 갖추게 합니다.
        prompt = f"""
        당신은 평택성모병원의 로비에 설치된 친절하고 전문적인 AI 안내 직원입니다.
        아래 제공된 [병원 정보]와 [의료진 명단]을 바탕으로 환자의 질문에 답변하세요.

        [병원 정보 (위치 및 시간)]
        {hospital_info}

        [의료진 명단 (진료과 및 전문분야)]
        {doctors_info}

        지시사항:
        - 진료 시간, 층별 위치는 [병원 정보]를 기준으로 답변하세요.
        - 환자가 아픈 부위나 증상을 말하면 [의료진 명단]에서 적절한 진료과와 성함을 찾아 추천하세요.
        - 답변은 환자를 배려하는 따뜻한 '해요체'를 사용하세요.
        - 명단에 없는 진료과나 상세 정보는 "본관 1층 안내 데스크나 대표번호로 문의해 주세요"라고 안내하세요.
        """

        # 6. 응답 생성
        response = model.generate_content(f"{prompt}\n\n환자 질문: {user_query}")
        return response.text

    except Exception as e:
        return f"답변을 생성하는 중 오류가 발생했습니다: {str(e)}"
