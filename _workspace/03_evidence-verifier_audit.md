# 03 — Kiểm chứng bằng chứng (evidence-verifier audit)

*Agent:* evidence-verifier · *Ngày kiểm chứng / truy cập:* 2026-10-24
*Đầu vào:* `01_clinical-advisor_clinical.md`, `01_device-scout_devices.md`, `01_thermo-modeler_models.md`, `02_algorithm-engineer_{alert_engine.py, thresholds.json, prototype.md, sim_log.txt}`, `02_market-analyst_market.md`, `.claude/skills/core-temp-modeling/{scripts/heatstrain.py, references/equations.md}`.
*Phương pháp:*
- PubMed MCP: tra metadata **41 PMID**. Đọc toàn văn PMC của IOC 2021 (PMC8639927), de Korte 2022 (PMC9256956) và Hunt 2019 (PMC6567444). Toàn văn NATA 2015 (PMC4639891) trả về rỗng.
- WebSearch: số 510(k), sáng chế, văn bản pháp luật VN, trạng thái thị trường. WebFetch bị proxy chặn nên không mở trực tiếp được trang FDA, Google Patents hay thuvienphapluat; mọi kết luận về các nguồn này dựa trên đoạn trích tìm kiếm.
- Chạy lại `02_algorithm-engineer_alert_engine.py`: tự kiểm tra **ĐẠT (0 vi phạm)**. Tự tính lại đỉnh parabol ECTemp.

**Nhãn:** ✅ xác nhận · ⚠️ một phần / cần ghi rõ · ❌ sai, bắt buộc sửa · ❓ không kiểm chứng được

---

## Tóm tắt

| Nhãn | Số mục | Tỷ lệ |
|---|---|---|
| ✅ | 47 | 64 % |
| ⚠️ | 19 | 26 % |
| ❌ | 2 | 3 % |
| ❓ | 6 | 8 % |
| **Tổng** | **74** | |

**Kết luận chính**
1. **Hệ số ECTemp và PSI khớp nhau** giữa code (`heatstrain.py`), `equations.md`, `thermo-modeler` và `thresholds.json`.
   - ECTemp: a = 1; γ = 0,022²; b0 = −7887,1; b1 = 384,4286; b2 = −4,5714; σ = 18,88²; Tc0 = 37,1.
   - PSI: công thức khớp nguyên văn tóm tắt Moran 1998 trên PubMed.
   - Hệ số ECTemp so với **bản PDF gốc** của Buller 2013 chỉ đạt ⚠️: phương trình trong toàn văn PMC của Hunt 2019 bị mất khi trích xuất. Tuy vậy, hệ số nhất quán nội tại (σ = 356,45; đạo hàm c = −9,1428·Tc + 384,4286) và trình tự 6 phương trình khớp với Hunt 2019.
2. **Ngưỡng lâm sàng cốt lõi đã xác minh với toàn văn IOC 2021:**
   - EHS: *"generally ≥40.5 °C"* kèm rối loạn TKTW.
   - Ngừng làm mát khi Tre *"<39 °C"*, theo dõi ≥ 15 phút; giữ ấm nếu Tre *"rapid drop toward 36 °C"*.
   - Đo Tre: đầu dò ≥ 10 cm, do bác sĩ hoặc điều dưỡng dưới giám sát bác sĩ thực hiện.
   - Hai ngưỡng ACSM 38,6 °C và NATA 38,9 °C vẫn chỉ có nguồn thứ cấp (◐).
3. **Toàn bộ 41 PMID tra được đều tồn tại** và khớp tác giả đầu, năm, tạp chí. Không phát hiện trích dẫn ma.
4. **Số 510(k) K210924, K113054, K113045 và sáng chế US10702165, US12426839 đều đúng.** Lưu ý: K113054 và K113045 là clearance cho **máy theo dõi sinh lý / ECG**, **không** bao gồm chức năng ước tính Tc.
5. **Hai lỗi ❌ bắt buộc sửa:** (i) thư viện `heatstrain.py` tự nâng eTc lên **mức 4 "nghi EHS"**; (ii) device-scout còn viện dẫn **NĐ 13/2023**, văn bản đã bị thay thế.
6. **Quy tắc R8 và sàn 38,5 °C cho tốc độ tăng: ⚠️.** Không trái hướng dẫn quốc tế nào (không hướng dẫn nào đặt ngưỡng cho eTc), nhưng **mâu thuẫn với chính quy tắc R5 và mục tiêu "độ nhạy cao cho mức 3" của clinical-advisor**. Sàn 38,5 còn làm phần cộng +1 của SCR-R1 trở thành mã chết. Phân tích chi tiết ở §F.

---

## A. Hệ số và phương trình (code ↔ tài liệu ↔ bài gốc)

| # | Tuyên bố | Vị trí | Nhãn | Bằng chứng | Sửa đề xuất |
|---|---|---|---|---|---|
| 1 | Hệ số ECTemp (a, γ, b0, b1, b2, σ, Tc0) giống hệt nhau ở 4 nơi | heatstrain.py `ECTEMP_PARAMS`; equations.md §1; thermo §1.1; JSON `ectemp` | ✅ | Đối chiếu trực tiếp các file | — |
| 2 | Các hệ số này đúng như Buller 2013 | thermo §1.1 | ⚠️ | PMID 23780514 ([doi](https://doi.org/10.1088/0967-3334/34/7/781)): tóm tắt không có hệ số; phương trình trong PMC Hunt 2019 mất khi trích xuất. Nhất quán nội tại: 18,88² = 356,45; 2·b2 = −9,1428 | Đối chiếu Bảng 1 trong PDF Buller 2013 hoặc eq. 1–6 Hunt 2019 (qua thư viện ĐHYD) trước khi công bố |
| 3 | Bước lặp Kalman 6 phương trình (Tĉ, v̂, c, k, Tc, v) | heatstrain `ectemp()`; equations.md | ✅ | Hunt 2019 toàn văn ([doi](https://doi.org/10.1186/s40779-019-0208-7)) mô tả đúng trình tự eq. 1→6 | — |
| 4 | Đỉnh parabol ≈ 42,05 °C / 195 bpm; bảng HR(Tc) | thermo §1.1; JSON `hr_clip_src` | ✅ | Tính lại: Tc* = 42,047; HR* = 194,96. Bảng 37→41 °C khớp từng số | — |
| 5 | Kiểm định gốc: bias −0,03 ± 0,32 °C; LoA ±0,63 °C; n = 83; > 52 000 quan sát | equations.md; thermo; clinical R5 | ✅ | Tóm tắt PMID 23780514 | — |
| 6 | v0 = 0 khi Tc0 đo được; 0,01 (Hunt, Tc0 37,0); 0,02 (de Korte, Tc0 37,0) | thermo §1.1; equations.md | ✅ | Toàn văn Hunt 2019 ("37.0 °C … 0.01"); de Korte 2022 ("37.0 °C … starting variance of 0.02") | Có thể bỏ ❓ ở JSON `v0_src` |
| 7 | JSON dùng Tc0 = **37,1** cùng v0 = **0,02** | JSON `ectemp` | ⚠️ | Không nguồn nào dùng cặp này: de Korte dùng 37,0/0,02; Buller dùng 37,1 | Thống nhất một trong hai: 37,0 + 0,02 (de Korte) hoặc 37,1 + 0,01–0,02, ghi rõ là lựa chọn |
| 8 | de Korte 2022 dùng bản ECTemp **sigmoid** | thermo §1.3 | ✅ | Toàn văn: "Kalman filter and a sigmoid curve (Looney)" | — |
| 9 | Phần bù R5 (+0,5 °C) dựa trên de Korte, nhưng engine chạy bản **bậc 2** | JSON `etc_safety_offset_src` | ⚠️ | Độ nhạy theo ngưỡng của de Korte đo trên bản sigmoid. Hunt 2019 (bậc 2, đồ EOD) hỗ trợ khoảng bù 0,6 °C | Ghi rõ khác biệt phiên bản; R5 dựa chủ yếu vào Hunt 2019 |
| 10 | de Korte: bias 0,15 ± 0,36 (tóm tắt ghi ± 0,29); LoA ±0,45; RMSE 0,35. Tại đỉnh: LoA ±0,92, RMSE 0,47. Độ nhạy 96/88/48/13/4/0 % ở ngưỡng 38,0…39,75 °C | thermo; device-scout; JSON | ✅ | Bảng 2 toàn văn PMC9256956 | — |
| 11 | Hunt 2019: ngưỡng ECTemp 38,4 °C bảo vệ khỏi Tc > 39,0 °C (độ nhạy 86 %, 19/22 điểm); bias −0,32 khi Tc > 38,5 | thermo; JSON R5 | ✅ | Toàn văn PMC6567444 | — |
| 12 | PSI = 5(Tc−Tc0)/(39,5−Tc0) + 5(HR−HR0)/(180−HR0) | heatstrain `psi()`; equations; CSV SCR-P1 | ✅ | Tóm tắt PMID 9688970 ([doi](https://doi.org/10.1152/ajpregu.1998.275.1.R129)) | — |
| 13 | Thang PSI 5 mức (0–2 … 9–10) | equations.md §3 | ❓ | Tóm tắt Moran không có thang này | Giữ ❓ hoặc trích nguồn thứ cấp cụ thể |
| 14 | Engine tính PSI với **HRmax cá nhân** thay cho 180 | alert_engine `psi.use_personal_hrmax` | ⚠️ | Khác công thức gốc. Hợp lý theo Buller 2023 (PSI "quá cao" ở VĐV) nhưng ngưỡng 7/9 không còn cùng thang với Moran | Gọi là "PSI-HRmax (biến thể)", không gọi "PSI Moran" trên dashboard |
| 15 | aPSI: Tc_crit = 39,5 + ((Tc−Tsk)−4)/4; HR_crit = 0,9·(220−tuổi) | JSON `apsi`; thermo §5.2 | ❓ | Tóm tắt Buller 2023 chỉ nêu nguyên lý (điều chỉnh theo Tc−Tsk), không có công thức. JSON đang để `enabled: true` | Đặt `enabled: false` mặc định cho tới khi đối chiếu Buller 2023 hoặc sáng chế |
| 16 | Buller 2023: PSI 11,4 so với 7,6; aPSI 9,9 so với 9,0; Tc 40,1 so với 38,4 | thermo §5.2 | ✅ | PMID 37703905 ([doi](https://doi.org/10.1088/1361-6579/acf991)) | — |
| 17 | Buller 2025: aPSI 86,7 %, Tsk 83,3 %, PSI 63,3 %, Tc−Tsk 60 %, ECTemp 23,3 %; ~35 phút; ~15 % dương tính giả; n = 5080; 30 ca | thermo; equations; JSON | ✅ | PMID 40930133 ([doi](https://doi.org/10.1088/1361-6579/ae05ae)) | equations.md ghi "87 %": nên ghi 86,7 % |
| 18 | Buller 2022: ECTemp + dáng đi phát hiện 6/6 ca EHS, sớm ≥ 3,5 phút, dương tính giả 6,1 %; ECTemp của ca EHS 39,2–40,8 °C | thermo; device-scout; JSON `gait` | ✅ | PMID 35022161 ([doi](https://doi.org/10.1136/bjsports-2021-104081)). Bổ sung: Tre của cả 6 ca > 41 °C | — |
| 19 | Gunga 2008, *J Therm Biol* 33(5):297–307 | thermo; equations | ✅ | Kho SINTEF; DOI 10.1016/j.jtherbio.2008.03.004 | — |
| 20 | Gunga 2009, *Respir Physiol Neurobiol* 169 Suppl 1:S63 | thermo | ✅ | PMID 19428314 | — |
| 21 | Tc = T1 + K·(T1 − T2) | heatstrain `double_sensor()` | ⚠️ | Đúng nguyên lý dòng nhiệt; giá trị K trong Gunga 2008 chưa đọc được | Giữ ghi chú "K phải hiệu chỉnh" |
| 22 | Looney 2018, *JMPB* 1:79–86: sigmoid bias −0,04, RMSE 0,26 °C; bậc 2 bias −0,19, RMSE 0,35 °C; n = 16 | thermo §1.2 | ✅ | WebSearch (academia.edu, UW thesis); không có trên PubMed. Có bản đính chính | Ghi chú "có correction" |
| 23 | Davey 2021: PSI/aPSI cuối không phân biệt TTL; tốc độ thay đổi (ROC) thì phân biệt được | thermo; JSON R8 | ✅ | PMID 33677693 | — |
| 24 | "Buller 2017, *J Appl Physiol* 124:432" | thermo §5.2 | ⚠️ | PMID 28798200: xuất bản 2018 (epub 2017). Danh mục tham khảo #45 ghi 2018 | Sửa thành 2018 cho thống nhất |

## B. Ngưỡng: JSON ↔ bảng CSV lâm sàng ↔ hướng dẫn

| # | Tuyên bố | Vị trí | Nhãn | Bằng chứng | Sửa đề xuất |
|---|---|---|---|---|---|
| 25 | EHS = Tre ≥ 40,5 °C + rối loạn TKTW; ngưỡng cũ > 40 °C | CSV DX-T1; JSON `clinical.tre_ehs` | ✅ | IOC 2021 toàn văn: "generally ≥40.5 °C … 40.5 °C may be more specific" ([doi](https://doi.org/10.1136/bjsports-2020-103854)) | — |
| 26 | Ngừng làm mát ở Tre 39,0 °C; theo dõi ≥ 15 phút; ngâm lại nếu Tre tăng | CSV DX-T3; JSON `tre_stop_cooling` | ✅ | IOC 2021: "until the rectal temperature reaches <39 °C … stabilised … at least 15 min" | Nhỏ: IOC dùng "<39"; code dùng `<=`. Không ảnh hưởng thực hành |
| 27 | ACSM 2021/2023: ngừng làm mát ở 38,6 °C | clinical §3.2 | ⚠️ | Chỉ có tóm tắt NAEMSP. Nguồn gốc ngưỡng 38,6 là nghiên cứu *J Athl Train* 2010 (PMC2938313) | Giữ ◐; đối chiếu toàn văn ACSM 2023 |
| 28 | NATA 2015: ≈ 38,9 °C (102 °F); tóm tắt điều hành ghi < 102,5 °F (39,2 °C) trong 30 phút | clinical §3.2 | ⚠️ | WebSearch xác nhận 102,5 °F (tóm tắt điều hành). Con số 38,9 °C chưa xác nhận; PMC4639891 trả về rỗng | Giữ ◐ |
| 29 | Tốc độ làm mát > 0,15 °C/phút tốt; ≥ 0,08 chấp nhận được | CSV DX-T5; JSON | ⚠️ | Chỉ nguồn thứ cấp (ACSM) | Giữ ◐ |
| 30 | Tre giảm nhanh về 36 °C → giữ ấm | CSV DX-T4; JSON `tre_overcool` | ✅ | IOC 2021: "rapid drop toward 36 °C … dried … insulated" | — |
| 31 | WBGT cờ ACSM: xanh < 18; vàng 18–23; đỏ 23–28; đen > 28 °C | CSV ENV-0..3; JSON `wbgt_flags` | ⚠️ | Nguồn thứ cấp nhất quán (≈ 65/73/82 °F). Văn bản ACSM 1996 chưa đọc. JSON 28,0001 thể hiện đúng "> 28" | Giữ ◐ |
| 32 | Ngưỡng eTc 38,5 / 39,0 / 39,5 / 40,0 → mức 1 / 2 / 3 / 3 | JSON `etc_levels` ↔ CSV SCR-T1..T4 | ✅ | Khớp từng dòng | — |
| 33 | Nguồn cho SCR-T2/T3 là Gribok 2010 (alert 39, alarm 39,5) | JSON; CSV | ⚠️ | PMID 20371418: ngưỡng 39/39,5 có thật, nhưng áp cho Tc **dự báo bằng mô hình AR từ Tc đo được**, không phải eTc từ HR | Ghi "ngưỡng tham khảo từ mô hình AR; áp cho eTc là ngoại suy (expert)" |
| 34 | PSI ≥ 7 → mức 2; ≥ 9 → mức 3 (cả PSI và aPSI) | JSON ↔ CSV SCR-P1/P2 | ✅ | Khớp; đã gắn expert | — |
| 35 | EAH: Na⁺ < 135 mmol/L | CSV LAB-NA1; JSON `eah.na_low` | ✅ | WMS 2019, PMID 32044213 | — |
| 36 | Kim 2012: 0,54/100 000 người; 71 % tử vong | clinical §4 | ✅ | PMID 22236223 | — |
| 37 | R5: bù ~0,5 °C | clinical R5; JSON | ✅ | Phù hợp Hunt 2019 (39,0 − 38,4 = 0,6 °C) | — |
| 38 | **heatstrain.py `DEFAULT_THRESHOLDS`: eTc ≥ 40,0 → mức 4 "NGUY HIỂM – nghi EHS"; cộng mức do tốc độ tăng có thể đưa lên 4** | `.claude/skills/core-temp-modeling/scripts/heatstrain.py` | ❌ | Mâu thuẫn R3 (eTc tối đa mức 3), IOC 2022 ("too early to take individual decisions … based on portable technology alone") và IOC 2021 (EHS cần Tre + TKTW). Ngoài ra ECTemp có độ nhạy chỉ 4 % ở > 39,5 °C | Đổi dòng 40,0 thành **mức 3** "Nguy cơ cao – dừng, cần nhân viên y tế đánh giá TKTW + đo Tre"; giới hạn `classify()` bằng `min(level+1, 3)` |
| 39 | Oyama 2023: ngưỡng 28 °C có thể nguy hiểm, đề xuất 24–27 °C | clinical ENV-3 | ✅ | PMID 38577294 (tồn tại; con số lấy theo clinical) | — |

## C. Trích dẫn PubMed (tồn tại, tác giả, năm, tạp chí)

| # | Tuyên bố | Nhãn | Bằng chứng |
|---|---|---|---|
| 40 | 41 PMID (danh sách ở cột Bằng chứng) tồn tại, khớp tác giả đầu, năm, tạp chí | ✅ | 23780514 Buller 2013 · 9688970 Moran 1998 · 35813051 de Korte 2022 · 37703905 Buller 2023 · 40930133 Buller 2025 · 35022161 Buller 2022 · 33888465 Hosokawa 2021 · 36150754 Racinais 2022/23 · 34524191 & 37036463 Roberts (ACSM) · 37036464 · 26381473 Casa (NATA) · 34502822 Verdel · 38950497 Januário · 31196190 Hunt · 20371418 Gribok · 18946156 Buller 2008 · 32044213 Bennett (WMS) · 26102445 Hew-Butler · 22236223 Kim · 33677693 Davey · 36919415 Hintz · 42613781 Stevenson · 42319298 Sakamoto · 28798200 Buller 2018 · 38577294 Oyama · 26069301 Racinais 2015 · 38425235 Eifling · 33655999 Nye · 23478560 Kazman · 37022963 Aylwin · 34723866 Namineni · 29803944 Welles · 23760405 Niedermann · 26963194 Seng · 19428314 Gunga 2009 · 42405303 Zhao 2026 · 36939844 Goods · 36796923 Daanen · 25967760 Buller 2015 · 32408286 Buller 2020 (cùng các DOI tương ứng) |
| 41 | Hintz 2023: 1364 học viên; ngưỡng ECT > 39,7 °C; độ nhạy 20 % (2/10 ca); độ đặc hiệu 98,9 % | ✅ | PMID 36919415 ([doi](https://doi.org/10.1080/00913847.2023.2190729)). Lưu ý: định nghĩa EHS trong bài là "approaching or > 40 °C" |
| 42 | Stevenson 2026: CCC 0,26–0,85; LoA 1,25–2,22 °C; RMSE tăng khi > 38,5 °C; Equivital tốt nhất khi vận động; CORE và Equivital tốt nhất khi gộp vận động + hồi phục | ✅ | PMID 42613781 ([doi](https://doi.org/10.1249/MSS.0000000000004113)) |
| 43 | Januário 2024: ICC 0,98; bias 0,01 °C; giới hạn −0,35/+0,38 °C | ✅ | PMID 38950497. Chuẩn tham chiếu là **viên nang**, không phải đo trực tràng; device-scout ghi "±0,37" là làm tròn |
| 44 | Verdel 2021: ~50 % cặp đo lệch > 0,3 °C | ✅ | PMID 34502822 |
| 45 | Sakamoto 2026: 162 người chạy, 27,2 °C, RH 87 %; đỉnh Tc 39,4 ± 0,6 °C; tối đa 41,1 °C | ✅ | PMID 42319298 |
| 46 | "ACSM 2023 sửa và thay thế toàn bộ bản 2021" | ⚠️ | Cả hai PMID tồn tại, cùng tiêu đề. Chưa xác minh được ghi chú "thay thế" |
| 47 | Looney 2018 *JMPB* (không có trên PubMed) | ✅ | WebSearch (xem #22) |
| 48 | Peggen 2024 và Lignier 2026 dùng bản ECTemp sigmoid | ❓ | Chưa đọc được bài |
| 49 | Zhao 2026: RMSE của EKF chỉ dùng HR là 0,41 / 0,66 °C so với 0,21–0,41 °C trong bài gốc | ✅ | PMID 42405303 |

## D. Thị trường, FDA, sáng chế

| # | Tuyên bố | Vị trí | Nhãn | Bằng chứng | Sửa đề xuất |
|---|---|---|---|---|---|
| 50 | e-Celsius **K210924**: SE ngày 28/06/2023; mã FLL; Class II; người ≥ 18 tuổi, > 80 lb, theo dõi > 6 h | market 1A | ✅ | regdatalab/510kdatabase; GUDID 03665810000168 | — |
| 51 | Equivital **K113054**: Hidalgo, 17/02/2012 | market 1C | ✅ | accessdata.fda.gov (đoạn trích); GUDID 05060483830056; 21 CFR 870.1025 | — |
| 52 | Cột "Giấy phép" của Equivital/Zephyr ngầm hiểu là FDA cho cả chức năng ước tính Tc | market 1C; device-scout C1/C2 | ⚠️ | K113054 = monitor đa thông số (ECG, nhịp thở, nhiệt độ da). K113045 = ECG một đạo trình. **Không** có clearance cho ECTemp/Tc | Thêm câu: "510(k) cho phần cứng theo dõi sinh lý; chức năng ước tính Tc (ECTemp) không thuộc phạm vi clearance" |
| 53 | Zephyr **K113045**: BioHarness 3.0, 14/08/2012, MHX, Class II; predicate K100040 | market 1C | ✅ | accessdata.fda.gov pdf11/k113045 | Cập nhật device-scout C2 (đang ghi "❓ cần số hồ sơ") |
| 54 | CorTemp **K880639** | device-scout; market | ✅ | Nhiều bản ghi GUDID (00857414006001…) ghi K880639, mã FLL | Có thể bỏ ❓ |
| 55 | **US 10,702,165 B2**: Department of the Army; Buller; cấp 07/07/2020; ưu tiên 20/12/2012; hết hạn dự kiến 16/12/2033 | market §5 | ✅ | MTEC; Google Patents; USPTO | — |
| 56 | **US 12,426,839 B2**: Buller & Looney; US Army; OG 30/09/2025; ưu tiên 07/02/2019 (US 2022/0125388 A1) | market §5; thermo | ✅ | USPTO Patents Gazette; Google Patents | Nội dung claim về sigmoid chưa đọc |
| 57 | ECTemp được cấp phép không độc quyền cho Zephyr và EVALAN | market; device-scout | ❓ | Không tìm được nguồn sơ cấp | Ghi ❓ |
| 58 | Dräger Tcore "End of Sales" | market 1B | ✅ | Trang Dräger nhiều vùng | — |
| 59 | Kenzen và Bodytrak "Out of Business" (PitchBook) | market | ❓ | Không có thông cáo; tin mới nhất 2021–2022. Đã gắn 🔴❓ là phù hợp | Giữ ❓, không viết "đã ngừng" |
| 60 | Samsung SmartThings Pro Heat Stress: ra mắt 09/2025, nâng cấp 07/2026, ngưỡng 33/35/38 °C | market | ✅ | wareable, sammobile, digitaltrends | — |
| 61 | CORE 2 không phải thiết bị y tế; 269,95 CHF lúc ra mắt | market 1B | ✅ | corebodytemp.com (FAQ, trang "medical use"), blog ra mắt | Có lịch sử EUA COVID-19 (COREmedical), đã ghi |

## E. Văn bản pháp luật Việt Nam

| # | Tuyên bố | Vị trí | Nhãn | Bằng chứng | Sửa đề xuất |
|---|---|---|---|---|---|
| 62 | NĐ 98/2021/NĐ-CP về quản lý TTBYT (hiệu lực 01/01/2022) | market §2.2 | ✅ | thuvienphapluat; VBHN 05/VBHN-BYT/2025 | — |
| 63 | NĐ 07/2023/NĐ-CP (03/03/2023) sửa NĐ 98 | market | ✅ | Bản tiếng Anh trên thuvienphapluat | — |
| 64 | NĐ 04/2025/NĐ-CP (01/01/2025) sửa Điều 76; giấy phép nhập khẩu 2018–2021 dùng đến 30/06/2025 | market | ✅ | caselaw.vn, luatvietan | Có thêm NĐ 96/2023 sửa NĐ 98 (TT 44/2025 viện dẫn), nên bổ sung |
| 65 | TT 05/2022/TT-BYT (hiệu lực 01/08/2022); bị sửa bởi TT 59/2025, TT 24/2026 | market | ⚠️ | Thông tư tồn tại; ngày hiệu lực và các văn bản sửa đổi chưa xác minh | Giữ ❓ cho phần sửa đổi |
| 66 | Luật BVDLCN 91/2025/QH15: thông qua 26/06/2025, hiệu lực 01/01/2026 | market | ✅ | VCCI, PwC, thuvienphapluat | Bổ sung NĐ 330/2026 về xử phạt (hiệu lực 19/8/2026, theo nguồn thứ cấp ❓) |
| 67 | NĐ 356/2025/NĐ-CP hướng dẫn luật, thay NĐ 13/2023, hiệu lực 01/01/2026 | market | ✅ | Ban hành 31/12/2025 (vbpl.moj.gov.vn) | — |
| 68 | "Tình trạng sức khoẻ" là dữ liệu nhạy cảm theo **Điều 4** NĐ 356/2025 | market | ❓ | Chưa đọc được văn bản để xác nhận số điều | Kiểm tra số điều |
| 69 | **"Dữ liệu sức khoẻ thuộc phạm vi NĐ 13/2023"** | `01_device-scout_devices.md` dòng 336 | ❌ | NĐ 13/2023 đã bị NĐ 356/2025 thay thế từ 01/01/2026 | Sửa thành: "Luật BVDLCN 91/2025/QH15 và NĐ 356/2025/NĐ-CP (hiệu lực 01/01/2026)" |

## F. Đánh giá quy tắc R8 và sàn 38,5 °C cho tốc độ tăng (algorithm-engineer)

Phần này chỉ đánh giá, không sửa code.

| # | Tuyên bố | Nhãn | Phân tích |
|---|---|---|---|
| 70 | **R8:** tín hiệu "căng thẳng" bị chặn ở mức 2. Lên mức 3 khi có tín hiệu cứng (dáng đi/gục, hoặc eTc thô ≥ 39,5) hoặc ≥ 2 phiếu | ⚠️ | **Phù hợp hướng dẫn quốc tế** về tinh thần: IOC 2022 không cho ra quyết định cá nhân chỉ dựa vào thiết bị; nhiều VĐV > 40 °C không có triệu chứng. Mức 2 vẫn điều người quan sát tới đánh giá TKTW, và R2 nâng lên mức 3 khi có dấu hiệu.<br>**Mâu thuẫn nội bộ** với clinical-advisor:<br>(a) R5 hạ ngưỡng eTc 0,5 °C để mức 3 kích hoạt từ eTc 39,0, nhưng R8 đòi eTc thô ≥ 39,5 mới là tín hiệu cứng. Ở ngưỡng này độ nhạy ECTemp chỉ khoảng 4 % (de Korte 2022), và 1/6 ca EHS trong Buller 2022 có ECTemp chỉ 39,2 °C. Như vậy R8 đảo ngược phần lớn tác dụng của R5 ở mức 3.<br>(b) clinical §2.3 viết "mục tiêu ưu tiên là độ nhạy cao cho mức 3, chấp nhận báo động giả".<br>(c) Các "phiếu độc lập" thực ra **không độc lập**: eTc, PSI, tốc độ tăng và HR ≥ 95 % HRmax đều suy ra từ cùng một chuỗi HR. WBGT đen là yếu tố chung cho cả đám đông.<br>Mô phỏng S2 cho thấy chế độ chỉ dùng HR (biến thể H) lên mức 3 muộn hơn 12 phút so với mặc định (p40 so với p28).<br>**Đề xuất cho clinical-advisor duyệt:**<br>(i) Gộp mọi tín hiệu suy từ HR thành tối đa 1 phiếu.<br>(ii) Thêm **bộ hẹn giờ leo thang**: mức 2 không được người quan sát xác nhận hoặc huỷ trong ≤ 5 phút → mức 3.<br>(iii) Hoặc coi eTc + bù ≥ 39,5 **kéo dài ≥ 3–5 phút** là tín hiệu cứng.<br>(iv) Báo cáo độ nhạy mức 3 riêng cho cấu hình chỉ dùng HR. |
| 71 | **Sàn tốc độ tăng:** chỉ xét SCR-R1 khi eTc ≥ 38,5 | ⚠️ | Lý do sinh lý (Tc tăng nhanh ở pha khởi động) là hợp lý, và không hướng dẫn nào quy định ngưỡng tốc độ. Nhưng có **lỗi logic**: khi eTc ≥ 38,5 thì eTc + bù R5 ≥ 39,0, tức đã ở mức 2 = `strain_cap`. Vì vậy phần +1 của SCR-R1 **không bao giờ thay đổi mức**, chỉ còn tác dụng như một phiếu R8. Điều này trái mục đích dòng CSV SCR-R1 ("nâng mức khi eTc tăng nhanh **dù chưa vượt ngưỡng tuyệt đối**") và bỏ phí tín hiệu mà Davey 2021 cho là phân biệt được.<br>**Đề xuất:** thay sàn eTc bằng **cửa sổ thời gian** (bỏ qua 20–25 phút đầu), hoặc hạ sàn xuống 38,0 với điều kiện tăng ≥ 0,5 °C/10 phút ở 2 cửa sổ liên tiếp. |
| 72 | R7: WBGT đỏ (≥ 23 °C) cộng +1 cho mọi người đã ở mức ≥ 1 | ⚠️ | Mô phỏng S1 (người chạy bình thường, Tc thật ≤ 38,4 °C) có **99/121 phút ở mức ≥ 2**. Sakamoto 2026 ghi Tc trung bình 38,5–38,7 °C ở người chạy phong trào tại Singapore. Như vậy ở giải VN có WBGT 23–28 °C (phổ biến), phần lớn đám đông sẽ ở mức 2 và đội quan sát sẽ quá tải. Không trái hướng dẫn, nhưng làm mức 2 mất giá trị phân loại | Cần clinical-advisor quyết định: chỉ áp R7 khi cờ đen (biến thể B), hoặc tách "mức 2 môi trường" (thông báo chung) khỏi "mức 2 cá nhân" (điều người quan sát) |
| 73 | "eTc thô (chưa bù R5)" trong tín hiệu cứng | ⚠️ | Code tính `etc + rf_offset`, tức đã cộng bù R6 | Sửa nhãn thành "eTc + R6, chưa R5" |
| 74 | equations.md: "Welles 2018 — aĉTemp dùng thêm gia tốc/nhiệt da" | ⚠️ | PMID 29803944: Kalman filter tuyến tính dùng Tsk + dòng nhiệt + HR; không có gia tốc. Tên "aĉTemp" chưa thấy | Sửa mô tả theo thermo §8 #5 |

---

## Sửa bắt buộc trước khi xuất bản (❌)

1. **`.claude/skills/core-temp-modeling/scripts/heatstrain.py` — `DEFAULT_THRESHOLDS` và `classify()`**
   - Hiện tại: dòng `(40.0, 4, "NGUY HIỂM – nghi say nắng gắng sức (EHS) …")` và `level = min(level + 1, 4)`.
   - Giá trị đúng: dòng 40,0 → **mức 3** (nhãn: "NGUY CƠ CAO – dừng vận động; nhân viên y tế đánh giá TKTW + đo Tre; chuẩn bị CWI"); `min(level + 1, 3)`. Mức 4 chỉ dành cho người xác nhận (Tre ≥ 40,5 °C + TKTW) hoặc nghi ngừng tim (R3/R4; IOC 2021 PMID 33888465; IOC 2022 PMID 36150754).
   - Lý do: baseline `heatstrain.run()` đang được dùng để so sánh trong prototype; người dùng thư viện riêng lẻ sẽ nhận cảnh báo "nghi EHS" chỉ từ thiết bị.
2. **`_workspace/01_device-scout_devices.md` dòng 336**
   - Hiện tại: "dữ liệu sức khoẻ thuộc phạm vi NĐ 13/2023".
   - Giá trị đúng: "**Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15** và **NĐ 356/2025/NĐ-CP** (thay NĐ 13/2023; hiệu lực 01/01/2026)".

## Cần thận trọng (⚠️ / ❓), xếp theo mức ưu tiên

1. **R8, sàn tốc độ tăng và R7** (#70–72): clinical-advisor cần duyệt trước khi đưa vào báo cáo. Ít nhất phải nêu rõ rằng R8 đánh đổi độ nhạy mức 3 lấy tải vận hành, và SCR-R1 hiện không nâng được mức.
2. **aPSI đang bật mặc định với công thức ❓** (#15): mô phỏng S2 lên mức 3 sớm một phần nhờ aPSI. Đề nghị tắt mặc định, hoặc trình bày kết quả có và không có aPSI.
3. **Phạm vi FDA của Equivital và Zephyr** (#52): không viết "thiết bị ước tính Tc được FDA cấp phép".
4. **Hệ số ECTemp so với PDF gốc** (#2) và cặp Tc0/v0 trong JSON (#7, #9).
5. **Ngưỡng ACSM 38,6 / NATA 38,9 / tốc độ làm mát / cờ WBGT** (#27–29, #31): còn ◐, cần toàn văn.
6. Gribok 2010 làm nguồn cho ngưỡng eTc (#33): ghi rõ là ngoại suy.
7. ❓ còn lại: thang PSI 5 mức (#13), Peggen và Lignier dùng sigmoid (#48), cấp phép ECTemp cho Zephyr/EVALAN (#57), Kenzen/Bodytrak đóng cửa (#59), số điều NĐ 356 (#68).
8. Sửa nhỏ: Buller 2017 → 2018 (#24); 87 % → 86,7 % trong equations.md (#17); mô tả Welles 2018 (#74); bổ sung NĐ 96/2023 (#64).

*Dữ liệu thư mục lấy từ PubMed (NLM), truy cập 2026-10-24. Nguồn web chính:*
- [510k K210924](https://www.regdatalab.com/510k/K210924)
- [K113054](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm?ID=K113054)
- [K113045](https://www.accessdata.fda.gov/cdrh_docs/pdf11/k113045.pdf)
- [GUDID CorTemp](https://accessgudid.nlm.nih.gov/devices/00857414006032)
- [US10702165 (MTEC)](https://mtec-sc.org/patents/US-10702165-B2)
- [US12426839 (USPTO OG)](https://patentsgazette.uspto.gov/week39/OG/html/1538-5/US12426839-20250930.html)
- [Dräger Tcore](https://www.draeger.com/en_uk/Products/Tcore-Temperature-Monitoring-System)
- [Samsung heat stress (Wareable)](https://www.wareable.com/samsung/samsung-galaxy-watch-heat-stress-tracking-platform-korea)
- [NĐ 356/2025](https://thuvienphapluat.vn/van-ban/Quyen-dan-su/Nghi-dinh-356-2025-ND-CP-huong-dan-Luat-Bao-ve-du-lieu-ca-nhan-687428.aspx)
- [NĐ 04/2025](https://caselaw.vn/van-ban-phap-luat/411561-nghi-dinh-so-04-2025-nd-cp-ngay-01-01-2025-cua-chinh-phu-sua-doi-nghi-dinh-98-2021-nd-cp-ve-quan-ly-thiet-bi-y-te-da-duoc-sua-doi-theo-nghi-dinh-07-2023-nd-cp)
- [NATA (tóm tắt điều hành)](https://www.nata.org/sites/default/files/heat-illness-executive-summary.pdf)
- [NAEMSP (ACSM)](https://naemsp.org/2019-7-5-feel-the-heat-managing-exertional-heat-stroke/)
- [Gunga 2008 (SINTEF)](https://sintef.no/en/publications/publication/1038916)
