# 📚 Tài liệu đồ án PetShop

Thư mục này chứa **báo cáo Word đầy đủ** và **slide PowerPoint** cho đồ án _Xây dựng ứng dụng PetShop trên Android_ – nhóm 4 thành viên.

## Cấu trúc thư mục

```
docs/
├── BAO_CAO.docx            ← BÁO CÁO WORD CHÍNH  (~95 trang)
├── BAO_CAO.pdf             ← Bản PDF preview của báo cáo
├── BAO_CAO_SLIDES.pptx     ← SLIDE POWERPOINT  (37 slide, 16:9)
├── BAO_CAO_SLIDES.pdf      ← Bản PDF preview của slide
├── README.md               ← File này
│
├── build_report.py         ← Script Python tự sinh lại file Word
├── _chapters_body.py       ← Mở đầu, Chương 1, 2
├── _chapters_body2.py      ← Chương 3, 4, 5, 6 (4 module – 4 thành viên)
├── _chapters_body3.py      ← Chương 7, Kết luận, Tài liệu tham khảo, Phụ lục
├── build_slides.py         ← Script Python tự sinh lại file PPTX
│
├── diagrams/               ← 18 file Mermaid (.mmd) – source sơ đồ
└── images/                 ← 18 ảnh PNG đã render từ Mermaid (1600 px)
```

## 1. Báo cáo Word (`BAO_CAO.docx`)

**95 trang**, font Times New Roman 13pt, line spacing 1.5, lề chuẩn (3-2-2-2 cm). Cấu trúc đầy đủ theo yêu cầu giảng viên:

| # | Nội dung | Ghi chú |
|---|---------|---------|
| 1 | Trang bìa chính | Logo, tên đề tài, danh sách nhóm |
| 2 | Trang bìa phụ | Bảng thông tin đề tài + danh sách 4 thành viên |
| 3 | Lời cảm ơn | Mẫu sẵn, nhóm có thể chỉnh tên GV |
| 4 | Lời cam đoan | Mẫu sẵn, có chỗ ký tên |
| 5 | Nhận xét của GV hướng dẫn | Form trống để in |
| 6 | Bảng phân công công việc nhóm | **4 thành viên 25% mỗi người** |
| 7 | Danh mục từ viết tắt | 21 thuật ngữ |
| 8 | Danh mục hình ảnh | 20 hình + hướng dẫn auto-update bằng F9 |
| 9 | Danh mục bảng biểu | 19 bảng |
| 10 | Mục lục | Hướng dẫn auto-generate bằng Word References |
| 11 | **Mở đầu** | 5 mục: lý do, mục tiêu, đối tượng, phương pháp, bố cục |
| 12 | **Chương 1** – Tổng quan đề tài & Công nghệ | 4 mục lớn |
| 13 | **Chương 2** – Phân tích & Thiết kế hệ thống | 6 mục lớn (Use Case, ERD, MVVM, UI/UX, Security Rules) |
| 14 | **Chương 3** – Module Tài khoản & Hồ sơ (TV1) | 11 mục, ~6 trang |
| 15 | **Chương 4** – Module Danh mục & Trang chủ (TV2) | 10 mục, ~6 trang |
| 16 | **Chương 5** – Module Giỏ hàng – Thanh toán (TV3) | 8 mục, ~7 trang |
| 17 | **Chương 6** – Module Quản trị & Chatbot (TV4) | 13 mục, ~7 trang |
| 18 | **Chương 7** – Kiểm thử & Triển khai | 5 mục + 49 test case |
| 19 | Kết luận & Hướng phát triển | 3 mục, 12 hướng mở rộng |
| 20 | Tài liệu tham khảo | 17 nguồn |
| 21 | **Phụ lục A** – Bảng phân công chi tiết & tiến độ | 29 đầu việc, gắn với từng TV |
| 22 | **Phụ lục B** – Cấu trúc thư mục mã nguồn | Sơ đồ thư mục đầy đủ |
| 23 | **Phụ lục C** – Sơ đồ Firestore & Security Rules | Toàn văn rules |
| 24 | **Phụ lục D** – Ảnh chụp màn hình toàn bộ ứng dụng | Khu vực để chèn screenshot |

> ⚠ Trong báo cáo có khoảng **20 chỗ đánh dấu `[CHỤP ẢNH …]`** chỉ rõ nên chèn screenshot nào – nhóm chỉ cần chụp ảnh emulator và chèn vào đúng vị trí.

## 2. Slide PowerPoint (`BAO_CAO_SLIDES.pptx`)

**37 slide**, 16:9, theme cam ấm với gradient + 8 màu phụ trợ phân biệt 8 chương:

- Cover (gradient + decorative shapes)
- Agenda 8 mục (8 màu)
- 5 slide chương dẫn (chapter divider có gradient)
- 18 slide nội dung (mỗi slide chứa 1 sơ đồ Mermaid + 2-3 thẻ side card)
- 1 slide Bố cục Trang chủ (mockup phone bằng shapes thuần)
- 1 slide Tổng kết test case (5 module – PASS 100%)
- 1 slide Ưu/Nhược điểm
- 1 slide **Phân công 4 thành viên** (4 cột màu khác nhau)
- 1 slide Kết luận & Hướng phát triển
- 1 slide Cảm ơn (gradient)

**Đặc điểm**: ít chữ, nhiều sơ đồ trực quan, mỗi sơ đồ Mermaid được render PNG riêng. Mọi văn bản tiếng Việt hiển thị chính xác, không lỗi font.

## 3. 18 sơ đồ Mermaid

| Tên file | Mô tả |
|----------|------|
| `usecase.mmd` | Use Case tổng quát (2 tác nhân) |
| `architecture.mmd` | Kiến trúc MVVM + Repository + Firebase |
| `package-layout.mmd` | Tổ chức package mã nguồn |
| `mvvm-dataflow.mmd` | Sequence luồng dữ liệu giữa các tầng |
| `erd.mmd` | ERD logic của Firestore |
| `firestore-collections.mmd` | Sơ đồ collection Firestore |
| `security-rules.mmd` | Logic Firestore Security Rules |
| `auth-flow.mmd` | Activity – Đăng ký, Đăng nhập |
| `customer-journey.mmd` | Hành trình khách hàng |
| `admin-journey.mmd` | Hành trình quản trị viên |
| `checkout-flow.mmd` | Activity – Đặt hàng & Thanh toán |
| `sequence-vnpay.mmd` | Sequence – Thanh toán VNPay |
| `payment-data-flow.mmd` | Luồng dữ liệu thanh toán VNPay |
| `order-state.mmd` | State Diagram – 11 trạng thái đơn hàng |
| `order-status-bar.mmd` | Thanh trạng thái đơn cho khách |
| `return-flow.mmd` | Activity – Yêu cầu hoàn trả |
| `chat-rag.mmd` | Kiến trúc Chatbot RAG nhẹ |
| `admin-dashboard.mmd` | Sequence – Admin Dashboard real-time |

Để chỉnh sửa, mở `.mmd` trong [https://mermaid.live](https://mermaid.live) hoặc dùng CLI:

```bash
npm i -g @mermaid-js/mermaid-cli
mmdc -i diagrams/usecase.mmd -o images/diagram_usecase.png -b transparent -w 1600 -H 900
```

## 4. Phân công 4 thành viên

| TV | Họ và tên | Module | Tỉ lệ |
|----|-----------|--------|------|
| TV1 | Nguyễn Hữu Đức Thọ (Trưởng nhóm) | **Chương 3** – Tài khoản, Auth, Profile, Notification | 25% |
| TV2 | Đào Trúc Mai | **Chương 4** – Trang chủ, Danh mục, Pet/Food Detail | 25% |
| TV3 | Nguyễn Văn Trường | **Chương 5** – Giỏ hàng, Checkout, VNPay, Đơn hàng, Hoàn trả | 25% |
| TV4 | …………………………………… | **Chương 6** – Admin (CRUD đầy đủ) + Chatbot OpenAI | 25% |

> Họ tên TV4 và mã số sinh viên 4 thành viên cần được nhóm tự điền vào trang bìa chính, trang bìa phụ và bảng phân công.

## 5. Tự sinh lại tài liệu

Nếu cần điều chỉnh nội dung báo cáo hoặc slide, sau đó tự build lại:

```bash
pip install python-docx python-pptx Pillow lxml
cd docs

# Build lại Word
python3 build_report.py
# Build lại PPT
python3 build_slides.py
```

## 6. Việc cần làm thêm trước khi nộp

1. **Điền MSSV + tên giảng viên + tên trường + tên TV4** vào BAO_CAO.docx (tìm dấu “……………”).
2. **Chụp ảnh ứng dụng** trên emulator/thiết bị thật theo hướng dẫn `[CHỤP ẢNH …]` và `Phụ lục D`.
3. **Chèn ảnh** vào các vị trí đánh dấu trong báo cáo Word.
4. **Auto-update Mục lục, Mục lục hình, Mục lục bảng**: chuột phải vào các bảng đó → `Update Field` (hoặc nhấn F9).
5. **Kiểm tra lại các bảng** bằng cách scroll xuống và sửa cell width nếu cần.
6. **In bìa**, ký tên ở Lời cảm ơn / Lời cam đoan / Nhận xét.

---

🐾 **Chúc nhóm trình bày thành công!**
