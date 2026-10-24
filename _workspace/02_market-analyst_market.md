# 02 — Hiện trạng thị trường, Việt Nam, giấy phép, sáng chế & khoảng trống

*Agent:* market-analyst · *Ngày kiểm tra / truy cập web:* **2026-10-24** (mọi nguồn dưới đây truy cập ngày này trừ khi ghi khác)
*Đầu vào:* `_workspace/00_brief.md`, `_workspace/01_device-scout_devices.md` (§3 sơ bộ + danh sách ❓)
*Phạm vi:* §3 skill `wearable-device-survey`, gồm trạng thái, kênh/giá, Việt Nam, giấy phép, sáng chế và ma trận khoảng trống.

**Ký hiệu trạng thái:**

| Ký hiệu | Nghĩa |
|---|---|
| 🟢 | Đang bán (B2C hoặc B2B) |
| 🟡 | Thí điểm, beta, hoặc chỉ bán cho quân đội/doanh nghiệp/khu vực hẹp |
| 🔴 | Ngừng bán, công ty đóng cửa hoặc bị mua lại |
| ⚪ | Chỉ là nghiên cứu hoặc nguyên mẫu |
| ❓ | Chưa kiểm chứng |

Ghép hai ký hiệu (ví dụ "🟢❓") nghĩa là trạng thái có khả năng đúng nhưng **không có bằng chứng ≤ 12 tháng**.

> **Hạn chế phương pháp (cần đọc trước).** Trong phiên này, proxy của môi trường chặn truy cập trực tiếp mọi website (WebFetch/curl bị từ chối CONNECT, kể cả corebodytemp.com và kenzen.com). Vì vậy **mọi thông tin dưới đây lấy từ đoạn trích kết quả WebSearch**, không phải đọc trực tiếp trang gốc.
> - Việc website không truy cập được **không** được coi là bằng chứng công ty đã đóng cửa.
> - Giá, số hồ sơ FDA và số patent nên được `evidence-verifier` đối chiếu lại tại nguồn gốc (accessdata.fda.gov, patents.google.com, cổng Bộ Y tế).
> - Đây là sàng lọc sơ bộ, **không thay thế tư vấn pháp lý, quản lý TTBYT hay sở hữu trí tuệ**.

---

## 0. Tóm tắt điều hành

1. **Các thành phần đã có trên thị trường; giải pháp tích hợp cho giải chạy đông người thì chưa.**
   - **Đã có:** cảm biến ước tính Tc bán lẻ (CORE 2), thuật toán ước tính Tc từ HR (ECTemp, đang có patent Mỹ), và các nền tảng B2B cảnh báo stress nhiệt cho người lao động có dashboard người giám sát. Các nền tảng B2B gồm SlateSafety, Equivital, EVALAN ARMOR, Samsung SmartThings Pro Heat Stress (Hàn Quốc, 9/2025) và Biodata Bank CANARIA+ (Nhật).
   - **Chưa tìm thấy** sản phẩm nào gom đủ chuỗi sau cho **ban y tế giải chạy**: thiết bị VĐV tự mang + WBGT tại chỗ → ước tính Tc/nguy cơ → cảnh báo nhiều tầng → **phác đồ can thiệp lâm sàng** (EHS, hạ natri máu, tiêu cơ vân, sự cố tim).
   - Cũng chưa có sản phẩm nào **hiệu chỉnh cho VĐV Việt Nam/khí hậu nóng ẩm** hoặc có **tiếng Việt**.
2. **Đối thủ gần nhất về bối cảnh sự kiện thể thao** là **Biodata Bank CANARIA+**. Thiết bị này đã được phát cho tình nguyện viên và nhân viên tại World Athletics Championships Tokyo 2025, nhưng **người đeo là nhân viên, không phải VĐV**, và không gắn với phác đồ y tế.
3. **Đối thủ gần nhất về kiến trúc** là **Samsung SmartThings Pro – Heat Stress Management**.
   - Kiến trúc: Galaxy Watch (HR, vận động) + nhân trắc + nhiệt độ/độ ẩm tại chỗ → ước tính Tc → 3 mức cảnh báo → quản lý gửi lệnh nghỉ.
   - Phạm vi: B2B, cho người lao động, ở Hàn Quốc.
   - Đã có báo công nghệ Việt Nam đưa tin (vnreview), nên **có khả năng sẽ có mặt ở Việt Nam**, nhưng chưa thấy bán tại đây.
4. **Biến động thị trường đáng chú ý:**
   - **Dräger Tcore đã ngừng bán** (End of Sales).
   - **Bodytrak** được PitchBook ghi "Out of Business / liquidation".
   - **Kenzen** được PitchBook ghi "Out of Business". Chưa có thông cáo chính thức, nên xếp **🔴❓**.
5. **Việt Nam:**
   - Hàng tiêu dùng (Garmin, Polar…) có nhà phân phối chính hãng.
   - **Không tìm thấy** kênh phân phối CORE, viên nang, Equivital, Zephyr hay SlateSafety. Muốn có phải nhập khẩu.
   - Nếu hệ thống tuyên bố mục đích y tế (phát hiện hoặc cảnh báo say nắng), sẽ rơi vào phạm vi **NĐ 98/2021** (đã sửa đổi bởi NĐ 07/2023 và NĐ 04/2025; phân loại theo TT 05/2022).
   - Dữ liệu sức khoẻ là **dữ liệu cá nhân nhạy cảm**. Từ 01/01/2026, áp dụng **Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15** và **NĐ 356/2025/NĐ-CP** (thay NĐ 13/2023).
6. **Sáng chế:** lõi "HR → bộ lọc Kalman → Tc" được Quân đội Mỹ bảo hộ tại Mỹ.
   - **US 10,702,165 B2**: theo MTEC, dự kiến hết hạn khoảng 16/12/2033.
   - **US 12,426,839 B2**: cấp 30/09/2025.
   - Ngoài ra có đơn **US 2021/0338173 A1 / EP 4144068** cho tổ hợp *dáng đi + Tc ước tính → dự báo EHS*.
   - **Chưa tra cơ sở dữ liệu Cục SHTT Việt Nam.** Sáng chế có tính lãnh thổ; cần kiểm tra trước khi thương mại hoá, và cần thận trọng nếu sau này xuất khẩu sang Mỹ hoặc châu Âu.

---

## 1. Bảng trạng thái thị trường (cập nhật 2026-10-24)

### 1A. Lớp A — Viên nang / đo trực tiếp

| Sản phẩm | Trạng thái | Kênh & giá | Giấy phép | Bằng chứng (nguồn) |
|---|---|---|---|---|
| **e-Celsius (BodyCap, Pháp)** | 🟢❓ | B2B, nghiên cứu, lâm sàng. Giá khoảng 40–60 €/viên (2017) ❓ | **FDA 510(k) K210924** (e-Celsius Medical System), cấp 28/06/2023, mã FLL, Class II. Chỉ định hẹp: người ≥ 18 tuổi, > 80 lb, theo dõi liên tục > 6 h khi không đặt được ống trực tràng. **CE y tế** (2017) | 510k.innolitics.com/device/K210924; regdatalab.com/510k/K210924; accessgudid (03665810000168); healthcare-in-europe.com. Chưa có tin ≤ 12 tháng |
| **CorTemp (HQ Inc, Mỹ)** | 🟢❓ | B2B. Khoảng 46 USD/viên (không rõ ngày). Năm 2007: khoảng 30 USD/viên, hệ thống khoảng 2.200 USD | Hãng ghi "FDA cleared" (K880639 theo device-scout) ❓ | buyersguide.ohsonline.com (listing nhà phân phối); businessobserverfl.com. Không có tin 2025–2026 |
| **myTemp (Nijmegen, Hà Lan)** | ❓ (có thể ⚪ hoặc 🟡) | Không tìm thấy trang bán hoặc giá | ❓ | Chỉ có bài kiểm định (Bongers 2017/2018) và trang Radboudumc. Không tìm thấy nguồn công ty |
| **VitalSense (Mini Mitter → Respironics → Philips)** | ❓ (nghiêng 🔴 ở dạng bán lẻ độc lập) | Một bài không ghi ngày nói Philips **cấp phép công nghệ cho Equivital** | FDA K033534 (mã FLL). Bản ghi GUDID ghi "In Commercial Distribution" nhưng **cập nhật lần cuối 06/07/2018** | accessgudid.nlm.nih.gov/devices/00606959021648; mobihealthnews.com "Equivital uses old pill sensor…". Đợt Philips ngừng 19 sản phẩm (1/2024) không nhắc VitalSense |

### 1B. Lớp B — Dòng nhiệt / trong tai

| Sản phẩm | Trạng thái | Kênh & giá | Giấy phép | Bằng chứng |
|---|---|---|---|---|
| **CORE 2 (greenteg, Thuỵ Sĩ)** | 🟢 | Bán lẻ toàn cầu (web hãng, bike-components, bike24, Mantel…). Khoảng 289,95 CHF trên web hãng (đoạn trích, ngày ❓); 269,95 CHF / 359 USD / 243 € lúc ra mắt 3/2025. Mantel khoảng 314,95–326,66 € | **Không phải thiết bị y tế**. Spec sheet và FAQ ghi "không có FDA hay Medical CE". Trang US cũ từng viện dẫn EUA COVID-19 (đã lỗi thời) | nordicsemi.com (09/2025); ces.tech (CES Best of Innovation 2025); greenteg.com spec sheet; corebodytemp.com/pages/faq |
| **CALERA Research (greenteg)** | 🟢 | Shop greenteg: **999 CHF** (ngày ❓). Có OEM dev-kit, giá theo báo giá | Bản nghiên cứu; không có tuyên bố y tế ❓ | shop.greenteg.com/core-body-temperature/caleraresearch. Được dùng trong nghiên cứu nông nghiệp 2026 (Sousan, Am J Ind Med) |
| **Dräger Tcore / Double Sensor** | **🔴** | — | (Trước đây là thiết bị lâm sàng) | Trang Dräger (en_me, en_sa, en_za) ghi **"End of Sales – This model is no longer available"** |
| **3M SpotOn (ZHF)** | 🟢❓ (chỉ lâm sàng) | Bệnh viện | Thiết bị y tế; số hồ sơ không xác minh trong phiên ❓ | Không kiểm tra được trong phiên |
| **cosinuss° c-med° alpha** | 🟢 | B2B / y tế | **CE MDR loại IIa** (thông cáo 06/02/2023), FCC. Khuyến cáo dùng **trong nhà, kín gió** (bệnh viện, chăm sóc tại nhà) | cosinuss.com (thông cáo 2023; datasheet v08, 07/2025) |
| **Bodytrak (Anh, trong tai)** | **🔴❓** | (Trước đây B2B: cứu hoả, quân đội) | ❓ | PitchBook: "Out of Business", giao dịch cuối là liquidation (ngày ❓). Nguồn mới nhất về sản phẩm là 2023 |
| Miếng dán dual-heat-flux (JNIOSH), earbud ML (Fujii 2026), thermal-guiding sensor (Du 2026) | ⚪ | — | — | Chỉ có công bố khoa học |

### 1C. Lớp C — HR/Kalman & nền tảng B2B

| Sản phẩm | Trạng thái | Kênh & giá | Giấy phép | Bằng chứng |
|---|---|---|---|---|
| **Equivital EQ02+ LifeMonitor / eq LifeBand / Black Ghost (Anh)** | 🟢 (B2B, quân đội, nghiên cứu) | Hợp đồng; giá không công bố | **FDA 510(k) K113054** (Hidalgo, 17/02/2012; GUDID LifeMonitor EQ-02-SEM-012 trỏ tới số này); trước đó K061993 (EQ-01). CE ❓ | 510k.innolitics.com/device/K113054; accessgudid 05060483830056. **MoU với ST Engineering (Singapore), 10/11/2025**, cho quân đội và lực lượng ứng cứu, tức là có kênh vào Đông Nam Á |
| **Zephyr BioHarness 3 + OmniSense (Medtronic)** | 🟡❓ | B2B (quốc phòng, ứng cứu, thể thao chuyên nghiệp) | **FDA 510(k) K113045** (BioHarness 3.0, 14/08/2012; Class II, mã MHX); K100040 (BH 2.0) | accessdata.fda.gov/cdrh_docs/pdf11/k113045.pdf; Wikipedia Zephyr Technology. **Không có tin 2025–2026**; không tìm thấy thông báo ngừng bán |
| **Kenzen (Mỹ)** | **🔴❓** | Thuê bao theo người/tháng (khi còn hoạt động) | Wellness / an toàn lao động ❓ | PitchBook: **"Out of Business"** (bảng funding có mục 04/08/2022). Tin tức chính thức mới nhất tìm được là 2021–2022. Một blog nhà thầu năm 2025 (ringland.com) vẫn nhắc McCarthy thử nghiệm nhưng không phải nguồn sơ cấp. **Không tìm thấy** thông cáo đóng cửa hay bán tài sản |
| **SlateSafety BAND V2 (Mỹ)** | 🟢 | Qua SKC, Levitt. **804,95/thiết bị** (Levitt, Canada; khả năng là CAD ❓). **Bắt buộc mua Annual Portal Access riêng cho từng thiết bị** (SKU 506-209); có bộ kèm 3 năm portal; dùng thử 30 ngày | ❓ (không thấy tuyên bố y tế) | skcinc.com/products/band-v2; levitt-safety.com; ohsonline.com (08/2024) |
| **EVALAN ARMOR (Hà Lan)** | 🟡❓ | B2B; phát triển cùng Bộ Quốc phòng Hà Lan; giá không công bố | Dùng **ECTemp theo giấy phép của Quân đội Mỹ** (US 10,702,165) | evalan.com/products/armor; computable.nl |
| **Samsung SmartThings Pro – Heat Stress Management (Hàn Quốc)** | 🟡 (B2B, Hàn Quốc) | Giải pháp an toàn B2B, ra mắt **09/2025**, nâng cấp **07/2026**. Ước tính Tc từ HR, vận động, chiều cao, cân nặng, tuổi, giới cùng nhiệt độ/độ ẩm tại chỗ. Ngưỡng cảnh báo theo nhiệt độ cảm nhận 33/35/38 °C. Quản lý gửi lệnh nghỉ | Phát triển với Bộ Lao động Hàn Quốc và ĐH Incheon; theo tin là "được kiểm định lâm sàng" tại Samsung Seoul Hospital ❓ | wareable.com; sammobile.com (06/07/2026); digitaltrends.com; vnreview.vn (bản tin tiếng Việt) |
| **Biodata Bank CANARIA+ (Nhật)** | 🟢 (Nhật, B2B) | Thiết bị cổ tay **dùng một lần**, không cần sạc hay mạng. Hãng tự công bố **> 1 triệu thiết bị, > 2.000 khách hàng doanh nghiệp**. Giá ❓ | Hãng nói có patent cụm cảm biến dòng nhiệt ❓ | renesas.com (customer story); kingsalmon.metro.tokyo.lg.jp. **Thí điểm tại World Athletics Championships Tokyo 2025** cho tình nguyện viên và nhân viên; cảnh báo kích hoạt ở khoảng 3% tình huống (báo cáo của dự án) |
| **Hexoskin (Canada)** | 🟢 | Smart Shirt 199 USD, ProShirt 249 USD, bộ kit 849–899 USD (trang hãng, không ghi ngày) | ❓ | support.hexoskin.com; **REST API OAuth1/2, dữ liệu thô** (api.hexoskin.com/docs), Android SDK. Cấp key qua api@hexoskin.com |

### 1D. Lớp D — Chỉ báo gián tiếp / mồ hôi

| Sản phẩm | Trạng thái | Kênh & giá | Giấy phép | Bằng chứng / API |
|---|---|---|---|---|
| Garmin | 🟢 | Bán lẻ; **có ở Việt Nam** (xem §2) | Wellness | **Health API / Health SDK**: đánh giá miễn phí; **dùng thương mại cần phí license hoặc cam kết số lượng thiết bị tối thiểu**; dữ liệu beat-to-beat phải trả phí. Một blog (tryterra.co) nói Connect Developer Program **đang tạm dừng nhận đơn** ❓ (developer.garmin.com). Không có tính năng Tc gốc; CORE hiển thị trên Garmin qua ANT+/BLE và Connect IQ |
| Apple Watch | 🟢 | Bán lẻ, có ở VN (hiểu biết chung, không xác minh trong phiên) | Nhiệt độ cổ tay không dùng cho mục đích y tế | Không có cảnh báo stress nhiệt gốc. CORE 2 có app hiển thị trên Apple Watch |
| Samsung Galaxy Watch | 🟢 | Bán lẻ, có ở VN (hiểu biết chung) | — | Bản tiêu dùng **không** có cảnh báo nhiệt; chỉ bản B2B SmartThings Pro (1C) |
| Oura | 🟢 | Bán lẻ quốc tế | Wellness | **API v2** có chuỗi HR/IBI thô. Nhẫn Gen3 **không có membership thì mất quyền API** (support.ouraring.com) |
| WHOOP | 🟢 | Thuê bao | Wellness | **API V2 (07/2025)**: chế độ dev giới hạn 10 thành viên; chủ yếu là **tóm tắt** HR, không thấy luồng HR thô ❓ |
| Polar H10 / Verity Sense | 🟢 | Bán lẻ. Nhà phân phối VN: **StreamCast Asia** (từ 07/2020; hiện tại ❓) | — | BLE Heart Rate Profile chuẩn; Polar SDK ❓ |
| **Gx Sweat Patch (Gatorade/Epicore)** | 🟢❓ | Ra mắt Mỹ 2021, 24,99 USD; có ở Canada, Mỹ Latinh. Không có xác nhận 2025 | Wellness | cnbc.com (2021); runningmagazine.ca |
| **Epicore Connected Hydration (B2B)** | 🟢 | Series B 26 triệu USD (02/2025); armband tái sử dụng (08/2025); hợp tác DuPont, Chevron, REUS Cares; Hydration Readiness Score (06/2026) | ❓ | pulse2.com; ishn.com; thông cáo Cision 09/06/2026 |
| **Nix Biosensors** | 🟢 | 129 USD (theo device-scout). **Series A 10 triệu USD (15/09/2026)**; được UCI chấp thuận cho thi đấu (mùa 2025); Coaches Network (10/2025) | Wellness | endurancesportswire.com; bicycleretailer.com (01/2025); insider.fitt.co |
| **hDrop** | ❓ | Gen 2: 249,99 USD (trang hãng, không ngày). Tin mới nhất **06/2024** (Sweat Zones) | ❓ | hdroptech.com; insider.fitt.co |

### 1E. Lớp E — Môi trường / phần mềm

| Sản phẩm | Trạng thái | Ghi chú | Nguồn |
|---|---|---|---|
| **Kestrel 5400 Heat Stress Tracker (+LiNK)** | 🟢 | Là mẫu thay thế 4400/4600 (đã ngừng). Còn trên web hãng và các nhà bán lẻ Úc 2026. **Không có bằng chứng ngừng bán**; thông tin "ngừng" của device-scout nhiều khả năng là nói về 4400/4600 | kestrelmeters.com; instrumentchoice.com.au |
| **OSHA-NIOSH Heat Safety Tool** | 🟡 | Vẫn tải được, nhưng NIOSH ghi app **"không nhận cập nhật vào lúc này"**. Chỉ dựa trên heat index, không có đầu vào sinh lý | cdc.gov/niosh/topics/heatstress/heatapp.html |
| HeatGuard (cổ tay, triathlete) – *Sensors* 2026;26(8):2556 | ⚪ | Nguyên mẫu + dashboard web; chi tiết ❓ (chỉ thấy tiêu đề) | mdpi.com/1424-8220/26/8/2556 |
| Heat Stroke Warning Prototype – *Sensors* 2025;25(2):294 | ⚪ | Pilot n = 1; cảm biến HR MAX30102 kém (r = 0,179) | ncbi PMC11769488 |

---

## 2. Việt Nam

### 2.1. Kênh phân phối & mua hàng

| Nhóm | Tình trạng tại VN | Nguồn / ghi chú |
|---|---|---|
| **Garmin** | 🟢 Chính hãng. Đối tác: FPT Trading, Synnex FPT, Petrosetco. Có **Garmin Brand Store** ở Hà Nội (từ 04/2021) và TP.HCM; đại diện khu vực Garmin VN | fptshop.com.vn; viettimes.vn; doanhnhanplus.vn; vnreview.vn. Đơn vị phân phối *hiện tại* ❓ |
| **Polar** | 🟢❓ StreamCast Asia (TP.HCM) được uỷ quyền độc quyền từ 07/2020 | brandsvietnam.com (2020). Hiện trạng ❓ |
| Apple, Samsung | 🟢 (hiểu biết chung; không xác minh trong phiên) | — |
| **CORE 2 / CALERA** | ❌ **Không tìm thấy** đại lý, sàn TMĐT VN hay giá VND | Muốn có phải mua quốc tế (web hãng bán bằng CHF; khả năng giao hàng tới VN ❓) hoặc xách tay. Không có bảo hành chính hãng tại VN |
| Viên nang (e-Celsius, CorTemp) | ❌ Không tìm thấy nhà phân phối | Phải nhập khẩu. Nếu nhập để dùng trên người (kể cả nghiên cứu) cần làm thủ tục TTBYT (xem 2.2). **Không tìm thấy nghiên cứu nào tại VN dùng viên nang Tc** |
| Equivital, Zephyr, SlateSafety, Kenzen, EVALAN | ❌ Không tìm thấy kênh VN | Equivital có MoU với ST Engineering (Singapore), là kênh khu vực tiềm năng ❓ |
| Samsung SmartThings Pro Heat Stress | ❓ Chưa thấy triển khai ở VN; mới có bản tin trên vnreview.vn | Đây là ứng viên dễ vào VN nhất vì Samsung có hạ tầng lớn tại VN (suy luận, cần xác minh) |
| Shopee, Lazada | ❓ Không có kết quả tìm kiếm cho CORE, Polar H10 hay Whoop trên sàn VN (công cụ tìm không lập chỉ mục sàn VN tốt) | Cần kiểm tra thủ công |
| Startup VN về cảnh báo sốc nhiệt bằng thiết bị đeo | **Không tìm thấy** | Chỉ có tài liệu quy trình phòng stress nhiệt nơi làm việc của COHED (Quỹ Rockefeller tài trợ) |

**Bối cảnh nhu cầu tại VN (báo chí):**
- **Quang Binh International Marathon (28/07/2024):** 2 VĐV nhập viện vì **sốc nhiệt, tiêu cơ vân, suy thận cấp do thiếu dịch**. Cả hai được cứu sống (plo.vn).
- **VnExpress Marathon Huế (06/04/2025):** 4 VĐV cấp cứu, 1 nữ 53 tuổi tử vong. Nguyên nhân được mô tả là "dấu hiệu đột quỵ", **chưa xác định liên quan nhiệt**.
- **Các ca khác 2024:** có ca tử vong hoặc đột quỵ (TP.HCM, Việt Nam Ultra Marathon – Hoà Bình), nguyên nhân không được công bố cụ thể.
- **Đánh giá:** đây là bằng chứng báo chí, không phải số liệu dịch tễ. Ca Quảng Bình minh hoạ đúng tổ hợp EHS + tiêu cơ vân + tổn thương thận cấp (AKI) mà hệ thống cần bao phủ.

### 2.2. Khung pháp lý trang thiết bị y tế (TTBYT)

- **Văn bản nền:**
  - **NĐ 98/2021/NĐ-CP** về quản lý TTBYT.
  - Sửa đổi bởi **NĐ 07/2023/NĐ-CP** (03/03/2023): gia hạn giấy phép, bổ sung hậu kiểm (Điều 39a), quy định công khai giá.
  - Sửa đổi tiếp bởi **NĐ 04/2025/NĐ-CP** (01/01/2025): sửa Điều 76 về chuyển tiếp; giấy phép nhập khẩu cấp 2018–2021 được dùng đến 30/06/2025.
  - **Văn bản hợp nhất 05/VBHN-BYT (2025).**
- **Phân loại:** theo **TT 05/2022/TT-BYT** (hiệu lực 01/08/2022), Phụ lục I, mức A/B/C/D theo rủi ro (khung ASEAN AMDD).
  - Một trang thứ cấp ghi TT 05/2022 đã được sửa bởi **TT 59/2025/TT-BYT** và **TT 24/2026/TT-BYT** ❓ (chưa đọc văn bản).
  - **TT 44/2025/TT-BYT** quy định phân cấp, gồm cấp số lưu hành cho loại C, D.
- **Áp dụng sơ bộ cho dự án** (suy luận theo nguyên tắc phân loại; ❓ **cần đối chiếu Phụ lục I và tư vấn Cục Cơ sở hạ tầng & TTBYT**):

| Thành phần | Nhiều khả năng thuộc | Lý do / lưu ý |
|---|---|---|
| Đồng hồ, đai HR, CORE dùng như wellness (không tuyên bố y tế) | Ngoài phạm vi TTBYT | Hãng tự tuyên bố "không phải thiết bị y tế" |
| Nhiệt kế điện tử / hồng ngoại | TTBYT; TT 05/2022 (Điều 4) liệt kê **nhiệt kế điện tử, hồng ngoại** trong danh mục loại B–D được **mua bán như hàng hoá thông thường** | Theo đoạn trích thuvienphapluat.vn; mức phân loại cụ thể ❓ |
| Viên nang nuốt đo Tc (FDA Class II, mã FLL) | TTBYT, nhiều khả năng **loại B** (hoặc C) ❓ | Thiết bị chủ động, đưa qua lỗ tự nhiên, dùng ngắn hạn. Nghiên cứu hiệu chỉnh trên người cần hồ sơ đạo đức + thủ tục nhập khẩu |
| **Phần mềm/hệ thống tuyên bố "phát hiện, cảnh báo say nắng, hướng dẫn can thiệp"** | Nhiều khả năng là **TTBYT (phần mềm là thiết bị y tế)**, loại B hoặc C ❓ | Mục đích sử dụng quyết định. Định vị là "công cụ hỗ trợ ban y tế / an toàn sự kiện" khác về pháp lý với "chẩn đoán". Cần ý kiến pháp lý trước khi tuyên bố lâm sàng |

### 2.3. Dữ liệu sức khoẻ

- **NĐ 13/2023/NĐ-CP đã được thay thế:**
  - **Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15** (thông qua 26/06/2025, **hiệu lực 01/01/2026**).
  - **NĐ 356/2025/NĐ-CP** hướng dẫn thi hành, thay NĐ 13/2023, hiệu lực 01/01/2026 (theo EY Legal Alert 03/2026).
  - Kế hoạch triển khai: Quyết định 2623/QĐ-TTg (29/11/2025).
- **"Tình trạng sức khoẻ"** thuộc **dữ liệu cá nhân nhạy cảm** (Điều 4 NĐ 356/2025).
- **Hệ quả cho hệ thống:**
  - Cần sự đồng ý rõ ràng của VĐV cho từng mục đích.
  - Cần thông báo và đánh giá tác động xử lý dữ liệu.
  - Cần cân nhắc **chuyển dữ liệu ra nước ngoài**: các nền tảng cloud nước ngoài như Garmin/Oura API, Equivital, SlateSafety đều lưu dữ liệu ngoài VN.
  - Chi tiết thủ tục ❓, cần tư vấn pháp lý.
  - Đây là **lợi thế cho giải pháp lưu trữ trong nước**.

### 2.4. Rào cản tại VN (tổng hợp)

1. **Giá:**
   - CORE 2: khoảng 290–360 USD/người.
   - SlateSafety: khoảng 800 (tiền tệ ❓) + phí portal hằng năm.
   - Viên nang: khoảng 40–60 USD/viên, chưa tính bộ thu.
   - Tất cả đều không khả thi khi trang bị cho hàng nghìn người chạy.
2. **Không có kênh chính hãng** cho thiết bị ước tính Tc, nên không có bảo hành hay hỗ trợ kỹ thuật.
3. **Ngôn ngữ:** không sản phẩm nào có tiếng Việt cho ban y tế. Thiết bị tiêu dùng có thể có tiếng Việt ở giao diện, nhưng không có tính năng nhiệt.
4. **API:** truy cập dữ liệu thiết bị VĐV tự mang bị hạn chế.
   - Garmin: phí license hoặc yêu cầu số lượng tối thiểu (MOQ), có thể đang tạm dừng nhận đơn.
   - Oura: cần membership.
   - Whoop: chủ yếu dữ liệu tóm tắt.
   - **Giải pháp thực tế:** đọc HR trực tiếp qua **BLE Heart Rate Profile/ANT+ broadcast**, hoặc nhập file FIT sau giải.
5. **Pháp lý TTBYT + dữ liệu nhạy cảm** (xem 2.2–2.3).

---

## 3. Sáng chế (sàng lọc sơ bộ, Google Patents / USPTO qua WebSearch)

| Số | Tên / nội dung | Chủ sở hữu | Trạng thái (theo Google Patents, không phải kết luận pháp lý) | Liên quan |
|---|---|---|---|---|
| **US 10,702,165 B2** | *Estimation of human core temperature based on heart rate*: EKF từ HR → Tc (ECTemp) | **U.S. Dept. of the Army**; tác giả Buller MJ | Active; cấp 07/07/2020; ưu tiên 12/2012; **hết hạn dự kiến 16/12/2033** (MTEC) | **Lõi ECTemp.** Đã cấp phép không độc quyền cho Zephyr và EVALAN |
| **US 12,426,839 B2** | *Method for estimating core body temperature*: EKF trên mô hình **sigmoid** HR ↔ Tc, khởi tạo Tc từ HR đầu tiên hoặc giá trị nghỉ | U.S. Army; Buller MJ, Looney DP | Active; công bố 30/09/2025; ưu tiên 07/02/2019 | Phiên bản cải tiến của ECTemp |
| **US 2021/0338173 A1; EP 4144068 A1** | *Predicting exertional heat stroke with a worn sensor*: chỉ số mất ổn định dáng đi (gia tốc 3 trục) + Tc ước tính từ HR → điểm nguy cơ EHS | Chính phủ Mỹ (Army) là applicant EP; MIT TLO liệt kê | **Đơn đã công bố**, chưa thấy bằng cấp ❓ | Trùng ý tưởng "Tc + gait → cảnh báo EHS" (Buller 2022, BJSM) |
| US 11,540,723 B2; US 11,517,203 B2 | *Real-time estimation of human core body temperature based on non-invasive physiological measurements* | ❓ (có trong danh mục MTEC) | ❓ | Cần đọc claims |
| US 11,089,961 B2 | Theo dõi Tc bằng kênh dòng nhiệt + 2 cảm biến + "thermal cage" | Thalman Health Ltd → **James Foody** | Active | Lớp B |
| US 10,709,384 B2 | Thiết bị đeo đo dòng nhiệt (làm mát bay hơi) → Tc | MC10, Inc. | ❓ | Lớp B |
| US 11,647,954 B2 | *Ear device for heat stroke detection*: Tc, tốc độ mồ hôi, Na⁺ | ❓ | Đã cấp (B2) | Thiết bị tai + cảnh báo |
| US 12,629,034 | *Electronic device and method of estimating core body temperature* | ❓ (có thể là hãng điện tử tiêu dùng) | ❓ | Cần kiểm tra; có thể liên quan Samsung |
| US 8,930,147 B2 | *Multi-sensor patch and system* | Prima-Temp Inc. | **Expired – fee related** | Không cản trở |
| US 8,511,892 | *Device for measuring body core temperature* (dòng Dräger?) | ❓ | ❓ | Sản phẩm Tcore đã ngừng bán |
| JP 6675552 B2 | Thiết bị ước tính nhiệt độ sâu | ❓ | ❓ | Nhật |
| greenteg (CORE/CALERA) | Hãng nói "patented heat flux sensing"; **không tìm thấy số patent** | — | ❓ | — |
| Biodata Bank | Hãng nói có patent cụm cảm biến dòng nhiệt; số ❓ | — | ❓ | — |
| Kenzen | **Không tìm thấy patent** | — | — | — |

**Nhận định sơ bộ về tự do vận hành (FTO; không thay tư vấn SHTT):**
- **Tại Mỹ:** phương pháp HR → EKF → Tc (ECTemp) bị **US 10,702,165 bảo hộ đến khoảng 2033**, và biến thể sigmoid được **US 12,426,839** bảo hộ. Thương mại hoá tại Mỹ cần **xin license** (USARIEM có chương trình chuyển giao; ECTemp/iHATT từng nhận giải FLC 2023) hoặc thiết kế khác đi.
- **Tại VN:** patent có tính lãnh thổ. **Chưa tra WIPO Patentscope / IP Lib (Cục SHTT)** xem các patent trên có đơn tại VN không. Đây là việc bắt buộc trước khi thương mại hoá.
  - Phương trình Buller 2013 đã công bố công khai, nên việc dùng cho **nghiên cứu khoa học** thường ít rủi ro; mức độ miễn trừ cụ thể theo Luật SHTT VN ❓.
- **Tổ hợp "Tc + dáng đi → EHS":** Army đã nộp đơn (US/EP). Nếu hệ thống dùng gait, cần đọc claims.
- **Tổ hợp "WBGT + HR thiết bị tự mang + phác đồ can thiệp cho ban y tế giải chạy":** **không tìm thấy** patent nào nhắm trực tiếp. Đây là sàng lọc từ khoá giới hạn, độ tin cậy thấp.

---

## 4. Ma trận khoảng trống

Ký hiệu: ✔ có · ◐ một phần · ✘ không · ❓ chưa rõ

| Chức năng | CORE 2 / CALERA | Equivital / Zephyr (ECTemp) | SlateSafety BAND V2 | Samsung SmartThings Pro Heat | Biodata Bank CANARIA+ | EVALAN ARMOR | Đồng hồ tiêu dùng | Epicore / Nix (mồ hôi) | Viên nang | Kestrel 5400 |
|---|---|---|---|---|---|---|---|---|---|---|
| Đo Tc trực tiếp | ✘ | ◐ (nhận viên nang) | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | ✔ | ✘ |
| Ước tính Tc không xâm lấn | ✔ (sai số không đều) | ✔ (kém ở > 39 °C) | ✔ (kém, Callihan 2024) | ✔ (chưa có kiểm định độc lập ❓) | ◐ (xu hướng Tc) | ✔ (ECTemp) | ✘ | ✘ | — | ✘ |
| Tầng môi trường (WBGT) | ✘ | ✘ | ✘ | ◐ (nhiệt độ, độ ẩm tại chỗ) | ✘ | ✘ | ✘ | ✘ | ✘ | ✔ |
| Cảnh báo thời gian thực cho người đeo | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✘ | ◐ | ◐ | ✔ (môi trường) |
| Dashboard đội nhóm / ban y tế | ✘ | ✔ (B2B) | ✔ | ✔ | ◐ | ✔ (tablet) | ✘ | ✔ (B2B, Coaches) | ◐ | ◐ (LiNK) |
| Quy mô hàng nghìn người, đeo một lần | ✘ | ✘ | ✘ | ◐ (cần Galaxy Watch) | **✔** (dùng một lần, không sạc) | ✘ | ◐ (VĐV tự mang) | ◐ | ✘ | — |
| Nhận dữ liệu từ thiết bị VĐV **tự mang** | ◐ (chính nó là thiết bị) | ✘ | ✘ | ✘ (chỉ Galaxy Watch) | ✘ | ◐ (đai HR) | — | ✘ | ✘ | — |
| Gắn **phác đồ can thiệp lâm sàng** (EHS: ngâm nước lạnh; hạ natri máu; tiêu cơ vân; tim) | ✘ | ✘ | ◐ (khuyến nghị nghỉ) | ◐ (lệnh nghỉ) | ✘ | ✘ | ✘ | ◐ (bù dịch, điện giải) | ✘ | ◐ (bảng làm việc/nghỉ) |
| Bao phủ ngoài EHS (natri, tim) | ✘ | ◐ (ECG) | ✘ | ✘ | ✘ | ✘ | ◐ (cảnh báo nhịp tim) | ◐ (Na⁺ ước tính) | ✘ | ✘ |
| Hiệu chỉnh cho **người Việt / nóng ẩm VN** | ✘ | ✘ (de Korte 2022: 31,6 °C/74% RH, VĐV châu Âu) | ✘ | ✘ (Hàn Quốc) | ❓ (Nhật, nóng ẩm) | ✘ | ✘ | ✘ | — | ✘ |
| **Tiếng Việt** | ✘ | ✘ | ✘ | ◐ (Samsung có hạ tầng VN ❓) | ◐ (giao diện không phụ thuộc ngôn ngữ) | ✘ | ◐ | ✘ | ✘ | ✘ |
| Có tại VN | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | ✔ | ✘ | ✘ | ❓ |
| Giấy phép y tế | ✘ (wellness) | ✔ FDA 510(k) | ❓ | ❓ | ❓ | ❓ | ✘ | ✘ | ✔ FDA/CE | — |
| Giá phù hợp quy mô marathon VN | ✘ (khoảng 300 USD) | ✘ | ✘ | ◐ | ◐ (giá ❓) | ✘ | ✔ (VĐV tự trang bị) | ✘ | ✘ | ✔ (vài trạm) |
| Trạng thái thị trường | 🟢 | 🟢 / 🟡❓ | 🟢 | 🟡 | 🟢 (Nhật) | 🟡❓ | 🟢 | 🟢 | 🟢❓ | 🟢 |

### Kết luận: "Giải pháp tích hợp đã có trên thị trường chưa?"

**Câu trả lời: các thành phần đã có, nhưng chưa có giải pháp tích hợp đầy đủ cho bối cảnh giải chạy hoặc đội tuyển tại Việt Nam.**
Độ tin cậy: trung bình. Lý do: chỉ dựa trên đoạn trích tìm kiếm, và thị trường B2B châu Á (Nhật, Hàn) thay đổi nhanh.

**Phần đã có, không nên làm lại:**
- Phần cứng ước tính Tc (CORE 2, viên nang làm chuẩn).
- Thuật toán ECTemp (đã công bố; có patent tại Mỹ).
- Mô hình "đồng hồ thông minh + nhân trắc + môi trường → Tc → cảnh báo nhiều mức → lệnh nghỉ từ quản lý". Samsung (2025–2026) và các nền tảng lao động (SlateSafety, Equivital, ARMOR) đã làm mô hình này.
- Thiết bị dùng một lần quy mô lớn cho sự kiện thể thao: CANARIA+ ở Tokyo 2025, nhưng chỉ cho nhân viên.

**Khoảng trống thực sự (cơ hội):**
1. **Hướng tới ban y tế giải chạy đông người**, tức là VĐV chứ không phải người lao động. Cần nhận dữ liệu HR từ **thiết bị VĐV tự mang** qua BLE/ANT+ hoặc FIT, thay vì bắt mua thiết bị riêng.
2. **Cảnh báo nhiều tầng gắn trực tiếp với phác đồ can thiệp lâm sàng** cho EHS (ngâm nước lạnh tại chỗ), hạ natri máu do gắng sức (EAH), tiêu cơ vân và sự cố tim, kèm điều phối đội cứu thương theo vị trí. Không sản phẩm nào làm việc này; các sản phẩm hiện có chỉ dừng ở "nghỉ / uống nước".
3. **Hiệu chỉnh và kiểm định trên VĐV Việt Nam trong điều kiện nóng ẩm.** Tất cả thuật toán hiện có đều kém ở Tc > 39 °C (de Korte 2022; Hintz 2023; Stevenson 2026). Một nghiên cứu hiệu chỉnh bằng viên nang là đóng góp khoa học thực sự.
4. **Tiếng Việt, lưu trữ dữ liệu trong nước** (phù hợp Luật BVDLCN 2025 / NĐ 356/2025), **chi phí thấp**.
5. **Định vị pháp lý rõ ràng:** công cụ hỗ trợ quyết định cho ban y tế, hoặc đăng ký TTBYT nếu tuyên bố chẩn đoán.

**Rủi ro cạnh tranh cần theo dõi:**
- Samsung mở SmartThings Pro Heat Stress sang VN (Samsung có hiện diện sản xuất lớn tại VN).
- Biodata Bank mở rộng sang Đông Nam Á.
- Equivital thông qua ST Engineering (Singapore).

---

## 5. Việc còn mở cho `evidence-verifier` / orchestrator

- Đối chiếu trực tiếp các mục sau (bị chặn truy cập web trong phiên này): K210924, K113054, K113045 tại accessdata.fda.gov; US 10,702,165 và US 12,426,839 tại patents.google.com.
- Xác nhận Kenzen và Bodytrak đã đóng cửa bằng nguồn thứ hai: Secretary of State Missouri/Delaware; Companies House (UK).
- Tra **IP Lib / WIPO Patentscope** xem các patent ECTemp có đơn tại VN không.
- Đọc **Phụ lục I TT 05/2022/TT-BYT** (bản hợp nhất mới nhất, gồm TT 59/2025 và TT 24/2026 ❓) để chốt mức phân loại cho viên nang và phần mềm cảnh báo.
- Giá CANARIA+, giá Samsung SmartThings Pro; khả năng giao CORE 2 tới VN; giá trên Shopee/Lazada VN.
- Trạng thái myTemp, VitalSense, hDrop, Gx Sweat Patch năm 2025–2026.

---

## 6. Nguồn (truy cập 2026-10-24, qua WebSearch)

**Giấy phép / FDA / CE**
- https://510k.innolitics.com/device/K210924 ; https://www.regdatalab.com/510k/K210924 ; https://accessgudid.nlm.nih.gov/devices/03665810000168
- https://510k.innolitics.com/device/K113054 ; https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm?ID=K113054 ; https://accessgudid.nlm.nih.gov/devices/05060483830056
- https://www.accessdata.fda.gov/cdrh_docs/pdf11/k113045.pdf ; https://www.510kdatabase.net/k113045/
- https://accessgudid.nlm.nih.gov/devices/00606959021648 (VitalSense)
- https://www.cosinuss.com/en/2023/02/06/cosinuss-receives-medical-ce-certificate-mdr-for-its-c-med-alpha-in-ear-vital-signs-sensor ; https://www.cosinuss.com/wp-content/uploads/2025/07/cos_datasheet_cmed_en_1603891941_v08.pdf
- https://www.greenTEG.com/uploads/CORE_Spec_Sheet_V1_9_9_9f803ef780.pdf ; https://corebodytemp.com/pages/faq ; https://corebodytemp.com/disclaimer

**Trạng thái / giá**
- CORE 2: https://www.nordicsemi.com/Nordic-news/2025/09/CORE-2-integrates-Nordic-nRF52840-to-deliver-real-time-performance-insights-to-athletes ; https://ces.tech/ces-innovation-awards/2025/core-2-thermal-sensor ; https://www.bike-components.de/en/greenTEG/CORE-2-Temperature-Sensor-p215882/ ; https://www.mantel.com/fi/core-2-thermal-sensor
- CALERA: https://shop.greenteg.com/core-body-temperature/caleraresearch ; https://onlinelibrary.wiley.com/doi/full/10.1002/ajim.70103
- Dräger Tcore: https://www.draeger.com/en_me/Products/Tcore-Temperature-Monitoring-System
- Kenzen: https://pitchbook.com/profiles/company/124141-42 ; https://www.mobihealthnews.com/news/employee-health-company-kenzen-begins-partnership-examinetics-and-receives-investment ; https://ringland.com/construction-heat-safety-technology-smart-ppe-wearables-2025/
- Bodytrak: https://pitchbook.com/profiles/company/125262-28
- Zephyr: https://en.wikipedia.org/wiki/Zephyr_Technology
- Equivital: https://equivital.com/?p=6857 (10/11/2025, ST Engineering)
- SlateSafety: https://skcinc.com/products/band-v2 ; https://skcinc.com/products/band-v2-annual-software-service-subscription ; https://www.levitt-safety.com/Marques/Slate-Safety/Catalogue/Fast-Track/Heat-Stress ; https://ohsonline.com/directory/2024/08/prevent-heat-stress-with-slatesafety.aspx
- EVALAN ARMOR: https://evalan.com/products/armor/ ; https://www.computable.nl/?p=289804
- Samsung: https://www.wareable.com/samsung/samsung-galaxy-watch-heat-stress-tracking-platform-korea ; https://www.sammobile.com/news/galaxy-watch-can-help-manage-heat-stress-for-outdoor-workers/ ; https://vnreview.vn/threads/samsung-galaxy-watch-canh-bao-soc-nhiet-ca-nhan-hoa-bao-ve-cong-nhan-giua-nang-nong.88096/
- Biodata Bank: https://www.renesas.com/en/about/customer-success-stories/biodata-bank ; https://kingsalmon.metro.tokyo.lg.jp/en/world-athletics2025/biodata-bank_final.html
- Hexoskin: https://support.hexoskin.com/how-much-does-hexoskin-cost ; https://api.hexoskin.com/docs/
- Epicore: https://pulse2.com/epicore-biosystems-26-million-series-b-raised-to-advance-sweat-sensing-wearables-platform ; https://www.ishn.com/articles/114896-epicore-biosystems-and-reus-cares-partner-to-combat-heat-stress-in-agritech-workers
- Nix: https://insider.fitt.co/?p=32991 ; https://bicycleretailer.com/announcements/2025/01/14/uci-approves-nix-biosensors-personalized-hydration-monitoring-technology
- hDrop: https://hdroptech.com/product/hdrop-device/
- Gx: https://www.cnbc.com/2021/03/01/gatorade-launches-gx-sweat-patch-that-measures-sweat-hydration-levels.html
- CorTemp: https://buyersguide.ohsonline.com/company/297786/products/26215/cortemp-ingestible-core-body-temperature-monitoring-system ; https://www.businessobserverfl.com/article/cortemp-ingestible-body-temperature-sensor-and-cortemp-data-recorder
- myTemp: https://researchonline.ljmu.ac.uk/id/eprint/6799/
- Kestrel: https://kestrelmeters.com/products/kestrel-5400-heat-stress-tracker ; https://www.instrumentchoice.com.au/products/ic-0854vtan
- NIOSH app: https://www.cdc.gov/Niosh/Topics/HeatStress/HeatApp.html
- API: https://developer.garmin.com/gc-developer-program/health-api/ ; https://developer.garmin.com/health-sdk/questions-answers/ ; https://tryterra.co/blog/garmin-connect-developer-program-pause ; https://support.ouraring.com/hc/en-us/articles/4415266939155-The-Oura-API ; https://tryterra.co/blog/whoop-api-data-access-permissions-limitations-2026
- Nghiên cứu nguyên mẫu: https://www.mdpi.com/1424-8220/26/8/2556 ; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11769488/

**Việt Nam**
- Garmin: https://fptshop.com.vn/tin-tuc/tin-khuyen-mai/fpt-shop-tien-phong-hop-tac-cung-garmin-khai-truong-chuoi-garmin-brand-store-cao-cap-nhat-tai-viet-nam-145381 ; https://viettimes.vn/dong-ho-thong-minh-garmin-chinh-thuc-vao-viet-nam-gia-tu-2-trieu-dong-post50465.html
- Polar: https://www.brandsvietnam.com/congdong/topic/26270-Dong-ho-the-thao-do-nhip-tim-Polar-gia-nhap-duong-dua-thi-truong-Viet-Nam
- Ca bệnh tại giải chạy: https://plo.vn/2-nguoi-nhap-vien-cap-cuu-sau-khi-tham-gia-giai-chay-marathon-o-quang-binh-post802819.html ; https://viettimes.vn/tu-viec-nu-vdv-giai-marathon-tu-vong-dot-ngot-lam-the-nao-de-chay-bo-an-toan-post184343.html ; https://plo.vn/canh-bao-nguy-co-cac-vdv-marathon-tu-vong-va-loi-khuyen-cua-bac-si-post782430.html
- TTBYT: https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Nghi-dinh-07-2023-ND-CP-sua-doi-Nghi-dinh-98-2021-ND-CP-quan-ly-trang-thiet-bi-y-te-557403.aspx ; https://caselaw.vn/van-ban-phap-luat/411561-nghi-dinh-so-04-2025-nd-cp-ngay-01-01-2025-cua-chinh-phu-sua-doi-nghi-dinh-98-2021-nd-cp-ve-quan-ly-thiet-bi-y-te-da-duoc-sua-doi-theo-nghi-dinh-07-2023-nd-cp ; https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Van-ban-hop-nhat-05-VBHN-BYT-2025-Nghi-dinh-quan-ly-thiet-bi-y-te-649819.aspx ; https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Thong-tu-05-2022-TT-BYT-huong-dan-Nghi-dinh-98-2021-ND-CP-quan-ly-thiet-bi-y-te-499978.aspx ; https://luatvietnam.vn/co-cau-to-chuc/thong-tu-44-2025-tt-byt-quy-dinh-phan-cap-va-quan-ly-thiet-bi-y-te-bo-y-te-419365-d1.html
- Dữ liệu cá nhân: https://sbv.gov.vn/en/w/tri%E1%BB%83n-khai-thi-h%C3%A0nh-lu%E1%BA%ADt-b%E1%BA%A3o-v%E1%BB%87-d%E1%BB%AF-li%E1%BB%87u-c%C3%A1-nh%C3%A2n-1 ; https://www.ey.com/content/dam/ey-unified-site/ey-com/vi-vn/technical/tax/documents/ey-vietnam-legal-alert-march-2026-decree-no356-2025-nd-cp-providing-detailed-guidance-for-implementation-of-personal-data-protection-law-viet.pdf ; https://thuvienphapluat.vn/hoi-dap-phap-luat/tinh-trang-suc-khoe-la-du-lieu-ca-nhan-nhay-cam-tu-nam-2026-dung-khong-138076906.html
- Phòng stress nhiệt nơi làm việc (COHED): https://www.rockefellerfoundation.org/wp-content/uploads/Standard-Process-of-Heat-Stress-Prevention-at-Work-for-Workers.pdf

**Sáng chế**
- https://patents.google.com/patent/US10702165 ; https://mtec-sc.org/patents/US-10702165-B2
- https://patents.google.com/patent/US12426839 ; https://patentsgazette.uspto.gov/week39/OG/html/1538-5/US12426839-20250930.html
- https://patents.justia.com/patent/20210338173 ; https://data.epo.org/publication-server/rest/v1.2/patents/EP4144068NWA1/document.html ; https://tlo.mit.edu/industry-entrepreneurs/available-technologies/system-and-method-predict-exertional-heat-stroke
- https://patents.google.com/patent/US11089961 ; https://patents.google.com/patent/US10709384 ; https://patents.google.com/patent/US11647954/en ; https://patents.google.com/patent/US8930147 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11540723 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12629034
- USARIEM chuyển giao ECTemp: https://usariem.health.mil/index.cfm/media/news/article/2023/USARIEM_data_scientist_receives_FLC_excellence_in_technology_transfer_award
