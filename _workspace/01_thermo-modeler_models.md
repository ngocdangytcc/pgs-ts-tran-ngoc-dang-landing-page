# 01 — Mô hình & phương trình ước tính nhiệt độ lõi (Tc) và chỉ số căng thẳng nhiệt

*Agent: thermo-modeler · Ngày lập: 2026-10-24 · Đầu vào: `_workspace/00_brief.md` · Điểm xuất phát: skill `core-temp-modeling/references/equations.md`*

**Nguồn tra cứu:** PubMed (E-utilities/PMC qua MCP, truy cập 2026-10-24); WebSearch (truy cập 2026-10-24). **Giới hạn:** WebFetch/curl tới ResearchGate, Google Patents, IOPscience, frontiersin.org, usariem.health.mil bị chặn (DNS/proxy 403). Vì vậy bản PDF gốc Buller 2013 **không đọc trực tiếp được**. Hệ số ECTemp được đối chiếu gián tiếp qua (a) đoạn trích tìm kiếm của bản PDF Buller 2013 trên ResearchGate và (b) bằng sáng chế US10702165B2 (cùng nhóm tác giả). Phương trình trong toàn văn PMC bị mất khi trích xuất (dạng ảnh/MathML), nên mọi hệ số chỉ lấy được từ ảnh hoặc đoạn trích đều được ghi ❓.

**Ký hiệu mức bằng chứng:**
- 🟢 đã có kiểm định độc lập (nhóm khác nhóm phát triển)
- 🟡 chỉ có trong nghiên cứu gốc hoặc nhóm phát triển
- 🔴 đề xuất lý thuyết / tiền khả thi
- ❓ chưa kiểm chứng, cần đối chiếu bản gốc

---

## 0. Tóm tắt điều hành

1. **Hệ số ECTemp trong `equations.md` KHỚP với công bố gốc.** Các giá trị a = 1; γ = 0,022²; b0 = −7887,1; b1 = 384,4286; b2 = −4,5714; σ = 18,88² trùng với bản ResearchGate của Buller 2013 và bằng sáng chế US10702165B2. Mức tin cậy là trung bình–cao: hai nguồn độc lập về hình thức đều cho cùng giá trị, nhưng chưa đọc được trực tiếp trang PDF. Mã `scripts/heatstrain.py` dùng đúng các giá trị này.
2. **Kết quả kiểm định gốc trong `equations.md` cần sửa** từ "LoA khoảng ±0,5 °C" thành **bias −0,03 ± 0,32 °C, 95 % LoA ±0,63 °C, n = 83, > 52 000 quan sát** (PMID 23780514).
3. **Phiên bản ECTemp đang dùng hiện nay là bản sigmoid** (Looney 2018; Buller 2020/2022), không còn là bản bậc 2. Các nghiên cứu ở VĐV (de Korte 2022), người đi bộ (Peggen 2024) và công nhân (Lignier 2026) đều dùng bản sigmoid. **Chưa tìm được hệ số sigmoid** ❓.
4. **ECTemp rất kém ở vùng nguy hiểm.**
   - Ở 101 VĐV ưu tú trong môi trường nóng ẩm (WBGT 28,6 °C), độ nhạy chỉ 48 % tại ngưỡng Tc > 39,0 °C và 4 % tại ngưỡng > 39,5 °C.
   - Ở 5080 tân binh Thủy quân lục chiến Mỹ, ECTemp chỉ phát hiện 23 % ca say nóng gắng sức (EHI), trong khi **aPSI dựa trên nhiệt độ da phát hiện 87 %**.
   - Kết luận: **không dùng ECTemp đơn độc để cảnh báo say nắng gắng sức (EHS)**.
5. **Hai điểm sai trong `equations.md`:**
   - "aPSI (Buller 2008)" là sai. Buller 2008 là *bộ phân loại nguy cơ* từ HR + nhiệt độ da ngực (PSI ≥ 7,5). aPSI được công bố ở Buller 2023 (Physiol Meas 44) và sáng chế WO2017181195.
   - Gunga 2008 không đăng ở "Respir Physiol Neurobiol 163:18". Nguồn xác minh được là J Therm Biol 33:297–307 (2008). Bài Respir Physiol Neurobiol là của năm 2009 (169 Suppl 1:S63–8).
6. **Cảm biến dòng nhiệt (CORE/Calera) có kết quả kiểm định độc lập không nhất quán.** Phần lớn nghiên cứu cho thấy sai số > ±0,3 °C ở 40–60 % mẫu, và sai số tăng khi Tc cao, khi tập cường độ cao, ở người mỡ dưới da dày hoặc tổn thương tủy sống. Có hai nghiên cứu cho kết quả tốt (Januário 2024; nhóm non-SCI của Sanchez-Jimenez 2026).

---

## 1. ECTemp — Kalman filter mở rộng (EKF) từ nhịp tim

### 1.1 Phiên bản bậc 2 gốc (Buller et al., 2013) 🟢

**Nguồn:** Buller MJ, Tharion WJ, Cheuvront SN, et al. *Physiol Meas* 2013;34(7):781–798. DOI [10.1088/0967-3334/34/7/781](https://doi.org/10.1088/0967-3334/34/7/781). PMID 23780514.

**Mô hình:**
- Mô hình trạng thái: `Tc_t = a·Tc_{t-1} + w`, với w ~ N(0, γ).
- Mô hình quan sát: `HR_t = b2·Tc_t² + b1·Tc_t + b0 + v`, với v ~ N(0, σ).

**Đối chiếu hệ số:**

| Tham số | Ý nghĩa / đơn vị | `equations.md` | Bản gốc (RG Buller 2013 + US10702165B2) | Khớp? |
|---|---|---|---|---|
| a | hệ số chuyển trạng thái (không thứ nguyên) | 1 | 1 | ✅ |
| γ | phương sai nhiễu quá trình (°C²/phút) | 0,022² (= 4,84·10⁻⁴) | 0,022² | ✅ |
| b0 | hệ số chặn (bpm) | −7887,1 | −7887,1 | ✅ |
| b1 | bpm/°C | 384,4286 | 384,4286 (≈ 384,43) | ✅ |
| b2 | bpm/°C² | −4,5714 | −4,5714 (≈ −4,57) | ✅ |
| σ | phương sai nhiễu quan sát (bpm²) | 18,88² (= 356,45) | 18,88² | ✅ |
| Tc0 | Tc ban đầu (°C) | 37,1 | 37,1 khi chưa đo được Tc nền (Buller; Falcone 2024 cũng mô tả như vậy) | ✅ |
| v0 | phương sai ban đầu | 0 | **Không thống nhất giữa các nguồn**, xem dưới | ⚠️ |

**Chọn v0 theo cách khởi tạo:**
- Nếu Tc0 là giá trị **đo được**, đặt **v0 = 0** (Hunt 2019, Falcone 2024).
- Nếu Tc0 là giá trị **giả định**:
  - Hunt 2019 dùng Tc0 = 37,0 °C và **v0 = 0,01**.
  - de Korte 2022 dùng Tc0 = 37,0 °C và **v0 = 0,02**, trích dẫn Buller.
  - → ❓ Cần đối chiếu Buller 2013 hoặc Looney 2018 để biết giá trị khuyến nghị chính thức. Đề xuất cho prototype: tham số hoá v0 và mặc định 0,01–0,02 khi không đo được Tc nền.

**Ảnh hưởng của Tc0:** khi dùng Tc0 cố định 37,1 °C thay cho giá trị đo, lợi thế về độ chính xác của giá trị đo mất đi trong khoảng 30 phút (trích theo Falcone 2024, dẫn Buller).

**Bước lặp mỗi phút** (HR là trung bình 1 phút, thứ tự phương trình 1→6 theo Hunt 2019):

```
1. Tĉ  = a·Tc_{t-1}
2. v̂   = a²·v_{t-1} + γ
3. c   = 2·b2·Tĉ + b1                         # đạo hàm dHR/dTc tại Tĉ
4. k   = v̂·c / (c²·v̂ + σ)
5. Tc_t = Tĉ + k·(HR_t − (b2·Tĉ² + b1·Tĉ + b0))
6. v_t = (1 − k·c)·v̂
```

**Nhận xét toán học** (tự tính từ hệ số gốc; dùng để code, không phải số liệu công bố). Đường cong quan sát HR(Tc):

| Tc (°C) | HR dự kiến (bpm) | Độ dốc (bpm/°C) |
|---|---|---|
| 37,0 | 78,5 | 46,1 |
| 38,0 | 120,1 | 37,0 |
| 39,0 | 152,5 | 27,9 |
| 39,5 | 165,3 | 23,3 |
| 40,0 | 175,8 | 18,7 |
| 41,0 | 189,9 | 9,6 |
| 42,05 | 195,0 (đỉnh) | 0 |

Hệ quả:
- Ở vùng 40–42 °C, độ dốc c → 0 nên Kalman gain k → 0. Ước tính **"bão hoà"** và tăng rất chậm. Đây là cơ chế toán học giải thích việc **đánh giá thấp Tc ở vùng nguy hiểm** quan sát được trong mọi nghiên cứu kiểm định.
- VĐV có HR > 195 bpm (de Korte 2022 ghi nhận HR tới 207) nằm ngoài miền xác định của parabol. Khi code cần **giới hạn (clip) HR**, hoặc dùng bản sigmoid.

**Dữ liệu cần:** HR (dây đeo ngực ECG ưu tiên hơn PPG), trung bình 1 phút; Tc0 nếu có. **Không cần** thông tin nhân trắc hay dữ liệu môi trường.

**Giới hạn đã biết:**
- HR tách rời khỏi Tc trong các trường hợp: mất nước (thay đổi thể tích máu), sốt hoặc nhiễm virus, caffein, căng thẳng tâm lý, thuốc chẹn beta, gắng sức tĩnh, nhịp ngày đêm, và giai đoạn hồi phục (hiện tượng trễ HR–Tc: HR giảm nhanh hơn Tc).
- Dữ liệu huấn luyện chủ yếu là nam quân nhân trẻ.
- Dữ liệu huấn luyện gốc: 17 tình nguyện viên, bài tập dã ngoại quân sự 24 giờ, nhiệt độ không khí 24–36 °C, RH 42–97 %, Tc 36,0–40,0 °C.

### 1.2 ECTemp sigmoid (Looney et al., 2018; Buller 2020/2022) 🟢

**Nguồn:** Looney DP, Buller MJ, et al. "Estimating Resting Core Temperature Using Heart Rate." *J Meas Phys Behav* 2018;1(2):79–86. DOI [10.1123/jmpb.2017-0003](https://doi.org/10.1123/jmpb.2017-0003) (thông tin thư mục lấy từ WebSearch; không có trên PubMed). Sáng chế liên quan: US20220125388A1 / US12426839.

**Cấu trúc:** giữ nguyên Kalman filter, thay hàm quan sát bậc 2 bằng **hàm sigmoid** HR = f(Tc), có tiệm cận ở cả hai đầu (HR bão hoà ở Tc thấp và Tc cao).

**Kết quả gốc** (đánh giá khi nghỉ / ngủ, n = 16 trong buồng đo năng lượng):

| Mô hình | Bias | RMSE |
|---|---|---|
| Sigmoid | −0,04 ± 0,26 °C | 0,26 °C |
| Bậc 2 | −0,19 ± 0,29 °C | 0,35 °C |

Ở Tc cao, ước tính của sigmoid gần như trùng với bậc 2.

**Dạng hàm và hệ số sigmoid:** ❓ **chưa tìm được, cần đối chiếu bản gốc** (Looney 2018 hoặc US20220125388A1). Không tự điền.

**Khuyến nghị cho `algorithm-engineer`:**
- Dùng bản bậc 2 (đã xác minh hệ số) làm mặc định.
- Tạo interface để thay hàm quan sát (`h(Tc)`, `h'(Tc)`), sẵn sàng cắm hệ số sigmoid khi có bản gốc.
- ECTemp™ là thương hiệu của US Army/USARIEM và có bằng sáng chế (US10702165B2). Cần kiểm tra quyền sử dụng/cấp phép trước khi thương mại hoá.

### 1.3 Các nghiên cứu kiểm định ECTemp

Ưu tiên VĐV, môi trường nóng và hiện trường.

| Nghiên cứu | Quần thể / điều kiện | Tham chiếu | Kết quả chính | Mức |
|---|---|---|---|---|
| Buller 2013 (PMID 23780514) | 83 quân nhân, 9 nghiên cứu, nhiều điều kiện nhiệt / độ ẩm / trang phục | trực tràng / viên nang | bias −0,03 ± 0,32 °C; LoA ±0,63 °C; > 52 000 quan sát | 🟡 |
| Buller 2015, *Ergonomics* 58:1830 (DOI [10.1080/00140139.2015.1036792](https://doi.org/10.1080/00140139.2015.1036792)) | 27 quân nhân mặc PPE hoá-sinh, 45–90 phút | viên nang | bias 0,02 °C; RMSE 0,21 °C; LoA ±0,48 °C | 🟡 |
| Hunt 2019, *Mil Med Res* 6:20 (DOI [10.1186/s40779-019-0208-7](https://doi.org/10.1186/s40779-019-0208-7)) | 8 nam mặc đồ rà phá bom mìn (EOD), WBGT 21 và 29 °C, tập xen kẽ nghỉ | viên nang | bias 0,01 °C; LoA ±0,64 °C; RMSE 0,32 °C. Ở Tc > 38,5 °C: bias **−0,32** ± 0,56 °C. Đánh giá thấp đỉnh Tc 0,5–0,8 °C. **Ngưỡng ECTemp 38,4 °C** bảo vệ 97,5 % người khỏi Tc > 39,0 °C (độ nhạy 86 %) | 🟢 |
| Buller 2020, *Physiol Meas* 41 (DOI [10.1088/1361-6579/ab934b](https://doi.org/10.1088/1361-6579/ab934b)) | 21 tân binh Royal Marines, hành quân 14,5 km, 16 °C, RH ≥ 84 % | viên nang | Nhóm "HOT" (Tc > 40 °C): bias −0,10 ± 0,37 °C, RMSE 0,37 °C, theo kịp tới 40 °C. Nhóm "WARM": **đánh giá cao** 0,34 ± 0,40 °C, được hiệu chỉnh bằng hồi quy logistic (entropy nhiệt độ da + HR trung bình) → bias 0,00 ± 0,29 °C | 🟡 |
| Pearson 2021, *Saf Health Work* (DOI [10.1016/j.shaw.2021.11.003](https://doi.org/10.1016/j.shaw.2021.11.003)) | 44 lính cứu hoả, huấn luyện | viên nang | Lin's CCC 0,74 (kém); cá thể 0,11–0,83 → **không phù hợp**, đặc biệt ở Tc cao | 🟢 |
| **de Korte 2022**, *Front Sports Act Living* 4:882254 (DOI [10.3389/fspor.2022.882254](https://doi.org/10.3389/fspor.2022.882254), PMID 35813051) | **101 VĐV ưu tú** (13 môn), đạp xe tăng dần trong môi trường mô phỏng Tokyo: 31,6 °C, RH 74 %, WBGT 28,6 °C; bản sigmoid; Tc0 = 37,0, v0 = 0,02 | viên nang (myTemp) | bias 0,15 ± 0,36 °C (tóm tắt ghi ± 0,29 — không nhất quán trong bài); LoA ±0,45 °C; RMSE 0,35 °C. Tại đỉnh Tc: LoA ±0,92 °C, RMSE 0,47 °C. **Độ nhạy:** 96 % (> 38,0), 88 % (> 38,5), 48 % (> 39,0), 13 % (> 39,25), 4 % (> 39,5), 0 % (> 39,75). Không khác biệt theo giới hoặc môn | 🟢 |
| Hagen 2020, *J Funct Morphol Kinesiol* 5:46 (DOI [10.3390/jfmk5030046](https://doi.org/10.3390/jfmk5030046)) | Bóng bầu dục Mỹ NCAA, trại hè; thuật toán ECT tích hợp trong Zephyr BioHarness (❓ không rõ có phải ECTemp hay không) | viên nang | CCC 0,643; 78 % điểm trong ±1,0 °F; chính xác hơn ở nhóm %mỡ ≥ 6 % | 🟢 |
| Peggen 2024, *J Therm Biol* (DOI [10.1016/j.jtherbio.2024.103982](https://doi.org/10.1016/j.jtherbio.2024.103982)) | 18 người (56 ± 16 tuổi) đi bộ 30–50 km, 22→29 °C | viên nang | bias 0,09 °C; LoA ±0,44 °C nhưng r = 0,28. Bias cá thể từ −0,45 đến +0,62 °C; chỉ 3/18 người có bias < 0,1 °C | 🟢 |
| Falcone 2024, *Front Public Health* 12:1219595 (DOI [10.3389/fpubh.2024.1219595](https://doi.org/10.3389/fpubh.2024.1219595)) | 13 công nhân trung niên (6 nữ), 32 °C, RH 40 % | viên nang | Buller bậc 2: RMSE 0,34 ± 0,16 °C (hoạt động 0,25; hồi phục 0,39) | 🟢 |
| Lignier 2026, *Environ Res Commun* (DOI [10.1088/2515-7620/ae7bc5](https://doi.org/10.1088/2515-7620/ae7bc5)) | 102 công nhân xây dựng, mùa hè, một ca làm việc | viên nang | HR từ dây ngực Polar H10: bias −0,16 ± 0,30 °C. HR từ đồng hồ Garmin (PPG): bias −0,09 ± 0,28 °C. Kendall τ 0,36–0,39. Hai nguồn HR cho ECTemp gần như trùng nhau (0,03 ± 0,06 °C) → **dùng PPG được ở mức nhóm** | 🟢 |
| Zhao 2026, *Build Environ* (DOI [10.1016/j.buildenv.2026.114591](https://doi.org/10.1016/j.buildenv.2026.114591), PMID 42405303) | Tổng quan hệ thống 38 nghiên cứu + benchmark cài đặt lại 14 mô hình trên 2 bộ dữ liệu | trực tràng | EKF chỉ dùng HR: RMSE **0,41 °C** (đi bộ trên thảm chạy) và **0,66 °C** (đạp xe), so với 0,21–0,41 °C trong các bài gốc. Không mô hình nào vượt trội ổn định | 🟢 |
| Buller 2022, *Br J Sports Med* (DOI [10.1136/bjsports-2021-104081](https://doi.org/10.1136/bjsports-2021-104081)) | 1806 quân nhân, chạy 4–5 dặm và hành quân 7–12 dặm; 6 ca EHS | trực tràng lúc ngã quỵ | Ca EHS có ECTemp 39,2–40,8 °C. **ECTemp + mất ổn định dáng đi** (gia tốc kế thân) phát hiện 6/6 ca, sớm ≥ 3,5 phút trước khi ngã; dương tính giả 6,1 % | 🟡 |
| Buller 2025, *Physiol Meas* 46 (DOI [10.1088/1361-6579/ae05ae](https://doi.org/10.1088/1361-6579/ae05ae), PMID 40930133) | 5080 tân binh USMC; 30 ca EHI | — | ECTemp đơn độc phát hiện **23,3 %** ca EHI (xem §5) | 🟡 |

**Kết luận cho bối cảnh VĐV ở môi trường nóng ẩm:**
- ECTemp chấp nhận được ở mức nhóm và trong khoảng Tc 37,75–38,75 °C, tức đủ để theo dõi tập thích nghi nhiệt.
- ECTemp **không đủ nhạy để phát hiện Tc ≥ 39,5 °C**.
- Nếu vẫn dùng ECTemp làm một tầng cảnh báo, nên đặt **ngưỡng thấp và bảo thủ**, ví dụ ECTemp ≥ 38,4 °C theo Hunt 2019. Ngưỡng này chỉ áp dụng cho điều kiện tương tự nghiên cứu gốc và cần kiểm định riêng cho VĐV Việt Nam.

### 1.4 Các biến thể HR-only sau ECTemp

| Mô hình | Ý tưởng | Hiệu năng | Hệ số | Mức |
|---|---|---|---|---|
| **BKFB — Kalman hai pha** (Falcone 2024) | Hai bộ (γ, σ, h(Tc)) riêng cho pha "lên" và pha "xuống". Chuyển pha khi có ≥ 3 mẫu HR liên tiếp trên / dưới **115 bpm**. Tc0 = 37,43 °C (trung bình nhóm), v0 = 0. Dữ liệu lấy trung bình mỗi 30 giây | RMSE tổng 0,28 ± 0,12 °C, so với 0,34 của Buller trên cùng dữ liệu (khác biệt không có ý nghĩa thống kê). Chỉ kiểm định tới khoảng 38 °C | a ≈ 1. γ: 0,016 (lên) / 0,011 (xuống), bài mô tả là "SD" ❓ không rõ đã bình phương hay chưa. σ: 14,081 / 8,692 ❓ tương tự. h(Tc) bậc 2: **hệ số bị lỗi khi trích xuất** ❓ — pha xuống có thể là HR = 5,922·Tc² − 416,4·Tc + 7366, cho HR ≈ 79 bpm tại 37,5 °C (hợp lý), nhưng **cần đối chiếu bản gốc** | 🟡 |
| PSSK / TCBK đa mô hình (Zhao 2025, *Physiol Meas*, DOI [10.1088/1361-6579/ae0efd](https://doi.org/10.1088/1361-6579/ae0efd)) | Nhiều Kalman filter theo trạng thái (nghỉ / tập / hồi phục) hoặc theo cụm, gộp kết quả theo phương sai | Trong cùng bộ dữ liệu: RMSE 0,38–0,41 °C. Khi chuyển sang bộ dữ liệu khác: 0,88 (PSSK) và 1,56 °C (TCBK) | Theo đoạn trích tìm kiếm, khi khớp lại mô hình Buller trên dữ liệu khác thu được γ ≈ 0,0447, σ ≈ 24,23 ❓ chưa kiểm chứng | 🟡 |
| EKF + ánh xạ HR phòng ngừa (Aslani 2026, *IEEE JBHI*, DOI [10.1109/JBHI.2025.3650475](https://doi.org/10.1109/JBHI.2025.3650475)) | Thêm một lớp biến đổi HR trước khi đưa vào EKF | RMSE 0,34 °C (không có lớp này: 0,41), n = 18 | ❓ | 🟡 |
| Kalman thích nghi bù phần dư (2025, ScienceDirect PII S0208521625000762) | ❓ | ❓ | ❓ chưa đọc được | 🔴❓ |

---

## 2. Mô hình HR + nhiệt độ da (Tsk) + dòng nhiệt (HF) + môi trường

| Mô hình | Phương trình / cấu trúc | Đầu vào | Dữ liệu & kết quả | Mức |
|---|---|---|---|---|
| **Welles 2018**, *Comput Biol Med* 99:1–6 (DOI [10.1016/j.compbiomed.2018.05.021](https://doi.org/10.1016/j.compbiomed.2018.05.021)) | Kalman filter **tuyến tính**; các tham số học bằng hồi quy tuyến tính và hiệp phương sai giữa Tc với Tsk, HF, HR | Tsk, HF (6 vị trí), HR | n = 8 nam; 25 °C/50 %, 35 °C/70 %, 40 °C/20 %; công suất ~350 và ~550 W. Cơ ngực: RMSE 0,18 ± 0,04 °C; vùng sườn 0,18; xương ức 0,20. Chỉ 2 trong 3 biến cũng cho độ chính xác tương đương. Benchmark Zhao 2026: phụ thuộc mạnh vào vị trí đo và bộ dữ liệu. Hệ số theo vị trí: ❓ (nằm trong bảng của bài gốc) | 🟢 |
| **Xu 2013**, *Eur J Appl Physiol* 113:2381 (DOI [10.1007/s00421-013-2674-z](https://doi.org/10.1007/s00421-013-2674-z)) | Hồi quy tuyến tính bội Tc ~ Tsk + HF theo từng vị trí | Tsk, HF | n = 9, mặc quân phục + áo giáp. Xương ức giải thích ~75 % phương sai. **Trán không phù hợp khi vận động trong nóng** (do mồ hôi). Thuật toán chỉ áp dụng cho trang phục tương tự | 🟡 |
| **Eggenberger 2018**, *Front Physiol* 9:1780 (DOI [10.3389/fphys.2018.01780](https://doi.org/10.3389/fphys.2018.01780), PMC6295644) | Hồi quy tuyến tính bội. "Max-Input" dùng 18 biến; một mô hình rút gọn dùng 2 biến quan trọng nhất | Tsk (cách nhiệt / không cách nhiệt), HF, HR | n = 13 nam; 35,4 °C, RH 56 %; đạp xe 75 % HRmax (đồ thể thao) hoặc 50 % HRmax (đồ cứu hoả). SEE 0,28 °C, R² 0,70, không hơn mô hình Niedermann 6 biến (SEE 0,28, R² 0,71). Hệ số: ❓ (trong bài gốc) | 🟡 |
| **Niedermann 2013/2014**, *Int J Biometeorol* 58:7–15 (DOI [10.1007/s00484-013-0687-2](https://doi.org/10.1007/s00484-013-0687-2)) | Phân tích thành phần chính (PCA) trên 6 biến (3 Tsk, 2 HF, HR) → 2 nhân tố → hồi quy tuyến tính | Tsk, HF, HR | Ở 10 °C và 30 °C: RMSD 0,28–0,34 °C. *Ghi chú: `equations.md` ghi "Niedermann 2014"; bài online 2013, số in 2014* | 🟢 (được tái lập trong Eggenberger 2018) |
| **Richmond 2015**, *Ann Occup Hyg* 59:1168–78 (DOI [10.1093/annhyg/mev054](https://doi.org/10.1093/annhyg/mev054)) | Hồi quy từng bước trên 30 biến, mở rộng mô hình nhiệt độ da cách nhiệt (Tis) + nhiệt độ vi khí hậu trong quần áo (Tmc) của Richmond 2013 | Tis, Tmc, HR, Tsk 11 vị trí… | 12 nam + 9 nữ; 25–40 °C, có / không có bức xạ mặt trời, đồ thấm / không thấm. Theo Hunt 2019 dẫn lại: SEE ≈ 0,27 °C. Hệ số: ❓. Bất lợi: cần cảm biến cách nhiệt và vi khí hậu, không phù hợp cho VĐV chạy | 🟡 |
| **Laxminarayan 2018**, *J Appl Physiol* (DOI [10.1152/japplphysiol.00837.2017](https://doi.org/10.1152/japplphysiol.00837.2017), PMC6032092) | Mô hình toán + Kalman filter **cá thể hoá tham số** theo thời gian thực | hoạt động thể lực, HR, Tsk, nhiệt độ không khí, RH | 166 người, 3 nghiên cứu: RMSE 0,33 ± 0,18 °C. Với Tc > 38,5 °C: 0,25 °C. Mất 40 % dữ liệu chỉ làm sai số tăng ≤ 16 % | 🟡 |
| **Seng 2016**, *Physiol Meas* 37:485 (DOI [10.1088/0967-3334/37/4/485](https://doi.org/10.1088/0967-3334/37/4/485)) | Mô hình hiệu ứng hỗn hợp phi tuyến (NLME); tham số chính là hàm sigmoid-hyperbolic của tải mang vác và/hoặc Tsk ngực | Tc nền, Tsk ngực, tải | Hành quân 12–15 km, n = 34; RMSD 0,16 °C. *Lưu ý:* trong benchmark Zhao 2026 còn có "Seng EKF (HR + Tsk ngực)" ❓ — cần tách biệt với bài NLME này | 🟡 |
| **Buller 2008**, *Physiol Meas* 29:N79 (DOI [10.1088/0967-3334/29/12/N01](https://doi.org/10.1088/0967-3334/29/12/N01)) | Hồi quy logistic phân loại "có nguy cơ" (PSI ≥ 7,5) | HR, Tsk ngực | 6 nghiên cứu; tỉ lệ phân loại sai 10 %; 1 âm tính giả (2,7 %) | 🟡 |
| **Buller 2020** — hiệu chỉnh ECTemp | Hồi quy logistic (entropy gần đúng ApEn của Tsk + HR trung bình) phân nhóm WARM / HOT ở phút 20, rồi cộng hệ số hiệu chỉnh | HR, Tsk | Độ chính xác 95 %; bias sau hiệu chỉnh 0,00 ± 0,29 °C | 🟡 |
| **Sakamoto 2026**, *Med Sci Sports Exerc* 58:2299 (DOI [10.1249/MSS.0000000000004048](https://doi.org/10.1249/MSS.0000000000004048), PMC13561105) | *Không phải mô hình ước tính.* Hồi quy các yếu tố quyết định đỉnh Tc | Tc nền, HR trung bình, diện tích da (BSA), tốc độ | **162 người chạy phong trào ở Singapore**, 27,2 °C, RH 87 %, cự ly 10 km và 21 km. Đỉnh Tc **39,4 ± 0,6 °C (tối đa 41,1 °C)**. Tc nền giải thích 18 % biến thiên, HR trung bình 13 %, BSA 11 %, tốc độ 9 %. Có dashboard thời gian thực cho nhiều người. **Bằng chứng thực địa gần Việt Nam nhất** | 🟢 (dữ liệu thực địa) |

---

## 3. Cảm biến kép / dòng nhiệt (heat-flux, "double sensor")

**Phương trình cân bằng dòng nhiệt một chiều** (nguyên lý chung; Gunga 2008):

```
Tc ≈ T1 + K·(T1 − T2),   với K = R_mô / R_cảm biến
```

- T1: nhiệt độ mặt tiếp xúc da (°C).
- T2: nhiệt độ mặt ngoài của lớp cách nhiệt (°C).
- K: hiệu chỉnh thực nghiệm theo vị trí đặt (trán, xương ức…). Giá trị K cụ thể trong Gunga 2008: ❓ chưa đọc được.

**Nguồn đã xác minh:**
- Gunga HC, Sandsund M, Reinertsen RE, Sattler F, Koch J. *J Therm Biol* 2008;33(5):297–307. DOI [10.1016/j.jtherbio.2008.03.004](https://doi.org/10.1016/j.jtherbio.2008.03.004) (xác minh qua WebSearch / SINTEF; không có trên PubMed).
- Gunga 2009, *Respir Physiol Neurobiol* 169 Suppl 1:S63–8 (DOI [10.1016/j.resp.2009.04.005](https://doi.org/10.1016/j.resp.2009.04.005)): khi so với nhiệt độ trực tràng lúc nghỉ trong 24 giờ, sai khác cá thể từ −0,72 đến +0,55 °C. Kết luận của tác giả: chưa đủ chính xác để đo từng cá thể, nhưng hợp lệ để mô tả nhịp ngày đêm.
- ⚠️ `equations.md` ghi "Respir Physiol Neurobiol 163:18" — **không tìm thấy**, cần sửa.

**Sản phẩm thương mại** (CORE / greenTEG, nay là CALERA Research; Tcore của Dräger; 3M; Medisim) dùng thuật toán độc quyền, kết hợp Tsk + HF + HR (theo Priego-Quesada 2025). Không có phương trình công khai ❓.

**Bằng chứng kiểm định độc lập:**

| Nghiên cứu | Điều kiện | Kết quả | Hướng sai số |
|---|---|---|---|
| Verdel 2021, *Sensors* 21:5932 (DOI [10.3390/s21175932](https://doi.org/10.3390/s21175932)) | Đạp xe 19 °C và 31 °C, n = 12 + 13 | Độ lặp lại tốt (0,02 °C), nhưng **~50 % cặp đo lệch > 0,3 °C** so với trực tràng | không đạt tiêu chí |
| Goods 2023, *Eur J Sport Sci* 23:1509 (DOI [10.1080/17461391.2023.2193953](https://doi.org/10.1080/17461391.2023.2193953)) | 19 nữ VĐV khúc côn cầu Úc, trại tập nóng trước Tokyo | Lin's CCC "kém"; bias −0,06 đến −0,34 °C; **41–60 % mẫu lệch > ±0,3 °C**; đánh giá thấp nhiều hơn khi Tc tăng | **đánh giá thấp ở Tc cao** |
| Daanen 2023, *J Therm Biol* 112:103480 (DOI [10.1016/j.jtherbio.2023.103480](https://doi.org/10.1016/j.jtherbio.2023.103480)) | 3M / Medisim / CORE; 18 °C, tập tới kiệt sức | CORE có xu hướng đánh giá cao suốt buổi (đỉnh 38,6 so với 38,4 °C trực tràng); 3M sai lớn cuối buổi do mồ hôi | khác nhau theo thiết bị |
| Januário 2024, *J Therm Biol* 123:103907 (DOI [10.1016/j.jtherbio.2024.103907](https://doi.org/10.1016/j.jtherbio.2024.103907)) | CALERA, đạp xe 32 °C / RH 60 %, n = 15, hai lần thử | ICC 0,98; bias 0,01 °C; giới hạn khoảng −0,35 đến +0,38 °C → **đạt** | (kết quả tích cực) |
| Priego-Quesada 2025, *J Therm Biol* 127:104067 (DOI [10.1016/j.jtherbio.2025.104067](https://doi.org/10.1016/j.jtherbio.2025.104067)) | CALERA, test tăng dần tới kiệt sức ở 22 °C, n = 20 | bias −0,3 ± 0,2 °C; ICC 0,47; không phụ thuộc thể lực | đánh giá thấp |
| McLaughlin 2025, *J Therm Biol* 132:104241 (DOI [10.1016/j.jtherbio.2025.104241](https://doi.org/10.1016/j.jtherbio.2025.104241)) | Đạp xe 60 phút ở 35,9 °C, n = 24 | Toàn buổi bias +0,15 ± 0,43 °C; quý 3–4 của buổi tập +0,31 đến +0,36 °C. Tsk của CORE cao hơn thực tế +1,28 °C. Bias tương quan với độ dày mỡ dưới da (r ≈ 0,44–0,48) | **đánh giá cao ở cuối buổi** |
| Richard 2025, *Int J Sports Physiol Perform* 20:1068 (DOI [10.1123/ijspp.2025-0034](https://doi.org/10.1123/ijspp.2025-0034)) | 8 nữ, CORE và SlateSafety BandV2 | Độ lặp lại tốt nhưng không chính xác: lúc nghỉ −0,27 °C; ở phút 55 +0,33 °C (CORE) và +0,51 °C (BandV2) | nghỉ thấp, tập cao |
| van den Bogaard 2026, *J Therm Biol* 140:104541 (DOI [10.1016/j.jtherbio.2026.104541](https://doi.org/10.1016/j.jtherbio.2026.104541)) | CALERA trong 9 ngày tập thích nghi nhiệt, n = 15 | Đáp ứng kém với thay đổi Tc do thích nghi (ICC ≤ 0,18); đánh giá thấp "liều nhiệt" (thời gian Tc ≥ 38,5 °C) | đánh giá thấp |
| Goulet 2026, *Sensors* 26:5042 (DOI [10.3390/s26165042](https://doi.org/10.3390/s26165042)) | Nạp nước lạnh 4 °C khi nghỉ | Viên nang ghi nhận Tc giảm 0,76 °C; CORE chỉ thấy giảm 0,09 °C; ICC 0,12 | không phát hiện được làm mát bên trong |
| Sanchez-Jimenez 2026, *Top Spinal Cord Inj Rehabil* 32:68 (DOI [10.46292/sci25-00072](https://doi.org/10.46292/sci25-00072)) | Quay tay ergometer; người tổn thương tủy sống (SCI) và người không SCI | Không SCI: ICC 0,65, bias 0,06 °C. SCI: ICC −0,12 → **không hợp lệ** ở người SCI | — |

**Kết luận:** cảm biến dòng nhiệt thương mại có **độ lặp lại tốt nhưng độ chính xác tuyệt đối không ổn định**. Sai số tăng ở Tc cao, ở cuối buổi tập cường độ cao, ở người nhiều mỡ dưới da, khi làm mát bên trong, và ở người SCI. Có thể dùng làm **tín hiệu xu hướng** (ΔTc) hoặc một đầu vào cho mô hình hỗn hợp, nhưng **không dùng làm giá trị Tc tuyệt đối cho cảnh báo EHS**.

---

## 4. Mô hình học máy (ML) và mô hình lai, 2020–2026

| Mô hình | Kiến trúc | Đầu vào | Dữ liệu / kiểm định | Kết quả | Mức |
|---|---|---|---|---|---|
| **Kenzen** (Moyen 2021, *IJERPH* 18:13126, DOI [10.3390/ijerph182413126](https://doi.org/10.3390/ijerph182413126)) | ML độc quyền ❓ | sinh lý thời gian thực (thiết bị đeo) + nhân trắc | 4 nghiên cứu, 52 lượt đo, 27 người, > 4000 phút, 13–43 °C | MAE 0,25; RMSE 0,30; r 0,94; bias 0,07 °C. Nghiên cứu do nhà sản xuất tài trợ | 🟡 |
| **Conformal deep learning** (Strickland 2025, *Commun Eng* 4:219, DOI [10.1038/s44172-025-00548-6](https://doi.org/10.1038/s44172-025-00548-6), PMC12727793) | Học sâu + dự đoán conformal (khoảng dự đoán có hiệu chuẩn) + bộ cảnh báo theo ngưỡng × độ tin cậy | sinh lý (Equivital), nhân khẩu học, môi trường | > 140 000 phép đo, 6 lĩnh vực nghề nghiệp | Sai số trên tập test 0,29 °C. Độ chính xác xác suất hiệu chuẩn tốt hơn ECTemp 12 lần. Có liên quan thương mại (Intellegens / Equivital) | 🟡 |
| **Kalman + Informer** (Han 2025, *J Therm Biol*, DOI [10.1016/j.jtherbio.2025.104079](https://doi.org/10.1016/j.jtherbio.2025.104079)) | Kalman filter → Informer (mô hình dự báo chuỗi dài) | Tsk 7 vị trí + HR | n = 13, buồng nhiệt 34–40 °C | RMSE 0,09 °C; 95 % sai số trong ±0,17 °C. **Rủi ro quá khớp (overfit) cao** do mẫu nhỏ và nội kiểm | 🔴/🟡 |
| **Tai nghe nhét tai + ML** (Fujii 2026, *Scand J Med Sci Sports* 36:e70315, DOI [10.1111/sms.70315](https://doi.org/10.1111/sms.70315)) | ML ❓ | nhiệt độ ống tai + môi trường (2 thermistor) | Đạp xe nhẹ ở 10–30 °C, có gió 3 m/s | bias −0,003 °C; LoA ±0,52 °C; RMSE 0,26 °C. Chỉ thử ở cường độ nhẹ | 🟡 |
| **Phát hiện bất thường EHS** (Yaldiz 2023, *IEEE JBHI* 27:5803, DOI [10.1109/JBHI.2023.3323014](https://doi.org/10.1109/JBHI.2023.3323014)) | Bộ mã hoá nén quỹ đạo căng thẳng sinh lý (HR) / áp lực vận động (chuyển hoá ước tính) → phát hiện bất thường | HR, gia tốc 3 trục | 2102 quân nhân, 3 ca EHS | Dự báo EHS sớm **33–69 phút** trước khi ngã. Số ca rất ít | 🔴/🟡 |
| **ECTemp + dáng đi** (Buller 2022) | Hai thuật toán song song | HR, gia tốc kế thân | 3422 bộ dữ liệu, 6 ca EHS | 6/6 ca phát hiện sớm ≥ 3,5 phút; dương tính giả 6,1 % | 🟡 |
| **HeatGuard** (Silawarawet 2026, *Sensors* 26:2556, DOI [10.3390/s26082556](https://doi.org/10.3390/s26082556)) | ESP32 + HR quang học (MAX30101) + Tsk (MAX30205) + SHT31 + GSR; **mô hình tuyến tính Tsk → Tc** ❓ | HR, Tsk, môi trường, GSR | 15 VĐV ba môn phối hợp (Thái Lan), buồng nhiệt 24→27 °C, RH 70→90 % | Tc ước tính **khác có ý nghĩa** so với chuẩn (p = 0,003). Là nguyên mẫu ở Đông Nam Á, đáng tham khảo cho thiết kế | 🔴 |
| Benchmark Zhao 2026 | 14 mô hình KF / thống kê / ML cài đặt lại | — | 2 bộ dữ liệu | Không mô hình nào tốt nhất ổn định. Thêm Tsk cải thiện một số cấu hình. **Độ nhạy phát hiện Tc ≥ 38,0 °C khác nhau nhiều** giữa các mô hình | 🟢 |

**Đánh giá chung về ML:**
- RMSE báo cáo trong bài gốc (0,09–0,30 °C) thường **lạc quan hơn** khi đem kiểm định ngoài: Zhao 2026 cho thấy RMSE tăng gấp 1,5–2 lần, và Zhao 2025 cho thấy RMSE tăng lên 0,9–1,6 °C khi đổi bộ dữ liệu.
- Với prototype ở Việt Nam, cần **dữ liệu huấn luyện tại chỗ có Tc tham chiếu** (viên nang) và **kiểm định chéo theo người, theo sự kiện** (leave-one-subject-out / leave-one-event-out).

---

## 5. Chỉ số căng thẳng sinh lý (PSI) và các biến thể

### 5.1 PSI gốc (Moran et al., 1998) 🟢 — **công thức trong `equations.md` KHỚP**

```
PSI = 5·(Tre_t − Tre_0)/(39,5 − Tre_0) + 5·(HR_t − HR_0)/(180 − HR_0)      (thang 0–10)
```

- **Nguồn:** Moran DS, Shitzer A, Pandolf KB. *Am J Physiol* 1998;275(1):R129–R134. DOI [10.1152/ajpregu.1998.275.1.R129](https://doi.org/10.1152/ajpregu.1998.275.1.R129). PMID 9688970. Tóm tắt PubMed nêu đúng công thức trên.
- **Giả định gốc:** Tc tăng tối đa 3 °C (36,5→39,5) và HR tăng tối đa 120 bpm (60→180). Hai thành phần có trọng số bằng nhau.
- **Dữ liệu xây dựng:** 100 nam, 40 °C, RH 40 %, đi bộ 1,34 m/s, độ dốc 2 %, 120 phút.
- **Mở rộng:** Moran 1998b (*Am J Physiol* 275:R854, DOI [10.1152/ajpregu.1998.275.3.R854](https://doi.org/10.1152/ajpregu.1998.275.3.R854)) cho thấy PSI phân biệt được các mức mất nước 1,1–4,2 % khối lượng cơ thể.
- **Thang phân loại** (0–2 không/rất thấp, 3–4 thấp, 5–6 vừa, 7–8 cao, 9–10 rất cao): ❓ không có trong tóm tắt bài gốc. Thang này thường được trích lại (ví dụ Buller 2008 dùng PSI ≥ 7,5 làm "có nguy cơ"). Cần đối chiếu toàn văn.
- **Hạn chế khi áp dụng cho VĐV:** ở VĐV ưu tú, Tc 40 °C và HR ~180–200 bpm là bình thường khi thi đấu, nên PSI vượt 10. Buller 2023 ghi nhận PSI cuối buổi 11,4 ± 0,8 ở VĐV, "quá cao" so với thực tế. **Nên dùng HRmax cá nhân** thay cho 180.

### 5.2 aPSI — PSI thích nghi (Buller et al., 2023; 2025) 🟡

- **Nguồn:**
  - Buller MJ, Atkinson EA, Driver K, et al. *Physiol Meas* 2023;44. DOI [10.1088/1361-6579/acf991](https://doi.org/10.1088/1361-6579/acf991). PMID 37703905.
  - Sáng chế WO2017181195A1 / US11564579 / US12303238B2.
  - Ý tưởng aPSI đã được nêu trong Buller 2017, *J Appl Physiol* 124:432 (DOI [10.1152/japplphysiol.00353.2017](https://doi.org/10.1152/japplphysiol.00353.2017)).
- **Nguyên lý:** "Tc tới hạn" 39,5 °C trong PSI được **điều chỉnh động theo chênh lệch Tc − Tsk**. Khi Tsk cao (chênh lệch nhỏ), căng thẳng tim mạch tăng nên Tc tới hạn hạ xuống.
- **Công thức:** ❓ chưa kiểm chứng. Đoạn trích văn bản sáng chế (bị lỗi khi trích) gợi ý dạng sau, **cần đối chiếu Buller 2023 trước khi code**:

  ```
  aPSI = 5·(Tc_t − Tc_0)/(Tc_crit − Tc_0) + 5·(HR_t − HR_0)/(HR_crit − HR_0)
  Tc_crit ≈ 39,5 + [(Tc − Tsk) − 4]/4        ❓
  HR_crit ≈ 0,90·(220 − tuổi)                 ❓
  ```

- **Kết quả:**
  - Buller 2023: VĐV ưu tú chạy 8 km có Tc 40,1 °C, nhân viên mặc PPE kín có Tc 38,4 °C. PSI khác nhau rõ (11,4 so với 7,6), trong khi aPSI tương đương (9,9 so với 9,0), phản ánh cả hai nhóm cùng "rất cao".
  - **Buller 2025** (*Physiol Meas* 46, DOI [10.1088/1361-6579/ae05ae](https://doi.org/10.1088/1361-6579/ae05ae)), 5080 tân binh USMC, 30 ca EHI. Tỷ lệ phát hiện ca EHI:

    | Chỉ số | Phát hiện |
    |---|---|
    | **aPSI** | **86,7 %** (cảnh báo trước ~35 phút, dương tính giả ~15 %) |
    | Tsk một điểm | 83,3 % |
    | PSI | 63,3 % |
    | Tc − Tsk | 60 % |
    | ECTemp | 23,3 % |

  - Các ca aPSI bỏ sót gồm 2 ca sốt do virus và 2 ca kiệt sức nhiệt có Tre < 39 °C.
- **Phản biện:** Davey 2021, *Eur J Appl Physiol* 121:1701 (DOI [10.1007/s00421-021-04642-3](https://doi.org/10.1007/s00421-021-04642-3)), 136 lượt thử. Giá trị cuối của PSI, aPSI và các biến thể **không phân biệt** được lượt bị dừng do chạm ngưỡng chịu nhiệt với lượt hoàn thành. Chỉ có Tsk, Tc − Tsk, cảm giác nhiệt và **tốc độ thay đổi** của PSI / Tc / HR phân biệt được. Tác giả đề xuất chỉ số kết hợp sinh lý + cảm nhận.
- **Hàm ý:** cảnh báo nên dựa trên **aPSI kết hợp tốc độ tăng (dTc/dt, dHR/dt) và triệu chứng hoặc cảm nhận**, không dựa trên một giá trị đơn lẻ.

### 5.3 Các biến thể khác cần tra thêm

CSI (Contextual/Cumulative Strain Index), Heat Strain Score Index, PSI dùng HRmax cá nhân, PSI dựa trên tích trữ nhiệt: **chưa tra trong lượt này** ❓. Davey 2021 có so sánh PSI với PSI dựa trên tích trữ nhiệt.

---

## 6. Mô hình sinh lý nhiệt dự báo (dùng trước buổi tập / thi đấu)

- **Predicted Heat Strain (PHS, ISO 7933):** dự báo Tc / Tre, lượng mồ hôi và thời gian phơi nhiễm tối đa từ môi trường, chuyển hoá và cách nhiệt quần áo. Dùng để **đánh giá nguy cơ trước sự kiện**, không phải ước tính thời gian thực (Zhao 2026, mục Phụ lục).
- **SCENARIO** (USARIEM): mô hình điều nhiệt. Welles 2018 (*J Therm Biol* 72:44, DOI [10.1016/j.jtherbio.2017.12.007](https://doi.org/10.1016/j.jtherbio.2017.12.007)) dùng ngược mô hình này để ước tính chuyển hoá từ Tc.
- Gagge 2 nút, Fiala, HSDA: **chưa tra trong lượt này** ❓.
- **Gợi ý tích hợp:** PHS / SCENARIO dự báo từ WBGT dự báo thời tiết để chọn giờ xuất phát và vị trí trạm y tế (tầng 0), kết hợp với ước tính thời gian thực trong lúc chạy (tầng 1–3).

---

## 7. Hàm ý thiết kế cho prototype cảnh báo nhiều tầng (gửi `algorithm-engineer`)

1. **Chọn mô hình theo phần cứng:**
   - **Chỉ có HR** (đồng hồ PPG hoặc dây ngực): ECTemp bậc 2 với hệ số đã xác minh. Clip HR ≤ ~195 bpm; v0 = 0,01–0,02 nếu không có Tc0; đặt cờ "độ tin cậy thấp khi HR > 185".
   - **HR + Tsk một điểm** (ngực hoặc xương ức): **aPSI** sau khi xác minh công thức, kèm Tsk đơn thuần (độ nhạy 83 % trong Buller 2025). Đây là cấu hình tốt nhất về **phát hiện EHI** trên dữ liệu thực địa lớn.
   - **HR + gia tốc kế thân:** thêm chỉ số mất ổn định dáng đi (Buller 2022) làm tầng xác nhận.
   - **Cảm biến dòng nhiệt:** chỉ dùng ΔTc hoặc xu hướng làm đặc trưng cho mô hình; không dùng giá trị tuyệt đối.
2. **Ngưỡng ước tính phải thấp hơn ngưỡng lâm sàng:** do ECTemp đánh giá thấp ở vùng > 38,5 °C, ngưỡng hành động dựa trên ECTemp nên ≈ 38,4 °C (Hunt 2019) thay vì 39,5–40 °C. Ngưỡng lâm sàng lấy từ agent `heat-illness-clinical` và lưu dưới dạng tham số.
3. **Ưu tiên độ nhạy:** báo cáo độ nhạy và độ đặc hiệu tại từng ngưỡng, như bảng của de Korte 2022. Chấp nhận dương tính giả khoảng 6–15 % (mức trong Buller 2022 và 2025).
4. **Cá thể hoá:** Tc nền là yếu tố dự báo đỉnh Tc mạnh nhất ở người chạy nhiệt đới (Sakamoto 2026). Nên thu Tc0 (nếu có viên nang trong nghiên cứu) hoặc ít nhất HR0 lúc nghỉ. Hiệu chỉnh lại b0–b2 hoặc tham số sigmoid trên VĐV Việt Nam bằng viên nang.
5. **Dùng kèm độ bất định:** phương sai Kalman v_t (hoặc khoảng dự đoán conformal như Strickland 2025) để quyết định "cần kiểm tra trực tràng tại chỗ".
6. **Kiểm định:** Bland–Altman cho phép đo lặp (Bland & Altman, LoA có hiệu chỉnh), RMSE theo người, độ nhạy tại ngưỡng; chia dữ liệu theo người và theo sự kiện.

---

## 8. Danh sách sai lệch so với `references/equations.md` (đề nghị cập nhật skill)

| # | Mục trong `equations.md` | Hiện ghi | Đề nghị sửa | Nguồn |
|---|---|---|---|---|
| 1 | ECTemp, hệ số | a, γ, b0–b2, σ, Tc0 | **Giữ nguyên** (khớp) | RG Buller 2013; US10702165B2 |
| 2 | ECTemp, v0 | 0 | 0 nếu Tc0 đo được; 0,01 (Hunt) hoặc 0,02 (de Korte) nếu Tc0 giả định ❓ | PMID 31196190, 35813051 |
| 3 | Kiểm định gốc | "LoA khoảng ±0,5 °C" | bias −0,03 ± 0,32 °C; LoA ±0,63 °C; n = 83; > 52 000 quan sát | PMID 23780514 |
| 4 | Phiên bản hiện hành | chỉ có bản bậc 2 | thêm bản **sigmoid** (Looney 2018), hệ số ❓ | JMPB 2018 |
| 5 | "Welles 2018 — aĉTemp dùng thêm gia tốc / nhiệt da" | | Welles 2018 là **Kalman filter tuyến tính dùng Tsk + HF + HR**; không thấy tên "aĉTemp" ❓ | PMID 29803944 |
| 6 | Cảm biến kép | Gunga 2008, *Respir Physiol Neurobiol* 163:18 | Gunga 2008, *J Therm Biol* 33:297–307; và Gunga 2009, *Respir Physiol Neurobiol* 169 Suppl 1:S63 | DOI 10.1016/j.jtherbio.2008.03.004; PMID 19428314 |
| 7 | aPSI | "Buller 2008" | Buller 2023 (*Physiol Meas* 44) + sáng chế WO2017181195; **Buller 2008 là bộ phân loại PSI ≥ 7,5** | PMID 37703905, 18946156 |
| 8 | Niedermann | 2014 | 2013 (online), *Int J Biometeorol* 58:7–15 (2014) | PMID 23760405 |
| 9 | PSI | công thức | **Khớp**; thang phân loại 5 mức ❓ cần đối chiếu toàn văn | PMID 9688970 |
| 10 | Seng 2016 | liệt kê như nghiên cứu kiểm định ECTemp | Seng 2016 là mô hình NLME (Tsk ngực, tải mang vác), không phải kiểm định ECTemp | PMID 26963194 |

---

## 9. Tài liệu tham khảo (PMID / DOI; truy cập 2026-10-24)

1. Buller MJ, et al. Estimation of human core temperature from sequential heart rate observations. *Physiol Meas.* 2013;34:781–98. PMID 23780514. DOI 10.1088/0967-3334/34/7/781.
2. Buller MJ, et al. Real-time core body temperature estimation from heart rate for first responders wearing different levels of PPE. *Ergonomics.* 2015;58:1830–41. PMID 25967760. DOI 10.1080/00140139.2015.1036792.
3. Looney DP, Buller MJ, et al. Estimating resting core temperature using heart rate. *J Meas Phys Behav.* 2018;1(2):79–86. DOI 10.1123/jmpb.2017-0003 (chưa có PMID; thông tin từ WebSearch).
4. Hunt AP, et al. Validity of a noninvasive estimation of deep body temperature when wearing PPE during exercise and recovery. *Mil Med Res.* 2019;6:20. PMID 31196190. DOI 10.1186/s40779-019-0208-7.
5. Buller MJ, et al. Estimated and measured core temperature responses to high-intensity warm weather military training. *Physiol Meas.* 2020;41. PMID 32408286. DOI 10.1088/1361-6579/ab934b.
6. Hagen J, et al. Test and evaluation of heart rate derived core temperature algorithms for use in NCAA Division I football athletes. *J Funct Morphol Kinesiol.* 2020;5:46. PMID 33467262. DOI 10.3390/jfmk5030046.
7. Pearson et al. Comparisons of core temperature between a telemetric pill and heart rate estimated core temperature in firefighters. *Saf Health Work.* 2021. PMID 35936211. DOI 10.1016/j.shaw.2021.11.003.
8. de Korte JQ, et al. A heart rate based algorithm to estimate core temperature responses in elite athletes exercising in the heat. *Front Sports Act Living.* 2022;4:882254. PMID 35813051. DOI 10.3389/fspor.2022.882254.
9. Buller MJ, et al. Gait instability and estimated core temperature predict exertional heat stroke. *Br J Sports Med.* 2022. PMID 35022161. DOI 10.1136/bjsports-2021-104081.
10. Falcone T, et al. A real-time biphasic Kalman filter-based model for estimating human core temperature from heart rate measurements. *Front Public Health.* 2024;12:1219595. PMID 38528868. DOI 10.3389/fpubh.2024.1219595.
11. Peggen et al. Validity of the estimated core temperature algorithm during real-world prolonged walking exercise under warm ambient conditions. *J Therm Biol.* 2024. PMID 39383600. DOI 10.1016/j.jtherbio.2024.103982.
12. Zhao et al. Core body temperature estimation from heart rate via multi-model Kalman filtering and variance-based fusion. *Physiol Meas.* 2025. PMID 41038236. DOI 10.1088/1361-6579/ae0efd.
13. Aslani et al. A novel method for real-time human core temperature estimation based on EKF. *IEEE J Biomed Health Inform.* 2026. PMID 41489953. DOI 10.1109/JBHI.2025.3650475.
14. Lignier et al. Validation of the ECTemp™ algorithm in construction workers: PPG smartwatch vs chest strap. *Environ Res Commun.* 2026. PMID 42325812. DOI 10.1088/2515-7620/ae7bc5.
15. Zhao et al. Data-driven estimation of core body temperature during physical activity under heat exposure: systematic review and standardized evaluation. *Build Environ.* 2026. PMID 42405303. DOI 10.1016/j.buildenv.2026.114591.
16. Welles AP, et al. Estimation of core body temperature from skin temperature, heat flux, and heart rate using a Kalman filter. *Comput Biol Med.* 2018;99:1–6. PMID 29803944. DOI 10.1016/j.compbiomed.2018.05.021.
17. Xu X, et al. Relationship between core temperature, skin temperature, and heat flux during exercise in heat. *Eur J Appl Physiol.* 2013;113:2381–9. PMID 23775374. DOI 10.1007/s00421-013-2674-z.
18. Eggenberger P, et al. Prediction of core body temperature based on skin temperature, heat flux, and heart rate… *Front Physiol.* 2018;9:1780. PMID 30618795. DOI 10.3389/fphys.2018.01780.
19. Niedermann R, et al. Prediction of human core body temperature using non-invasive measurement methods. *Int J Biometeorol.* 2014;58:7–15. PMID 23760405. DOI 10.1007/s00484-013-0687-2.
20. Richmond VL, et al. Prediction of core body temperature from multiple variables. *Ann Occup Hyg.* 2015;59:1168–78. PMID 26268995. DOI 10.1093/annhyg/mev054.
21. Laxminarayan S, et al. Individualized estimation of human core body temperature using noninvasive measurements. *J Appl Physiol.* 2018. PMID 29420153. DOI 10.1152/japplphysiol.00837.2017.
22. Seng KY, et al. Nonlinear mixed effects modelling for the analysis of longitudinal body core temperature data. *Physiol Meas.* 2016;37:485. PMID 26963194. DOI 10.1088/0967-3334/37/4/485.
23. Buller MJ, et al. A real-time heat strain risk classifier using heart rate and skin temperature. *Physiol Meas.* 2008;29:N79–85. PMID 18946156. DOI 10.1088/0967-3334/29/12/N01.
24. Sakamoto Y, et al. Physiological demands and contributors to variance of core temperature in 162 recreational runners… warm-humid. *Med Sci Sports Exerc.* 2026;58:2299–313. PMID 42319298. DOI 10.1249/MSS.0000000000004048.
25. Gunga HC, et al. A non-invasive device to continuously determine heat strain in humans. *J Therm Biol.* 2008;33:297–307. DOI 10.1016/j.jtherbio.2008.03.004 (xác minh qua WebSearch).
26. Gunga HC, et al. The Double Sensor — a non-invasive device to continuously monitor core temperature in humans on earth and in space. *Respir Physiol Neurobiol.* 2009;169 Suppl 1:S63–8. PMID 19428314. DOI 10.1016/j.resp.2009.04.005.
27. Verdel N, et al. Reliability and validity of the CORE sensor to assess core body temperature during cycling exercise. *Sensors.* 2021;21:5932. PMID 34502822. DOI 10.3390/s21175932.
28. Goods PSR, et al. Concurrent validity of the CORE wearable sensor with BodyCap… elite women's field hockey heat camp. *Eur J Sport Sci.* 2023;23:1509–17. PMID 36939844. DOI 10.1080/17461391.2023.2193953.
29. Daanen HAM, et al. Heat flux systems for body core temperature assessment during exercise. *J Therm Biol.* 2023;112:103480. PMID 36796923. DOI 10.1016/j.jtherbio.2023.103480.
30. Januário et al. Validity and reproducibility of the CALERA Research Sensor… cycling in the heat. *J Therm Biol.* 2024;123:103907. PMID 38950497. DOI 10.1016/j.jtherbio.2024.103907.
31. Priego-Quesada JI, et al. Effect of aerobic fitness on the validity of the Calera Research™ sensor. *J Therm Biol.* 2025;127:104067. PMID 39923389. DOI 10.1016/j.jtherbio.2025.104067.
32. McLaughlin et al. Validity of the CORE wearable sensor during constant-load cycling exercise in the heat. *J Therm Biol.* 2025;132:104241. PMID 40876129. DOI 10.1016/j.jtherbio.2025.104241.
33. Richard et al. Accuracy and precision of the SlateSafety BandV2 and CORE devices… eumenorrheic females. *Int J Sports Physiol Perform.* 2025;20:1068–78. PMID 40537134. DOI 10.1123/ijspp.2025-0034.
34. van den Bogaard et al. Responsiveness of the CALERA Research Sensor to heat-acclimation-induced reductions in rectal temperature. *J Therm Biol.* 2026;140:104541. PMID 42462462. DOI 10.1016/j.jtherbio.2026.104541.
35. Goulet et al. Validity of the CORE wearable sensor during internal cooling induced by hyperhydration with cold water at rest. *Sensors.* 2026;26:5042. PMID 42655352. DOI 10.3390/s26165042.
36. Sanchez-Jimenez et al. Validity of CaleraSensor… arm crank exercise in individuals with SCI. *Top Spinal Cord Inj Rehabil.* 2026;32:68–77. PMID 42583328. DOI 10.46292/sci25-00072.
37. Moyen NE, et al. Accuracy of algorithm to non-invasively predict core body temperature using the Kenzen wearable device. *IJERPH.* 2021;18:13126. PMID 34948736. DOI 10.3390/ijerph182413126.
38. Strickland J, et al. Degrees of uncertainty: conformal deep learning for non-invasive core body temperature prediction in extreme environments. *Commun Eng.* 2025;4:219. PMID 41266785. DOI 10.1038/s44172-025-00548-6.
39. Han et al. A practical deep learning model for core temperature prediction of specialized workers in high-temperature environments. *J Therm Biol.* 2025. PMID 39970650. DOI 10.1016/j.jtherbio.2025.104079.
40. Fujii et al. Core temperature estimation using wearable earbud-type thermometer and machine learning… *Scand J Med Sci Sports.* 2026;36:e70315. PMID 42257542. DOI 10.1111/sms.70315.
41. Yaldiz CO, Buller MJ, et al. Early prediction of impending exertional heat stroke with wearable multimodal sensing and anomaly detection. *IEEE J Biomed Health Inform.* 2023;27:5803–14. PMID 37812534. DOI 10.1109/JBHI.2023.3323014.
42. Silawarawet et al. Development of wearable heatstroke warning system (HeatGuard)… triathletes. *Sensors.* 2026;26:2556. PMID 42076666. DOI 10.3390/s26082556.
43. Moran DS, Shitzer A, Pandolf KB. A physiological strain index to evaluate heat stress. *Am J Physiol.* 1998;275:R129–34. PMID 9688970. DOI 10.1152/ajpregu.1998.275.1.R129.
44. Moran DS, Montain SJ, Pandolf KB. Evaluation of different levels of hydration using a new physiological strain index. *Am J Physiol.* 1998;275:R854–60. PMID 9728084. DOI 10.1152/ajpregu.1998.275.3.R854.
45. Buller MJ, et al. Wearable physiological monitoring for human thermal-work strain optimization. *J Appl Physiol.* 2018;124:432–41. PMID 28798200. DOI 10.1152/japplphysiol.00353.2017.
46. Buller MJ, et al. Individualized monitoring of heat illness risk: novel adaptive physiological strain index… *Physiol Meas.* 2023;44. PMID 37703905. DOI 10.1088/1361-6579/acf991.
47. Buller MJ, et al. Skin temperature adapted physiological strain index (aPSI) predicts exertional heat illness. *Physiol Meas.* 2025;46. PMID 40930133. DOI 10.1088/1361-6579/ae05ae.
48. Davey SL, et al. The physiological strain index does not reliably identify individuals at risk of reaching a thermal tolerance limit. *Eur J Appl Physiol.* 2021;121:1701–13. PMID 33677693. DOI 10.1007/s00421-021-04642-3.
49. Welles AP, et al. Estimation of metabolic energy expenditure from core temperature using a human thermoregulatory model. *J Therm Biol.* 2018;72:44–52. PMID 29496014. DOI 10.1016/j.jtherbio.2017.12.007.
50. Sáng chế: US10702165B2 (ECTemp, bản bậc 2); US20220125388A1 / US12426839 (bản sigmoid); WO2017181195A1 / US11564579 / US12303238B2 (aPSI). Chỉ xem qua đoạn trích của WebSearch; ❓ chưa đọc toàn văn.

*Dữ liệu thư mục trong tài liệu này lấy từ PubMed (NLM).*
