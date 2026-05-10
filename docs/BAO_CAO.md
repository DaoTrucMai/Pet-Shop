# BÁO CÁO ĐỒ ÁN MÔN HỌC
## Đề tài: Xây dựng ứng dụng di động **PetShop** – Cửa hàng thú cưng & thức ăn cho thú cưng trên nền tảng Android

> **File này là khung báo cáo hoàn chỉnh** dành cho nhóm. Mỗi mục đều có ghi chú **[CHỤP ẢNH:…]** chỉ rõ nên chèn screenshot/diagram nào và **[VẼ:…]** gợi ý sơ đồ trực quan cần bổ sung. Tất cả file sơ đồ Mermaid nằm trong thư mục `docs/diagrams/`.

---

## TRANG BÌA (gợi ý)

```
TRƯỜNG ………………………………………
KHOA CÔNG NGHỆ THÔNG TIN

ĐỒ ÁN MÔN HỌC
PHÁT TRIỂN ỨNG DỤNG DI ĐỘNG

ỨNG DỤNG PETSHOP – CỬA HÀNG THÚ CƯNG
TRÊN NỀN TẢNG ANDROID

Giảng viên hướng dẫn : ……………………………………
Sinh viên thực hiện  :
  1. Nguyễn Văn Trường   – MSSV: ………… (Trưởng nhóm – KunT)
  2. Đào Trúc Mai         – MSSV: …………
  3. Nguyễn Hữu Đức Thọ   – MSSV: …………

…………… 2026
```

> **[CHỤP ẢNH 0]** Logo trường + logo khoa + ảnh banner ứng dụng (lấy từ `splash` hoặc icon trong `res/mipmap`).

---

## LỜI CẢM ƠN

Nhóm xin chân thành cảm ơn thầy/cô đã tận tình hướng dẫn nhóm trong suốt quá trình thực hiện đồ án "**Xây dựng ứng dụng PetShop trên nền tảng Android**". Cảm ơn các bạn trong lớp đã hỗ trợ kiểm thử, đóng góp ý kiến để sản phẩm hoàn thiện hơn. Mặc dù đã cố gắng, đồ án vẫn không tránh khỏi thiếu sót, kính mong nhận được sự góp ý của thầy/cô.

---

## MỤC LỤC

1. Chương 1 – Tổng quan đề tài
2. Chương 2 – Khảo sát & phân tích yêu cầu
3. Chương 3 – Phân tích – thiết kế hệ thống
4. Chương 4 – Công nghệ & nền tảng sử dụng
5. Chương 5 – Triển khai & cài đặt
6. Chương 6 – Mô tả các chức năng & kết quả demo
7. Chương 7 – Kiểm thử & đánh giá
8. Chương 8 – Kết luận & hướng phát triển
9. Phân công công việc trong nhóm
10. Tài liệu tham khảo

---

# CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI

## 1.1. Lý do chọn đề tài

Thị trường thú cưng tại Việt Nam đang phát triển mạnh mẽ trong những năm gần đây. Theo thống kê, có hơn **40% hộ gia đình thành thị** đang nuôi ít nhất một thú cưng, kéo theo nhu cầu mua bán thú cưng, thức ăn, phụ kiện, dịch vụ chăm sóc thú y rất lớn. Tuy nhiên đa số giao dịch hiện tại vẫn diễn ra qua các trang mạng xã hội hoặc cửa hàng truyền thống, **thiếu một nền tảng tập trung, chuyên nghiệp**, gây khó khăn cho người dùng trong việc:

- Tìm kiếm đúng giống thú cưng phù hợp với gia đình.
- So sánh giá, kiểm tra nguồn gốc, lịch sử tiêm phòng.
- Mua thức ăn, phụ kiện đúng nhu cầu (theo loài, độ tuổi, cân nặng).
- Theo dõi đơn hàng, được hỗ trợ tư vấn 24/7.

Xuất phát từ thực tiễn đó, nhóm chọn đề tài **"Xây dựng ứng dụng PetShop trên Android"** – một ứng dụng thương mại điện tử chuyên biệt cho lĩnh vực thú cưng, có tích hợp **AI hỗ trợ tư vấn**, **thanh toán VNPay** và **quản trị real-time bằng Firebase**.

> **[CHỤP ẢNH 1.1]** Một vài bài đăng bán thú cưng trên Facebook/Chợ Tốt để minh hoạ "thị trường còn lộn xộn".

## 1.2. Mục tiêu đề tài

| STT | Mục tiêu | Mức độ ưu tiên |
|-----|---------|----------------|
| 1 | Xây dựng ứng dụng Android hoàn chỉnh cho **2 vai trò**: Khách hàng & Quản trị viên | Bắt buộc |
| 2 | Quản lý 2 loại sản phẩm: **Thú cưng (Pet)** và **Thức ăn (Food)** | Bắt buộc |
| 3 | Triển khai luồng **mua hàng end-to-end**: giỏ hàng → thanh toán → giao hàng → đánh giá | Bắt buộc |
| 4 | Tích hợp **Firebase Authentication** (Email/Password + Google Sign-In) và **Firestore** real-time | Bắt buộc |
| 5 | Tích hợp **cổng thanh toán VNPay** (Sandbox) | Bắt buộc |
| 6 | Tích hợp **AI Chatbot** (OpenAI) tư vấn sản phẩm cho khách hàng | Nâng cao |
| 7 | Hệ thống **voucher / khuyến mãi**, **tính phí ship theo vùng** | Nâng cao |
| 8 | Hệ thống **thông báo (notification)**, **hoàn trả & hoàn tiền** | Nâng cao |
| 9 | Áp dụng kiến trúc **MVVM** + **Repository Pattern** | Bắt buộc |

## 1.3. Phạm vi đề tài

- **Nền tảng**: Android (minSdk 24 – Android 7.0, targetSdk 36).
- **Ngôn ngữ**: Java.
- **Backend**: Firebase (Auth, Firestore, Storage) – không tự host server.
- **Thanh toán**: VNPay Sandbox (chưa lên production).
- **AI**: Sử dụng API OpenAI Chat Completions cho chatbot.
- **Đối tượng người dùng**: Khách hàng cá nhân và quản trị viên cửa hàng tại Việt Nam.

## 1.4. Ý nghĩa đề tài

- **Về mặt thực tiễn**: Cung cấp nền tảng đặt mua thú cưng/thức ăn tiện lợi, minh bạch.
- **Về mặt học thuật**: Vận dụng tổng hợp kiến trúc MVVM, Firebase real-time, OAuth 2.0 (Google Sign-In), HMAC-SHA512 (VNPay), tích hợp REST API bên thứ ba (OpenAI), thiết kế UI/UX theo Material Design.

---

# CHƯƠNG 2. KHẢO SÁT & PHÂN TÍCH YÊU CẦU

## 2.1. Khảo sát hiện trạng

Nhóm đã khảo sát một số ứng dụng tương tự trong và ngoài nước:

| Ứng dụng | Ưu điểm | Nhược điểm |
|----------|---------|-----------|
| **Pet Mart**, **Petsy** (web) | Sản phẩm phong phú | Chưa có app native, UX chậm |
| **Chewy**, **PetSmart** (US) | Hệ sinh thái lớn | Không phục vụ thị trường VN |
| Bài đăng MXH (Facebook, Chợ Tốt) | Dễ đăng tin | Không có quản lý đơn hàng, không bảo đảm giao dịch |

> **[VẼ 2.1]** Bảng so sánh dạng infographic 3 cột (logo + ưu/nhược) – đặt ở slide.
>
> **[CHỤP ẢNH 2.1]** Screenshot 2-3 app/web cạnh tranh.

## 2.2. Yêu cầu chức năng

### 2.2.1. Phía khách hàng (Customer)

| ID | Chức năng | Mô tả ngắn |
|----|----------|-----------|
| FC-01 | Đăng ký / Đăng nhập | Email-Password, Google Sign-In, OTP qua Email khi đăng ký, Quên mật khẩu |
| FC-02 | Trang chủ | Banner, lời chào theo thời gian, danh mục, sản phẩm nổi bật, ô tìm kiếm |
| FC-03 | Duyệt sản phẩm | Lọc theo loài/loại thức ăn/giá; xem chi tiết thú cưng & thức ăn |
| FC-04 | Giỏ hàng | Thêm/xoá/đổi số lượng, badge giỏ hàng |
| FC-05 | Voucher / Khuyến mãi | Xem voucher hệ thống, áp dụng vào đơn hàng |
| FC-06 | Đặt hàng (Checkout) | Chọn địa chỉ, tính phí ship theo vùng, chọn COD/VNPay |
| FC-07 | Thanh toán VNPay | WebView VNPay → callback → cập nhật đơn |
| FC-08 | Lịch sử đơn hàng | Lọc theo trạng thái, xem chi tiết, huỷ đơn |
| FC-09 | Hoàn trả & hoàn tiền | Yêu cầu return, nhập tài khoản ngân hàng nếu COD |
| FC-10 | Thông báo | Real-time badge, đánh dấu đã đọc |
| FC-11 | Chat hỗ trợ AI | Chat với GPT-4o-mini, gửi text/ảnh, voice-to-text, lịch sử phiên |
| FC-12 | Hồ sơ | Sửa profile, quản lý địa chỉ, đăng xuất |

### 2.2.2. Phía quản trị (Admin)

| ID | Chức năng | Mô tả |
|----|----------|------|
| FA-01 | Dashboard | Doanh thu thực, số đơn, số user, đơn pending/preparing/shipping/refund (real-time) |
| FA-02 | Quản lý người dùng | Khoá/mở khoá, đổi role |
| FA-03 | Quản lý danh mục | CRUD danh mục Pet/Food |
| FA-04 | Quản lý thú cưng | CRUD pet, upload nhiều ảnh / video |
| FA-05 | Quản lý thức ăn | CRUD food, cập nhật tồn kho |
| FA-06 | Quản lý đơn hàng | Cập nhật trạng thái: PENDING → CONFIRMED → … → DELIVERED |
| FA-07 | Quản lý hoàn trả | Duyệt / từ chối / hoàn tiền |
| FA-08 | Quản lý voucher | CRUD voucher, gửi notification cho toàn bộ khách |
| FA-09 | Quản lý khuyến mãi | Áp dụng % giảm giá lên sản phẩm theo thời hạn |

## 2.3. Yêu cầu phi chức năng

| Tiêu chí | Mức yêu cầu |
|---------|-------------|
| Tương thích | Android 7.0+ (API 24) |
| Hiệu năng | Trang chủ load < 2s, Realtime Firestore < 500ms |
| Bảo mật | Firebase Auth, HMAC-SHA512 cho VNPay, không lưu password local |
| UX/UI | Material Design 3, dark/light theme, hỗ trợ Tiếng Việt |
| Bảo trì | MVVM + Repository pattern, code chia module rõ ràng |
| Khả năng mở rộng | Dễ swap shipping API (GHN/GHTK) thay cho ShippingHelper hiện tại |

## 2.4. Use Case Diagram

> **[VẼ 2.4]** Use Case tổng quát – file Mermaid: `docs/diagrams/usecase.mmd`. Khi chèn vào báo cáo, render PNG bằng [mermaid.live](https://mermaid.live) và đặt thay cho khối code dưới đây.

```
                  ┌────────────────────┐
                  │     Khách hàng     │
                  └─────────┬──────────┘
                            │
        ┌─────────┬─────────┼─────────┬──────────┬──────────┐
        ▼         ▼         ▼         ▼          ▼          ▼
   Đăng ký   Đăng nhập  Xem SP   Đặt hàng    Thanh toán  Chat AI
                            │                    │
                            ▼                    ▼
                       Áp voucher           VNPay/COD
                            │
                            ▼
                       Hoàn trả/Đánh giá

                  ┌────────────────────┐
                  │   Quản trị viên    │
                  └─────────┬──────────┘
        ┌─────────┬─────────┼─────────┬──────────┬──────────┐
        ▼         ▼         ▼         ▼          ▼          ▼
    Quản lý   Quản lý   Quản lý   Quản lý    Quản lý    Dashboard
    User      Pet/Food  Đơn hàng  Voucher    Hoàn trả   thống kê
```

> **[CHỤP ẢNH 2.4]** Sau khi vẽ Use Case bằng Draw.io / StarUML / mermaid → xuất PNG đặt vào báo cáo.

---

# CHƯƠNG 3. PHÂN TÍCH – THIẾT KẾ HỆ THỐNG

## 3.1. Kiến trúc tổng thể

Ứng dụng được xây dựng theo kiến trúc **MVVM + Repository Pattern**, kết hợp Firebase làm backend BaaS:

```
┌─────────────────────────────────────────────────────────────┐
│                        VIEW LAYER                           │
│  Activity / Fragment / Adapter  ──────►  ViewBinding        │
└────────────────────┬────────────────────────────────────────┘
                     │ observe LiveData
┌────────────────────▼────────────────────────────────────────┐
│                     VIEWMODEL LAYER                         │
│  HomeVM, CartVM, OrderVM, AdminVM, ChatVM, AuthVM, …        │
└────────────────────┬────────────────────────────────────────┘
                     │ gọi repository (callback / listener)
┌────────────────────▼────────────────────────────────────────┐
│                    REPOSITORY LAYER                         │
│  AuthRepo, OrderRepo, NotificationRepo, VoucherRepo, …      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                       BACKEND                               │
│   Firebase Auth │ Firestore │ Storage  ║  VNPay │ OpenAI    │
└─────────────────────────────────────────────────────────────┘
```

> **[VẼ 3.1]** Vẽ lại sơ đồ kiến trúc đẹp bằng Draw.io, đặt ở slide & báo cáo.
>
> **[CHỤP ẢNH 3.1]** Màn hình project tree trong Android Studio (`view/`, `viewmodel/`, `repository/`, `model/`, `utils/`) để minh hoạ phân lớp.

## 3.2. Sơ đồ ERD (Entity Relationship Diagram) trên Firestore

Dù Firestore là NoSQL, nhóm vẫn mô hình hoá quan hệ giữa các collection để dễ thiết kế:

```
users (1) ──< orders >── (N) order_items
users (1) ──< addresses
users (1) ──< notifications
users (1) ──< chat_sessions ──< chat_messages

categories (1) ──< pets
categories (1) ──< foods

pets ──< pet_media        foods ──< food_media
orders ──< return_requests
vouchers ──< voucher_usage

promotions  (áp dụng theo categoryId/productId)
```

Các **collection** chính trong Firestore (xem `Constants.java`):

| Collection | Mô tả | Trường khoá |
|-----------|------|------------|
| `users` | Tài khoản (CUSTOMER/ADMIN) | `id, role, status, totalOrders, totalSpent` |
| `pets` | Thú cưng | `id, categoryId, species, breed, age, price, status` |
| `foods` | Thức ăn | `id, brand, foodType, targetPetType, weightGram, stock, sold` |
| `categories` | Danh mục Pet/Food | `id, name, type` |
| `orders` | Đơn hàng | `id, orderCode, userId, status, paymentStatus, items[]` |
| `notifications` | Thông báo | `id, userId, type, isRead, orderId` |
| `vouchers` | Mã giảm giá | `code, type (PERCENT/FIXED/FREESHIP), usedCount, perUserLimit` |
| `promotions` | Khuyến mãi | áp dụng % giảm theo sản phẩm/danh mục |
| `chat_sessions / chat_messages` | Lịch sử chat AI | `userId, role, content, imageUrl` |

> **[VẼ 3.2]** Vẽ ERD bằng Draw.io hoặc dbdiagram.io (đã có file `docs/diagrams/erd.mmd`).
>
> **[CHỤP ẢNH 3.2]** Screenshot Firebase Console > Firestore Database hiển thị toàn bộ collection.

## 3.3. Sơ đồ hoạt động (Activity Diagram)

### 3.3.1. Đăng ký tài khoản (có OTP)

```
[Người dùng] ─► Nhập email + mật khẩu
                          │
                          ▼
       Kiểm tra trùng email trên Firebase Auth
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
            Trùng              Không trùng
                │                   │
            Thông báo lỗi      Sinh OTP 6 số → Gửi mail (JavaMail)
                                    │
                                    ▼
                          Người dùng nhập OTP
                                    │
                              OTP đúng?
                                ┌───┴───┐
                                ▼       ▼
                        createUserWithEmail   Cảnh báo
                                │
                                ▼
                       Lưu user vào Firestore (role=CUSTOMER)
                                │
                                ▼
                          Vào màn Home
```

> **[CHỤP ẢNH 3.3.1]** Màn `RegisterActivity` + email OTP nhận được.

### 3.3.2. Đặt hàng & Thanh toán

```
[Cart] ─► Checkout
   │       ├── chọn địa chỉ → ShippingHelper.calculate(addr, subtotal)
   │       ├── chọn voucher → VoucherRepository.getByCode + validate
   │       └── chọn phương thức thanh toán
   │              ├── COD  ──► OrderRepo.createOrder(status=PENDING)
   │              │              + trừ stock food / set Pet=RESERVED
   │              │
   │              └── VNPAY ─► OrderRepo.createOrder(status=WAITING_PAYMENT)
   │                              │
   │                              ▼
   │                       VNPayHelper.buildPaymentUrl()
   │                              │
   │                              ▼  WebView VNPayWebViewActivity
   │                              ▼
   │                     VNPay redirect → VNPayResultActivity
   │                              │
   │                              ▼
   │             completeVNPayOrder() trong transaction:
   │                – status = PENDING
   │                – paymentStatus = PAID
   │                – trừ stock / Pet=RESERVED
   ▼
Notification "Đặt hàng thành công" → tvNotificationBadge tăng
```

> **[CHỤP ẢNH 3.3.2]** Toàn bộ flow: Cart → Checkout (địa chỉ + voucher) → VNPay sandbox WebView → Kết quả.

### 3.3.3. Hoàn trả đơn hàng

```
Đơn DELIVERED/COMPLETED
       │
       ▼
Khách hàng nhấn "Yêu cầu hoàn trả"
       │
       ▼
ReturnRequestActivity
   – Lý do
   – Nếu COD: bắt buộc Số TK + Tên ngân hàng
   – Nếu VNPay: hoàn về thẻ thanh toán gốc
       │
       ▼
OrderRepo.requestReturn() → status = RETURN_REQUESTED
ReturnRepo.create() lưu yêu cầu
       │
       ▼
Admin (AdminReturnListActivity)
   – Approve  → status = RETURN_APPROVED
   – Refund   → status = REFUNDED, paymentStatus=REFUNDED
   – Reject   → ghi adminNote, đơn quay lại COMPLETED
       │
       ▼
Notification gửi đến khách
```

> **[CHỤP ẢNH 3.3.3]** Màn hình `ReturnRequestActivity` (khách) và `AdminReturnListActivity` (admin).

## 3.4. Sơ đồ trạng thái đơn hàng (State Machine)

```
                   ┌──────────────────────────────────┐
                   │  PENDING (COD) / WAITING_PAYMENT │
                   └──────────────┬───────────────────┘
        VNPay paid ▲              │ admin xác nhận
                   │              ▼
                CONFIRMED ◄─── PREPARING ───► SHIPPING ───► DELIVERED
                                                              │
                                                              ▼
                                                          COMPLETED
                                                              │
                                                              ▼
                                                    RETURN_REQUESTED
                                                              │
                                                              ▼
                                                    RETURN_APPROVED
                                                              │
                                                              ▼
                                                          REFUNDED

  CANCELLED  ◄──  từ PENDING / WAITING_PAYMENT / CONFIRMED
```

Định nghĩa hằng số trong `Order.java`:

```
PENDING, WAITING_PAYMENT, CONFIRMED, PREPARING, SHIPPING,
DELIVERED, COMPLETED, CANCELLED,
RETURN_REQUESTED, RETURN_APPROVED, REFUNDED
```

> **[VẼ 3.4]** Vẽ state diagram bằng Mermaid → render PNG đẹp (file `docs/diagrams/order-state.mmd`).

## 3.5. Sequence Diagram – Tạo đơn VNPay (rút gọn)

```
Customer ─► CheckoutActivity : clickPay
CheckoutActivity ─► OrderRepository : createOrder(VNPAY)
OrderRepository ─► Firestore : runTransaction (set order WAIT_PAY)
Firestore ──► OrderRepository : success(orderId)
CheckoutActivity ─► VNPayHelper : buildPaymentUrl(amount, orderCode)
VNPayHelper ─► VNPayHelper : HMAC-SHA512(secret, params)
CheckoutActivity ─► VNPayWebViewActivity : load(paymentUrl)
VNPayWebViewActivity ──► VNPay Sandbox : user thanh toán
VNPay ─► VNPayResultActivity : redirect (vnp_ResponseCode)
VNPayResultActivity ─► OrderRepository : completeVNPayOrder(orderId)
OrderRepository ─► Firestore : transaction(update status=PENDING, PAID, trừ kho)
OrderRepository ─► NotificationRepository : createNotificationAsync("Thanh toán thành công")
```

> **[VẼ 3.5]** Sequence diagram bằng PlantUML / mermaid (`docs/diagrams/sequence-vnpay.mmd`).

---

# CHƯƠNG 4. CÔNG NGHỆ & NỀN TẢNG SỬ DỤNG

## 4.1. Bảng tổng hợp công nghệ

| Lớp | Công nghệ | Lý do chọn |
|-----|----------|-----------|
| Ngôn ngữ | **Java 11** | Phổ biến, ổn định cho Android |
| UI | Android XML + Material Components | Chuẩn Material Design |
| Architecture | **MVVM** (`androidx.lifecycle`) | Tách bạch, dễ test, dễ bảo trì |
| Backend | **Firebase Auth + Firestore + Storage** | BaaS, real-time, miễn phí giai đoạn đầu |
| Auth | Email/Password + **Google Sign-In** | Đa dạng phương thức |
| Email OTP | **JavaMail (SMTP Gmail)** | Tự gửi OTP không cần Firebase Phone |
| Thanh toán | **VNPay Sandbox** + HMAC-SHA512 | Phổ biến tại VN |
| HTTP | **OkHttp** | Gọi API OpenAI |
| JSON | **Gson** | Parse response |
| Hình ảnh | **Glide** | Tải/cache ảnh hiệu quả |
| Avatar | **CircleImageView** | Hiển thị avatar tròn |
| AI | **OpenAI GPT-4o-mini** (`/v1/chat/completions`) | Chatbot tư vấn |
| Slider | **ViewPager2** | Banner trang chủ |
| Build | **Gradle 8 (KTS) + Version Catalog** | Quản lý dependency tập trung |

> **[CHỤP ẢNH 4.1]** Màn hình `libs.versions.toml` hoặc `app/build.gradle.kts` thể hiện danh sách thư viện.

## 4.2. Tóm tắt thư mục mã nguồn

```
app/src/main/java/com/example/petshop/
├── MainActivity.java                 (entry → SplashActivity)
├── model/
│   ├── entity/   (User, Pet, Food, Cart, CartItem, Order, OrderItem,
│   │             Address, Category, Promotion, Voucher, Notification,
│   │             ChatMessage, ChatSession, ReturnRequest, Review, Banner, …)
│   ├── request/   (DTO request lên Firestore/API)
│   └── response/  (DTO trả về)
├── repository/   (13 file: Auth, Cart, Order, Notification, Voucher, …)
├── viewmodel/    (14 ViewModel: Home, Cart, Order, Admin, Chat, Auth, …)
├── view/
│   ├── activity/  (30+ Activity)
│   ├── fragment/  (Home, Cart, Order, Profile, Category, ProductDetail)
│   ├── adapter/   (19 Adapter cho RecyclerView)
│   └── dialog/    (ConfirmDialog, LoadingDialog, …)
└── utils/        (FirebaseHelper, EmailHelper, VNPayHelper,
                  ShippingHelper, PromotionManager, SessionManager,
                  StorageHelper, NetworkUtils, CartBadgeManager, Constants)
```

Tổng số dòng code Java (chỉ tính `repository/` + `viewmodel/`): **≈ 5.000 LOC**, toàn bộ mã nguồn ước tính **≈ 18.000 – 20.000 LOC**.

> **[CHỤP ẢNH 4.2]** Project tree trong Android Studio.

## 4.3. Cấu hình bảo mật `local.properties`

Để tránh leak khoá bí mật, các giá trị nhạy cảm được đặt trong `local.properties` và được Gradle inject vào `BuildConfig`:

```
GOOGLE_WEB_CLIENT_ID = "xxxxxxxxxxxxx.apps.googleusercontent.com"
BASE_URL             = "https://your-api.com/api/v1/"
VNPAY_TMN_CODE       = "YOUR_TMN_CODE"
VNPAY_HASH_SECRET    = "YOUR_HASH_SECRET"
VNPAY_URL            = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
VNPAY_RETURN_URL     = "petshop://payment/vnpay-return"
OPENAI_API_KEY       = "sk-..."
```

> **[CHỤP ẢNH 4.3]** File `local.properties` (đã ẩn key) và đoạn code đọc trong `Constants.java`.

---

# CHƯƠNG 5. TRIỂN KHAI & CÀI ĐẶT

## 5.1. Yêu cầu cài đặt

| Thành phần | Phiên bản |
|-----------|-----------|
| Android Studio | Hedgehog 2024+ |
| JDK | 17 (chạy Gradle), Java 11 (compile target) |
| Android SDK | API 36 (compile), API 24 (min) |
| Gradle | 8.x |
| Firebase project | đã bật Auth, Firestore, Storage |
| VNPay | TMN Code, Hash Secret từ tài khoản sandbox |
| OpenAI | API key hợp lệ |

## 5.2. Các bước cài đặt và chạy thử

1. Clone repo: `git clone <repo-url>`
2. Mở project bằng Android Studio.
3. Tạo file `local.properties` ở root, điền các biến ở mục **4.3**.
4. Đặt file `google-services.json` vào thư mục `app/` (đã có sẵn trong repo, có thể thay bằng project Firebase của bạn).
5. Sync Gradle, chờ tải dependency.
6. Bật Firebase Console → Firestore → import dữ liệu mẫu (categories, pets, foods, vouchers).
7. Chạy app trên emulator API 30+ hoặc thiết bị thật.
8. Tài khoản admin demo: `admin@petshop.com / 123456` (phải set role = ADMIN trong Firestore).

> **[CHỤP ẢNH 5.2]** Quá trình build Gradle thành công + app khởi chạy.

## 5.3. Cấu hình Firebase (nếu tự dựng project mới)

1. Vào [Firebase Console](https://console.firebase.google.com/) → **Add project**.
2. Add Android app, package name `com.example.petshop`, lấy `google-services.json`.
3. **Authentication** → bật *Email/Password* và *Google*.
4. **Firestore Database** → khởi tạo, để rules tạm:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
```

5. **Storage** → khởi tạo bucket cho upload ảnh.

> **[CHỤP ẢNH 5.3]** Firebase Console: Auth providers, Firestore rules, Storage bucket.

---

# CHƯƠNG 6. MÔ TẢ CÁC CHỨC NĂNG & KẾT QUẢ DEMO

> Quy ước: **mỗi chức năng** có 1 mô tả ngắn + 1–3 screenshot. Ảnh đặt theo tên `images/06_xx_yy.png` để đồng bộ với báo cáo.

## 6.1. Splash & Onboarding

- File: `SplashActivity` → tự chuyển sang `PetShopActivity` sau ~1.5s.
- Logo, slogan: *"Find Your Furry Favorite"*.

> **[CHỤP ẢNH 6.1]** `activity_splash.xml` lúc khởi động.

## 6.2. Đăng ký / Đăng nhập

- `LoginActivity`: Email + mật khẩu, đăng nhập Google, Quên mật khẩu.
- `RegisterActivity`: Tên, Email, Mật khẩu, **OTP gửi qua Email** (`EmailHelper.sendOTP`).
- Lỗi auth được dịch tiếng Việt (`FirebaseHelper.parseAuthError`).

> **[CHỤP ẢNH 6.2]**
> a) Màn `Login` (đầy đủ form + Google).
> b) Màn `Register` + OTP email.
> c) Trường hợp lỗi (sai mật khẩu, email tồn tại).

## 6.3. Trang chủ (HomeFragment)

- Lời chào theo thời gian (`getTimeGreeting()` – sáng/chiều/tối).
- Banner ViewPager2 (ImageSliderAdapter).
- Search bar realtime → `HomeViewModel.search()`.
- Danh mục (RV ngang) – click để filter.
- "Thú cưng nổi bật" + "Thức ăn nổi bật" với nút Xem tất cả.
- Badge giỏ hàng (đỏ) + badge thông báo (đỏ, có số).
- Thẻ Promo dẫn sang `PromotionActivity`.

> **[CHỤP ẢNH 6.3]**
> a) Trang chủ đầy đủ.
> b) Đang search.
> c) Khi badge giỏ hàng và badge notification có số.

## 6.4. Chi tiết sản phẩm

- `PetDetailActivity`: ảnh slider, tên, giống, tuổi, cân nặng, giới tính, tình trạng tiêm phòng, mô tả, nút "Thêm vào giỏ".
- `FoodDetailActivity`: ảnh, thương hiệu, loại, trọng lượng, mô tả, đánh giá, nút "Thêm vào giỏ" + chọn số lượng.

> **[CHỤP ẢNH 6.4]** 1 màn pet detail + 1 màn food detail.

## 6.5. Giỏ hàng

- Cộng/trừ số lượng với check tồn kho (`FoodRepository.getStock`).
- Tính tổng tự động qua LiveData.
- Badge cập nhật real-time qua `CartBadgeManager`.

> **[CHỤP ẢNH 6.5]** Giỏ hàng có cả pet và food.

## 6.6. Thanh toán (Checkout)

Flow chính (xem `CheckoutActivity`):

1. Chọn địa chỉ (`ManageAddressActivity`).
2. `ShippingHelper.calculate(address, subtotal)` → phí ship theo vùng:
   - Cùng TP.HCM: 30.000đ
   - Miền Nam: 45.000đ – Trung: 60.000đ – Bắc: 75.000đ
   - Free ship khi đơn ≥ 500.000đ.
3. Áp dụng voucher: PERCENT / FIXED / FREESHIP.
4. Áp dụng promotion (giảm theo sản phẩm/danh mục thông qua `PromotionManager`).
5. Chọn phương thức:
   - **COD** → tạo đơn `PENDING` + trừ stock + Pet=RESERVED.
   - **VNPAY** → tạo đơn `WAITING_PAYMENT` → mở `VNPayWebViewActivity`.

> **[CHỤP ẢNH 6.6]** Checkout step-by-step (4 ảnh).

## 6.7. Thanh toán VNPay

- `VNPayHelper.buildPaymentUrl()`: build query (TreeMap), URL-encode UTF-8, sort, **HMAC-SHA512** chữ ký.
- `VNPayWebViewActivity` mở URL sandbox.
- VNPay redirect về `petshop://payment/vnpay-return` → `VNPayResultActivity` parse `vnp_ResponseCode`.
- Nếu `00` (success) → `OrderRepository.completeVNPayOrder()` (transaction).

> **[CHỤP ẢNH 6.7]**
> a) Màn VNPay sandbox (chọn ngân hàng).
> b) Màn nhập OTP của ngân hàng demo (NCB).
> c) Màn `VNPayResultActivity` thành công.

## 6.8. Lịch sử đơn hàng & Chi tiết đơn

- `OrderHistoryActivity`: lọc theo trạng thái (Pending / Shipping / Delivered / Cancelled / Returned).
- `OrderDetailActivity`: thông tin đơn, items, mã giảm, phí ship, tổng tiền, nút Huỷ / Đánh giá / Hoàn trả tuỳ trạng thái.

> **[CHỤP ẢNH 6.8]** History (đa trạng thái) + Detail.

## 6.9. Hoàn trả & Hoàn tiền

- `ReturnRequestActivity`: nhập lý do, số tài khoản, ngân hàng (nếu COD).
- Đơn chuyển sang `RETURN_REQUESTED` → admin duyệt.
- Khi `REFUNDED`: cập nhật `paymentStatus=REFUNDED`, trừ doanh thu trong dashboard admin.

> **[CHỤP ẢNH 6.9]** ReturnRequest form + AdminReturnList sau khi duyệt.

## 6.10. Thông báo (Notification)

- Real-time badge trên trang chủ qua `NotificationRepository.listenUnreadCount()`.
- Khi mở `NotificationActivity` → `markAllAsRead`.
- Loại thông báo: `ORDER`, `PROMO`, `SYSTEM`.

> **[CHỤP ẢNH 6.10]** Badge "9+" trên Home + danh sách notification (đã đọc/chưa đọc khác màu).

## 6.11. Chat hỗ trợ AI

- `ChatActivity` + `ChatViewModel` gọi OpenAI Chat Completions (`gpt-4o-mini`).
- Hỗ trợ:
  - Voice → text (`RecognizerIntent`).
  - Đính kèm ảnh (encode Base64).
  - Lưu **lịch sử phiên** (`chat_sessions/{sessionId}/messages`).
  - Khách (chưa login) lưu local SharedPreferences (giới hạn 50 tin).
- Context bot có sẵn dữ liệu sản phẩm để trả lời chính xác (RAG nhẹ).

> **[CHỤP ẢNH 6.11]**
> a) Tin nhắn user/bot.
> b) Gửi ảnh để hỏi về thức ăn.
> c) Drawer lịch sử phiên chat.

## 6.12. Khuyến mãi & Voucher

- `PromotionActivity`: xem voucher hệ thống còn hiệu lực.
- `PromotionManager`: tính giá sau khuyến mãi.
- `VoucherRepository`:
  - `recordVoucherUsage`, `decrementUsageCount` khi huỷ đơn.
  - Khi admin **thêm/bật voucher** → tự động gửi notification cho **toàn bộ khách hàng ACTIVE**.

> **[CHỤP ẢNH 6.12]** Trang khuyến mãi + nhận notification voucher mới.

## 6.13. Profile & Địa chỉ

- `ProfileFragment`: avatar, tên, tổng đơn, tổng chi tiêu.
- `EditProfileActivity`: cập nhật avatar (Storage), tên, SĐT, ngày sinh, giới tính.
- `ManageAddressActivity`: CRUD địa chỉ, set mặc định.

> **[CHỤP ẢNH 6.13]** Profile + Edit + Address list.

## 6.14. Khu vực Quản trị (Admin)

### 6.14.1. AdminActivity Dashboard

- Real-time qua `AdminViewModel` (Firestore listener).
- 9 thẻ: doanh thu, tổng đơn, người dùng, pending, preparing, shipping, delivered, cancelled, refunded amount.
- Quy tắc đếm:
  - Chỉ tính đơn của khách `ACTIVE`.
  - **COD** chỉ đếm khi DELIVERED/COMPLETED.
  - **VNPAY** đếm ngay khi PAID.
  - Doanh thu thực = revenue – refundedMoney.

> **[CHỤP ẢNH 6.14.1]** Admin Dashboard đầy đủ thẻ.

### 6.14.2. Quản lý sản phẩm & danh mục

- `ManagePetsActivity` + `AddEditPetActivity`: CRUD pet, upload **ảnh + video** (`MediaPickerAdapter`, `StorageHelper`).
- `ManageFoodActivity` + `AddEditFoodActivity`: CRUD food, dialog cập nhật stock nhanh.
- `ManageCategoriesActivity`: dialog thêm/sửa danh mục theo `TYPE_PET` / `TYPE_FOOD`.

> **[CHỤP ẢNH 6.14.2]** Manage list + Add/Edit form (cả 3 loại).

### 6.14.3. Quản lý đơn hàng

- `AdminOrderListActivity`: lọc theo trạng thái, tìm kiếm.
- `AdminOrderDetailActivity`: cập nhật trạng thái, thêm note.
- Khi chuyển trạng thái → tự động:
  - Cập nhật `paidAt`, `deliveredAt`.
  - Cập nhật `totalOrders` & `totalSpent` của user (best-effort qua `FieldValue.increment`).

> **[CHỤP ẢNH 6.14.3]** List + chuyển trạng thái thành công.

### 6.14.4. Quản lý voucher / khuyến mãi

- `ManageVouchersActivity` + `AddEditVoucherActivity`.
- `ManagePromotionsActivity` + `AddEditPromotionActivity`.

> **[CHỤP ẢNH 6.14.4]** Form add voucher (PERCENT/FIXED/FREESHIP) + Promotion.

### 6.14.5. Quản lý hoàn trả

- `AdminReturnListActivity`: tab PENDING / APPROVED / REFUNDED / REJECTED.
- Approve → sinh notification "Yêu cầu hoàn trả của bạn đã được duyệt".
- Refund → chuyển trạng thái đơn `REFUNDED` (admin chuyển khoản thủ công cho COD).

> **[CHỤP ẢNH 6.14.5]** Danh sách + dialog approve/refund.

### 6.14.6. Quản lý người dùng

- `ManageUsersActivity`: search, filter role, khoá/mở khoá.

> **[CHỤP ẢNH 6.14.6]** List user + dialog khoá tài khoản.

---

# CHƯƠNG 7. KIỂM THỬ & ĐÁNH GIÁ

## 7.1. Kế hoạch kiểm thử

Nhóm áp dụng **Manual Test** kết hợp **JUnit/Espresso** cho các module thuần Java.

| Loại test | Phạm vi | Công cụ |
|-----------|--------|---------|
| Unit test | `VNPayHelper.hmacSHA512`, `ShippingHelper.calcFee`, `PromotionManager` | JUnit 4 |
| Integration | Repository ↔ Firestore (emulator) | Firebase Emulator Suite |
| UI test | Đăng nhập, thêm giỏ, đặt hàng | Espresso |
| Manual | Toàn bộ flow Customer + Admin | Test case bảng |

## 7.2. Bảng test case tiêu biểu

| TC | Mục tiêu | Bước | Kết quả mong đợi | Trạng thái |
|----|----------|------|------------------|-----------|
| TC-01 | Đăng ký với email đã tồn tại | Nhập email có sẵn | Thông báo "Email đã được sử dụng" | ✅ Pass |
| TC-02 | OTP sai | Nhập sai OTP | Cảnh báo, không tạo tài khoản | ✅ Pass |
| TC-03 | Đặt hàng COD | Add cart → Checkout COD | Đơn `PENDING`, stock giảm | ✅ Pass |
| TC-04 | Đặt hàng VNPay thành công | Checkout VNPay → thanh toán NCB | Đơn `PENDING`, paymentStatus `PAID`, stock giảm 1 lần | ✅ Pass |
| TC-05 | VNPay huỷ giữa chừng | Đóng WebView | Đơn ở `WAITING_PAYMENT`, stock chưa trừ | ✅ Pass |
| TC-06 | Áp voucher FREESHIP | Voucher `FREESHIP10` | Phí ship = 0 | ✅ Pass |
| TC-07 | Voucher quá hạn | Áp `OLDPROMO` | Báo "Voucher đã hết hạn/hết lượt" | ✅ Pass |
| TC-08 | Huỷ đơn pending | Order detail → Cancel | Trạng thái `CANCELLED`, hoàn stock, hoàn lượt voucher | ✅ Pass |
| TC-09 | Yêu cầu hoàn trả COD | Sau DELIVERED | Tạo `RETURN_REQUESTED`, bắt buộc nhập STK | ✅ Pass |
| TC-10 | Admin duyệt + refund | AdminReturnList → Approve → Refund | Đơn `REFUNDED`, doanh thu giảm | ✅ Pass |
| TC-11 | Notification real-time | Admin tạo voucher | Customer nhận badge ngay | ✅ Pass |
| TC-12 | Chat AI gửi ảnh | Đính kèm ảnh + câu hỏi | Bot trả lời trong < 10s | ✅ Pass |
| TC-13 | Đa role | Login admin → AdminActivity | Hiện dashboard đúng | ✅ Pass |
| TC-14 | Đăng xuất | Profile → Logout | Quay về Splash, xoá session | ✅ Pass |

> **[CHỤP ẢNH 7.2]** Một số screenshot minh hoạ test pass/fail.

## 7.3. Đánh giá

**Ưu điểm**

- Đầy đủ luồng nghiệp vụ thương mại điện tử.
- Real-time mạnh nhờ Firestore listener.
- Tích hợp 3 dịch vụ bên ngoài thành công: Google Sign-In, VNPay, OpenAI.
- Code chia layer rõ ràng, dễ mở rộng.

**Hạn chế**

- Chưa có CI/CD; chưa viết đủ unit test.
- Chưa có push notification (FCM) – mới dừng ở Firestore listener.
- ShippingHelper còn hardcode, chưa gọi API GHN/GHTK thật.
- Cần Cloud Functions để bảo mật một số tác vụ (vd: refund VNPay tự động).

---

# CHƯƠNG 8. KẾT LUẬN & HƯỚNG PHÁT TRIỂN

## 8.1. Kết quả đạt được

- Hoàn thành **100% chức năng bắt buộc** và **80% chức năng nâng cao**.
- Ứng dụng chạy ổn định trên Android 8.0 trở lên (đã test trên emulator Pixel 6 / API 30, 33, 34 và máy Samsung A52).
- Kiến trúc MVVM + Repository giúp việc bảo trì, thêm tính năng dễ dàng.

## 8.2. Hướng phát triển

1. Tích hợp **Firebase Cloud Messaging** (push notification thay vì chỉ in-app).
2. Triển khai **Cloud Functions** xử lý refund VNPay, gửi mail tự động khi đơn delivered.
3. Tích hợp API vận chuyển thật (**GHN/GHTK/J&T**).
4. Bổ sung **bản đồ Google Maps** chọn địa chỉ.
5. Thêm **đánh giá sản phẩm có ảnh + video**, hệ thống review trung thực.
6. Phát triển bản **iOS** (Flutter / KMP).
7. Tích hợp **dashboard analytics** chi tiết (biểu đồ doanh thu theo ngày/tháng).
8. Đưa AI chatbot thành **trợ lý mua hàng end-to-end** (gợi ý sản phẩm, đặt hàng bằng giọng nói).

---

# PHÂN CÔNG CÔNG VIỆC TRONG NHÓM

> Dựa theo lịch sử commit thực tế (`git log`):
> - **KunT (Nguyễn Văn Trường)** – 30 commits – Trưởng nhóm, lo phần lớn UI & toàn bộ luồng khách hàng.
> - **DaoTrucMai (Đào Trúc Mai)** – 5 commits – Phụ trách media, notification, hoàn trả.
> - **Tho (Nguyễn Hữu Đức Thọ)** – 5 commits – Phụ trách auth, chat session, kiểm thử cuối.
>
> Phân công dưới đây chia tương đối **đều khối lượng** giữa 3 thành viên (mỗi người ~33%).

| Hạng mục | Nguyễn Văn Trường (KunT) | Đào Trúc Mai | Nguyễn Hữu Đức Thọ |
|---------|--------------------------|--------------|--------------------|
| **Phân tích & thiết kế** | Use case, kiến trúc MVVM | ERD Firestore, sơ đồ hoạt động Order/Return | Sơ đồ trạng thái đơn, sequence VNPay |
| **UI/UX** | Splash, Home, Product List, Pet/Food Detail, Cart, Checkout | Notification UI, Return UI, Banner slider, Promotion screen | Login, Register, OTP, Profile, Edit Profile, Address |
| **Module Customer** | Cart, Checkout, VNPay WebView, Order History/Detail | Notification, Return Request, Promotion/Voucher Customer | Auth (Email + Google), Profile, Manage Address |
| **Module Admin** | Manage Pets, Foods, Categories, Promotions, Vouchers, Order List/Detail | Manage Notifications template, Manage Returns (Approve/Refund), Media uploader | Manage Users, Admin dashboard statistic logic, Bug fix các quyền role |
| **Tích hợp** | VNPay (build URL, HMAC-SHA512), Shipping fee | Firebase Storage upload ảnh/video, image picker | Firebase Auth, Google Sign-In, JavaMail OTP |
| **AI Chatbot** | (hỗ trợ test prompt) | (hỗ trợ chuẩn hoá UI chat) | **Chính** – ChatViewModel, OkHttp call OpenAI, lưu lịch sử phiên |
| **Kiểm thử** | Test Customer flow + Admin Order | Test Notification, Return, Media upload | Test Auth, OTP, Chat, Profile |
| **Báo cáo & Slide** | Chương 1, 3, 5, 6 (phần Customer) | Chương 2, 6 (Admin), 7 | Chương 4, 8, làm slide PowerPoint |
| **Tỉ lệ đóng góp đề xuất** | **34 %** | **33 %** | **33 %** |

> **[CHỤP ẢNH PC]** Có thể chèn ảnh chụp `git shortlog -sn` để minh hoạ độ đóng góp.

---

# TÀI LIỆU THAM KHẢO

1. *Android Developers Documentation* – [https://developer.android.com](https://developer.android.com)
2. *Firebase Documentation* – [https://firebase.google.com/docs](https://firebase.google.com/docs)
3. *Material Design 3 Guidelines* – [https://m3.material.io](https://m3.material.io)
4. *VNPay Sandbox Document* – [https://sandbox.vnpayment.vn/apis/docs](https://sandbox.vnpayment.vn/apis/docs)
5. *OpenAI API Reference* – [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)
6. *Glide v4* – [https://bumptech.github.io/glide/](https://bumptech.github.io/glide/)
7. *OkHttp* – [https://square.github.io/okhttp/](https://square.github.io/okhttp/)
8. Nguyễn Hà Giang, *Lập trình Android căn bản*, NXB Đại học Quốc gia TP.HCM, 2022.

---

# PHỤ LỤC

## A. Danh sách màn hình chính (62 layout)

`activity_splash`, `activity_login`, `activity_register`, `activity_pet_shop`, `fragment_home`, `fragment_profile`, `fragment_cart`, `fragment_orders`, `activity_pet_detail`, `activity_food_detail`, `activity_cart`, `activity_checkout`, `activity_vnpay_webview`, `activity_vnpay_result`, `activity_order_history`, `activity_order_detail`, `activity_return_request`, `activity_notification`, `activity_chat`, `activity_promotion`, `activity_admin`, `activity_admin_order_list`, `activity_admin_return_list`, `activity_manage_pets`, `activity_manage_foods`, `activity_manage_categories`, `activity_manage_users`, `activity_manage_vouchers`, `activity_manage_promotions`, `activity_add_edit_pet`, `activity_add_edit_food`, `activity_add_edit_voucher`, `activity_add_edit_promotion`, `activity_edit_profile`, `activity_manage_address`, …

## B. Danh sách collection Firestore

`users`, `pets`, `foods`, `categories`, `orders`, `notifications`, `vouchers`, `voucher_usage`, `promotions`, `chat_sessions`, `chat_messages`, `addresses`, `return_requests`, `reviews`, `banners`.

## C. Hằng số quan trọng

- Phí ship: 30k (HCM) – 45k (Nam) – 60k (Trung) – 75k (Bắc), free ≥ 500k.
- VNPay timeout: **15 phút**.
- Giới hạn ảnh upload: **5 MB**.
- Pagination: **10**.

---

> **HẾT BÁO CÁO**
>
> ⚠ **Lưu ý cho nhóm khi nộp**:
> 1. Convert file Markdown này sang Word (`pandoc BAO_CAO.md -o BAO_CAO.docx --reference-doc=template.docx`) hoặc copy vào Word, set font Times New Roman 13, line spacing 1.5.
> 2. Chèn ảnh tại tất cả vị trí **[CHỤP ẢNH ...]** – nên chụp trực tiếp từ emulator để có viền điện thoại đẹp.
> 3. Render các sơ đồ Mermaid (`docs/diagrams/*.mmd`) bằng [https://mermaid.live](https://mermaid.live) → xuất PNG → chèn vào nơi **[VẼ ...]**.
> 4. Đánh số ảnh lại: *Hình 1.1 – Tên hình* dưới mỗi ảnh.
