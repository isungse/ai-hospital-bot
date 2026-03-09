# 평택성모병원 AI 안내 데스크 - 프로젝트 현황

## 프로젝트 개요
- **서비스명**: 평택성모병원 AI 안내 데스크
- **목표**: 프로토타입 → Production-ready 상업용 서비스 고도화
- **AI 엔진**: Google Gemini 1.5 Flash
- **UI 프레임워크**: Streamlit

---

## 디렉토리 구조

```
ai-hospital/
├── CLAUDE.md
├── .env                          # API 키 (gitignore 처리)
├── .gitignore
├── .streamlit/
│   └── config.toml               # Streamlit 테마 설정
├── requirements.txt              # 핵심 패키지 4개 명시
├── data/
│   ├── hospital_info.md          # 병원 운영정보 학습 데이터
│   └── doctors_list.csv          # 의료진 명단 (40명)
└── src/
    ├── app.py                    # 메인 엔트리 포인트
    ├── ai_engine.py              # Gemini AI 엔진
    ├── styles/
    │   └── main.css              # 전체 CSS (정적)
    ├── utils/
    │   ├── __init__.py
    │   └── clinic_status.py      # 진료 상태 비즈니스 로직
    └── components/
        ├── __init__.py
        ├── sidebar.py            # 사이드바 컴포넌트
        └── header.py             # 헤더 + 자주 묻는 질문 컴포넌트
```

---

## 실행 방법

```bash
cd C:\Users\SPW\ai-project\ai-hospital
streamlit run src/app.py
```

---

## 완료된 작업

### 1단계 - 기능 개선
- [x] 대화 히스토리 전달 (Gemini `start_chat` 방식으로 맥락 유지)
- [x] `requirements.txt` 핵심 패키지 4개 버전 명시
- [x] 예외 처리 고도화 (`logging` 모듈 추가, 오류 원인 터미널 출력)

### 2단계 - 아키텍처 고도화
- [x] 단일 `app.py` → 역할별 모듈 분리 (Production-ready 구조)
- [x] CSS 외부 파일 분리 (`styles/main.css`)
- [x] 비즈니스 로직 분리 (`utils/clinic_status.py`)
- [x] UI 컴포넌트 함수화 (`components/sidebar.py`, `components/header.py`)
- [x] 시간표 데이터를 List로 정의 → 함수가 자동 렌더링 (하드코딩 제거)
- [x] CSS Custom Properties로 동적 색상 주입 (`--status-color` 등)

### 3단계 - UI/UX 디자인 (SaaS 스타일)
- [x] Inter 폰트 적용 (Google Fonts)
- [x] Streamlit 테마 설정 (`config.toml`)
- [x] 실시간 진료 상태 배지 (진료 중 → 초록 펄스 애니메이션)
- [x] 사이드바 미니멀 리디자인 (섹션 제목, 시간표, 응급실 배너)
- [x] 자주 묻는 질문 pill 버튼 (왼쪽 밀착 배치)
- [x] 대화 초기화 버튼
- [x] 채팅 입력창 포커스 glow 효과

### 4단계 - 학습 데이터 추가
- [x] 주차 이용 안내 (무료 혜택, 요금, 정산 방법)
- [x] 면회 무료 주차 1시간 추가
- [x] 입원 환자 이용 안내 전체 추가 (병문안 에티켓, 개인 준비 물품, 종교 활동, 식사 시간, 간호·간병 통합병동, 퇴원 절차, 의무기록 발급 등)

### 5단계 - 프롬프트 최적화
- [x] 진료 시간 관련 질문에만 일정 변경 안내 문구 출력 (모든 답변 노출 → 조건부 노출)

---

## 자주 묻는 질문 버튼 현황

```python
QUICK_QUESTIONS = [
    "진료 시간이 어떻게 되나요?",
    "주차장 이용 안내",
    "입원 절차 안내",        # 학습 데이터 등록 완료
]
```

---

## 향후 작업 (Backlog)

### 기능
- [x] 입원 절차 안내 학습 데이터 추가 (`hospital_info.md`)
- [ ] 자주 묻는 질문 데이터 기반으로 지속 확장
- [ ] Phase 1: config.py 중앙화 설정 관리
- [ ] Phase 2: 로그 파일 저장 + 날짜별 로테이션
- [ ] Phase 3: 사용자 입력 길이 제한 및 sanitization
- [ ] Phase 4: AI 응답 스트리밍 출력

### 디자인
- [ ] 모바일/태블릿 반응형 대응
- [ ] 다국어 지원 (영어, 외국어 안내)

---

## 코딩 원칙 (Production-ready)
1. **확장성**: 향후 기능 추가가 용이한 디자인 패턴 적용
2. **안정성**: 철저한 예외 처리 및 로깅 시스템
3. **보안**: API Key 관리 및 사용자 데이터 보호 최우선
4. **성능**: 리소스 최적화 및 빠른 응답 속도 유지
5. **디자인**: 현대적이고 직관적인 UX/UI, 대기업 SaaS 스타일 미니멀 UI
