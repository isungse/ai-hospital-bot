# 평택성모병원 AI 안내 데스크 - 프로젝트 현황

## 프로젝트 개요
- **서비스명**: 평택성모병원 AI 안내 데스크
- **목표**: 프로토타입 → Production-ready 상업용 서비스 고도화
- **AI 엔진**: Google Gemini 1.5 Flash
- **UI 프레임워크**: Streamlit
- **배포**: Streamlit Cloud
- **라이브 URL**: https://ptsm-ai-bot.streamlit.app/
- **GitHub**: https://github.com/isungse/ai-hospital-bot (Public)

---

## 디렉토리 구조

```
ai-hospital/
├── CLAUDE.md
├── .env                          # API 키 (gitignore 처리)
├── .gitignore
├── .gitattributes                # LF 줄바꿈 강제 설정
├── .streamlit/
│   └── config.toml               # Streamlit 테마 설정
├── requirements.txt              # 핵심 패키지 4개 명시
├── data/
│   ├── hospital_info.md          # 병원 운영정보 학습 데이터
│   ├── doctors_list.csv          # 의료진 명단 (40명)
│   ├── mri_ct_fees.csv           # CT 보험수가 (102개 항목)
│   └── mri_fees.csv              # MRI 보험수가 (317개 항목, 급여/비급여)
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
- [x] 입원 절차 5단계 추가 (외래 진료 → 입원 수속 → 병동 배정 → 복용약 제출 → 오리엔테이션)
- [x] 보호자 손목 바코드 라벨 발급 안내 추가 (원무과 또는 병동, 야간·휴일은 응급원무과)

### 5단계 - 프롬프트 최적화
- [x] 진료 시간 관련 질문에만 일정 변경 안내 문구 출력 (모든 답변 노출 → 조건부 노출)

### 6단계 - 버그 수정
- [x] 자주 묻는 질문 버튼 줄바꿈 문제 해결 (한글 문자 너비 2배 환산 알고리즘 적용)
- [x] "입원 절차 안내" 질문 시 퇴원 절차가 출력되던 문제 해결 (입원 절차 섹션 신규 추가)

### 7단계 - 프로젝트 환경 설정
- [x] `.gitattributes` 추가 (py, css, md 파일 LF 줄바꿈 강제)

### 8단계 - CT/MRI 보험수가 학습 데이터 추가
- [x] `data/mri_ct_fees.csv` 추가 (102개 CT 항목, 수가코드/한글명칭/보험수가)
- [x] `data/mri_fees.csv` 추가 (317개 MRI 항목, 수가코드/한글명칭/보험수가/일반수가)
- [x] `ai_engine.py`에 CT/MRI 수가 데이터 개별 로드 및 캐싱 (`_FEES_INFO`, `_MRI_FEES_INFO`) 추가
- [x] 시스템 프롬프트에 `[CT 보험수가]`, `[MRI 보험수가]` 섹션 분리 추가
- [x] MRI 급여/비급여 구분 안내 로직 추가 (보험수가 0 → 일반수가로 안내)
- [x] 수가 데이터 주의사항 추가 (야간·응급·연령·난이도 가산 및 3T 장비 가산 미반영 명시)
- [x] 조영제(CE) 사용 여부 고지 로직 추가
- [x] `(HC)` → `건강검진` 용어 일괄 치환 후 전체 삭제 (CT 11개, MRI 20개, 총 31개 제거 — 진료비 0원으로 안내 불필요)

### 9단계 - 프롬프트 고도화
- [x] 필수 고지 문구 추가 (금액 안내 시 항상 출력)
  - 보험 기본 단가 기준 추정값임을 명시
  - 야간·응급·연령·가산·3T 장비 가산에 따른 실제 금액 차이 안내
  - 원무팀/수납 창구 확인 안내
- [x] 답변 형식 규칙 6가지 추가 (시스템 프롬프트 지시사항 6번)
  - 문장 구조: 40자 이내, 정보 1개 per 문장
  - 단락 구성: 2~3문장, 단락 간 줄 띄움
  - 강조: 금액·핵심 단어 굵게, 주의사항 인용 블록
  - 목록: 3개 이상 bullet/번호 목록
  - 줄바꿈: bullet 항목 간 빈 줄 삽입
  - 금지 표현: "~라고 할 수 있습니다", "~의 경우에는" 대체

### 10단계 - 학습 데이터 추가 (층별 상세 위치)
- [x] `hospital_info.md` 1층 상세 위치 안내 추가
  - 신경외과/정형외과/비뇨의학과: 안내 데스크 우측
  - 외래석고실/외래처치실/척추관절센터/골밀도검사실: 정형외과 맞은 편
  - 산부인과: 엘리베이터 옆 복도 우측 끝 (바닥 분홍색 선 안내)
  - 영상의학과: 엘리베이터 바로 옆
  - 공차/카페, 응급실, 진료협력실, 원무팀 사무실, 보험청구 상담센터 위치
- [x] `hospital_info.md` 2층 상세 위치 안내 추가
  - 복도 좌측/중앙/우측 끝 기준으로 진료과 구분 안내
  - 수유실/기저귀갈이대: 소아청소년과 내 위치 안내
- [x] `hospital_info.md` 3층 보호자 대기실 항목 추가
- [x] `hospital_info.md` 4층 2중환자실 이동 방법 안내 추가
  - 5호기 엘리베이터 전용 이동 (다른 엘리베이터 이용 불가 명시)

### 11단계 - 프롬프트 가독성 개선
- [x] 답변 형식 규칙 6가지 추가 (줄바꿈, 기호, 문장 구조 등)
- [x] 답변 형식 규칙 전체 삭제 — Gemini 기본 포맷으로 변경 (커스텀 규칙이 오히려 출력 품질 저하)

### 12단계 - Streamlit Cloud 배포 (2026-03-13)
- [x] `requirements.txt` 버전 고정 해제 (Streamlit Cloud 호환)
- [x] GitHub 리포지토리 Public 전환
- [x] Streamlit Cloud 배포 완료 (`https://ptsm-ai-bot.streamlit.app/`)

### 13단계 - UI/UX 전면 개선 (2026-03-14)

#### 컬러 시스템 (CSS Custom Properties)
- [x] 의료 신뢰 블루 기반 컬러 토큰 정의 (`--primary: #0F4C9A`, `--primary-light: #E6F1FB` 등)
- [x] WCAG AA 대비율 ≥ 4.5:1 준수
- [x] `config.toml` 테마 컬러 동기화 (`primaryColor: #0F4C9A`, `secondaryBackgroundColor: #F5F7FA`)

#### 사이드바 경량화
- [x] 진료 시간표를 사이드바에서 제거 → 메인 `st.expander`로 이동
- [x] 사이드바 구성: 병원명 + 상태 배지 + 대표전화(`031-1800-8800`) + 응급실 + 설정
- [x] 컴포넌트 간 상하 간격 확대 (`28px` spacer 삽입)

#### 진료 시간 안내 (st.expander)
- [x] 메인 콘텐츠 상단에 `st.expander` 배치 (`expanded=False`)
- [x] HTML 테이블(`schedule-table`) 기반 시간표 렌더링
- [x] Primary 블루 테두리 + 연한 블루 배경으로 시각적 강조
- [x] 텍스트 색상 고대비 네이비(`#0A3470`) 적용
- [x] 👉 이모지로 클릭 유도 표현

#### 채팅 버블 디자인
- [x] AI 버블: `#E6F1FB` 배경 + `3px solid #0F4C9A` 좌측 보더
- [x] User 버블: `#0F4C9A` 배경 + 흰색 텍스트 + 우측 정렬
- [x] 리스트 카드 스타일 (white bg, 0.5px border, 8px radius)
- [x] 인라인 코드 강조 칩 (`#FFF3E0` bg, `#E65100` text)
- [x] blockquote 주의사항 블록 (오렌지 강조)

#### 반응형 레이아웃 (CSS 미디어 쿼리)
- [x] `< 768px` (모바일): 패딩 축소, `safe-area-inset-bottom` 적용
- [x] `768–1024px` (태블릿/키오스크): 폰트 +2px
- [x] `≥ 1024px` (데스크톱): `max-width: 960px`
- [x] `initial_sidebar_state: "auto"` (모바일 자동 숨김)

#### 타이포그래피
- [x] 페이지 헤더: `1.5rem / 700 / Primary`
- [x] 본문: `0.90rem / 400 / line-height 1.7`
- [x] 보조 텍스트: `0.75rem / 600 / Text Muted`

---

## 자주 묻는 질문 버튼 현황

```python
# app.py에서 정의
QUICK_QUESTIONS = [
    "진료 시간이 어떻게 되나요?",
    "주차장 이용 안내",
    "입원 절차 안내",
]
```

> 버튼 추가 시 `app.py`의 `QUICK_QUESTIONS` 리스트만 수정하면 됩니다.
> 컬럼 너비는 `app.py`의 `_text_width()` 함수가 한글 너비를 자동 계산합니다.
> 버튼 스타일 수정: `src/styles/main.css` → `.main .stButton > button` 섹션

---

## 향후 작업 (Backlog)

### 기능
- [ ] 자주 묻는 질문 데이터 기반으로 지속 확장
- [ ] Phase 1: config.py 중앙화 설정 관리
- [ ] Phase 2: 로그 파일 저장 + 날짜별 로테이션
- [ ] Phase 3: 사용자 입력 길이 제한 및 sanitization
- [ ] Phase 4: AI 응답 스트리밍 출력

### 학습 데이터
- [ ] 외래 진료 예약 방법 안내
- [ ] 증명서 발급 종류 및 절차 상세화
- [ ] 식이 관련 안내 (특식, 금식 등)

### 디자인
- [ ] 다국어 지원 (영어, 외국어 안내)

---

## 알려진 이슈 및 주의사항

- **모델 캐싱**: `ai_engine.py`의 `_CACHED_MODEL`은 앱 실행 중 메모리에 고정됨.
  `hospital_info.md`, `mri_ct_fees.csv`, `mri_fees.csv` 수정 후 반드시 **앱 재시작** 필요.
- **CSS 선택자**: Streamlit 버전에 따라 `.main` 클래스가 달라질 수 있음.
  현재 `.main .stButton > button` 선택자 사용 중.
- **한글 버튼 너비**: `_text_width()` 함수로 한글(2) / ASCII(1) 너비 환산.
  버튼 추가 시 자동 적용되므로 별도 수정 불필요.
- **st.columns 버튼 간격 제한**: Streamlit `st.columns`는 `gap="small"` (약 16px)이 최소값.
  CSS `!important`로도 인라인 JS width 오버라이드 불가 — 8px 간격 구현은 Streamlit 구조적 한계.

---

## 코딩 원칙 (Production-ready)
1. **확장성**: 향후 기능 추가가 용이한 디자인 패턴 적용
2. **안정성**: 철저한 예외 처리 및 로깅 시스템
3. **보안**: API Key 관리 및 사용자 데이터 보호 최우선
4. **성능**: 리소스 최적화 및 빠른 응답 속도 유지
5. **디자인**: 현대적이고 직관적인 UX/UI, 대기업 SaaS 스타일 미니멀 UI
