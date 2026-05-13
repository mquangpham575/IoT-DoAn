def build_recommendation(reasons: list[str], status_label: str) -> str:
    """
    Generate human-centered recommendations for dashboard/mobile/Discord.

    Important design principle:
    - The IoT device is a fixed monitoring node.
    - Recommendations should guide people to improve the environment.
    - Do not suggest moving or changing the monitoring device itself.
    """
    if status_label == "NORMAL":
        return (
            "Môi trường hiện đang ổn định. "
            "Tiếp tục theo dõi định kỳ để phát hiện sớm các thay đổi bất thường."
        )

    reason_text = " | ".join(reasons).lower()
    recommendations: list[str] = []

    has_gas_issue = "gas" in reason_text or "air quality" in reason_text
    has_temp_issue = "temperature" in reason_text
    has_humidity_issue = "humidity" in reason_text
    has_light_issue = "light" in reason_text
    has_noise_issue = "noise" in reason_text
    has_multiple_issue = "multiple abnormal" in reason_text

    if status_label == "CRITICAL":
        recommendations.append(
            "Cảnh báo mức cao, nên kiểm tra tình trạng môi trường trong khu vực ngay."
        )

    if has_gas_issue:
        recommendations.append(
            "Không khí có dấu hiệu kém an toàn. "
            "Nên tăng thông gió, mở cửa hoặc kiểm tra xem trong phòng có khói, mùi lạ hay nguồn khí bất thường không."
        )

    if has_temp_issue:
        recommendations.append(
            "Nhiệt độ đang cao hơn mức dễ chịu. "
            "Nên bật quạt, điều hòa hoặc giảm các nguồn sinh nhiệt trong phòng nếu cần."
        )

    if has_humidity_issue:
        recommendations.append(
            "Độ ẩm đang nằm ngoài mức lý tưởng. "
            "Nên kiểm tra độ thông thoáng của phòng và cân nhắc dùng máy hút ẩm hoặc tăng lưu thông không khí."
        )

    if has_light_issue:
        recommendations.append(
            "Ánh sáng trong khu vực chưa phù hợp. "
            "Nên điều chỉnh đèn hoặc tận dụng ánh sáng tự nhiên để đảm bảo điều kiện sinh hoạt và làm việc tốt hơn."
        )

    if has_noise_issue:
        recommendations.append(
            "Mức tiếng ồn đang cao. "
            "Nên giảm các nguồn phát tiếng ồn trong khu vực hoặc hạn chế những hoạt động gây ồn kéo dài."
        )

    if has_multiple_issue:
        recommendations.append(
            "Nhiều chỉ số môi trường đang bất thường cùng lúc, nên kiểm tra tổng thể khu vực thay vì chỉ xử lý một yếu tố riêng lẻ."
        )

    if not recommendations:
        recommendations.append(
            "Môi trường có dấu hiệu bất thường. "
            "Nên kiểm tra lại khu vực xung quanh và tiếp tục theo dõi các chỉ số trong vài phút tiếp theo."
        )

    return " ".join(recommendations)
