def build_recommendation(reasons: list[str], status_label: str) -> str:
    """
    Generate a human-readable recommendation for dashboard/mobile.

    This is intentionally rule-based so it can be explained clearly in the demo.
    """
    if status_label == "NORMAL":
        return "Môi trường hiện ổn định. Tiếp tục theo dõi định kỳ."

    recommendations: list[str] = []

    reason_text = " | ".join(reasons).lower()

    if "gas" in reason_text or "air" in reason_text:
        recommendations.append("Tăng thông gió, mở cửa hoặc kiểm tra nguồn khí/khói bất thường.")

    if "temperature" in reason_text:
        recommendations.append("Điều chỉnh nhiệt độ phòng hoặc bật quạt/điều hòa nếu cần.")

    if "humidity" in reason_text:
        recommendations.append("Kiểm tra độ ẩm, cân nhắc dùng máy hút ẩm hoặc tăng thông gió.")

    if "light" in reason_text:
        recommendations.append("Điều chỉnh ánh sáng để đảm bảo môi trường sinh hoạt/làm việc phù hợp.")

    if "noise" in reason_text:
        recommendations.append("Giảm nguồn tiếng ồn hoặc di chuyển thiết bị ra khu vực yên tĩnh hơn.")

    if not recommendations:
        recommendations.append("Kiểm tra lại môi trường và cảm biến để xác định nguyên nhân bất thường.")

    if status_label == "CRITICAL":
        recommendations.insert(0, "Cảnh báo mức cao: cần kiểm tra môi trường ngay.")

    return " ".join(recommendations)
