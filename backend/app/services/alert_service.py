def build_recommendation(reason_codes: list[str], status_label: str) -> str:
    """
    Generate human-centered recommendations based on structured reason codes.

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

    recommendations: list[str] = []

    if status_label == "CRITICAL":
        recommendations.append(
            "Cảnh báo mức cao, nên kiểm tra tình trạng môi trường trong khu vực ngay."
        )

    # Decoupled mapping using reason codes to prevent English text dependency
    code_to_recommendation = {
        "gas_critical": "Không khí có dấu hiệu kém an toàn. Nên tăng thông gió, mở cửa hoặc kiểm tra xem trong phòng có khói, mùi lạ hay nguồn khí bất thường không.",
        "gas_high": "Không khí có dấu hiệu kém an toàn. Nên tăng thông gió, mở cửa hoặc kiểm tra xem trong phòng có khói, mùi lạ hay nguồn khí bất thường không.",
        "gas_moderate": "Không khí có dấu hiệu kém an toàn. Nên tăng thông gió, mở cửa hoặc kiểm tra xem trong phòng có khói, mùi lạ hay nguồn khí bất thường không.",
        "temp_critical": "Nhiệt độ đang cao hơn mức dễ chịu. Nên bật quạt, điều hòa hoặc giảm các nguồn sinh nhiệt trong phòng nếu cần.",
        "temp_high": "Nhiệt độ đang cao hơn mức dễ chịu. Nên bật quạt, điều hòa hoặc giảm các nguồn sinh nhiệt trong phòng nếu cần.",
        "temp_low": "Nhiệt độ đang thấp hơn mức dễ chịu. Cân nhắc điều chỉnh thiết bị sưởi ấm hoặc đóng bớt cửa thoáng gió.",
        "humid_very_high": "Độ ẩm đang ở mức rất cao. Nên tăng thông thoáng phòng hoặc sử dụng máy hút ẩm để tránh ẩm mốc.",
        "humid_high": "Độ ẩm đang ở mức cao. Nên tăng thông thoáng phòng hoặc sử dụng máy hút ẩm để tránh ẩm mốc.",
        "humid_low": "Độ ẩm đang thấp dưới mức lý tưởng. Cân nhắc sử dụng máy tạo ẩm hoặc bổ sung nguồn hơi nước để bảo vệ sức khỏe.",
        "light_extremely_low": "Ánh sáng trong khu vực chưa phù hợp. Nên điều chỉnh đèn hoặc tận dụng ánh sáng tự nhiên để đảm bảo điều kiện sinh hoạt và làm việc tốt hơn.",
        "light_low": "Ánh sáng trong khu vực chưa phù hợp. Nên điều chỉnh đèn hoặc tận dụng ánh sáng tự nhiên để đảm bảo điều kiện sinh hoạt và làm việc tốt hơn.",
        "noise_high": "Mức tiếng ồn đang cao. Nên giảm các nguồn phát tiếng ồn trong khu vực hoặc hạn chế những hoạt động gây ồn kéo dài.",
        "noise_moderate": "Mức tiếng ồn đang cao. Nên giảm các nguồn phát tiếng ồn trong khu vực hoặc hạn chế những hoạt động gây ồn kéo dài.",
        "multiple_abnormal": "Nhiều chỉ số môi trường đang bất thường cùng lúc, nên kiểm tra tổng thể khu vực thay vì chỉ xử lý một yếu tố riêng lẻ.",
        "ai_anomaly": "AI phát hiện có sự bất thường trong tương quan các chỉ số, nên lưu ý theo dõi sát."
    }

    # Avoid duplicate recommendations for similar issues (e.g. gas_high and gas_moderate)
    added_recommendations = set()
    for code in reason_codes:
        rec = code_to_recommendation.get(code)
        if rec and rec not in added_recommendations:
            recommendations.append(rec)
            added_recommendations.add(rec)

    if not recommendations:
        recommendations.append(
            "Môi trường có dấu hiệu bất thường. "
            "Nên kiểm tra lại khu vực xung quanh và tiếp tục theo dõi các chỉ số trong vài phút tiếp theo."
        )

    return " ".join(recommendations)
