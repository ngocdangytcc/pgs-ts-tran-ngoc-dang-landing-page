---
name: core-temp-research
description: Orchestrator nghiên cứu theo dõi nhiệt độ lõi & cảnh báo say nắng cho VĐV — điều phối đội 6 agent (thiết bị, thị trường, mô hình/phương trình, lâm sàng, thuật toán, kiểm chứng) để ra báo cáo tổng hợp + prototype cảnh báo. BẮT BUỘC dùng khi người dùng hỏi về thiết bị/phần mềm đo hoặc ước tính nhiệt độ lõi, nhiệt độ da, nhịp tim để cảnh báo heat stroke/say nắng/sốc nhiệt, căng thẳng nhiệt ở VĐV chạy bộ/thể thao/lao động nóng; "đã có trên thị trường chưa"; phương trình chuyển đổi; hệ thống cảnh báo & can thiệp. Cũng dùng cho việc tiếp theo: "chạy lại", "cập nhật báo cáo", "bổ sung thiết bị mới", "chỉ làm lại phần thị trường/phương trình/lâm sàng", "sửa ngưỡng cảnh báo", "dựa trên kết quả trước cải thiện…".
---
# Orchestrator: Nghiên cứu nhiệt độ lõi & cảnh báo say nắng

**Chế độ thực thi:** sub-agent (công cụ `Agent`, `model: "opus"`, chạy song song bằng `run_in_background`). Môi trường có `TeamCreate` thì có thể chuyển sang Agent Teams với cùng phân vai.
**Mẫu kiến trúc:** Fan-out/Fan-in (Phase 2) → Pipeline (Phase 3–4) → Producer-Reviewer (Phase 5).
Mỗi agent được gọi với `subagent_type: "general-purpose"`, prompt mở đầu: "Đọc `.claude/agents/<tên>.md` và làm theo; skill liên quan nằm ở `.claude/skills/...`", kèm đường dẫn đầu vào/đầu ra.

## Đội ngũ
| Agent | Skill | Đầu ra |
|---|---|---|
| device-scout | wearable-device-survey | `_workspace/01_device-scout_devices.md` |
| thermo-modeler | core-temp-modeling | `_workspace/01_thermo-modeler_models.md` |
| clinical-advisor | heat-illness-clinical | `_workspace/01_clinical-advisor_clinical.md` |
| market-analyst | wearable-device-survey (§3) | `_workspace/02_market-analyst_market.md` |
| algorithm-engineer | core-temp-modeling | `_workspace/02_algorithm-engineer_prototype.md` + `.py` |
| evidence-verifier | evidence-verification | `_workspace/03_evidence-verifier_audit.md` |

## Phase 0 — Kiểm tra ngữ cảnh
- Không có `_workspace/` → **chạy lần đầu**.
- Có `_workspace/` + người dùng yêu cầu sửa một phần → **chạy lại một phần**: chỉ gọi agent liên quan + các agent phía sau phụ thuộc nó + evidence-verifier.
- Có `_workspace/` + câu hỏi/phạm vi mới → chuyển `_workspace/` thành `_workspace_prev/` rồi chạy mới.

## Phase 1 — Brief
Viết `_workspace/00_brief.md`: câu hỏi nghiên cứu, đối tượng (VĐV chạy bền/thể thao, bối cảnh Việt Nam nóng ẩm), phạm vi, định nghĩa thuật ngữ, ngày thực hiện, yêu cầu riêng của người dùng.

## Phase 2 — Thu thập song song (fan-out)
Gọi đồng thời `device-scout`, `thermo-modeler`, `clinical-advisor` (`run_in_background: true`).

## Phase 3 — Kiểm tra thị trường + Thuật toán
Sau khi Phase 2 xong, gọi song song:
- `market-analyst` (cần file của device-scout): **sản phẩm đã có trên thị trường chưa**, trạng thái bán, Việt Nam, giấy phép, sáng chế, ma trận khoảng trống.
- `algorithm-engineer` (cần cả ba file Phase 2): prototype + mô phỏng.

## Phase 4 — Kiểm chứng
Gọi `evidence-verifier` trên toàn bộ `_workspace/01_*`, `02_*`. Nếu có ❌ ảnh hưởng hệ số/ngưỡng → gọi lại đúng agent sở hữu nội dung để sửa (tối đa 1 vòng), rồi kiểm chứng lại phần đó.

## Phase 5 — Tổng hợp báo cáo (orchestrator tự làm)
Viết `_workspace/04_final_report.md` (tiếng Việt), cấu trúc:
1. Tóm tắt điều hành (≤ 1 trang): trả lời thẳng "có thiết bị/phần mềm nào làm được chưa", độ tin cậy.
2. Nền tảng sinh lý: vì sao Tc, liên hệ Tc–HR–Tsk.
3. Thiết bị & phần mềm: bảng so sánh + độ chính xác.
4. **Hiện trạng thị trường**: trạng thái từng sản phẩm, tình hình tại Việt Nam, sáng chế, ma trận khoảng trống.
5. Phương trình & mô hình: công thức, tham số, độ chính xác, giới hạn.
6. Ngưỡng cảnh báo → can thiệp (bảng hành động) + chẩn đoán phân biệt.
7. Prototype hệ thống cảnh báo: kiến trúc, kết quả mô phỏng.
8. Đề xuất cho Việt Nam: hướng nghiên cứu kiểm định, lộ trình sản phẩm.
9. Giới hạn & kết quả kiểm chứng (tỷ lệ ✅/⚠️/❌/❓).
10. Tài liệu tham khảo (Vancouver, có DOI/PMID).
Chỉ đưa nội dung không bị ❌ (hoặc đã sửa). Giữ mâu thuẫn giữa nguồn kèm cả hai nguồn. Có thể xuất thêm HTML/DOCX nếu người dùng muốn.

## Xử lý lỗi
- Agent thất bại → thử lại 1 lần; thất bại lần 2 → tiếp tục không có phần đó và ghi rõ thiếu trong báo cáo.
- Không truy cập được nguồn/web → ghi ❓, không bịa.
- Dữ liệu mâu thuẫn → không xoá, ghi cả hai nguồn.

## Luồng dữ liệu
00_brief → (01_device, 01_models, 01_clinical) → (02_market ← 01_device; 02_prototype ← 01_*) → 03_audit ← 01_*,02_* → 04_final_report.

## Kịch bản kiểm thử
- **Bình thường:** "Tìm hiểu thiết bị theo dõi nhiệt độ lõi VĐV marathon & thuật toán cảnh báo say nắng" → đủ 6 file trung gian + báo cáo, script chạy được, audit không còn ❌ chưa sửa.
- **Chạy lại một phần:** "Cập nhật lại phần thị trường, kiểm tra Kenzen còn bán không" → chỉ gọi market-analyst + evidence-verifier, cập nhật mục 4 báo cáo.
- **Lỗi:** web bị chặn → agent trả về với nhiều ❓; báo cáo nêu rõ phần chưa kiểm chứng, không dừng toàn bộ quy trình.
