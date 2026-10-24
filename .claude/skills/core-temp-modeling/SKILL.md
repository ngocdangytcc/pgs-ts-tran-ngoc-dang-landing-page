---
name: core-temp-modeling
description: Phương trình và thuật toán ước tính nhiệt độ lõi (Tc) từ nhịp tim (ECTemp – Kalman filter), nhiệt độ da/dòng nhiệt (cảm biến kép), mô hình ML đa cảm biến, chỉ số căng thẳng nhiệt (PSI, aPSI) và logic cảnh báo nhiều tầng; có script Python chạy được. Dùng khi cần "công thức tính nhiệt độ lõi từ nhịp tim", "phương trình chuyển đổi nhiệt độ da → nhiệt độ lõi", "tính PSI", "xây thuật toán cảnh báo say nắng", "mô phỏng Tc", hoặc chỉnh ngưỡng/tham số cảnh báo.
---
# Mô hình ước tính nhiệt độ lõi & cảnh báo

## Tài nguyên
- `references/equations.md` — danh mục phương trình đã biết, tham số, điều kiện kiểm định, giới hạn. Đọc trước khi tổng hợp hoặc code.
- `scripts/heatstrain.py` — thư viện + CLI thuần Python (không phụ thuộc):
  - `ectemp(hr_series)` · `double_sensor(t_skin, t_outer, k)` · `psi(...)` · `classify(...)` · `run(rows)`
  - `python3 scripts/heatstrain.py demo` · `python3 scripts/heatstrain.py run data.csv --hr0 70 --tc0 37.0`
    (CSV: `minute,hr[,tc_measured]`; HR lấy mẫu 1 phút, đúng như ECTemp gốc yêu cầu).

## Cách làm
1. **Chọn mô hình theo dữ liệu sẵn có**: chỉ HR → ECTemp; có cảm biến dòng nhiệt → cảm biến kép (cần K hiệu chỉnh); có HR + nhiệt da + gia tốc + môi trường → mô hình hỗn hợp/ML (cần dữ liệu huấn luyện có Tc tham chiếu).
2. **Cá thể hoá**: Tc0 và HR0 lúc nghỉ; tham số ECTemp gốc được ước lượng trên quân nhân — với VĐV ưu tú/người Việt nên hiệu chỉnh lại b0–b2 bằng dữ liệu viên nang.
3. **Tách cảnh báo khỏi ước tính**: ước tính Tc kèm độ bất định (phương sai Kalman); cảnh báo dựa trên Tc, tốc độ tăng, PSI, triệu chứng. Ngưỡng lấy từ `heat-illness-clinical`, lưu thành tham số.
4. **Kiểm định**: so với Tc tham chiếu bằng Bland–Altman (bias, 95% LoA), RMSE; báo cáo độ nhạy/độ đặc hiệu tại ngưỡng cảnh báo (vd. phát hiện Tc ≥ 39,5 °C) — với cảnh báo an toàn, độ nhạy quan trọng hơn.
5. **Giới hạn phải nêu**: HR tách khỏi Tc khi mất nước, sốt, caffein, căng thẳng tâm lý, thuốc chẹn beta, giai đoạn hồi phục; HR quang học cổ tay nhiễu khi chạy cường độ cao; nhiệt độ da bị ảnh hưởng bởi mồ hôi, gió, tưới nước.

## Cảnh báo pháp lý
Mã nguồn là prototype nghiên cứu, không phải thiết bị y tế. Muốn đưa ra thị trường cần đăng ký trang thiết bị y tế.
