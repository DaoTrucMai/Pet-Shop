# 📚 Tài liệu đồ án PetShop

Thư mục này chứa **báo cáo đầy đủ** và **slide PowerPoint** cho đồ án _Ứng dụng PetShop trên Android_ – nhóm 3 thành viên.

## Cấu trúc thư mục

```
docs/
├── BAO_CAO.md              ← Báo cáo Markdown chi tiết (~ 800 dòng)
├── BAO_CAO_SLIDES.pptx     ← File PowerPoint 28 slide
├── BAO_CAO_SLIDES.pdf      ← Bản PDF của slide (preview nhanh)
├── build_slides.py         ← Script Python tự sinh lại file PPTX
├── README.md               ← File này
├── diagrams/               ← 10 file Mermaid (.mmd) – source sơ đồ
│   ├── usecase.mmd
│   ├── architecture.mmd
│   ├── erd.mmd
│   ├── auth-flow.mmd
│   ├── checkout-flow.mmd
│   ├── order-state.mmd
│   ├── sequence-vnpay.mmd
│   ├── chat-rag.mmd
│   ├── return-flow.mmd
│   └── admin-dashboard.mmd
└── images/                 ← 10 ảnh PNG đã render từ Mermaid
    └── diagram_*.png
```

## Cách sử dụng

### 1. Đọc báo cáo (Markdown)

Mở file `BAO_CAO.md` bằng **VS Code** / **Typora** / **Obsidian** để đọc trực quan, hoặc convert sang Word:

```bash
# Cần cài pandoc trước: sudo apt install pandoc
pandoc BAO_CAO.md -o BAO_CAO.docx
```

Báo cáo có **8 chương + phụ lục**:

1. Tổng quan đề tài
2. Khảo sát & Phân tích yêu cầu
3. Phân tích – Thiết kế hệ thống
4. Công nghệ & Nền tảng
5. Triển khai & Cài đặt
6. Mô tả các chức năng & Demo
7. Kiểm thử & Đánh giá
8. Kết luận & Hướng phát triển
9. Phân công công việc
10. Tài liệu tham khảo + Phụ lục

> ⚠ Trong báo cáo có **rất nhiều ghi chú `[CHỤP ẢNH …]` và `[VẼ …]`** – chỉ rõ **vị trí cần chèn ảnh / sơ đồ**. Hãy chụp ảnh từ emulator và chèn vào đúng vị trí trước khi nộp.

### 2. Mở slide PowerPoint

Mở file `BAO_CAO_SLIDES.pptx` bằng PowerPoint hoặc Keynote / LibreOffice Impress.

- 28 slide, 16:9, **theme cam (#F5A623) đồng bộ với app**.
- **Ít chữ – nhiều hình** theo yêu cầu.
- Slide demo (17–21) có sẵn 4 khung trống đặt tên `[ Screenshot ]` – nhóm chỉ cần **click → Insert → Picture** để thay ảnh thật chụp từ emulator.

### 3. Sửa lại sơ đồ

Tất cả sơ đồ đều dùng **Mermaid** (text → diagram). Để chỉnh sửa:

- Mở file `.mmd` trong `diagrams/`, sửa nội dung.
- Render online bằng [https://mermaid.live](https://mermaid.live) – paste nội dung → tải về PNG.
- Hoặc dùng CLI:

```bash
npm i -g @mermaid-js/mermaid-cli
mmdc -i diagrams/usecase.mmd -o images/diagram_usecase.png -b transparent -w 1600 -H 900
```

### 4. Tự build lại slide

Nếu cần điều chỉnh nội dung slide (đổi tên thành viên, đổi màu, thêm slide…), sửa trong `build_slides.py` rồi chạy:

```bash
pip install python-pptx Pillow
python3 build_slides.py
```

## Phân công nhanh (xem chi tiết ở Slide 24 và Chương Phân công)

| Thành viên | Tỉ lệ | Phần phụ trách chính |
|------------|------|---------------------|
| **Nguyễn Văn Trường (KunT)** | 34 % | Trưởng nhóm – Customer flow, VNPay, Admin CRUD Pet/Food/Voucher |
| **Đào Trúc Mai** | 33 % | Notification, Hoàn trả, Upload media, Admin Approve |
| **Nguyễn Hữu Đức Thọ** | 33 % | Auth (Email/Google/OTP), Profile, Chat AI OpenAI, Slide |

## Thứ tự việc cần làm trước khi nộp

1. **Convert** `BAO_CAO.md` → `BAO_CAO.docx` (pandoc) hoặc copy thủ công vào Word.
2. **Chụp ảnh** ứng dụng theo hướng dẫn `[CHỤP ẢNH …]` rải khắp báo cáo.
3. **Chèn ảnh** vào file Word + 4 khung trống ở Slide 17–21 trong PPTX.
4. **Đánh số hình**: dưới mỗi ảnh ghi *Hình 1.1 – Tên hình*.
5. **In bìa** + làm trang lời cảm ơn theo mẫu trường (đã có gợi ý ở đầu báo cáo).
6. Kiểm tra **font Times New Roman 13, line spacing 1.5, lề chuẩn** cho báo cáo Word.

---

🐾 **Chúc nhóm trình bày thành công!**
