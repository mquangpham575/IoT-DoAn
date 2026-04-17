# Đề tài: Hệ thống giám sát sức khỏe và tiện nghi trong nhà:

> Mục tiêu: Xây dựng hệ thống IoT giám sát môi trường trong nhà (nhiệt độ, độ ẩm, CO₂, ánh sáng, tiếng ồn) theo thời gian thực. Dữ liệu được phân tích bằng AI để đánh giá mức độ thoải mái và phát hiện các rủi ro sức khỏe như không khí ngột ngạt hoặc độ ẩm cao. Hệ thống cung cấp cảnh báo và khuyến nghị nhằm cải thiện môi trường sống trong nhà.

## Thành viên 1 - Thiết kế Phần cứng (Hardware)

- Chịu trách nhiệm lựa chọn /thiết kế mạch hệ thống thiết bị.
- Mua/mượn thiết bị.
- Tạo thành hệ thống thiết bị để chuẩn bị cho thành viên 2.

## Thành viên 2 - Lập trình Nhúng & Edge Logic

- Đảm nhiệm việc viết code C/C++ trực tiếp cho thiết bị.
- Chạy được và chạy đúng mục tiêu đề ra. (có thể chỉnh sửa theo yêu cầu đề tài và mục tiêu nhóm hướng đến)

## Thành viên 3 - AI và Data

Phụ trách tất cả về AI:

- có rule-base để đảm bảo AI chạy đúng,
- có dự đoán (static model - đóng gói và xuất mô hình đã huấn luyện (ví dụ dưới dạng file .pkl) để tích hợp vào hệ thống.)
- Phụ code logic cho thành viên 2 để đồng bộ
- Tích hợp vào server của thành viên 4 tạo

## Thành viên 4 - Backend & Edge Logic (Backend & Edge Computing)

- Xây dựng Server trung tâm bằng Python (FastAPI/Flask) và quản lý Database.
- Xử lý việc nhận dữ liệu từ ESP32 gửi lên và giao tiếp với App Android.
- Edge computing

## Thành viên 5 - Phát triển App Android (Mobile App - Kotlin/Java)

- Xây dựng ứng dụng Android với tính năng Online/ Offline.
- Thiết lập cơ sở dữ liệu local (Room Database) để người dùng xem lại lịch sử ngay cả khi không có internet.
- Lập trình tính năng tự động tìm kiếm IP thiết bị trong mạng WiFi (mDNS) để hiển thị dữ liệu realtime khi ở chế độ Offline và đồng bộ với Cloud/Server khi có internet.
