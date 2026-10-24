---
name: evidence-verification
description: Kiểm chứng độc lập báo cáo nghiên cứu y sinh — tra DOI/PMID thật, đối chiếu số liệu, phương trình, hệ số mô hình, ngưỡng lâm sàng và trạng thái thị trường sản phẩm với nguồn gốc; phát hiện trích dẫn ma và mâu thuẫn giữa các phần. Dùng khi cần "kiểm tra nguồn", "verify citation", "số liệu này đúng không", "rà soát báo cáo trước khi công bố".
---
# Kiểm chứng bằng chứng

## Quy trình
1. **Trích xuất tuyên bố** có thể kiểm chứng: con số (sai số, ngưỡng, hệ số), trích dẫn, trạng thái sản phẩm, quy định pháp lý.
2. **Ưu tiên kiểm tra rủi ro cao**: hệ số phương trình (một chữ số sai làm hỏng toàn bộ ước tính), ngưỡng lâm sàng, tuyên bố "được FDA chấp thuận", "đang bán tại VN".
3. **Tra nguồn**: PubMed (`mcp__PubMed__*` nếu có), DOI resolver, trang hãng, cơ quan quản lý. Ghi PMID/DOI thực.
4. **So khớp giao diện giữa các phần**: hệ số trong code ↔ tài liệu mô hình ↔ bài gốc; ngưỡng cấu hình ↔ bảng lâm sàng; thiết bị đề xuất ↔ khả năng xuất dữ liệu ↔ trạng thái thị trường.
5. **Gắn nhãn**: ✅ xác nhận · ⚠️ một phần · ❌ sai (ghi giá trị đúng + nguồn) · ❓ không truy cập được.

## Đầu ra
Bảng: `# | Tuyên bố | Vị trí (file/mục) | Nhãn | Bằng chứng (DOI/URL) | Sửa đề xuất`, sau đó mục "Sửa bắt buộc trước khi xuất bản" (mọi ❌) và "Cần thận trọng" (⚠️/❓).
Tỷ lệ tổng: số ✅/⚠️/❌/❓.
