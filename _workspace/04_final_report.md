# Theo dõi nhiệt độ lõi và cảnh báo say nắng gắng sức ở vận động viên: thiết bị, thị trường, phương trình và hệ thống can thiệp

*Báo cáo tổng hợp của harness `core-temp-research` · Ngày 24/10/2026*
*Người yêu cầu: PGS.TS. Trần Ngọc Đăng (ĐH Y Dược TP.HCM)*
*Nguồn chi tiết trong `_workspace/`:*
- `01_device-scout_devices.md` (thiết bị)
- `01_thermo-modeler_models.md` (phương trình)
- `01_clinical-advisor_clinical.md` (lâm sàng)
- `02_market-analyst_market.md` (thị trường)
- `02_algorithm-engineer_*` (prototype)
- `03_evidence-verifier_audit.md` (kiểm chứng)

> **Phạm vi và giới hạn.** Báo cáo là tổng quan nghiên cứu. Mã nguồn kèm theo là prototype nghiên cứu, **không phải thiết bị y tế**. Proxy của môi trường chặn truy cập trực tiếp website, nên phần thị trường, FDA, sáng chế và pháp luật dựa trên đoạn trích tìm kiếm cùng PubMed. 41/41 PMID đã được xác minh tồn tại và đúng metadata. Ký hiệu: ✅ đã kiểm chứng · ◐ nguồn thứ cấp · ❓ chưa kiểm chứng.

---

## 1. Tóm tắt điều hành

1. **Có thiết bị và phần mềm ước tính nhiệt độ lõi (Tc), nhưng chưa thiết bị nào đủ tin cậy để ra quyết định an toàn ở vùng nguy hiểm.**
   - So sánh độc lập bốn thiết bị Equivital, Kenzen, Zephyr và CORE **trên lính cứu hoả** khi tăng thân nhiệt do vận động cho 95 % LoA rộng 1,25–2,22 °C; sai số tăng khi Tc > 38,5 °C (Stevenson 2026, MSSE ✅). Đây là bằng chứng gián tiếp cho VĐV.
   - Thuật toán ước tính Tc từ nhịp tim (ECTemp) đạt yêu cầu ở mức nhóm, nhưng **bỏ sót gần hết vùng > 39,5 °C**. Độ nhạy chỉ 4 % ở VĐV ưu tú trong nóng ẩm (de Korte 2022 ✅) và 20–23 % với ca bệnh do nhiệt thật (Hintz 2023 ✅; Buller 2025 ✅).
2. **Đã có trên thị trường chưa? Từng thành phần thì đã có; giải pháp tích hợp cho ban y tế giải chạy thì chưa** (độ tin cậy trung bình). Các nhóm hiện có:
   - Cảm biến bán lẻ: CORE 2.
   - Viên nang chuẩn tham chiếu: e-Celsius (FDA K210924 ✅), CorTemp.
   - Nền tảng B2B cho người lao động: SlateSafety, Equivital, EVALAN ARMOR, Samsung SmartThings Pro Heat Stress (Hàn Quốc, 9/2025), Biodata Bank CANARIA+ (Nhật; dùng cho **nhân viên** tại World Athletics Tokyo 2025).
   - Chưa sản phẩm nào gộp đủ chuỗi **thiết bị VĐV tự mang + WBGT → ước tính nguy cơ → cảnh báo nhiều tầng → phác đồ can thiệp** cho EHS, hạ natri máu, tiêu cơ vân và sự cố tim, được hiệu chỉnh cho khí hậu nóng ẩm và có tiếng Việt.
3. **Phương trình:** ba họ chính.
   - ECTemp: bộ lọc Kalman từ HR (Buller 2013 ✅; bản sigmoid Looney 2018).
   - Cảm biến kép / dòng nhiệt: Tc = T1 + K·(T1 − T2) (Gunga 2008 ✅).
   - Chỉ số căng thẳng: PSI (Moran 1998 ✅) và aPSI có thêm nhiệt độ da (Buller 2023 ✅). aPSI phát hiện 86,7 % ca bệnh do nhiệt, so với 23,3 % của ECTemp (Buller 2025 ✅; công thức aPSI chi tiết ❓).
   - **Kết hợp nhiều tín hiệu** cho kết quả tốt hơn: HR, nhiệt độ da, dáng đi (ECTemp + dáng đi phát hiện 6/6 ca EHS, Buller 2022 ✅), WBGT và quan sát của con người.
4. **Lâm sàng.** Chẩn đoán EHS cần **nhiệt độ trực tràng (Tre) ≥ 40,5 °C kèm rối loạn thần kinh trung ương (TKTW)** (IOC 2021 ✅).
   - Thiết bị đeo chỉ dùng để **sàng lọc**: tối đa đưa tới "yêu cầu đánh giá y tế" (mức 3), không được tự kết luận EHS.
   - Can thiệp: **làm mát trước, vận chuyển sau** bằng ngâm nước lạnh 5–15 °C và ngừng ở Tre 39 °C (IOC ✅).
   - Phải loại trừ ngừng tim trước, và loại trừ hạ natri máu trước khi cho uống.
5. **Prototype:** đã dựng engine cảnh báo 5 mức, chạy thật trên 4 kịch bản mô phỏng.
   - Ở kịch bản EHS, engine lên mức 3 **sớm hơn 39 phút** so với chỉ dùng ECTemp.
   - Engine không bao giờ khuyên uống thêm ở kịch bản hạ natri máu.
   - Đổi lại, gánh nặng báo động cao khi WBGT ở cờ đỏ. Cần quyết định lâm sàng (mục 7.4).
6. **Đề xuất cho Việt Nam.** Đóng góp có giá trị nhất là **nghiên cứu hiệu chỉnh–kiểm định bằng viên nang nuốt trên VĐV Việt Nam ở điều kiện nóng ẩm**, đi kèm một hệ thống hỗ trợ quyết định cho ban y tế giải chạy. Hệ thống này nhận HR từ thiết bị VĐV tự mang qua BLE/ANT+, lưu dữ liệu trong nước, giao diện tiếng Việt.

---

## 2. Nền tảng sinh lý

- Tc tăng khi sinh nhiệt chuyển hoá vượt khả năng thải nhiệt. Trong khí hậu nóng ẩm, bay hơi mồ hôi kém nên Tc tăng nhanh hơn mức WBGT phản ánh (IOC 2022 ✅).
- **HR phản ánh Tc gián tiếp:** HR tăng theo Tc do giãn mạch da và giảm thể tích tâm thu. Nhưng HR bị chi phối bởi cường độ, mất nước, caffein, cảm xúc và thuốc chẹn beta, và **bão hoà ở gần HRmax**. Parabol của ECTemp đạt đỉnh ở khoảng 195 bpm / 42 °C ✅, nên ECTemp đánh giá thấp Tc ở vùng nguy hiểm.
- **Nhiệt độ da (Tsk)** và chênh lệch Tc − Tsk quyết định khả năng thải nhiệt. Đây là lý do aPSI dùng Tsk để điều chỉnh ngưỡng nguy hiểm.
- **Thực địa gần Việt Nam nhất:** 162 người chạy phong trào ở Singapore (27,2 °C, RH 87 %) có Tc đỉnh 39,4 ± 0,6 °C, tối đa 41,1 °C (Sakamoto 2026 ✅). Như vậy Tc > 39 °C là **phổ biến** ở người chạy khoẻ mạnh, và một ngưỡng Tc đơn lẻ có độ đặc hiệu thấp.

---

## 3. Thiết bị và phần mềm

| Lớp | Đại diện | Độ chính xác so với chuẩn | Nhận định |
|---|---|---|---|
| **A. Đo trực tiếp (chuẩn tham chiếu)** | Viên nang e-Celsius, CorTemp, myTemp; Tre | Viên nang: sai số < 0,1 °C trong bể nước (Bongers 2018) | Chuẩn cho nghiên cứu hiệu chỉnh. Không thực tế cho hàng nghìn người |
| **B. Dòng nhiệt / cảm biến kép** | CORE 2 / CALERA (greenteg), cosinuss c-med alpha (tai, CE MDR IIa), Dräger Tcore (đã ngừng) | Không nhất quán: Januário 2024 bias 0,01 °C (đạt); Verdel 2021 ~50 % cặp lệch > 0,3 °C; Goods 2023 41–60 % lệch > ±0,3 °C, **đánh giá thấp ở Tc cao**; Goulet 2026 không phát hiện được làm mát bên trong ✅ | Dùng làm **xu hướng** hoặc một đầu vào, không dùng làm Tc tuyệt đối |
| **C. HR → Kalman / ML** | ECTemp (Equivital, Zephyr, EVALAN), Kenzen, SlateSafety, Samsung SmartThings Pro | ECTemp gốc: bias −0,03 ± 0,32 °C, LoA ±0,63 °C ✅. Ở vùng > 39 °C độ nhạy chỉ 4–48 % ✅. Các mô hình ML (RMSE gốc 0,09–0,30 °C) **kém đi 1,5–2 lần khi kiểm định ngoài** (Zhao 2026 ✅) | Tốt ở mức nhóm, yếu ở vùng nguy hiểm |
| **D. Chỉ báo gián tiếp** | Garmin, Apple Watch, Polar, Oura, Whoop; miếng dán mồ hôi Epicore/Gx, Nix | Không ước tính Tc | **Nguồn HR miễn phí** mà VĐV đã sẵn có |
| **E. Môi trường / phần mềm** | Kestrel 5400 (WBGT), OSHA-NIOSH app | — | Tầng môi trường cho ban tổ chức |

Lưu ý giấy phép: số 510(k) của Equivital (K113054) và Zephyr (K113045) là clearance cho **phần cứng theo dõi sinh lý/ECG**, không bao gồm chức năng ước tính Tc ✅.

---

## 4. Hiện trạng thị trường

### 4.1 Trạng thái sản phẩm (kiểm tra 24/10/2026)

| Trạng thái | Sản phẩm |
|---|---|
| 🟢 Đang bán | CORE 2 (≈ 270–290 CHF, **không phải thiết bị y tế**); CALERA Research (999 CHF); SlateSafety BAND V2 (kèm phí portal hằng năm cho mỗi thiết bị); cosinuss c-med alpha; Equivital (B2B; MoU với ST Engineering Singapore 11/2025); Hexoskin; Biodata Bank CANARIA+ (Nhật); Kestrel 5400; đồng hồ tiêu dùng |
| 🟢❓ Có thể đang bán (không có tin ≤ 12 tháng) | e-Celsius (FDA K210924 ✅, CE); CorTemp (FDA K880639 ✅) |
| 🟡 Thí điểm / B2B hẹp | Samsung SmartThings Pro Heat Stress (Hàn Quốc, ra 9/2025, nâng cấp 7/2026); EVALAN ARMOR (Hà Lan, quốc phòng); Zephyr BioHarness (không có tin 2025–2026) |
| 🔴 Ngừng bán | Dräger Tcore ("End of Sales" ✅) |
| 🔴❓ Có thể đã đóng cửa | Kenzen và Bodytrak. Chỉ PitchBook ghi "Out of Business", không có thông cáo chính thức |
| ⚪ Nghiên cứu / nguyên mẫu | HeatGuard (Thái Lan, 2026), miếng dán dòng nhiệt kép JNIOSH, tai nghe ML (Fujii 2026) |

### 4.2 Việt Nam
- **Kênh phân phối:**
  - Có kênh chính hãng: chỉ Garmin (FPT, Synnex FPT, Garmin Brand Store) và Polar (StreamCast Asia ❓).
  - Không tìm thấy kênh nào cho CORE, viên nang, Equivital, Zephyr, SlateSafety. Muốn dùng phải nhập khẩu, không có bảo hành.
- **Trang thiết bị y tế (TTBYT):**
  - Văn bản áp dụng: NĐ 98/2021/NĐ-CP, sửa đổi bởi NĐ 07/2023 và NĐ 04/2025 ✅; phân loại theo TT 05/2022/TT-BYT ◐.
  - Phần mềm tuyên bố "phát hiện, cảnh báo say nắng" nhiều khả năng là **TTBYT loại B–C** ❓. Định vị "công cụ hỗ trợ ban y tế" khác về pháp lý với "chẩn đoán". Cần ý kiến của Cục Cơ sở hạ tầng và Thiết bị y tế.
- **Dữ liệu sức khoẻ:**
  - Là dữ liệu cá nhân nhạy cảm theo **Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 + NĐ 356/2025/NĐ-CP** (hiệu lực 01/01/2026, thay NĐ 13/2023) ✅.
  - Hệ quả: cần sự đồng ý rõ ràng của VĐV và đánh giá tác động. Chuyển dữ liệu ra nước ngoài (cloud Garmin, Oura, SlateSafety…) cần cân nhắc, đây là **lợi thế cho giải pháp lưu trữ trong nước**.
- **Nhu cầu thực tế (theo báo chí, chưa có kết luận y khoa):**
  - Quảng Bình Marathon 7/2024: 2 ca sốc nhiệt kèm tiêu cơ vân và suy thận cấp.
  - Marathon Huế 4/2025: 4 người nhập viện, 1 tử vong.
  - Vietnam Ultra Marathon 3/2024: 1 tử vong.
  - **Không có công bố bình duyệt nào về EHS ở giải chạy Việt Nam** (PubMed, 24/10/2026). Đây là khoảng trống nghiên cứu.

### 4.3 Sáng chế (sàng lọc sơ bộ, không thay tư vấn sở hữu trí tuệ)
- **US 10,702,165 B2** (Quân đội Mỹ, ECTemp HR → Tc): còn hiệu lực, dự kiến hết hạn khoảng 2033 ✅.
- **US 12,426,839 B2** (bản ECTemp sigmoid): cấp 30/09/2025 ✅.
- **US 2021/0338173 A1 / EP 4144068** (dáng đi + Tc → dự báo EHS): mới là đơn đã công bố.
- **Chưa tra cơ sở dữ liệu Cục Sở hữu trí tuệ Việt Nam.** Sáng chế có tính lãnh thổ. Dùng các phương trình đã công bố cho nghiên cứu khoa học thường ít rủi ro; thương mại hoá, nhất là xuất khẩu sang Mỹ, cần xin license hoặc thiết kế khác đi.

### 4.4 Ma trận khoảng trống (rút gọn)

| Chức năng | Đã có ở sản phẩm nào | Khoảng trống |
|---|---|---|
| Ước tính Tc không xâm lấn | CORE, ECTemp, Samsung, SlateSafety | Kém ở > 39 °C; chưa hiệu chỉnh cho người Việt |
| Dashboard đội nhóm | Equivital, SlateSafety, Samsung, ARMOR | Hướng tới người lao động, không phải giải chạy |
| Quy mô hàng nghìn người | CANARIA+ (dùng một lần) | Chỉ dùng cho nhân viên |
| Nhận HR từ thiết bị **VĐV tự mang** | — | **Chưa có** |
| Gắn **phác đồ can thiệp** (EHS, hạ natri máu, tim, tiêu cơ vân) | — (chỉ có "nghỉ / uống nước") | **Chưa có** |
| Tiếng Việt, lưu trữ trong nước, giá thấp | — | **Chưa có** |

---

## 5. Phương trình và mô hình

### 5.1 ECTemp (Buller 2013, *Physiol Meas* 34:781; PMID 23780514)
```
Dự báo:   Tĉ = a·Tc(t−1);   v̂ = a²·v(t−1) + γ
Hệ số:    c = 2·b2·Tĉ + b1
Kalman:   k = v̂·c / (c²·v̂ + σ)
Cập nhật: Tc(t) = Tĉ + k·[HR(t) − (b2·Tĉ² + b1·Tĉ + b0)];   v(t) = (1 − k·c)·v̂
a = 1; γ = 0,022²; b0 = −7887,1; b1 = 384,4286; b2 = −4,5714; σ = 18,88²; Tc0 = 37,1 °C
v0 = 0 (khi Tc0 đo được) hoặc 0,01–0,02 (khi Tc0 giả định)
```
- Hệ số khớp giữa bản ResearchGate, sáng chế US10702165 và mã nguồn. Chưa đọc được bảng trong PDF gốc nên xếp ⚠️; nên đối chiếu qua thư viện ĐHYD.
- HR lấy mẫu mỗi phút. Kiểm định gốc: bias −0,03 ± 0,32 °C, LoA ±0,63 °C, n = 83 ✅.
- Bản hiện hành là **sigmoid** (Looney 2018: RMSE 0,26 so với 0,35 °C của bản bậc 2 ✅). Hệ số sigmoid chưa tìm được ❓.

### 5.2 Cảm biến kép / dòng nhiệt (Gunga 2008, *J Therm Biol* 33:297)
`Tc ≈ T1 + K·(T1 − T2)`, với K = R_mô / R_cảm biến, hiệu chỉnh theo vị trí đặt. Sản phẩm thương mại dùng thuật toán độc quyền.

### 5.3 PSI và aPSI
- **PSI** (Moran 1998, PMID 9688970 ✅): `PSI = 5·(Tc − Tc0)/(39,5 − Tc0) + 5·(HR − HR0)/(180 − HR0)`, thang 0–10.
- **aPSI** (Buller 2023, PMID 37703905): điều chỉnh ngưỡng Tc tới hạn theo chênh lệch Tc − Tsk. Trong 5080 tân binh, aPSI phát hiện 86,7 % ca bệnh do nhiệt, cảnh báo sớm khoảng 35 phút, dương tính giả khoảng 15 % (Buller 2025 ✅). **Công thức chi tiết chưa kiểm chứng** ❓; prototype dùng công thức theo đoạn trích sáng chế.

### 5.4 Mô hình đa biến và ML
- Kalman tuyến tính dùng Tsk + dòng nhiệt + HR: RMSE 0,18 °C (Welles 2018 ✅).
- Mô hình cá thể hoá tham số: RMSE 0,33 °C trên 166 người (Laxminarayan 2018).
- Học sâu kèm khoảng dự đoán hiệu chuẩn (conformal): sai số 0,29 °C trên hơn 140.000 phép đo (Strickland 2025).
- Cảnh báo EHS từ bất thường HR + gia tốc: báo sớm 33–69 phút, nhưng chỉ có 3 ca (Yaldiz 2023).
- Hạn chế chung: kiểm định ngoài thường kém hơn số trong bài gốc. Cần kiểm định chéo theo người và theo sự kiện.

### 5.5 Mô hình dự báo trước giải
SCENARIO, Heat Strain Decision Aid, ISO 7933 và JOS-3 dùng để chọn giờ xuất phát và bố trí nguồn lực. Với JOS-3, Oyama 2023 ✅ đề xuất ngưỡng WBGT marathon 24–27 °C thay cho 28 °C.

---

## 6. Ngưỡng cảnh báo → can thiệp

### 6.1 Thang 5 mức
| Mức | Kích hoạt (ví dụ) | Hành động | Ai, khi nào |
|---|---|---|---|
| 0 | — | Theo dõi nền | — |
| 1 Chú ý | eTc + bù ≥ 38,5 °C | VĐV tự giảm tốc, tạt nước làm mát, uống theo cảm giác khát | VĐV |
| 2 Cảnh báo | eTc + bù ≥ 39,0; PSI ≥ 7; tăng nhanh; WBGT đỏ (R7) | Giảm tốc rõ hoặc đi bộ; người quan sát tới đánh giá TKTW | Người quan sát, ≤ 5 phút |
| 3 Nguy cơ cao | eTc + bù ≥ 39,5; dáng đi mất ổn định; **bất kỳ dấu hiệu TKTW nào** | **Dừng chạy**; đưa tới khu xử trí nhiệt; đánh giá TKTW và đo Tre | Đội cơ động, ≤ 3–5 phút |
| 4 Cấp cứu | Tre ≥ 40,5 °C + TKTW (EHS); gục + bất động + mất HR (ngừng tim); TKTW + Na⁺ < 135 (hạ natri máu nặng) | Ngâm nước lạnh ngay / CPR + AED / NaCl 3 % | Toàn chuỗi cấp cứu |

**Quy tắc an toàn:**
- Thiết bị không bao giờ hạ mức do con người đặt (R1).
- Dấu hiệu TKTW luôn đưa lên tối thiểu mức 3 (R2).
- Tc ước tính tối đa mức 3 (R3; IOC 2022 ✅: *"too early to take individual decisions … based on portable technology alone"*).
- Nghi ngừng tim → mức 4 ngay (R4).
- Ngưỡng eTc hạ khoảng 0,5 °C để bù sai số (R5; Hunt 2019 ✅).

### 6.2 Phác đồ khu xử trí nhiệt (IOC 2021 ✅)
1. Loại trừ ngừng tim trước, sau đó đo Tre (đầu dò mềm, đưa vào ≥ 10 cm).
2. Tre ≥ 40,5 °C + TKTW → **ngâm toàn thân nước 5–15 °C**, khuấy liên tục. Cần 4 người mỗi bệnh nhân và 30–35 kg đá mỗi bồn. Mục tiêu hạ nhiệt trong 30 phút kể từ lúc gục.
3. **Ngừng làm mát ở Tre 39 °C** (IOC ✅), theo dõi ≥ 15 phút, ngâm lại nếu Tre tăng, giữ ấm nếu Tre tụt về 36 °C.
   - Các hướng dẫn khác: ACSM 38,6 °C ◐; NATA ≈ 38,9 °C ◐.
   - Lý do khác nhau: ngưỡng thấp hơn để bù quán tính nhiệt sau khi ra khỏi bồn. Cả hai cách chấp nhận được nếu theo dõi Tre liên tục.
4. Làm xét nghiệm Na⁺ và glucose tại chỗ. Mọi ca EHS phải chuyển viện **sau khi đã làm mát**.
5. Khi không có bồn: làm mát bằng bạt (TACO, 0,14–0,17 °C/phút ◐) hoặc khăn đá luân phiên. Túi đá đặt nách/bẹn **không đủ** để điều trị EHS.

### 6.3 Chẩn đoán phân biệt quyết định can thiệp
| Tình trạng | Manh mối | Xử trí khác biệt |
|---|---|---|
| Ngừng tim (0,54/100.000 người chạy; 71 % tử vong, Kim 2012 ✅) | Gục đột ngột, không thở bình thường | CPR + AED **trước** mọi xử trí nhiệt |
| Hạ natri máu do gắng sức (EAH) | Rối loạn TKTW với Tre bình thường hoặc tăng nhẹ; tăng cân trong giải; uống nhiều | **Không truyền dịch nhược trương, không cho uống**; NaCl 3 % (WMS 2019 ✅) |
| Hạ đường huyết | Đường huyết thấp | Glucose 50 % tĩnh mạch / glucagon |
| Tiêu cơ vân | CK ≥ 5 × ULN, nước tiểu sẫm | Bù dịch, chuyển viện nếu nguy cơ |
| Ngất sau về đích | Gục ngay sau vạch đích, tỉnh nhanh | Nằm, nâng chân |

### 6.4 Môi trường
- Cờ WBGT của ACSM ◐: xanh < 18 °C; vàng 18–23; đỏ 23–28; đen > 28 °C.
- IOC 2022 ✅ không đặt giới hạn chung. Khuyến nghị: đo WBGT tại chỗ ở độ cao 1,2–1,5 m và dựa trên ≥ 10 năm dữ liệu lịch sử để chọn giờ xuất phát.
- Thích nghi nhiệt: 60–90 phút/ngày, ≥ 2 tuần (IOC 2022 ✅).
- **Đề xuất cho Việt Nam** ❓: coi WBGT ≥ 26–27 °C là "đỏ đậm" để tăng nguồn lực y tế.

---

## 7. Prototype hệ thống cảnh báo

### 7.1 Kiến trúc
```
Thiết bị VĐV (dây ngực/đồng hồ: HR; tuỳ chọn Tsk, gia tốc)
   ──BLE/ANT+──► App điện thoại (engine chạy tại chỗ, hoạt động offline):
                  QC tín hiệu → clip HR → ECTemp → PSI/aPSI → quy tắc R1–R8 → cảnh báo tiếng Việt
   ──4G (~200 byte/phút)──► Dashboard ban y tế: danh sách theo mức, bản đồ GPS, "ai – làm gì – trong bao lâu",
                            panel khu xử trí nhiệt (tốc độ làm mát, ngưỡng ngừng 39 °C)
Trạm WBGT dọc đường ─┘    App người quan sát (báo TKTW, cân) ─┘    Khu y tế (nhập Tre, Na⁺, glucose) ─┘
```
Mã nguồn: `_workspace/02_algorithm-engineer_alert_engine.py` (Python thuần), cấu hình `02_algorithm-engineer_thresholds.json`, thư viện lõi `.claude/skills/core-temp-modeling/scripts/heatstrain.py`.

### 7.2 Kết quả mô phỏng (dữ liệu tổng hợp, chạy thật, có thể tái lập)
| Kịch bản | Engine | Chỉ dùng ECTemp (baseline) |
|---|---|---|
| S1 chạy bình thường, WBGT 26→28 | Không có mức 3/4; **mức 2 trong 99/121 phút** | Mức 2 từ phút 59 |
| S2 tiến tới EHS, HR bão hoà (Tc mô phỏng 41,3 °C; eTc chỉ 39,91) | **Mức 3 ở phút 28**; dáng đi bắt được ở phút 76; mức 4 EHS khi có Tre (phút 82); quy trình làm mát chạy tự động | Mức 3 ở phút 67, khi Tc đã 40,5 °C |
| S3 nhiễu và mất tín hiệu HR | Loại cả 8 mẫu nhiễu; giữ mức cũ khi mất tín hiệu; gục + mất HR → mức 4 nghi ngừng tim | Báo động giả do gai HR |
| S4 hạ natri máu | Chặn lời khuyên uống từ khi cân thấy tăng cân; mức 4 EAH (NaCl 3 %, không ngâm nước lạnh) | Mức 0 suốt 311 phút |

Tự kiểm tra các quy tắc an toàn: đạt, 0 vi phạm. **Lưu ý:** mức 3 sớm ở S2 có phần nhờ aPSI, mà công thức aPSI chưa kiểm chứng. Kết quả cũng phụ thuộc cách dựng kịch bản; đây **không phải** độ nhạy đã kiểm định.

### 7.3 Sửa đổi rút ra từ lần chạy này (đã áp dụng)
- Thư viện lõi trước đây tự đẩy eTc ≥ 40 °C lên mức 4 "nghi EHS". Đã sửa: Tc ước tính tối đa mức 3; mức 4 chỉ khi Tre đo được ≥ 40,5 °C.
- Bỏ lời khuyên "uống nước" mặc định ở mức 2, vì lời khuyên này gây hại khi VĐV bị hạ natri máu.

### 7.4 Cần chuyên gia lâm sàng quyết định
1. **Quy tắc R8** (agent đề xuất): chỉ lên mức 3 khi có tín hiệu cứng hoặc ≥ 2 tín hiệu độc lập. Quy tắc này giảm quá tải cho đội cơ động nhưng **đánh đổi độ nhạy mức 3**. Kiểm chứng viên chỉ ra rằng các "tín hiệu độc lập" đều suy ra từ HR nên thực chất không độc lập. Phương án thay thế:
   - gộp mọi tín hiệu suy từ HR thành tối đa 1 phiếu;
   - bộ hẹn giờ: mức 2 không được người quan sát xác nhận trong 5 phút → tự lên mức 3;
   - eTc + bù ≥ 39,5 kéo dài 3–5 phút được coi là tín hiệu cứng.
2. **Sàn 38,5 °C cho cảnh báo tốc độ tăng:** hiện làm cảnh báo này không còn tác dụng nâng mức. Nên thay bằng cửa sổ thời gian, ví dụ bỏ qua 20–25 phút đầu.
3. **R7 (WBGT đỏ +1 mức):** khiến phần lớn người chạy ở mức 2. Cách sửa: tách "mức 2 môi trường" (thông báo chung) khỏi "mức 2 cá nhân" (điều người quan sát tới).
4. **aPSI:** tắt mặc định cho tới khi đối chiếu được công thức gốc.

---

## 8. Đề xuất cho Việt Nam

1. **Nghiên cứu hiệu chỉnh–kiểm định (ưu tiên cao nhất).**
   - Thiết kế: VĐV Việt Nam (chạy bền, bóng đá, quân đội) mang viên nang làm chuẩn, kèm dây ngực HR, Tsk ngực và gia tốc kế, ở các buổi tập/giải trong điều kiện nóng ẩm.
   - Mục tiêu: hiệu chỉnh lại b0–b2 của ECTemp hoặc bản sigmoid; so sánh ECTemp, PSI, aPSI, CORE và mô hình đa biến.
   - Báo cáo: **độ nhạy/độ đặc hiệu tại ngưỡng 39,0 và 39,5 °C**, không chỉ RMSE. Phân tích Bland–Altman; kiểm định chéo theo người và theo sự kiện.
   - Thủ tục: hội đồng đạo đức, nhập khẩu viên nang theo NĐ 98/2021.
2. **Cơ sở dữ liệu dịch tễ.** Lập sổ đăng ký ca bệnh do nhiệt và ca cấp cứu tại các giải chạy Việt Nam, ghi Tre, Na⁺, CK, kết cục và WBGT. Hiện chưa có công bố bình duyệt nào.
3. **Lộ trình sản phẩm.**
   - Giai đoạn 1: công cụ hỗ trợ quyết định cho ban y tế (WBGT, dashboard, phác đồ, nút báo của người quan sát). Không tuyên bố chẩn đoán nên rủi ro pháp lý thấp.
   - Giai đoạn 2: thêm HR từ thiết bị VĐV tự mang (BLE Heart Rate Profile / ANT+, file FIT).
   - Giai đoạn 3: đăng ký TTBYT nếu tuyên bố phát hiện nguy cơ.
   - Song song: tra Cục Sở hữu trí tuệ Việt Nam; xin ý kiến pháp lý về Luật BVDLCN 2025.
4. **Chuẩn bị nguồn lực y tế giải** (theo IOC):
   - ≥ 1 khu xử trí nhiệt có bồn ngâm nước lạnh và đội 4 người mỗi bồn;
   - nhiệt kế trực tràng; xét nghiệm Na⁺/glucose tại chỗ; NaCl 3 %;
   - AED đủ để mọi điểm có thể sốc điện trong 3–5 phút;
   - bộ TACO tại trạm giữa đường;
   - giờ xuất phát chọn theo dự báo WBGT.

---

## 9. Giới hạn và kết quả kiểm chứng

**Kiểm chứng độc lập (74 mục):**

| Nhãn | Số mục | Tỷ lệ |
|---|---|---|
| ✅ | 47 | 64 % |
| ⚠️ | 19 | 26 % |
| ❌ | 2 | 3 % (đã sửa cả hai) |
| ❓ | 6 | 8 % |

- 41/41 PMID tồn tại và đúng metadata. Không phát hiện trích dẫn ma.

**Các mục còn mở:**
- Hệ số ECTemp chưa đối chiếu được với bảng trong PDF gốc.
- Công thức aPSI.
- Toàn văn ACSM 2023 và NATA 2015, gồm ngưỡng ngừng làm mát và cờ WBGT.
- Tình trạng Kenzen và Bodytrak.
- Số điều trong NĐ 356/2025 về dữ liệu sức khoẻ.
- Sáng chế tại Việt Nam.

**Giới hạn phương pháp:**
- Không đọc trực tiếp được website, nên phần thị trường dựa trên đoạn trích tìm kiếm.
- Mô phỏng dùng dữ liệu tổng hợp.
- Các ngưỡng dành cho thiết bị là **đề xuất chuyên gia**, chưa có hướng dẫn quốc tế nào quy định.

---

## 10. Tài liệu tham khảo chính (Vancouver)

1. Buller MJ, et al. Estimation of human core temperature from sequential heart rate observations. Physiol Meas. 2013;34(7):781–98. doi:10.1088/0967-3334/34/7/781. PMID 23780514.
2. Moran DS, et al. A physiological strain index to evaluate heat stress. Am J Physiol. 1998;275(1):R129–34. doi:10.1152/ajpregu.1998.275.1.R129. PMID 9688970.
3. Gunga HC, Sandsund M, Reinertsen RE, Sattler F, Koch J. J Therm Biol. 2008;33(5):297–307. doi:10.1016/j.jtherbio.2008.03.004. (Không có trên PubMed; xác minh qua SINTEF.)
4. Racinais S, et al. IOC consensus statement on recommendations and regulations for sport events in the heat. Br J Sports Med. 2022 (in 2023). doi:10.1136/bjsports-2022-105942. PMID 36150754.
5. Hosokawa Y, et al. Prehospital management of exertional heat stroke at sports competitions: International Olympic Committee Adverse Weather Impact Expert Working Group for the Olympic Games Tokyo 2020. Br J Sports Med. 2021. doi:10.1136/bjsports-2020-103854. PMID 33888465.
6. de Korte JQ, et al. A heart rate based algorithm to estimate core temperature responses in elite athletes exercising in the heat. Front Sports Act Living. 2022. doi:10.3389/fspor.2022.882254. PMID 35813051.
7. Buller MJ, et al. Gait instability and estimated core temperature predict exertional heat stroke. Br J Sports Med. 2022. doi:10.1136/bjsports-2021-104081. PMID 35022161.
8. Buller MJ, et al. Individualized monitoring of heat illness risk: novel adaptive physiological strain index to assess exercise-heat strain from athletes to fully encapsulated workers. Physiol Meas. 2023;44. doi:10.1088/1361-6579/acf991. PMID 37703905.
9. Buller MJ, et al. Skin temperature adapted physiological strain index (aPSI) predicts exertional heat illness. Physiol Meas. 2025. doi:10.1088/1361-6579/ae05ae. PMID 40930133.
10. Hintz C, et al. Heat stroke burden and validity of wearable-derived core temperature estimation during elite military training. Phys Sportsmed. 2023. doi:10.1080/00913847.2023.2190729. PMID 36919415.
11. Stevenson, et al. Validity and reliability of wearable heat stress monitors in firefighters during exercise-induced hyperthermia. Med Sci Sports Exerc. 2026. doi:10.1249/MSS.0000000000004113. PMID 42613781.
12. Hunt AP, et al. Validity of a noninvasive estimation of deep body temperature when wearing personal protective equipment during exercise and recovery. Mil Med Res. 2019. doi:10.1186/s40779-019-0208-7. PMID 31196190.
13. Januário, et al. Validity and reproducibility of the CALERA Research Sensor to estimate core temperature at different intensities of a cycling exercise in the heat. J Therm Biol. 2024;123:103907. doi:10.1016/j.jtherbio.2024.103907. PMID 38950497.
14. Verdel N, et al. Reliability and validity of the CORE sensor to assess core body temperature during cycling exercise. Sensors (Basel). 2021;21:5932. doi:10.3390/s21175932. PMID 34502822.
15. Sakamoto, et al. Physiological demands and contributors to variance of core temperature in 162 recreational runners during distance running in a warm-humid environment. Med Sci Sports Exerc. 2026;58:2299. doi:10.1249/MSS.0000000000004048. PMID 42319298.
16. Roberts WO, et al. ACSM expert consensus statement on exertional heat illness: recognition, management, and return to activity. Curr Sports Med Rep. 2021. doi:10.1249/JSR.0000000000000878. PMID 34524191 (bản 2023: PMID 37036463).
17. Bennett BL, et al. Wilderness Medical Society clinical practice guidelines for the management of exercise-associated hyponatremia: 2019 update. Wilderness Environ Med. 2020. doi:10.1016/j.wem.2019.11.003. PMID 32044213.
18. Kim JH, et al. Cardiac arrest during long-distance running races. N Engl J Med. 2012. doi:10.1056/NEJMoa1106468. PMID 22236223.
19. Looney DP, et al. J Meas Phys Behav. 2018;1:79–86. (Không có trên PubMed; có bản đính chính.)
20. Welles AP, et al. Estimation of core body temperature from skin temperature, heat flux, and heart rate using a Kalman filter. Comput Biol Med. 2018;99:1–6. doi:10.1016/j.compbiomed.2018.05.021. PMID 29803944.
21. Zhao, et al. Data-driven estimation of core body temperature during physical activity under heat exposure: a systematic review and standardized evaluation. Build Environ. 2026. doi:10.1016/j.buildenv.2026.114591. PMID 42405303.
22. Oyama, et al. Validation of upper thermal thresholds for outdoor sports using thermal physiology modelling. Temperature (Austin). 2023. doi:10.1080/23328940.2023.2210477. PMID 38577294.

*Tiêu đề, tạp chí và DOI của các mục có PMID được đối chiếu với PubMed (NLM) ngày 24/10/2026.*

Danh mục đầy đủ (> 40 bài, kèm DOI/PMID và nguồn web có ngày truy cập) nằm trong các file `01_*`, `02_*` và `03_*` trong `_workspace/`.
