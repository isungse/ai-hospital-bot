from datetime import datetime, timezone, timedelta


def get_clinic_status() -> tuple[bool, str]:
    """
    현재 한국 시간 기준으로 진료 중 여부와 상태 레이블을 반환합니다.
    Returns:
        (is_open: bool, label: str)
    """
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    weekday = now.weekday()             # 0=월 … 6=일
    current = now.hour * 60 + now.minute

    OPEN_TIME     = 8 * 60 + 30        # 08:30
    CLOSE_WEEKDAY = 17 * 60 + 30       # 17:30
    CLOSE_WEEKEND = 13 * 60            # 13:00

    if weekday == 6:
        return False, "일요일 휴진"

    close_time = CLOSE_WEEKEND if weekday == 5 else CLOSE_WEEKDAY
    is_open = OPEN_TIME <= current < close_time
    return is_open, "진료 중" if is_open else "진료 종료"


def get_status_theme(is_open: bool) -> dict[str, str]:
    """
    진료 상태에 따른 CSS 색상 값을 반환합니다.
    Returns:
        {"color": str, "bg": str, "animation": str}
    """
    if is_open:
        return {
            "color":     "#16A34A",
            "bg":        "#DCFCE7",
            "animation": "pulse 1.8s infinite",
        }
    return {
        "color":     "#DC2626",
        "bg":        "#FEE2E2",
        "animation": "none",
    }
