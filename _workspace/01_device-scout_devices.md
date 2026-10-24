# 01 — Khảo sát thiết bị & phần mềm theo dõi / ước tính nhiệt độ lõi (Tc) cho VĐV

*Agent:* device-scout · *Ngày lập / ngày truy cập web:* 2026-10-24 · *Đầu vào:* `_workspace/00_brief.md`
*Phạm vi:* §1, §2, §4 của skill `wearable-device-survey`. Mục §3 (thị trường, Việt Nam, sáng chế) chỉ là **trạng thái sơ bộ**, `market-analyst` sẽ làm sâu.
*Nguồn:* bài peer-review lấy qua PubMed (có PMID/DOI); thông tin giá, chứng nhận, tình trạng lấy qua WebSearch, phần lớn là nguồn hãng hoặc báo thương mại. Ký hiệu: **[ĐL]** = kiểm định độc lập · **[H]** = tác giả là người của hãng hoặc nguồn hãng · ❓ = chưa kiểm chứng.

---

## 0. Tóm tắt nhanh

1. **Chuẩn tham chiếu thực địa** vẫn là **viên nang nuốt** (e-Celsius, CorTemp, myTemp). Trong bể nước, sai số hệ thống của chúng < 0,1 °C (Bongers 2018, PMID 28816921). Hạn chế: dùng một lần, phải nuốt trước 4–6 h, bị nhiễu khi uống nước lạnh, và đắt khi dùng cho đông người.
2. **Ước tính bằng dòng nhiệt (heat flux)**, đại diện là CORE/CORE 2 và Calera Research của greenteg. Bằng chứng **mâu thuẫn**:
   - Có nghiên cứu tốt: bias 0,01 °C, LoA ±0,37 °C khi đạp xe ở 32 °C (Januário 2024).
   - Có nghiên cứu không đạt: khoảng 50% cặp đo lệch > 0,3 °C (Verdel 2021); bias −0,3 °C (Priego-Quesada 2025); không bắt được mức giảm Tc khi uống nước lạnh (Goulet 2026).
3. **Ước tính từ HR bằng bộ lọc Kalman (ECTemp, USARIEM)** được nhúng trong Equivital và Zephyr, có mô hình tương tự ở Kenzen.
   - Ở mức nhóm, sai số chấp nhận được: bias khoảng 0–0,15 °C, LoA ±0,45–0,64 °C.
   - Ở VĐV ưu tú trong điều kiện nóng ẩm (de Korte 2022), **độ nhạy tụt về 0–50% khi Tc > 39 °C**. Trong 10 ca say nắng gắng sức (EHS), độ nhạy chỉ 20% (Hintz 2023). Đây đúng là vùng nguy hiểm cần cảnh báo.
4. **So sánh đối đầu độc lập mới nhất** (Stevenson 2026, MSSE, lính cứu hoả mặc PPE) gồm Equivital, Kenzen, Zephyr và CORE. Tất cả đều có **CCC 0,26–0,85, LoA rộng 1,25–2,22 °C**, và sai số tăng khi Tc > 38,5 °C. Kết luận của tác giả: các thiết bị này theo được xu hướng nhưng **không đủ chính xác để ra quyết định an toàn**.
5. **Đồng hồ và nhẫn tiêu dùng** (Garmin, Apple, Samsung, Oura, Whoop) chỉ đo **nhiệt độ da khi ngủ, dạng độ lệch so với nền**. Không có bằng chứng peer-review nào cho thấy chúng ước tính được Tc khi vận động. Giá trị chính của chúng là **nguồn HR** cho thuật toán tự xây.
6. **Cơ hội cho thuật toán tự xây:** những thiết bị xuất được HR thô theo giây/phút qua BLE/ANT+ (đai ngực Polar/Garmin, Equivital SDK, Zephyr, Hexoskin API) cho phép chạy ECTemp hoặc Kalman tại chỗ, không phụ thuộc mô hình đóng của hãng.

---

## 1. Phân lớp công nghệ (khung)

| Lớp | Nguyên lý | Sản phẩm trong khảo sát này |
|---|---|---|
| A. Đo trực tiếp – chuẩn tham chiếu | Viên nang nuốt; nhiệt kế trực tràng hoặc thực quản | e-Celsius (BodyCap), CorTemp (HQ Inc), myTemp, VitalSense (❓ tình trạng), đầu dò trực tràng (YSI 401, DataTherm II) |
| B. Ước tính – dòng nhiệt / cảm biến kép / ZHF | Nhiệt độ da + dòng nhiệt (dual-heat-flux, zero-heat-flux) | CORE / CORE 2 (greenteg), Calera Research (greenteg), Dräger Tcore / Double Sensor, 3M SpotOn (ZHF, lâm sàng), Cosinuss° One (trong tai), miếng dán dual-heat-flux của Nhật (nghiên cứu) |
| C. Ước tính – HR/Kalman & ML đa cảm biến | HR (± gia tốc, nhiệt độ da, môi trường) → mô hình | Equivital EQ02+ LifeMonitor (ECTemp), Zephyr BioHarness (ECTemp), Kenzen, SlateSafety BAND V2, Hexoskin (nguồn HR) |
| D. Chỉ báo gián tiếp | Nhiệt độ da cổ tay/ngón, HRV, mồ hôi | Garmin, Apple Watch, Samsung Galaxy Watch, Oura, Whoop, Polar (đai HR); Gx Sweat Patch (Epicore), Nix Biosensors, hDrop |
| E. Phần mềm / nền tảng / môi trường | Dashboard đội nhóm, cảnh báo, WBGT | Kestrel 5400 Heat Stress Tracker + LiNK, OSHA-NIOSH Heat Safety Tool (❓), Zephyr OmniSense, Kenzen cloud, SlateSafety portal, CORE app + Garmin Connect IQ |

---

## 2. Bảng so sánh chi tiết (trường dữ liệu §2)

### 2A. Lớp A — Đo trực tiếp (chuẩn tham chiếu)

**A1. e-Celsius Performance / eCelsius Medical (BodyCap, Pháp)**
- **Tín hiệu, vị trí:** viên nang nuốt.
- **Sai số so với chuẩn:**
  - Bể nước: bias −0,081 ± 0,055 °C (Bongers 2018) [ĐL].
  - Thường được dùng làm chuẩn trong các nghiên cứu kiểm định CORE/Calera.
- **Xuất dữ liệu:** bộ thu (monitor) riêng; phần mềm hãng. Định dạng xuất ❓.
- **Chứng nhận:** CE y tế loại IIb (2017). Thông cáo hãng (2023) nói eCelsius Medical System được FDA chấp thuận; số hồ sơ ❓.
- **Giá:** khoảng 40–60 €/viên (thông tin 2017, có thể đã cũ).
- **Hạn chế:** dùng một lần. Kết quả phụ thuộc vị trí viên trong ống tiêu hoá. Bị nhiễu khi uống nước lạnh.

**A2. CorTemp (HQ Inc, Mỹ)**
- **Tín hiệu, vị trí:** viên nang nuốt; cũng dùng được làm viên đặt trực tràng.
- **Sai số so với chuẩn:**
  - Bể nước: bias +0,077 ± 0,040 °C (Bongers 2018) [ĐL].
  - Khi dùng làm viên đặt trực tràng tái sử dụng 50 h, bias nằm trong ±0,27 °C (Pancrate 2020) [ĐL].
- **Xuất dữ liệu:** bộ ghi dữ liệu đeo người (data recorder). Định dạng xuất ❓.
- **Chứng nhận:** hãng ghi "FDA cleared"; hồ sơ 510(k) K880639, mã FLL. Một số bản ghi GUDID ghi obsolete ❓.
- **Giá:** khoảng 46 USD/viên (nguồn báo, không ghi ngày) ❓.
- **Hạn chế:** đã được dùng nhiều trong nghiên cứu EHS quân đội và bóng bầu dục Mỹ.

**A3. myTemp (Hà Lan, spin-off Radboud)**
- **Tín hiệu, vị trí:** viên nang nuốt, không pin.
- **Sai số so với chuẩn:** bias −0,003 ± 0,006 °C, thấp nhất trong 4 hệ (Bongers 2018) [ĐL]. Lưu ý nhóm tác giả gắn với nhóm phát triển.
- **Xuất dữ liệu:** ❓
- **Chứng nhận:** ❓
- **Giá:** được mô tả là rẻ hơn các hệ thương mại khác ❓.
- **Hạn chế:** tình trạng thương mại ❓.

**A4. VitalSense (Philips Respironics / Mini Mitter)**
- **Tín hiệu, vị trí:** viên nang nuốt.
- **Sai số so với chuẩn:** bias −0,017 ± 0,023 °C (Bongers 2018) [ĐL].
- **Xuất dữ liệu, chứng nhận, giá:** ❓
- **Hạn chế:** có thể đã ngừng bán; **chưa xác nhận** (search không ra nguồn).

**A5. Đầu dò trực tràng/thực quản (YSI 401, DataTherm II…)**
- **Tín hiệu, vị trí:** đầu dò có dây.
- **Sai số:** đây chính là chuẩn tham chiếu.
- **Xuất dữ liệu, chứng nhận, giá:** tuỳ hệ thống.
- **Hạn chế:** không khả thi khi VĐV đang chạy giải. Đo trực tràng sau khi ngã gục vẫn là chuẩn chẩn đoán EHS.

**Nhận xét Lớp A:** viên nang phù hợp cho **nghiên cứu hiệu chỉnh** (ví dụ thu dữ liệu VĐV Việt Nam để huấn luyện hoặc hiệu chỉnh mô hình). Không phù hợp để giám sát hàng nghìn người chạy marathon.

### 2B. Lớp B — Ước tính bằng dòng nhiệt / ZHF / tai

**B1. CORE / CORE 2 (greenteg, Thuỵ Sĩ)**
- **Tín hiệu, vị trí:** nhiệt độ da + dòng nhiệt, cộng HR qua đai ngực ghép nối. Đeo ở ngực (kẹp đai HR) hoặc cánh tay.
- **Tần số mẫu:** ❓ (hiển thị theo giây trên app/thiết bị).
- **Sai số so với chuẩn:**
  - Verdel 2021 [ĐL]: n = 12 + 13, đạp xe ở 19 °C và 31 °C. Khoảng 50% cặp đo lệch > 0,3 °C so với nhiệt độ trực tràng (Tre). Kết luận: không xác nhận được tuyên bố của hãng.
  - Daanen 2023 [ĐL]: n = 9, 18 °C. CORE có xu hướng **đánh giá cao** (Tmax 38,6 so với 38,4 °C).
  - Goulet 2026 [ĐL]: n = 11, nghỉ, uống nước 4 °C. Viên nang ghi Tc giảm −0,76 °C nhưng CORE chỉ ghi −0,09 °C, tức **không bắt được giảm Tc** khi làm lạnh trong.
  - Xie 2026 [ĐL]: n = 26, khi ngủ. Theo Bland-Altman hiệu chỉnh tự tương quan, 49–66% điểm nằm ngoài LoA. Tác giả kết luận không đo đúng Tc tuyệt đối ban đêm.
  - Stevenson 2026 [ĐL]: lính cứu hoả mặc PPE. CORE (ngực/tay) thuộc nhóm "tốt nhất" khi gộp vận động và hồi phục. Tuy vậy, mọi thiết bị đều có LoA 1,25–2,22 °C.
  - Hu 2026: bóng chuyền bãi biển ngoài trời; chỉ đánh giá tính khả thi, không có chuẩn đối chiếu.
- **Xuất dữ liệu:** BLE và ANT+, app CORE. Ghi vào file FIT của Garmin qua Connect IQ; tích hợp Wahoo. **Không thấy API hoặc SDK công khai.**
- **Chứng nhận:** wellness, không phải thiết bị y tế ❓ (cần xác minh).
- **Giá:** CORE 2 khoảng 269,95 CHF / 359 USD / 243 € (bán lẻ, từ tháng 3/2025).
- **Hạn chế:** thuật toán đóng. Sai số lớn hơn khi làm lạnh nhanh và ở người tổn thương tuỷ sống.

**B2. Calera Research (greenteg), phiên bản nghiên cứu của CORE**
- **Tín hiệu, vị trí:** dòng nhiệt + nhiệt độ da + HR; đeo ở ngực.
- **Tần số mẫu:** 1/phút (theo Januário).
- **Sai số so với chuẩn:**
  - Januário 2024 [ĐL]: n = 15, 32 °C/60% RH, đạp xe. Bias 0,01 °C, LoA +0,38 / −0,35 °C, ICC 0,98.
  - Priego-Quesada 2025 [ĐL]: n = 20, 22 °C. Bias −0,3 ± 0,2 °C, ICC 0,47; độ chính xác chịu ảnh hưởng của thể lực hiếu khí.
  - Sanchez-Jimenez 2026 [ĐL]: n = 21. Ở người không tổn thương tuỷ sống: bias 0,06 (0,22) °C, ICC 0,65. Ở người tổn thương tuỷ sống: kém, ICC −0,12.
  - Kubota 2025 [ĐL]: nhịp sinh học. Pha Tc cho ICC 0,96 (chỉ đánh giá pha, không đánh giá giá trị tuyệt đối).
- **Xuất dữ liệu:** xuất dữ liệu cho nghiên cứu ❓ (định dạng chưa rõ).
- **Chứng nhận, giá:** ❓
- **Hạn chế:** kết quả không đồng nhất giữa các nghiên cứu.

**B3. Dräger Tcore / Double Sensor (Dräger, Đức)**
- **Tín hiệu, vị trí:** cảm biến kép theo nguyên lý cân bằng dòng nhiệt; đeo ở trán, cổ tay, có thể gắn vào mũ bảo hộ.
- **Tần số mẫu:** ❓
- **Sai số so với chuẩn:** nghiên cứu của Tsadok (13 nam, 90 phút trong nóng khô/nóng ẩm) [ĐL] cho thấy **thuật toán gốc của hãng không đạt**; nhóm nghiên cứu phải xây mô hình riêng. Chi tiết số liệu ❓ (chưa đọc toàn văn).
- **Xuất dữ liệu:** ❓
- **Chứng nhận:** ❓ (sản phẩm chủ yếu cho lâm sàng/công nghiệp).
- **Giá:** ❓
- **Hạn chế:** hiện còn bán hay không ❓.

**B4. 3M SpotOn / Bair Hugger (zero-heat-flux)**
- **Tín hiệu, vị trí:** ZHF có bộ gia nhiệt; dán ở trán, có dây.
- **Sai số so với chuẩn:** Daanen 2023 [ĐL]: khi nghỉ không khác Tre; **sai số lớn cuối buổi tập**.
- **Xuất dữ liệu:** máy theo dõi lâm sàng.
- **Chứng nhận:** thiết bị y tế (FDA, CE) ❓ (cần số hồ sơ).
- **Giá:** ❓
- **Hạn chế:** có dây, tốn điện. Thiết kế cho phòng mổ, **không dùng được khi chạy bộ**.

**B5. Cosinuss° One / c-med° alpha (Cosinuss, Đức)**
- **Tín hiệu, vị trí:** nhiệt độ ống tai + HR (PPG); đeo trong tai.
- **Tần số mẫu:** ❓
- **Sai số so với chuẩn:**
  - Ellebrecht 2022 [ĐL]: phẫu thuật, LoA −0,79 / +0,49 °C so với nhiệt độ bàng quang.
  - Roossien 2019 [ĐL]: lính cứu hoả. **Không hợp lệ khi làm việc**, ICC ≤ 0,38, LoA ≥ 1,71 °C.
- **Xuất dữ liệu:** BLE; có SDK ❓.
- **Chứng nhận:** c-med° alpha là thiết bị y tế CE ❓.
- **Giá:** ❓
- **Hạn chế:** bị ảnh hưởng bởi gió, mồ hôi và cách đeo.

**B6. Miếng dán dual-heat-flux ở ngực (Nhật, JNIOSH)**
- **Tín hiệu, vị trí:** dual-heat-flux; dán ở ngực trên.
- **Sai số so với chuẩn:** Tokizawa 2022 [ĐL]. Khi đi bộ ở 35 °C, RMSE 0,18–0,25 °C so với nhiệt độ thực quản và 0,31–0,34 °C so với Tre.
- **Xuất dữ liệu, chứng nhận, giá:** ❓
- **Hạn chế:** chưa xác định tên thương mại; có thể vẫn ở dạng nghiên cứu ❓.

**B7. Tai nghe nhét tai (earbud) + ML (Nhật)**
- **Tín hiệu, vị trí:** 2 thermistor (tai và môi trường) + IR, kết hợp ML; đeo trong tai.
- **Sai số so với chuẩn:** Fujii 2026 [ĐL?]: bias −0,003 °C, LoA ±0,52 °C, RMSE 0,26 °C, chỉ ở cường độ nhẹ.
- **Hạn chế:** **chỉ nghiên cứu**; tên sản phẩm ❓.

**B8. Hệ heat flux Medisim**
- **Tín hiệu:** heat flux; vị trí đeo ❓.
- **Sai số so với chuẩn:** Daanen 2023 [ĐL]: thấp hơn Tre khi nghỉ, cao hơn Tre khi gắng sức tối đa (38,8 so với 38,4 °C).
- **Hạn chế:** tên sản phẩm và tình trạng ❓.

### 2C. Lớp C — Ước tính từ HR/Kalman & ML đa cảm biến

**C0. Thuật toán ECTemp (USARIEM; Buller 2013), là "lõi" của C1–C2**
- **Bản chất:** thuật toán, không phải thiết bị. Đầu vào là chuỗi HR theo phút, lọc Kalman.
- **Sai số so với chuẩn:**
  - Buller 2013: n = 83 kiểm định, hơn 52.000 điểm. Bias −0,03 ± 0,32 °C, LoA ±0,63 °C [nhà phát triển, quân đội].
  - de Korte 2022 [ĐL]: **101 VĐV ưu tú, 31,6 °C/74% RH**. Bias 0,15 ± 0,29 °C, LoA ±0,45 °C, RMSE 0,35 °C. Ở ngưỡng 37,75–38,75 °C: độ nhạy 73–96%, độ đặc hiệu 72–93%. **Khi Tc > 39 °C, độ nhạy chỉ 0–50%.**
  - Peggen 2024 [ĐL]: đi bộ đường dài, n = 18. Bias 0,09 °C, LoA ±0,44 °C nhưng r = 0,28; chỉ 17% người có bias cá nhân < 0,1 °C.
  - Hunt 2019 [ĐL]: mặc đồ chống bom (EOD). Bias 0,01 °C, LoA ±0,64 °C, RMSE 0,32 °C.
  - Egbert 2022 [ĐL]: nông dân. Bias −0,14 °C, LoA ±0,76 °C.
  - Pearson 2021 [ĐL]: 44 lính cứu hoả. CCC 0,74, **kém**, đặc biệt ở Tc cao.
  - Buller 2022 (BJSM): kết hợp ECTemp với mất ổn định dáng đi (gait instability, đo bằng gia tốc kế). Phát hiện được **6/6 ca EHS** sớm ít nhất 3,5 phút; dương tính giả 6,1%.
- **Xuất dữ liệu:** phương trình đã công bố, có thể tự cài đặt.
- **Chứng nhận:** không áp dụng (thuật toán). Được cấp phép không độc quyền cho Zephyr.
- **Hạn chế:** cần giá trị Tc khởi đầu. Sai lệch cá nhân lớn; bị nhiễu khi HR tăng vì lý do khác (thuốc, lo âu, mất nước).

**C1. Equivital EQ02+ LifeMonitor (Hidalgo/Equivital, Anh)**
- **Tín hiệu, vị trí:** ECG/HR, nhịp thở, gia tốc, nhiệt độ da IR ở nách (mỗi 15 s); nhận được dữ liệu viên nang. Đeo bằng đai ngực.
- **Sai số so với chuẩn:**
  - Agostinelli 2023 [ĐL]: cứu hoả mô phỏng ở 40,6 °C. Tương đương thống kê với Tre nhưng **đánh giá cao** khoảng 0,1 °C.
  - Stevenson 2026 [ĐL]: **tốt nhất khi vận động** trong 4 thiết bị, nhưng LoA vẫn rộng.
- **Xuất dữ liệu:** SDK/API của hãng; dùng nhiều trong nghiên cứu quân sự ❓ (chi tiết SDK chưa kiểm chứng).
- **Chứng nhận:** CE y tế ❓
- **Giá:** B2B ❓
- **Hạn chế:** đai ngực gây khó chịu khi chạy đường dài; giá cao.

**C2. Zephyr BioHarness 3 + OmniSense (Medtronic)**
- **Tín hiệu, vị trí:** ECG/HR, nhịp thở, tư thế, gia tốc; tính ECT (ECTemp) mỗi phút. Đeo bằng đai ngực.
- **Sai số so với chuẩn:**
  - Hagen 2020 [ĐL]: bóng bầu dục Mỹ NCAA. CCC 0,643; 78% điểm lệch trong ±1 °F (≈ ±0,56 °C).
  - Hintz 2023 [ĐL]: 1.364 học viên quân sự. Ngưỡng ECT > 39,7 °C cho **độ nhạy 20%** (2/10 ca EHS), độ đặc hiệu 98,9%.
  - Stevenson 2026 [ĐL]: LoA rộng.
- **Xuất dữ liệu:** OmniSense (theo dõi đội nhóm thời gian thực); có SDK ❓.
- **Chứng nhận:** FDA 510(k) cho BioHarness ❓ (cần số hồ sơ).
- **Giá:** B2B ❓
- **Hạn chế:** trang web còn quảng bá, nhưng tình trạng 2025–2026 ❓.

**C3. Kenzen (Mỹ)**
- **Tín hiệu, vị trí:** HR, nhiệt độ da, nhiệt độ môi trường, gia tốc + nhân trắc; mô hình ML/EKF. Đeo ở bắp tay.
- **Sai số so với chuẩn:**
  - Moyen 2021 [H]: tác giả chính là người của Kenzen. n = 27, 52 lượt đo; MAE 0,25 °C, RMSE 0,30 °C, bias 0,07 °C.
  - Stevenson 2026 [ĐL]: CCC thấp; **độ lặp lại thấp hơn** khi đeo ở tay.
- **Xuất dữ liệu:** cloud + dashboard cho người giám sát; tính phí thuê bao theo người/tháng. Có API ❓.
- **Chứng nhận:** wellness / an toàn lao động ❓
- **Giá:** thuê bao, không công bố.
- **Hạn chế:** hướng tới an toàn lao động. Tin tức mới nhất tìm được là 2021–2022; tình trạng 2025–2026 ❓.

**C4. SlateSafety BAND V2 (Mỹ)**
- **Tín hiệu, vị trí:** HR, mức gắng sức, "core temperature" ước tính; đeo ở bắp tay.
- **Sai số so với chuẩn:** Callihan 2024 [ĐL]: tổ bay cấp cứu (HEMS), n = 9. Thiết bị **đọc cao hơn 0,48 °C**, RMSE 0,65 °C, r = 0,26.
- **Xuất dữ liệu:** portal thuê bao hằng năm; có Beacon/gateway.
- **Chứng nhận:** ❓
- **Giá:** khoảng 805 (đơn vị tiền tệ không ghi rõ) mỗi thiết bị + phí portal.
- **Hạn chế:** tương quan với chuẩn yếu.

**C5. Hexoskin Smart Shirt (Canada)**
- **Tín hiệu, vị trí:** ECG/HR, nhịp thở, thông khí, gia tốc; dạng áo.
- **Sai số so với chuẩn:** đã kiểm định HR và nhịp thở. **Không tìm thấy kiểm định ước tính Tc.**
- **Xuất dữ liệu:** API hoặc nền tảng dữ liệu ❓ (thường được biết đến là có, nhưng chưa kiểm chứng trong phiên này).
- **Chứng nhận, giá:** ❓
- **Hạn chế:** chỉ là **nguồn HR thô** cho thuật toán; bản thân không ước tính Tc.

### 2D. Lớp D — Chỉ báo gián tiếp (đồng hồ, nhẫn, mồ hôi)

**D1. Garmin (Forerunner, Fenix…) + đai HRM**
- **Tín hiệu:** HR (quang học/đai), nhiệt độ da ban đêm ở một số dòng, "heat acclimation" (thích nghi nhiệt).
- **Liên quan Tc:** ❌ không ước tính Tc. Cách tính heat acclimation không được công bố.
- **Xuất dữ liệu:** file FIT; Connect IQ; Garmin Health API (B2B); ANT+/BLE broadcast HR.
- **Hạn chế:** nguồn **HR tốt** cho thuật toán ECTemp tự xây.

**D2. Apple Watch (Series 8 trở lên / Ultra)**
- **Tín hiệu:** nhiệt độ cổ tay khi ngủ (dạng độ lệch so với nền), HR.
- **Liên quan Tc:** ❌. Hãng nêu rõ tính năng không dùng cho mục đích y tế. Không tìm thấy kiểm định khi vận động.
- **Xuất dữ liệu:** HealthKit (HR theo giây trong buổi tập).
- **Hạn chế:** chỉ đo khi ngủ.

**D3. Samsung Galaxy Watch 5 trở lên**
- **Tín hiệu:** nhiệt độ da cổ tay (IR) khi ngủ.
- **Liên quan Tc:** ❌. Kim 2026 [H, Samsung Medical Center]: tương quan vừa với nhiệt độ miệng, r ≈ 0,42–0,45, trong bối cảnh dự đoán rụng trứng.
- **Xuất dữ liệu:** Samsung Health SDK ❓

**D4. Oura Ring**
- **Tín hiệu:** độ lệch nhiệt độ da ngón tay ban đêm, HR, HRV.
- **Liên quan Tc:** ❌. Hãng tự báo cáo khớp với iButton > 99% trong phòng thí nghiệm [H]. Một abstract hội nghị quân y cho thấy tương quan Oura–Garmin yếu (r = 0,26) ❓.
- **Xuất dữ liệu:** Oura API v2 ❓
- **Hạn chế:** chỉ đo khi ngủ.

**D5. Whoop 4.0 / 5.0**
- **Tín hiệu:** nhiệt độ da ban đêm, HR, HRV.
- **Liên quan Tc:** ❌. Không tìm thấy kiểm định nhiệt độ da.
- **Xuất dữ liệu:** Whoop Developer API ❓
- **Hạn chế:** dùng thuê bao.

**D6. Polar H10 / Verity Sense (đai HR)**
- **Tín hiệu:** HR/RR-interval (ECG ngực).
- **Liên quan Tc:** ❌ (chỉ là đầu vào).
- **Xuất dữ liệu:** BLE chuẩn; Polar SDK; AccessLink API ❓
- **Hạn chế:** **đầu vào HR chất lượng cao, giá thấp**.

**D7. Gx Sweat Patch (Epicore Biosystems / Gatorade)**
- **Tín hiệu:** tốc độ mồ hôi và Cl⁻ đo bằng vi lưu so màu; Na⁺ được **suy ra** từ Cl⁻.
- **Liên quan Tc:** ❌ Tc. Dùng cho **mất dịch và natri**, liên quan hạ natri máu.
- **Sai số:**
  - Baker 2020, Sci Adv [H, đồng tác giả GSSI/Epicore]: n = 312 VĐV. MAE dự đoán tốc độ mồ hôi toàn thân 0,13 L/h (14%); MAE Cl⁻ 5 mmol/L (13%).
  - Nghiên cứu npj Digit Med 2025, n = 22 ❓.
- **Xuất dữ liệu:** app Gx; quét ảnh miếng dán.
- **Hạn chế:** dùng một lần; không cho dữ liệu thời gian thực liên tục.

**D8. Nix Hydration Biosensor (Mỹ)**
- **Tín hiệu:** mất dịch và điện giải theo giờ.
- **Liên quan Tc:** ❌
- **Sai số:** ❓ (không tìm thấy kiểm định độc lập).
- **Xuất dữ liệu:** app; Nix Pro cho đội nhóm (2024).
- **Giá:** 129 USD; gói 4 miếng dán thay thế 25 USD.
- **Hạn chế:** tình trạng 2025 ❓.

**D9. hDrop (tái sử dụng)**
- **Tín hiệu:** mồ hôi / điện giải.
- **Liên quan Tc:** ❌
- **Sai số:** ❓
- **Hạn chế:** tình trạng thương mại ❓.

### 2E. Lớp E — Phần mềm, nền tảng, môi trường

**E1. Kestrel 5400 Heat Stress Tracker + LiNK**
- **Chức năng:** đo WBGT và TWL; cảnh báo theo ngưỡng; tablet treo tường; Ambient Weather Network.
- **Đầu vào sinh lý:** không có (chỉ đo môi trường).
- **Xuất dữ liệu:** app LiNK (log, báo cáo).
- **Ghi chú:** dùng làm **tầng môi trường** của hệ cảnh báo. Một nhà phân phối báo đã ngừng bán, trong khi trang hãng vẫn còn bán ❓.

**E2. OSHA-NIOSH Heat Safety Tool (app)**
- **Chức năng:** chỉ số nhiệt (heat index) theo vị trí → mức nguy cơ (theo hiểu biết chung, ❓ chưa kiểm chứng phiên này).
- **Đầu vào sinh lý:** không có.
- **Ghi chú:** ❓ cần xác minh tình trạng.

**E3. Zephyr OmniSense**
- **Chức năng:** dashboard đội nhóm thời gian thực, ECT.
- **Đầu vào sinh lý:** từ BioHarness.
- **Ghi chú:** B2B.

**E4. Kenzen cloud / SlateSafety portal**
- **Chức năng:** dashboard cho người giám sát, cảnh báo, báo cáo tuân thủ.
- **Đầu vào sinh lý:** từ thiết bị đeo tay của hãng.
- **Ghi chú:** hướng lao động, không phải thể thao.

**E5. CORE app + Garmin Connect IQ**
- **Chức năng:** hiển thị Tc ước tính trên đồng hồ; ghi chỉ số heat strain vào file FIT.
- **Đầu vào sinh lý:** CORE + HR.
- **Ghi chú:** cá nhân; **không có dashboard đội nhóm dạng y tế** ❓.

---

## 3. Trạng thái thị trường — SƠ BỘ (market-analyst làm sâu)

| Sản phẩm | Trạng thái | Kênh / giá | Giấy phép (sơ bộ) |
|---|---|---|---|
| e-Celsius | 🟢 | B2B/nghiên cứu; ~40–60 €/viên (2017) | CE IIb; FDA (theo hãng, 2023) ❓ |
| CorTemp | 🟢 ❓ | B2B; ~46 USD/viên ❓ | FDA 510(k) K880639 (theo hãng) ❓ |
| myTemp | 🟡 ❓ | ❓ | ❓ |
| VitalSense | 🔴 ❓ | — | — |
| CORE 2 | 🟢 | Bán lẻ toàn cầu, ~243 € – 359 USD | wellness ❓ |
| Calera Research | 🟢 ❓ | Nghiên cứu | ❓ |
| Dräger Tcore | 🟡 ❓ | Công nghiệp/lâm sàng | ❓ |
| 3M SpotOn | 🟢 (lâm sàng) | Bệnh viện | Y tế ❓ |
| Cosinuss | 🟢 ❓ | Bán lẻ/B2B | c-med° alpha: CE y tế ❓ |
| Equivital EQ02+ | 🟢/🟡 | B2B, quân đội | ❓ |
| Zephyr BioHarness | 🟢 ❓ | B2B (Medtronic) | ❓ |
| Kenzen | 🟡 ❓ (chưa có tin 2025–26) | Thuê bao/người/tháng | ❓ |
| SlateSafety BAND V2 | 🟢 | Qua SKC/Levitt; + portal | ❓ |
| Hexoskin | 🟢 ❓ | Bán lẻ/nghiên cứu | ❓ |
| Garmin / Apple / Samsung / Oura / Whoop / Polar | 🟢 | Bán lẻ, có ở VN (theo hiểu biết chung, ❓ cần xác minh từng hãng) | wellness (Apple: tính năng nhiệt độ không dùng cho y tế) |
| Gx Sweat Patch | 🟢 | Bán lẻ (Mỹ) ❓ | wellness |
| Nix | 🟢 ❓ | 129 USD | wellness |
| hDrop | ❓ | ❓ | ❓ |
| Kestrel 5400 | 🟢 (một nhà phân phối báo ngừng) ❓ | Bán lẻ | — |
| Earbud ML, miếng dán dual-heat-flux Nhật, thermal-guiding sensor (Du 2026, Nat Commun) | ⚪ | — | — |

**Việt Nam:** chưa khảo sát (giao `market-analyst`). Gợi ý cần kiểm tra:
- nhà phân phối chính hãng của Garmin, Apple, Samsung, Polar (nhiều khả năng có);
- CORE (nhiều khả năng phải mua quốc tế);
- viên nang (phải nhập khẩu, có thể cần phân loại trang thiết bị y tế theo NĐ 98/2021);
- dữ liệu sức khoẻ thuộc phạm vi Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 + NĐ 356/2025/NĐ-CP (hiệu lực 01/01/2026; dữ liệu sức khoẻ là dữ liệu nhạy cảm).

**Sáng chế (gặp ngẫu nhiên, chưa tra cứu hệ thống):**
- US 12426839 "Method for estimating core body temperature": dùng HR từ EQ02. Chủ sở hữu và hiệu lực ❓.
- US 8930147 "Multi-sensor patch and system" ❓.
- US 8511892 "Device for measuring the body core temperature" (dòng Dräger?) ❓.
- ECTemp được USARIEM cấp phép không độc quyền cho Zephyr (army.mil).

**Ma trận khoảng trống (sơ bộ):**

| Chức năng | CORE 2 | ECTemp (Equivital/Zephyr) | Kenzen/Slate | Đồng hồ tiêu dùng | Viên nang |
|---|---|---|---|---|---|
| Đo Tc trực tiếp | không | không | không | không | **có** |
| Ước tính Tc không xâm lấn | có (sai số không đều) | có (kém ở > 39 °C) | có (kém) | không | — |
| Cảnh báo thời gian thực | một phần (cá nhân) | có | có | không | một phần |
| Dashboard ban y tế cho giải đông người | không ❓ | một phần (OmniSense, B2B) | có (hướng lao động) | không | không |
| Gắn phác đồ can thiệp EHS / hạ natri máu | không | không | một phần | không | không |
| Hiệu chỉnh cho VĐV Việt Nam / khí hậu nóng ẩm | không | không (de Korte có dữ liệu nóng ẩm 74% RH) | không | không | — |
| Tiếng Việt | không | không | không | một phần | không |
| Giá phù hợp quy mô marathon | trung bình (~250 USD/người) | cao | thuê bao | sẵn có (VĐV tự mang) | cao, dùng một lần |

→ **Khoảng trống sơ bộ:** chưa có giải pháp nào gom đủ chuỗi **HR từ thiết bị VĐV tự mang + WBGT tại chỗ + ước tính Tc + gait/hành vi → cảnh báo nhiều tầng → phác đồ can thiệp cho ban y tế giải**, được hiệu chỉnh cho bối cảnh nóng ẩm Việt Nam và có tiếng Việt. Cần `market-analyst` xác minh.

---

## 4. Ý nghĩa cho thuật toán (gửi `algorithm-engineer`)

- **Đầu vào khả thi nhất ở quy mô giải chạy:** HR theo giây/phút từ đồng hồ hoặc đai ngực của VĐV (BLE/ANT+, file FIT, HealthKit, Garmin/Polar API), kết hợp WBGT tại trạm (Kestrel). Từ đó chạy ECTemp (Buller 2013, phương trình công bố) hoặc EKF cải tiến:
  - Rizvi 2022: tách mô hình vận động và hồi phục; RMSE 0,09–0,16 °C, nhưng dữ liệu của chính nhóm tác giả.
  - Aslani 2026: pre-emptive mapping HR; RMSE 0,34 °C, n = 18.
- **Không nên chỉ dựa vào ngưỡng Tc ước tính > 39,5 °C:** độ nhạy ở vùng này rất thấp (de Korte 2022; Hintz 2023). Nên bổ sung **gait instability** (Buller 2022), xu hướng HR, WBGT và quan sát lâm sàng.
- **Dữ liệu hiệu chỉnh:** cần một nghiên cứu nhỏ có viên nang e-Celsius/CorTemp trên VĐV Việt Nam trong điều kiện nóng ẩm để hiệu chỉnh hoặc kiểm định.

---

## 5. Danh sách nguồn (truy cập 2026-10-24)

### Peer-review (theo PubMed)
1. Bongers CCWG et al. Validity, reliability, and inertia of four different temperature capsule systems. *Med Sci Sports Exerc* 2018. PMID 28816921. https://doi.org/10.1249/MSS.0000000000001403
2. Pancrate T et al. Validity and reliability of the CorTemp telemetric pill during 50 h of reuse. *J Therm Biol* 2020. PMID 33077148. https://doi.org/10.1016/j.jtherbio.2020.102737
3. Verdel N et al. Reliability and validity of the CORE sensor to assess core body temperature during cycling exercise. *Sensors* 2021;21(17):5932. PMID 34502822. https://doi.org/10.3390/s21175932
4. Daanen HAM et al. Heat flux systems for body core temperature assessment during exercise. *J Therm Biol* 2023. PMID 36796923. https://doi.org/10.1016/j.jtherbio.2023.103480
5. Januário WM et al. Validity and reproducibility of the CALERA Research Sensor… cycling exercise in the heat. *J Therm Biol* 2024. PMID 38950497. https://doi.org/10.1016/j.jtherbio.2024.103907
6. Priego-Quesada JI et al. Effect of aerobic fitness on the validity of the Calera Research sensor. *J Therm Biol* 2025. PMID 39923389. https://doi.org/10.1016/j.jtherbio.2025.104067
7. Sanchez-Jimenez JL et al. Validity of CaleraSensor… arm crank exercise in individuals with SCI. *Top Spinal Cord Inj Rehabil* 2026. PMID 42583328. https://doi.org/10.46292/sci25-00072
8. Goulet EDB et al. Validity of the CORE wearable sensor during internal cooling induced by hyperhydration with cold water at rest. *Sensors* 2026. PMID 42655352. https://doi.org/10.3390/s26165042
9. Xie et al. Performance of a wearable CORE sensor for nocturnal core temperature monitoring during sleep. *J Therm Biol* 2026. PMID 42086019. https://doi.org/10.1016/j.jtherbio.2026.104477
10. Hu et al. Feasibility of a noninvasive core temperature sensor… beach volleyball. *IJSPP* 2026. PMID 42061827. https://doi.org/10.1123/ijspp.2025-0588
11. Kubota et al. Circadian phase assessment of CBT using a wearable temperature sensor (CALERA). *Sleep Sci* 2025. PMID 40964223. https://doi.org/10.1055/s-0044-1800785
12. **Stevenson RD et al. Validity and reliability of wearable heat stress monitors in firefighters during exercise-induced hyperthermia. *Med Sci Sports Exerc* 2026. PMID 42613781.** https://doi.org/10.1249/MSS.0000000000004113
13. Buller MJ et al. Estimation of human core temperature from sequential heart rate observations. *Physiol Meas* 2013;34:781. PMID 23780514. https://doi.org/10.1088/0967-3334/34/7/781
14. Buller MJ et al. Gait instability and estimated core temperature predict exertional heat stroke. *Br J Sports Med* 2022. PMID 35022161. https://doi.org/10.1136/bjsports-2021-104081
15. de Korte JQ et al. A heart rate based algorithm to estimate core temperature responses in elite athletes exercising in the heat. *Front Sports Act Living* 2022. PMID 35813051. https://doi.org/10.3389/fspor.2022.882254
16. Peggen et al. Validity of the ECTemp algorithm during real-world prolonged walking. *J Therm Biol* 2024. PMID 39383600. https://doi.org/10.1016/j.jtherbio.2024.103982
17. Hunt AP et al. Validity of a noninvasive estimation of deep body temperature when wearing PPE. *Mil Med Res* 2019. PMID 31196190. https://doi.org/10.1186/s40779-019-0208-7
18. Egbert et al. Accuracy of an estimated core temperature algorithm for agricultural workers. *Arch Environ Occup Health* 2022. PMID 35114899. https://doi.org/10.1080/19338244.2022.2033672
19. Pearson et al. Comparisons of core temperature between a telemetric pill and HR-estimated core temperature in firefighters. *Saf Health Work* 2021. PMID 35936211. https://doi.org/10.1016/j.shaw.2021.11.003
20. Agostinelli et al. Validity of heart rate derived core temperature estimation during simulated firefighting tasks (EQ02+). *Sci Rep* 2023. PMID 38110650. https://doi.org/10.1038/s41598-023-49929-x
21. Hintz et al. Heat stroke burden and validity of wearable-derived core temperature estimation during elite military training (Zephyr). *Phys Sportsmed* 2023. PMID 36919415. https://doi.org/10.1080/00913847.2023.2190729
22. Hagen J et al. Test and evaluation of HR derived core temperature algorithms for NCAA Division I football athletes. *J Funct Morphol Kinesiol* 2020. PMID 33467262. https://doi.org/10.3390/jfmk5030046
23. Moyen NE et al. Accuracy of algorithm to non-invasively predict core body temperature using the Kenzen wearable device. *IJERPH* 2021. PMID 34948736. https://doi.org/10.3390/ijerph182413126 [H]
24. Callihan et al. Reliability of wearable technology to monitor core temperature among helicopter-based EMS crews (SlateSafety). *Workplace Health Saf* 2024. PMID 39221564. https://doi.org/10.1177/21650799241271139
25. Rizvi et al. A modified Kalman filter-based model for core temperature estimation… *J Therm Biol* 2022. PMID 36195382. https://doi.org/10.1016/j.jtherbio.2022.103307
26. Aslani et al. A novel method for real-time human core temperature estimation based on EKF. *IEEE JBHI* 2026. PMID 41489953. https://doi.org/10.1109/JBHI.2025.3650475
27. Tokizawa K et al. Validity of a wearable core temperature estimation system in heat using patch-type sensors on the chest. *J Therm Biol* 2022. PMID 36031215. https://doi.org/10.1016/j.jtherbio.2022.103294
28. Fujii et al. Core temperature estimation using wearable earbud-type thermometer and machine learning. *Scand J Med Sci Sports* 2026. PMID 42257542. https://doi.org/10.1111/sms.70315
29. Ellebrecht DB et al. Evaluation of a wearable in-ear sensor for temperature and HR monitoring (Cosinuss). *J Med Syst* 2022. PMID 36329338. https://doi.org/10.1007/s10916-022-01872-6
30. Roossien CC et al. Monitoring core temperature of firefighters to validate a wearable non-invasive core thermometer (Cosinuss°). *Appl Ergon* 2019. PMID 31739139. https://doi.org/10.1016/j.apergo.2019.103001
31. Park et al. Wired zero-heat-flux sensor vs wireless thermistor patch vs esophageal probe. *Sci Rep* 2026. PMID 42049813. https://doi.org/10.1038/s41598-026-48235-6
32. Du Y et al. Skin-interfaced thermal guiding sensor… core body temperature. *Nat Commun* 2026. PMID 42760284. https://doi.org/10.1038/s41467-026-77154-3
33. Żmigrodzki et al. Analytical analysis of factors affecting the accuracy of a dual-heat flux CBT sensor. *Sensors* 2024. PMID 38544149. https://doi.org/10.3390/s24061887
34. Kim SE et al. Accuracy of wrist skin temperature (Galaxy Watch 5) for ovulation prediction. *Biosens Bioelectron* 2026. PMID 42143892. https://doi.org/10.1016/j.bios.2026.118755
35. Baker LB et al. Skin-interfaced microfluidic system with personalized sweating rate and sweat chloride analytics for sports science applications. *Sci Adv* 2020;6:eabe3929. https://doi.org/10.1126/sciadv.abe3929 (PMID ❓; số liệu lấy qua tóm tắt của GSSI) [H]

### Web (thông tin sản phẩm / thị trường; phần lớn là nguồn hãng hoặc báo thương mại)
- CORE 2, giá: https://gadgetsandwearables.com/2025/01/03/core-2-body-temperature-sensor/ ; https://www.notebookcheck.net/CORE-2-Wearable-takes-training-and-performance-monitoring-to-the-next-level.940966.0.html ; https://www.bike-components.de/en/greenTEG/CORE-2-Temperature-Sensor-p215882/ ; https://corebodytemp.com/blogs/news/coming-march-2025-core-2
- BodyCap e-Celsius CE/FDA: https://healthcare-in-europe.com/en/news/bodycap-receives-medical-ce-mark-for-ingestible-connected-device.html ; https://mma.prnewswire.com/media/2238451/Full_Press_Release.pdf
- CorTemp: https://buyersguide.ohsonline.com/company/297786/products/26215/cortemp-ingestible-core-body-temperature-monitoring-system ; https://accessgudid.nlm.nih.gov/devices/00857414006018
- myTemp: https://www.radboudumc.nl/en/research/technology-centers/human-performance-lab
- Equivital: https://equivital.com/equivital-eq02-lifemonitor-leading-the-way-in-real-time-safety
- Zephyr / ECTemp: https://www.zephyranywhere.com/ ; https://www.army.mil/article/186577/
- Kenzen: https://www.tdworld.com/electric-utility-operations/article/21131444/kenzen-launches-body-heat-sensor-system-for-worker-safety ; https://www.startlandnews.com/2021/01/kenzen-examinetics
- SlateSafety: https://skcinc.com/products/band-v2 ; https://www.levitt-safety.com/Marques/Slate-Safety/Catalogue/Fast-Track/Heat-Stress
- Gx Sweat Patch: https://www.gssiweb.org/docs/default-source/educational-materials/research-infographics/gx-infographic---final.pdf ; https://rogersgroup.northwestern.edu/files/2020/sciadvgssi.pdf
- Nix: https://newatlas.com/wearables/nix-hydration-biosensor-sweat/ ; https://insider.fitt.co/?p=9804
- Oura (nguồn hãng): https://ouraring.com/blog/temperature-validated-accurate ; abstract Oura–Garmin: https://mhsrs.health.mil/MHSRS/download/downloadabstractfile/6712
- Kestrel 5400: https://kestrelmeters.com/products/kestrel-5400-heat-stress-tracker ; https://kestrelmeters.com/heat-stress-monitoring-system
- Dräger Double Sensor: https://clinicaltrials.gov/study/NCT02691832 ; https://extremephysiolmed.biomedcentral.com/articles/10.1186/2046-7648-4-S1-A28
- Sáng chế: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12426839 ; …/8930147 ; …/8511892

### Việc còn mở (❓) cho các agent sau
Kiểm chứng các mục sau:
- số hồ sơ FDA/CE của CORE, Zephyr, Equivital, Cosinuss;
- tình trạng 2025–2026 của Kenzen, VitalSense, myTemp, hDrop;
- API/SDK chính thức của Oura, Whoop, Hexoskin, Equivital;
- toàn văn nghiên cứu Tsadok (Dräger);
- PMID của Baker 2020;
- toàn bộ mục Việt Nam và sáng chế.
