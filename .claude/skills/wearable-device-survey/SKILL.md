---
name: wearable-device-survey
description: Khảo sát và so sánh thiết bị đeo/phần mềm đo hoặc ước tính nhiệt độ lõi, nhiệt độ da, nhịp tim, mồ hôi cho VĐV và lao động nóng — kèm kiểm tra thị trường (đã thương mại hoá chưa, còn bán không, có ở Việt Nam không, giá, giấy phép, sáng chế). Dùng khi được hỏi "có thiết bị nào đo nhiệt độ lõi", "so sánh CORE sensor / viên nang / Kenzen / Garmin...", "sản phẩm này đã có trên thị trường chưa", "mua ở VN được không", "đối thủ cạnh tranh", "khoảng trống thị trường".
---
# Khảo sát thiết bị & kiểm tra thị trường

## 1. Phân lớp công nghệ (dùng làm khung bảng)
| Lớp | Nguyên lý | Ví dụ khởi đầu (cần xác minh lại, không coi là đầy đủ) |
|---|---|---|
| Đo trực tiếp – chuẩn tham chiếu | Viên nang nuốt đo nhiệt, nhiệt kế trực tràng/thực quản | e-Celsius (BodyCap), CorTemp (HQ Inc), myTemp |
| Ước tính – dòng nhiệt/cảm biến kép | Nhiệt độ da + dòng nhiệt qua cảm biến | CORE body temperature sensor (greenteg), Dräger double sensor |
| Ước tính – HR/Kalman & ML đa cảm biến | HR (± gia tốc, nhiệt da, môi trường) → mô hình | ECTemp trong Equivital/Zephyr/Hidalgo, Kenzen, SlateSafety, Hexoskin |
| Chỉ báo gián tiếp | Nhiệt độ da cổ tay/ngón, HRV, mồ hôi | Garmin, Apple Watch, Whoop, Oura, Polar; Gx Sweat Patch (Epicore) |
| Phần mềm/nền tảng | Dashboard đội nhóm, cảnh báo, WBGT | App kèm thiết bị, nền tảng an toàn lao động, ứng dụng WBGT |

## 2. Trường dữ liệu bắt buộc cho mỗi sản phẩm
Tên · hãng · lớp · tín hiệu đo · vị trí đeo · tần số mẫu · **sai số so với chuẩn** (bias, 95% LoA, MAE/RMSE, n, điều kiện, nguồn độc lập hay của hãng) · xuất dữ liệu (API/SDK/CSV/ANT+/BLE) · chứng nhận · giá tham khảo · ghi chú hạn chế.

Lý do: mô hình cảnh báo chỉ tốt bằng dữ liệu vào; thiết bị không xuất được HR thô theo phút hoặc nhiệt da thì không dùng được cho thuật toán tự xây.

## 3. Kiểm tra thị trường (bước bắt buộc)
Mục đích: biết giải pháp **đã tồn tại hay chưa**, tránh làm lại cái đã có và tìm khoảng trống thật.

Với mỗi sản phẩm:
1. **Trạng thái**: 🟢 đang bán · 🟡 thí điểm/B2B/quân đội · 🔴 ngừng bán/công ty đóng cửa/bị mua lại · ⚪ chỉ nghiên cứu. Nguồn: trang bán hàng, thông cáo, tin tức, LinkedIn công ty — ghi **ngày truy cập**.
2. **Kênh bán & giá**: bán lẻ hay hợp đồng doanh nghiệp, giá thiết bị + thuê bao.
3. **Việt Nam**: có nhà phân phối/chính hãng? mua quốc tế? phân loại trang thiết bị y tế (NĐ 98/2021/NĐ-CP, sửa đổi bởi NĐ 07/2023 & NĐ 04/2025; TT 05/2022); dữ liệu sức khoẻ (Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 + NĐ 356/2025/NĐ-CP, thay NĐ 13/2023).
4. **Giấy phép**: FDA (510k/De Novo/wellness), CE MDR, hay chỉ "wellness" — quyết định có được dùng tuyên bố y tế không.

Với ý tưởng tổng thể (đo → ước tính Tc → cảnh báo → can thiệp):
5. **Sáng chế**: Google Patents/Espacenet với từ khoá kiểu "core temperature estimation heart rate Kalman", "heat strain alert wearable"; ghi số patent, chủ sở hữu, còn hiệu lực không. Đây là sàng lọc sơ bộ, không thay tư vấn sở hữu trí tuệ.
6. **Ma trận khoảng trống**: hàng = chức năng (đo Tc, ước tính Tc không xâm lấn, cảnh báo thời gian thực, dashboard ban y tế, phác đồ can thiệp, hiệu chỉnh người Việt/nóng ẩm, tiếng Việt, giá phù hợp); cột = sản phẩm; ô = có/một phần/không. Kết luận: phần nào đã có, phần nào là cơ hội.

## 4. Định dạng đầu ra
Markdown: bảng so sánh → bảng trạng thái thị trường → mục Việt Nam → sáng chế → ma trận khoảng trống → danh sách nguồn (URL/DOI + ngày truy cập).
