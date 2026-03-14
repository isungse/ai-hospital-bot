# 병원 AI 안내 데스크 — 전체 UI/UX 개선 프롬프트

## [역할]
당신은 의료 서비스 전문 UI/UX 디자이너이자 Streamlit 풀스택 개발자입니다.
병원 환자 및 보호자가 사용하는 AI 안내 데스크 웹앱을
접근성, 반응형 디자인, 가독성 기준으로 전면 개선하세요.

---

## [현재 서비스 분석 — 확인된 문제점]

### 1. 색상 시스템 부재
- 브랜드 컬러(빨강)가 일부 아이콘에만 산발적으로 적용됨
- 사이드바·본문·채팅 버블이 모두 흰색 계열로 시각 계층 없음
- Primary / Secondary / Accent 팔레트가 정의되지 않음

### 2. 모바일·키오스크 미최적화
- 사이드바(160px 고정)가 모바일 화면의 30% 이상 잠식
- FAQ 버튼 3개가 가로 배치 → 소형 화면에서 텍스트 잘림
- 키보드 오버랩 미대응 (safe-area-inset 부재)

### 3. 상단 FAQ 버튼 가독성 문제
- 버튼 내 텍스트가 왼쪽으로 치우쳐 정렬 불균형
- 버튼 간 여백이 과도하게 넓어 시각적 무게감 분산
- 버튼 크기와 텍스트 크기의 비율이 맞지 않음

### 4. 사이드바 진료 시간표 구조 문제
- 진료 시간 데이터가 사이드바에 고정 노출되어 화면 공간 낭비
- 모바일에서 사이드바 텍스트가 가독성을 심각하게 해침
- 숨김/펼침 기능 없이 항상 전체 노출

### 5. 채팅 버블 디자인 미흡
- AI 응답과 사용자 발화의 시각 구분이 아이콘 크기 차이뿐
- 긴 안내문이 단순 텍스트 나열로 스캔 불가
- 중요 정보(전화번호·계좌)가 본문에 묻혀 있음

### 6. 타이포그래피 위계 없음
- 섹션 제목과 본문이 동일 크기(약 14px)로 구분 불가
- 볼드/일반 텍스트 혼재로 읽기 부담 증가

---

## [개선 요구사항 — 구현 명세]

### 1. 색상 팔레트 정의 (CSS 변수 기반)
- Primary: `#0F4C9A` (의료 신뢰 블루)
- Primary Light: `#E6F1FB` (버블 배경, 강조 영역)
- Success: `#2E7D32` (진료 중 상태)
- Surface: `#F5F7FA` (사이드바, 입력 배경)
- Text Primary: `#1A1A2E`
- Text Secondary: `#6B7280`
- Accent: `#E53935` (긴급·응급 강조)

모든 색상은 WCAG AA 기준 대비율 4.5:1 이상 보장

### 2. 반응형 레이아웃 (Streamlit + CSS)
- 768px 미만 (모바일): 사이드바 자동 숨김, 하단 고정 네비 또는 상단 햄버거 메뉴 전환
- 768px~1024px (태블릿/키오스크): 사이드바 축소(120px), 폰트 크기 +2px
- 1024px 이상 (PC): 현행 2단 레이아웃 유지, 최대 너비 1280px 제한
- 입력창: `padding-bottom: env(safe-area-inset-bottom)` 적용

### 3. FAQ 버튼 개선
- 텍스트 정렬: `justify-content: center`, `text-align: center` 적용
- 버튼 패딩: 상하 12px, 좌우 16px 균형 적용
- 폰트 크기: 14px, `font-weight: 500`
- 버튼 간 gap: 8px (현행 대비 50% 축소)
- 모바일: 3개 버튼을 세로 스택 또는 가로 스크롤 칩으로 변환
- 호버 상태: `background-color` Primary Light, `border` Primary 0.5px

### 4. 사이드바 진료 시간표 → st.expander 이동
사이드바에서 진료 시간 데이터를 제거하고 메인 화면 상단에 배치:

```python
with st.expander("🕐 진료 시간 안내", expanded=False):
    st.markdown("""
    | 구분 | 평일 | 토요일 | 공휴일 |
    |------|------|--------|--------|
    | 진료 | 08:30–17:30 | 08:30–13:00 | 08:30–13:00 |
    | 종합검진 | 07:30–17:00 | 07:30–12:30 | 휴진 |
    | 기업검진 | 08:00–17:00 | 08:00–12:30 | 휴진 |
    | 일요일 | 휴진 | — | — |
    """)
```

- expander 기본값: `expanded=False` (접힘 상태로 시작)
- 사이드바에는 병원명, 진료 중 뱃지, 응급실 정보, 설정만 유지

### 5. 채팅 버블 스타일 개선
- AI 버블: `background #E6F1FB`, `border-left: 3px solid #0F4C9A`, `border-radius: 0 12px 12px 12px`
- 사용자 버블: `background #0F4C9A`, `color: white`, `border-radius: 12px 0 12px 12px`
- 섹션 내 리스트: 카드형 그룹핑 (배경 white, border 0.5px, border-radius 8px)
- 강조 정보(전화·계좌): 인라인 칩 스타일 (`background: #FFF3E0`, `color: #E65100`)
- AI 응답 상단: 병원 로고 아이콘 + "AI 안내" 라벨 표시

### 6. 타이포그래피 스케일 정의
- 섹션 제목: 16px / `font-weight: 600` / color Primary
- 본문: 14px / `font-weight: 400` / `line-height: 1.7`
- 보조 정보: 12px / `font-weight: 400` / color Text Secondary
- 강조 숫자(전화·계좌): 14px / `font-weight: 600` / `font-family: monospace`

---

## [기술 스택 및 제약]
- 프레임워크: Streamlit (Python)
- 스타일링: `st.markdown` + `unsafe_allow_html=True`, 또는 `components.html`
- 반응형: CSS media query + Streamlit column 비율 조정
- 접근성: WCAG 2.1 AA 준수, 키보드 네비게이션 지원
- 브라우저: Chrome/Safari 최신 2버전, 모바일 웹뷰 지원

---

## [산출물 요구사항]
1. 개선된 전체 Streamlit 앱 코드 (`app.py`)
2. 커스텀 CSS 스타일시트 (`style.css` 또는 인라인)
3. 반응형 레이아웃 구현 코드
4. `st.expander` 기반 진료 시간표 컴포넌트
5. 개선 전/후 비교 설명 (주석 포함)
