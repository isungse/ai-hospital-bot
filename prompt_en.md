# Hospital AI Info Desk — Full UI/UX Improvement Prompt

## [Role]
You are a medical-service UI/UX designer and Streamlit full-stack developer.
Redesign the hospital AI information desk web app used by patients and caregivers,
applying accessibility, responsive design, and readability standards throughout.

---

## [Current Service Analysis — Identified Issues]

### 1. No color system
- Brand color (red) applied sporadically to a few icons only
- Sidebar, main content, and chat bubbles share an undifferentiated white palette
- No defined Primary / Secondary / Accent token set

### 2. Mobile & kiosk not optimized
- Fixed-width sidebar (160px) occupies 30%+ of mobile viewport
- Three FAQ buttons arranged horizontally — text clips on small screens
- No keyboard overlap handling (missing safe-area-inset)

### 3. Top FAQ button readability issues
- Button text is left-aligned, creating visual imbalance
- Excessive gap between buttons dilutes visual weight
- Mismatch between button size and font size

### 4. Sidebar clinic schedule structural problem
- Schedule data is always visible in sidebar, wasting screen real estate
- On mobile, sidebar text severely impairs readability
- No collapse/expand functionality — always fully exposed

### 5. Chat bubble design shortcomings
- AI response and user message are distinguished only by icon size
- Long informational text is plain prose — not scannable
- Critical info (phone numbers, bank accounts) buried in body text

### 6. No typographic hierarchy
- Section headings and body text share the same size (~14px)
- Mixed bold / regular text increases cognitive load

---

## [Improvement Requirements — Implementation Spec]

### 1. Color palette (CSS variable–based)
- Primary: `#0F4C9A` (medical trust blue)
- Primary Light: `#E6F1FB` (bubble bg, highlight areas)
- Success: `#2E7D32` (open / active status)
- Surface: `#F5F7FA` (sidebar, input background)
- Text Primary: `#1A1A2E`
- Text Secondary: `#6B7280`
- Accent: `#E53935` (emergency / urgent emphasis)

All colors must meet WCAG AA contrast ratio ≥ 4.5:1

### 2. Responsive layout (Streamlit + CSS)
- < 768px (mobile): auto-hide sidebar; switch to sticky bottom nav or hamburger menu at top
- 768–1024px (tablet / kiosk): shrink sidebar to 120px; increase font sizes by 2px
- ≥ 1024px (desktop): keep current two-column layout; cap max-width at 1280px
- Input bar: apply `padding-bottom: env(safe-area-inset-bottom)`

### 3. FAQ button improvements
- Text alignment: apply `justify-content: center`, `text-align: center`
- Button padding: 12px top/bottom, 16px left/right — balanced
- Font: 14px, `font-weight: 500`
- Gap between buttons: 8px (reduce current gap by ~50%)
- Mobile: stack 3 buttons vertically, or convert to horizontal scroll chips
- Hover state: `background-color` Primary Light, `border` Primary 0.5px

### 4. Move clinic schedule from sidebar → st.expander
Remove schedule data from the sidebar and place at the top of main content:

```python
with st.expander("🕐 Clinic Hours", expanded=False):
    st.markdown("""
    | Category    | Weekdays    | Saturday    | Holiday     |
    |-------------|-------------|-------------|-------------|
    | General     | 08:30–17:30 | 08:30–13:00 | 08:30–13:00 |
    | Health Exam | 07:30–17:00 | 07:30–12:30 | Closed      |
    | Corp. Exam  | 08:00–17:00 | 08:00–12:30 | Closed      |
    | Sunday      | Closed      | —           | —           |
    """)
```

- Default state: `expanded=False` (collapsed on load)
- Sidebar retains: hospital name, open/closed badge, ER info, settings only

### 5. Chat bubble style improvements
- AI bubble: `background: #E6F1FB`, `border-left: 3px solid #0F4C9A`, `border-radius: 0 12px 12px 12px`
- User bubble: `background: #0F4C9A`, `color: white`, `border-radius: 12px 0 12px 12px`
- In-response lists: card-style grouping (white bg, 0.5px border, border-radius 8px)
- Highlighted info (phone / account): inline chip (`background: #FFF3E0`, `color: #E65100`)
- AI response header: hospital logo icon + "AI Guide" label

### 6. Typography scale
- Section heading: 16px / `weight: 600` / color Primary
- Body text: 14px / `weight: 400` / `line-height: 1.7`
- Supporting text: 12px / `weight: 400` / color Text Secondary
- Emphasis numbers (phone / account): 14px / `weight: 600` / `font-family: monospace`

---

## [Tech Stack & Constraints]
- Framework: Streamlit (Python)
- Styling: `st.markdown` with `unsafe_allow_html=True`, or `components.html`
- Responsive: CSS media queries + Streamlit column ratio adjustments
- Accessibility: WCAG 2.1 AA compliant, keyboard navigation supported
- Browser support: Latest 2 versions of Chrome/Safari, mobile webview

---

## [Expected Deliverables]
1. Full improved Streamlit app code (`app.py`)
2. Custom CSS stylesheet (`style.css` or inline)
3. Responsive layout implementation
4. `st.expander`-based clinic schedule component
5. Before/after comparison notes with inline comments
