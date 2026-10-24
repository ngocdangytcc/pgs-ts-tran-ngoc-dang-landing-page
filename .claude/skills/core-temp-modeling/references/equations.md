# Danh mục phương trình (điểm xuất phát — agent phải đối chiếu bản gốc)

## Mục lục
1. ECTemp – Kalman filter từ HR
2. Cảm biến kép / dòng nhiệt
3. PSI và biến thể
4. Mô hình đa biến / ML
5. Mô hình sinh lý nhiệt dự báo (rational models)
6. Chỉ số môi trường

## 1. ECTemp (Buller MJ et al., 2013, Physiol Meas 34:781–798)
Trạng thái: Tc_t = a·Tc_{t-1} + w, w ~ N(0, γ)
Quan sát:  HR_t = b2·Tc_t² + b1·Tc_t + b0 + v, v ~ N(0, σ)
Tham số công bố: a = 1; γ = 0,022²; b0 = −7887,1; b1 = 384,4286; b2 = −4,5714; σ = 18,88²; Tc0 = 37,1 °C; v0 = 0.
Bước lặp (mỗi phút):
  Tĉ = a·Tc_{t-1};  v̂ = a²·v_{t-1} + γ
  c = 2·b2·Tĉ + b1
  k = v̂·c / (c²·v̂ + σ)
  Tc_t = Tĉ + k·(HR_t − (b2·Tĉ² + b1·Tĉ + b0))
  v_t = (1 − k·c)·v̂
Kiểm định gốc: bias ~0 °C, LoA khoảng ±0,5 °C trên nhiều bộ dữ liệu quân sự (xác minh con số). Các nghiên cứu sau (vd. Buller 2015 — VĐV/huấn luyện quân sự; Seng 2016; Looney 2018; Eggenberger 2018; Welles 2018 — "aĉTemp" dùng thêm gia tốc/nhiệt da) → agent tra cứu và ghi kết quả.

## 2. Cảm biến kép / dòng nhiệt (Gunga HC et al., 2008, Respir Physiol Neurobiol 163:18)
Giả định dòng nhiệt một chiều qua mô (R_t) và qua cảm biến (R_s):
  Tc = T1 + (R_t/R_s)·(T1 − T2) = T1 + K·(T1 − T2)
T1 = nhiệt độ mặt tiếp xúc da, T2 = nhiệt độ mặt ngoài. K hiệu chỉnh thực nghiệm theo vị trí (trán, ngực). Sản phẩm thương mại (vd. CORE/greenteg) dùng biến thể có thuật toán độc quyền — ghi kết quả kiểm định độc lập (đã có báo cáo sai số lớn ở cường độ cao/môi trường nóng → xác minh).

## 3. PSI (Moran DS et al., 1998, Am J Physiol 275:R129–R134)
  PSI = 5·(Tc_t − Tc_0)/(39,5 − Tc_0) + 5·(HR_t − HR_0)/(180 − HR_0)   (thang 0–10)
Phân loại thường dùng: 0–2 không/rất thấp, 3–4 thấp, 5–6 vừa, 7–8 cao, 9–10 rất cao.
Biến thể cần tra: aPSI (Adaptive PSI, Buller 2008 — dựa trên ước tính Tc), PSI dùng HRmax cá nhân, CSI (Contextual/Cumulative strain), Heat Strain Score Index.

## 4. Mô hình đa biến / ML
Hồi quy/ML từ HR + nhiệt da + gia tốc + nhiệt độ/độ ẩm môi trường (vd. Richmond 2015; Niedermann 2014; Eggenberger 2018; các mô hình LSTM/gradient boosting gần đây). Ghi: dữ liệu huấn luyện, kiểm định ngoài, RMSE.

## 5. Mô hình sinh lý nhiệt dự báo
SCENARIO (USARIEM), Heat Strain Decision Aid (HSDA), Predicted Heat Strain (ISO 7933), mô hình nhiều nút (Gagge 2-node, Fiala). Dùng để dự báo trước buổi tập/thi đấu theo thời tiết, không thời gian thực.

## 6. Chỉ số môi trường
WBGT ngoài trời = 0,7·Tnw + 0,2·Tg + 0,1·Tdb (ISO 7243); Heat Index; UTCI. Dùng kết hợp với Tc để quyết định điều chỉnh/hoãn thi đấu.
