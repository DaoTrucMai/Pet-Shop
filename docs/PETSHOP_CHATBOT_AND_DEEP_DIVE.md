# 🤖 PETSHOP — Phần mở rộng: Đào sâu Phần B + CHATBOT AI

> Tài liệu này là **phần bổ sung** cho `PETSHOP_EXPLAINED.md`. Đọc file kia trước, rồi đọc file này để hiểu sâu hơn.
>
> Gồm 2 phần:
> - **Phần I:** Mở rộng Phần B (chi tiết thêm về cấu trúc, Firebase, Auth, Address, Notification).
> - **Phần II:** Chatbot AI — luồng hoạt động, vì sao trả lời được, lấy thông tin ra sao.

---

# 🧩 PHẦN I — MỞ RỘNG PHẦN B (chi tiết thêm)

## I.1 Cấu trúc dự án — Chi tiết hơn về Gradle build

Khi giáo viên hỏi "code chạy ra apk như nào?", bạn nên biết thứ tự build:

```
1. Android Studio bấm Build/Run
        ▼
2. Gradle đọc settings.gradle.kts
        ▼
3. Gradle đọc build.gradle.kts (root) → apply plugin
        ▼
4. Gradle đọc app/build.gradle.kts
        ▼
5. Plugin google-services đọc google-services.json
   → sinh ra file values.xml chứa Firebase config
        ▼
6. Đọc local.properties → inject vào BuildConfig.java
   (sinh ra trong app/build/generated/source/buildConfig/...)
        ▼
7. ViewBinding generator quét layout XML → sinh class binding
        ▼
8. Compile Java + xử lý resources → APK/AAB
        ▼
9. Sign APK bằng keystore → cài lên máy
```

**Hệ quả thực tế:**
- Sửa `local.properties` xong **phải Sync Gradle** mới có hiệu lực (vì `BuildConfig` cần được sinh lại).
- Mất `google-services.json` → app build vẫn được nhưng Firebase **không chạy**.
- Đổi `applicationId` (package name) → phải tải lại `google-services.json` từ Firebase Console với package mới.

## I.2 Firebase — Security Rules (giáo viên giỏi sẽ hỏi)

Một câu hỏi rất hay bị bỏ qua: **"Ai có thể đọc/ghi Firestore của em?"**

Project hiện tại **không kèm file `firestore.rules`** (file rules nằm ở Firebase Console). Nhưng bạn cần biết khái niệm:

```js
// Ví dụ Security Rule cần có (chưa có trong project, NÊN bổ sung)
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Users: chỉ chính chủ + admin mới được đọc/ghi user của mình
    match /users/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;

      // Subcollection addresses cũng vậy
      match /addresses/{addrId} {
        allow read, write: if request.auth != null && request.auth.uid == uid;
      }
    }

    // Pets, Foods: ai cũng đọc được, chỉ ADMIN ghi
    match /pets/{petId} {
      allow read: if true;
      allow write: if request.auth != null
                   && get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == "ADMIN";
    }

    // Orders: chỉ chính chủ đọc, chỉ admin sửa status
    match /orders/{orderId} {
      allow read: if request.auth != null
                  && (resource.data.userId == request.auth.uid
                      || get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == "ADMIN");
      allow create: if request.auth != null;
    }
  }
}
```

> ⚠️ **Nếu giáo viên hỏi:** "Em có Security Rules không?" → Trả lời thẳng: "Hiện em đang dùng rules test mode (cho phép tất cả) để dev. Trước khi production em sẽ siết theo logic: user chỉ đọc/ghi data của chính mình, ADMIN mới được CRUD pet/food/order. Em sẽ kiểm tra `request.auth.uid` và `role` trong Firestore."

## I.3 Firebase Offline Cache (đặc tính ít người biết)

Firestore **tự động cache local**. Khi app:
- Mất mạng → vẫn đọc được data đã từng load (từ cache SQLite ngầm).
- Có lại mạng → tự động sync ngược lên server.

→ Đây là lý do app vẫn xem được giỏ hàng khi không có mạng. Bạn KHÔNG cần code Room riêng.

## I.4 Auth Email — Các trường hợp edge case bạn cần biết

| Tình huống | Behavior Firebase | App xử lý |
|---|---|---|
| User đăng ký xong, đóng app | Firebase Auth giữ session vĩnh viễn | `getCurrentUser() != null` → tự vào app |
| User xoá app, cài lại | Session bị xóa | Phải login lại |
| Đổi password ở thiết bị khác | Token cũ bị invalid sau ~1h | Lần gọi API tiếp theo bị throw → quay về Login |
| Xóa account ở Firebase Console | User vẫn có token, nhưng `getUserData` fail | App cần xử lý lỗi này |
| Đăng ký Email rồi đăng ký Google CÙNG email | Firebase **gộp** thành 1 account (provider linking) | Code project chưa xử lý đặc biệt — user vẫn login được |

## I.5 Auth Google — Lifecycle của `idToken`

- `idToken` của Google có **hiệu lực 1 giờ**.
- Sau khi đổi sang Firebase Credential, Firebase **tự cấp `FirebaseIdToken` riêng** (cũng hết hạn 1 giờ).
- Firebase SDK tự refresh token ngầm khi sắp hết hạn → user không cần đăng nhập lại.

→ Đó là lý do user mở app sau 1 tuần vẫn vào được luôn, không cần re-login.

## I.6 Address — Vấn đề thiết kế hiện tại

Đoạn code này trong `Address.java` rất tinh tế:
```java
@com.google.firebase.firestore.PropertyName("isDefault")
public boolean isDefault() { return isDefault; }

@com.google.firebase.firestore.PropertyName("isDefault")
public void setDefault(boolean aDefault) { isDefault = aDefault; }
```

→ **Vì sao cần `@PropertyName`?**

Theo JavaBeans convention, field `isDefault` (kiểu boolean) sẽ có getter là `isDefault()` và setter là `setDefault(...)`. Firestore sẽ tự suy ra tên field là `"default"` (bỏ chữ "is") khi serialize → SAI! Field bên Firestore là `"isDefault"`.

`@PropertyName("isDefault")` ép Firestore dùng tên này khi đọc/ghi → đồng bộ giữa Java và Firestore.

**Đây là bug rất hay gặp với Java + Firestore** — đáng nói khi báo cáo. Nếu giáo viên hỏi "Vì sao có annotation `@PropertyName`?" → bạn trả lời được = ăn điểm.

## I.7 Notification — Vì sao KHÔNG dùng FCM (Push Notification)?

Đây là câu hỏi nâng cao. **FCM (Firebase Cloud Messaging)** là cơ chế push thông báo từ server xuống device, hiện trên thanh status bar **ngay cả khi app đóng**.

Project hiện tại **KHÔNG có FCM**. Chỉ có:
- Lưu doc trong `notifications/{id}` ở Firestore
- Real-time listener trong app đang mở (HomeFragment)

**Hệ quả:**
- App đóng → user **không nhận được thông báo** từ thanh notification.
- Chỉ khi mở app, badge mới cập nhật.

> Nếu giáo viên hỏi: "Sao đóng app không có thông báo?"
> **Trả lời:** "Em chưa tích hợp FCM. Hiện tại notification chỉ hiện in-app. Để có push notification khi app đóng, em sẽ: (1) thêm dependency `firebase-messaging`, (2) implement `FirebaseMessagingService` để nhận message, (3) viết Cloud Function trigger khi có doc mới trong `notifications/` → gửi FCM tới user. Em chưa làm vì project dùng free tier, Cloud Functions cần Blaze plan."

---

# 🤖 PHẦN II — CHATBOT AI (CHỦ ĐỀ MỚI, SIÊU CHI TIẾT)

Đây là **phần kỹ thuật xịn nhất** của project. Nếu bạn làm chủ phần này → bảo vệ đỉnh.

## II.1 Tổng quan: Chatbot là cái gì trong project?

```
┌─────────────────────────────────────────────────────────┐
│  USER                                                   │
│   "Shop có chó Corgi không? Giá bao nhiêu?"             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  ChatActivity (UI)                                      │
│   - 1 màn hình chat giống Messenger                     │
│   - Có thể gõ chữ, nói giọng, gửi ảnh                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  ChatViewModel                                          │
│   - Quản lý messages, sessions                          │
│   - Gom toàn bộ data shop từ Firestore (userContext)    │
│   - Gọi OpenAI API qua OkHttp                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  OpenAI ChatGPT (gpt-4o-mini)                           │
│   - Đọc prompt + dữ liệu shop                           │
│   - Sinh câu trả lời (streaming chunk by chunk)         │
└─────────────────────────────────────────────────────────┘
```

**Điều quan trọng:** ChatGPT **KHÔNG biết** shop của bạn có gì. Nó là model AI chung. **Bí mật làm cho nó "biết"** chính là phần thú vị nhất → giải thích ngay dưới đây.

## II.2 ❓ VÌ SAO CHATBOT CÓ THỂ TRẢ LỜI ĐƯỢC CHÍNH XÁC?

> **Câu trả lời ngắn:** Vì app **NHỒI toàn bộ dữ liệu shop vào prompt** trước khi gửi câu hỏi cho ChatGPT. Đây là kỹ thuật gọi là **"Context Injection"** hoặc đơn giản hơn là **"Retrieval-Augmented Generation (RAG) phiên bản đơn giản"**.

### Hình dung như này:

ChatGPT giống một học sinh giỏi nhưng không biết shop của bạn. App đóng vai trò **trợ giảng**:
1. Trợ giảng (app) đứng cạnh ChatGPT.
2. Khi user hỏi, trợ giảng đưa cho ChatGPT 1 tờ giấy ghi:
   - "Đây là DANH MỤC shop có: Chó, Mèo, Cá…"
   - "Đây là TẤT CẢ THÚ CƯNG ĐANG BÁN: Corgi 5tr, Husky 7tr, Mèo Anh 3tr…"
   - "Đây là KHUYẾN MÃI: Giảm 20% chó Corgi đến 31/12…"
   - "Đây là ĐƠN HÀNG CỦA USER NÀY: ORD123 đang giao, ORD456 đã hoàn thành…"
3. **Kèm câu hỏi của user**: "Shop có chó Corgi không? Giá bao nhiêu?"
4. ChatGPT đọc tờ giấy → tìm thông tin → trả lời.

→ Đây là **cốt lõi**. Hãy thuộc câu này:

> **"Em không huấn luyện AI riêng. Em dùng API ChatGPT của OpenAI. Mỗi lần user hỏi, em gom toàn bộ dữ liệu shop (pet, food, khuyến mãi, đơn hàng của user…) từ Firestore, ghép vào phần `system message` của prompt, rồi gửi cùng câu hỏi cho ChatGPT. ChatGPT chỉ trả lời dựa trên dữ liệu em cung cấp."**

## II.3 Cấu trúc 1 lần gọi API tới OpenAI

OpenAI Chat Completion API nhận **danh sách messages**, mỗi message có 3 vai trò:

| Role | Vai trò |
|---|---|
| `system` | "Hướng dẫn" cho AI — quy tắc, nhân vật, dữ liệu nền. Đặt ở đầu. |
| `user` | Câu user nói |
| `assistant` | Câu AI đã trả lời trước đó (để giữ ngữ cảnh hội thoại) |

App build JSON gửi lên giống như này:

```json
{
  "model": "gpt-4o-mini",
  "stream": true,
  "messages": [
    {
      "role": "system",
      "content": "Bạn là trợ lý ảo PetShop. DỰA VÀO DỮ LIỆU SAU ĐỂ TRẢ LỜI:\nDANH MỤC: Chó, Mèo, Cá, Chim...\n\nTHÚ CƯNG ĐANG BÁN:\n- Pet: Corgi vàng | ID: abc | Loài: DOG | Giống: Corgi | Tuổi: 3 tháng | Giá: 5500000đ | Vaccine: FULL | Tẩy giun: Có ...\n- Pet: Husky | ID: xyz ...\n\nTHỨC ĂN/PHỤ KIỆN:\n- Food: Royal Canin 1kg | Giá: 250000đ | Tồn kho: 45 ...\n\nĐƠN HÀNG CỦA BẠN: Mã ORD123 (DELIVERED, tổng 5500000đ), ...\n\nKHUYẾN MÃI: Sale tháng 12: Giảm 20% chó Corgi...\n\nVOUCHER: FREESHIP50K (Miễn ship đơn từ 200k)...\n\nQUY TẮC: 1. Chỉ dùng dữ liệu trên... 2. Không trả lời ngoài lề thú cưng... 3. Trả lời tiếng Việt thân thiện..."
    },
    {
      "role": "user",
      "content": "Chào shop"
    },
    {
      "role": "assistant",
      "content": "Chào bạn! Bạn cần tư vấn gì hôm nay?"
    },
    {
      "role": "user",
      "content": "Shop có chó Corgi không? Giá bao nhiêu?"
    }
  ]
}
```

ChatGPT đọc `system message`, thấy có "Corgi vàng | Giá: 5500000đ" → trả lời: *"Dạ shop có chó Corgi vàng 3 tháng tuổi, giá 5,500,000đ, đã tiêm vaccine đầy đủ và tẩy giun. Bạn có muốn xem chi tiết không?"*

## II.4 LẤY THÔNG TIN NHƯ THẾ NÀO? — Phân tích `initContext()`

Đây là phần **CHUẨN BỊ data**. Được gọi 1 lần khi mở `ChatActivity`:

```java
public void initContext(String userId) {
    // Kiểm tra nếu userId thay đổi, clear dữ liệu cũ
    if (!userId.equals(currentUserId)) {
        clearChatDataInternal();
    }
    this.currentUserId = userId;
    loadSessions();

    StringBuilder sb = new StringBuilder();

    new CategoryRepository().getAll(new CategoryRepository.Callback<>() {
        @Override
        public void onSuccess(List<Category> data) {
            sb.append("DANH MỤC: ");
            if (data != null) {
                for (Category c : data) {
                    if (c != null && c.isActive()) {
                        sb.append(c.getName()).append(", ");
                    }
                }
            }
            fetchPets(currentUserId, sb);
        }
```

### Pattern "Callback Chaining" — Quan trọng phải hiểu

Vì Firebase call là **async**, không thể viết tuần tự thẳng:
```java
// ❌ KHÔNG LÀM ĐƯỢC vì các call async
categoryRepo.getAll();
petRepo.getAll();
foodRepo.getAll();
// → các call này chạy đồng thời, không biết cái nào xong trước
```

Project dùng pattern **callback chain** — call sau gọi trong onSuccess của call trước:

```
initContext(userId)
   │
   ▼
1. CategoryRepository.getAll()  → onSuccess
       │  sb.append("DANH MỤC: ...")
       ▼
2. PetRepository.getAll()       → onSuccess
       │  sb.append("THÚ CƯNG ĐANG BÁN: ...")
       ▼
3. FoodRepository.getAll()      → onSuccess
       │  sb.append("THỨC ĂN/PHỤ KIỆN: ...")
       ▼
4. OrderRepository.getOrdersByUser(uid)  → onSuccess
       │  sb.append("ĐƠN HÀNG CỦA BẠN: ...")
       ▼
5. PromotionRepository.getActive()  → onSuccess
       │  sb.append("KHUYẾN MÃI: ...")
       ▼
6. VoucherRepository.getAll()  → onSuccess
       │  sb.append("VOUCHER: ...")
       │
       └─► userContext = sb.toString();   // ★ DỮ LIỆU SẴN SÀNG
```

> ⚠️ **Đây gọi là "callback hell"** — pattern phổ biến khi viết Java async. Nhược điểm: code lồng nhau khó đọc. Nếu dùng Kotlin Coroutine sẽ viết tuần tự dễ hơn nhiều.

### Code mỗi bước fetch

Mỗi bước có cấu trúc giống nhau (vd `fetchPets`):
```java
private void fetchPets(String userId, StringBuilder sb) {
    new PetRepository().getAll(new PetRepository.Callback<>() {
        @Override
        public void onSuccess(List<Pet> data) {
            sb.append("\nTHÚ CƯNG ĐANG BÁN:\n");
            if (data != null) {
                int count = 0;
                for (Pet p : data) {
                    if (p != null && p.isAvailable() && count < 30) {
                        sb.append(formatPetForAI(p)).append("\n");
                        count++;
                    }
                }
            }
            fetchFoods(userId, sb);
        }

        @Override
        public void onFailure(String error) {
            fetchFoods(userId, sb);   // ★ Lỗi vẫn chuyển bước tiếp
        }
    });
}
```

→ Lưu ý 3 chi tiết hay:
1. **Giới hạn 30 sản phẩm** (`count < 30`). Vì OpenAI tính tiền theo số token, không thể nhồi 1000 pet vào prompt → giới hạn để rẻ và nhanh.
2. **Chỉ lấy pet `isAvailable()`** — không nhồi pet `SOLD/RESERVED` vào prompt (vô nghĩa).
3. **`onFailure` vẫn gọi `fetchFoods`** — không dừng pipeline. Một bước fail, các bước sau vẫn chạy.

### Format dữ liệu cho AI — `formatPetForAI()`

```java
private String formatPetForAI(Pet p) {
    if (p == null) return "";

    StringBuilder s = new StringBuilder();
    s.append("- Pet: ").append(safe(p.getName()));

    appendField(s, "ID", p.getId());
    appendField(s, "Loài", p.getSpecies());
    appendField(s, "Giống", p.getBreed());
    appendField(s, "Danh mục", p.getCategory() != null ? p.getCategory().getName() : p.getCategoryId());
    appendField(s, "Tuổi", p.getAge() + " " + safe(p.getAgeUnit()));
    appendField(s, "Giới tính", p.getGender());
    appendField(s, "Cân nặng", p.getWeight() > 0 ? p.getWeight() + " kg" : "");
    ...
    appendField(s, "Giá", String.valueOf((long) p.getEffectivePrice()) + "đ");
    appendField(s, "Vaccine", p.getVaccineStatus());
    appendField(s, "Tẩy giun", p.isDewormed() ? "Có" : "Không");
    ...
}
```

→ **Bí quyết:** Mỗi pet được biểu diễn thành 1 dòng text có cấu trúc `Field: Value | Field: Value`. Đây là format AI đọc rất tốt (rõ ràng hơn JSON với AI). Ví dụ:

```
- Pet: Corgi vàng | ID: pet-001 | Loài: DOG | Giống: Corgi | Tuổi: 3 tháng |
  Giới tính: MALE | Cân nặng: 4.5 kg | Màu: Vàng | Xuất xứ: Việt Nam |
  Giá: 5500000đ | Vaccine: FULL | Tẩy giun: Có | Đánh giá: 4.8 sao / 12 đánh giá
```

ChatGPT đọc dòng này, nếu user hỏi "Corgi đã tiêm vaccine chưa?" → AI tìm thấy `Vaccine: FULL` → trả lời được.

## II.5 FLOW HOẠT ĐỘNG ĐẦY ĐỦ — Từ lúc user gõ câu hỏi tới khi thấy câu trả lời

Tôi vẽ flow đầy đủ 1 lần gửi tin nhắn:

```
[T=0ms] User nhập "Shop có Corgi không?" → bấm Send
        │
        ▼
[T=1ms] ChatActivity.sendMessage()
        │   - Tạo ChatMessage(text, imgUri, TYPE_USER)
        │   - Gọi vm.sendMessage(userMsg)
        ▼
[T=2ms] ChatViewModel.sendMessage(msg)
        │   - Nếu không có ảnh: addMessageInternal(msg) + callOpenAI(text, null)
        │   - Nếu có ảnh: uploadImageAndSend(msg) → upload lên Firebase Storage trước
        ▼
[T=3ms] addMessageInternal(msg)
        │   - Thêm msg vào messages LiveData → UI hiện bóng chat "User"
        │   - saveMessageToFirestore(msg) → ghi msg vào users/{uid}/chats
        ▼
[T=10ms] callOpenAI(userMsg, null)
        │   - isTyping.postValue(true) → UI hiện "AI đang soạn câu trả lời..."
        │   - Build JSON body:
        │       + system message (gồm userContext đã chuẩn bị từ initContext)
        │       + 6 message gần nhất từ history (để AI giữ ngữ cảnh)
        │       + user message hiện tại
        │   - "stream": true → bật chế độ streaming
        ▼
[T=15ms] OkHttp gửi POST tới https://api.openai.com/v1/chat/completions
        │   - Header: Authorization: Bearer sk-...
        │   - Body: JSON ở trên
        ▼
[T=500ms - 3000ms] OpenAI trả về response dạng STREAMING (chunked)
        │   data: {"choices":[{"delta":{"content":"Dạ"}}]}
        │   data: {"choices":[{"delta":{"content":" shop"}}]}
        │   data: {"choices":[{"delta":{"content":" có"}}]}
        │   data: {"choices":[{"delta":{"content":" Corgi"}}]}
        │   ...
        │   data: [DONE]
        ▼
[T=500ms] App nhận chunk đầu tiên "Dạ"
        │   - fullText = "Dạ"
        │   - Tạo ChatMessage("Dạ", TYPE_BOT) → cập nhật messages LiveData
        │   - UI render bóng chat AI hiện "Dạ"
        ▼
[T=600ms] Chunk thứ 2 " shop"
        │   - fullText = "Dạ shop"
        │   - UPDATE message cuối cùng trong list (không thêm mới)
        │   - UI hiện "Dạ shop"
        ▼
[T=700ms+] Tiếp tục append từng từ
        │   "Dạ shop có"
        │   "Dạ shop có Corgi"
        │   "Dạ shop có Corgi vàng"
        │   ...
        ▼
[T=3000ms] Nhận "data: [DONE]" → kết thúc
        │   - isTyping.postValue(false) → UI hiện "Đang hoạt động"
        │   - saveMessageToFirestore(finalMsg) → ghi câu trả lời cuối vào Firestore
        │   - Update title session nếu là tin nhắn đầu (vd "Shop có Corgi không?...")
        ▼
[Kết thúc] User thấy câu trả lời đầy đủ, được lưu vào lịch sử chat
```

## II.6 STREAMING — Vì sao chữ "đánh máy" từ từ?

Đây là điểm **hay nhất** về kỹ thuật. Tôi giải thích chi tiết:

### Streaming là gì?

Bình thường gọi API: bạn gửi request → đợi → nhận **toàn bộ** response cùng lúc. Vd 2 giây mới có chữ.

Streaming: bạn nhận response **từng phần nhỏ** (chunk) **ngay khi server vừa sinh ra**. Vd 0.2s đã có chữ đầu, từng từ đổ về liên tục.

### Cách OpenAI làm

OpenAI dùng giao thức **Server-Sent Events (SSE)**. Mỗi chunk có dạng:
```
data: {"choices":[{"delta":{"content":"từ"}}]}

data: {"choices":[{"delta":{"content":" tiếp"}}]}

data: [DONE]
```

### Code app xử lý

```java
okio.BufferedSource source = response.body().source();
StringBuilder fullText = new StringBuilder();

while (true) {
    String line = source.readUtf8Line();
    if (line == null) break;

    if (line.startsWith("data: ")) {
        String data = line.substring(6);
        if (data.equals("[DONE]")) break;

        try {
            JsonObject chunk = gson.fromJson(data, JsonObject.class);
            JsonArray choices = chunk.getAsJsonArray("choices");

            if (choices.size() > 0) {
                JsonObject delta = choices.get(0)
                        .getAsJsonObject()
                        .getAsJsonObject("delta");

                if (delta.has("content")) {
                    String content = delta.get("content").getAsString();
                    fullText.append(content);

                    ChatMessage updatedMsg =
                            new ChatMessage(fullText.toString(), ChatMessage.TYPE_BOT);
                    ...
                    List<ChatMessage> currentList = messages.getValue();
                    if (currentList != null && !currentList.isEmpty()) {
                        List<ChatMessage> newList = new ArrayList<>(currentList);
                        newList.set(newList.size() - 1, updatedMsg);
                        messages.postValue(newList);
                    }
                }
            }
        } catch (Exception ignored) { }
    }
}
```

**Giải thích từng dòng:**
1. `response.body().source()` — lấy "ống đọc" tới body response (chưa load full).
2. `while (true) { readUtf8Line() }` — đọc từng dòng một (vòng lặp).
3. Mỗi dòng bắt đầu bằng `"data: "` → parse JSON → lấy `delta.content` (chữ mới).
4. `fullText.append(content)` — gom lại thành chuỗi đầy đủ.
5. **Cập nhật message cuối cùng** trong list (không thêm mới) → UI render lại bóng chat AI với text dài hơn.
6. Khi gặp `[DONE]` → thoát vòng lặp → lưu vào Firestore.

### Lợi ích Streaming

| | Không streaming | Streaming |
|---|---|---|
| Thời gian thấy chữ đầu tiên | 2-5 giây | 0.2-0.5 giây |
| Cảm giác user | Đợi mòn mỏi | Thấy AI "đang nghĩ" |
| Có thể dừng giữa chừng? | Không | Có (đóng connection) |

> Nếu giáo viên hỏi "Sao chat AI đánh máy từ từ vậy em?" → Trả lời: "Em dùng `stream=true` của OpenAI API. Server gửi response theo dạng Server-Sent Events từng chunk nhỏ. Em đọc từng chunk bằng OkHttp `BufferedSource.readUtf8Line()`, parse JSON lấy delta content, ghép lại và cập nhật LiveData liên tục. UX giống ChatGPT chính chủ."

## II.7 MULTIMODAL — Gửi ảnh kèm câu hỏi

GPT-4o-mini có khả năng **"nhìn"** ảnh. App tận dụng để user gửi ảnh con vật rồi hỏi: "Đây là chó gì?"

### Cách làm

```java
JsonObject user = new JsonObject();
user.addProperty("role", "user");

if (imgUri != null) {
    JsonArray content = new JsonArray();

    JsonObject textPart = new JsonObject();
    textPart.addProperty("type", "text");
    textPart.addProperty("text", userMsg);
    content.add(textPart);

    String base64 = uriToBase64(imgUri);
    if (base64 != null) {
        JsonObject imgPart = new JsonObject();
        imgPart.addProperty("type", "image_url");

        JsonObject imgUrl = new JsonObject();
        imgUrl.addProperty("url", "data:image/jpeg;base64," + base64);

        imgPart.add("image_url", imgUrl);
        content.add(imgPart);
    }

    user.add("content", content);
    ...
```

→ Khi có ảnh, `content` là **mảng** thay vì string thường:
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Đây là chó gì?"},
    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,/9j/4AAQ..."}}
  ]
}
```

Ảnh được encode **Base64** rồi nhúng thẳng vào URL (data URI). Trước đó còn resize:

```java
private String uriToBase64(String uriString) {
    try {
        Uri uri = Uri.parse(uriString);
        InputStream inputStream = getApplication().getContentResolver().openInputStream(uri);
        Bitmap bitmap = BitmapFactory.decodeStream(inputStream);

        if (bitmap == null) return null;

        if (bitmap.getWidth() > 1024 || bitmap.getHeight() > 1024) {
            float scale = Math.min(
                    1024f / bitmap.getWidth(),
                    1024f / bitmap.getHeight()
            );

            bitmap = Bitmap.createScaledBitmap(
                    bitmap,
                    (int) (bitmap.getWidth() * scale),
                    (int) (bitmap.getHeight() * scale),
                    true
            );
        }

        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 80, outputStream);

        byte[] bytes = outputStream.toByteArray();
        return Base64.encodeToString(bytes, Base64.NO_WRAP);
    } catch (Exception e) {
        e.printStackTrace();
        return null;
    }
}
```

**3 bước xử lý ảnh:**
1. Decode URI → `Bitmap`
2. Resize nếu lớn hơn 1024px (tiết kiệm bandwidth + token)
3. Compress JPEG quality 80% → encode Base64 → trả về string

→ Ảnh còn được **upload lên Firebase Storage** để lưu lại trong lịch sử chat (không phải base64 vĩnh viễn).

## II.8 VOICE INPUT — Nói thay vì gõ

```java
private void startVoiceRecognition() {
    Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
    intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
    intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
    intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Hãy nói gì đó...");

    try {
        speechLauncher.launch(intent);
    } catch (Exception e) {
        Toast.makeText(this, "Thiết bị không hỗ trợ nhận diện giọng nói", Toast.LENGTH_SHORT).show();
    }
}
```

→ Dùng **`RecognizerIntent.ACTION_RECOGNIZE_SPEECH`** — đây là intent **có sẵn của Android**. Khi launch:
1. Hệ thống Android mở popup "Đang nghe..."
2. User nói câu cần hỏi
3. Google Speech-to-Text (free, có sẵn) chuyển giọng thành text
4. Text về app qua `speechLauncher` callback
5. Set vào ô EditText → user vẫn có thể sửa rồi bấm Send

**Lợi:** Không cần API key, không cần thư viện ngoài, dùng dịch vụ Google sẵn có trong Android.

## II.9 SESSION MANAGEMENT — Quản lý nhiều cuộc trò chuyện

Chatbot cho phép có **nhiều phiên chat song song**, giống ChatGPT website. Code phức tạp vì có **2 chế độ**:

### Chế độ A: User đã đăng nhập → Lưu Firestore

Cấu trúc Firestore:
```
users/{uid}/
   ├── sessions/             ← subcollection: các cuộc trò chuyện
   │   └── {sessionId}/
   │       ├── id, title (vd "Shop có Corgi không?...")
   │       └── lastTimestamp
   │
   └── chats/                ← subcollection: tất cả message
       └── {auto-id}/
           ├── text, type, timestamp
           └── sessionId     ← key để filter theo session
```

→ Query "lấy messages của session X":
```java
FirebaseHelper.db().collection("users").document(currentUserId)
        .collection("chats")
        .whereEqualTo("sessionId", sessionId)
        .orderBy("timestamp", Query.Direction.ASCENDING)
        .get()
```

### Chế độ B: User là khách (chưa login) → Lưu SharedPreferences

```java
private void loadGuestMessages(String sessionId) {
    String json = getApplication()
            .getSharedPreferences(PREFS_NAME, android.content.Context.MODE_PRIVATE)
            .getString(KEY_GUEST_MSGS + "_" + sessionId, null);
    if (json != null && !json.isEmpty()) {
        Type listType = new TypeToken<List<ChatMessage>>() {}.getType();
        List<ChatMessage> history = gson.fromJson(json, listType);
        messages.postValue(history != null ? history : new ArrayList<>());
    } else {
        messages.postValue(new ArrayList<>());
        addWelcomeMessage();
    }
}
```

→ Dùng **Gson** convert `List<ChatMessage>` → JSON string → ghi vào SharedPreferences. Khi đọc thì decode ngược lại.

**Giới hạn:** chỉ giữ 50 message gần nhất (`GUEST_MSG_LIMIT = 50`) để khỏi nặng máy.

> Pattern này hay vì cho phép **khách dùng chatbot mà không cần đăng nhập**, vẫn có lịch sử (local). Khi user login sau đó, chat cũ vẫn còn.

## II.10 TỐI ƯU GIỮ NGỮ CẢNH — Tại sao chỉ gửi 6 message gần nhất?

```java
List<ChatMessage> history = messages.getValue();
if (history != null) {
    int start = Math.max(0, history.size() - 7);
    for (int i = start; i < history.size() - 1; i++) {
        ChatMessage m = history.get(i);
        JsonObject h = new JsonObject();
        h.addProperty("role", m.getType() == ChatMessage.TYPE_USER ? "user" : "assistant");
        h.addProperty("content", m.getText());
        msgs.add(h);
    }
}
```

→ Lý do:
1. **Tiết kiệm token** — OpenAI tính tiền theo token. Gửi 100 message cũ rất tốn.
2. **Tránh quá giới hạn context window** — GPT-4o-mini có max ~128K token, nhưng càng nhiều history → AI càng chậm + dễ "quên" thông tin quan trọng (system message).
3. **6 tin nhắn = ~3 lượt qua lại** đủ để AI giữ mạch hội thoại ngắn.

> Trade-off: nếu user nói "Quay lại con Corgi mà em hỏi ban đầu" sau 20 lượt → AI có thể quên. Đây là **giới hạn**, không phải bug.

## II.11 BẢNG TÓM TẮT TOÀN BỘ CHATBOT

```
┌────────────────────────────────────────────────────────────────┐
│                    KIẾN TRÚC CHATBOT                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  INPUT (3 dạng):                                               │
│   - Text (gõ tay)                                              │
│   - Voice (nói → Google Speech-to-Text → text)                 │
│   - Image (gửi ảnh → resize → base64)                          │
│                                                                │
│  DATA SOURCE (6 Repository):                                   │
│   - CategoryRepository  → danh mục                             │
│   - PetRepository       → 30 pet đang bán                      │
│   - FoodRepository      → 30 food đang bán                     │
│   - OrderRepository     → đơn hàng của user                    │
│   - PromotionRepository → khuyến mãi đang active               │
│   - VoucherRepository   → voucher active                       │
│   → Gom thành userContext (string lớn)                         │
│                                                                │
│  PROMPT (gửi tới OpenAI):                                      │
│   - system: hướng dẫn + userContext + 5 quy tắc                │
│   - history: 6 message gần nhất                                │
│   - user: câu hỏi hiện tại (+ ảnh nếu có)                      │
│                                                                │
│  API CALL:                                                     │
│   - POST https://api.openai.com/v1/chat/completions            │
│   - Model: gpt-4o-mini                                         │
│   - Stream: true (SSE)                                         │
│   - Auth: Bearer Token (lưu trong BuildConfig)                 │
│                                                                │
│  OUTPUT:                                                       │
│   - Stream từng chunk → cập nhật UI dần                        │
│   - Lưu message vào Firestore (user đã login)                  │
│       hoặc SharedPreferences (khách)                           │
│   - Auto-set title cho session từ câu hỏi đầu tiên             │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## II.12 ĐIỂM YẾU VÀ CẢI TIẾN (nếu giáo viên hỏi)

| Điểm yếu hiện tại | Cách khắc phục |
|---|---|
| `OPENAI_API_KEY` nằm trong BuildConfig → ai decompile APK lấy được | Chuyển sang gọi qua proxy backend của mình, giấu API key |
| Mỗi lần chat đều fetch full 30 pet + 30 food → tốn token | Dùng **embedding + vector search**: chỉ lấy pet liên quan tới câu hỏi (RAG đúng nghĩa) |
| Chỉ 6 history → AI "quên" hội thoại dài | Tăng lên hoặc summarize hội thoại cũ thành 1 đoạn ngắn |
| Không có "function calling" → AI không thể tự thêm pet vào giỏ | Dùng OpenAI **Function Calling** để AI gọi `addToCart()` thay user |
| Nếu Firestore có 1000 pet, chỉ 30 vào prompt → user hỏi pet thứ 50 sẽ không có trong context | Search trước theo từ khóa user → lấy đúng pet liên quan |

> **Câu trả lời mẫu khi giáo viên hỏi "Có gì cần cải thiện?":**
> "Em sẽ chuyển sang dùng kỹ thuật **RAG (Retrieval-Augmented Generation) đúng nghĩa**: dùng embedding model để tạo vector cho từng pet/food, lưu vào vector database (như Pinecone). Khi user hỏi, em embed câu hỏi rồi tìm top-K pet gần nhất về ngữ nghĩa → chỉ gửi vài pet liên quan vào prompt. Như vậy vừa rẻ token, vừa hỗ trợ shop có hàng nghìn sản phẩm. Em cũng sẽ giấu API key qua backend proxy để chống decompile."

## II.13 CÂU HỎI GIÁO VIÊN HAY HỎI VỀ CHATBOT

**Q: "Em tự train AI à?"**
> Không. Em dùng API OpenAI ChatGPT (model gpt-4o-mini). Em chỉ "hướng dẫn" AI qua prompt + cung cấp dữ liệu shop để AI dựa vào đó trả lời.

**Q: "Sao AI biết shop của em có gì?"**
> Em dùng kỹ thuật **Context Injection**: trước mỗi lần gọi API, em fetch toàn bộ data shop (danh mục, pet, food, đơn hàng, khuyến mãi, voucher) từ Firestore, format thành text rồi ghép vào `system message` của prompt. AI đọc text này như đọc cheatsheet rồi trả lời. AI không lưu data sau khi trả lời — mỗi lần gọi API là 1 lần gửi data mới.

**Q: "Bao nhiêu data em gửi cho AI?"**
> Em giới hạn 30 pet + 30 food + tất cả category + đơn hàng của user + khuyến mãi/voucher đang active. Tổng cộng khoảng 5-10K token mỗi request, đủ ngắn để tiết kiệm chi phí mà vẫn cover phần lớn shop.

**Q: "Sao response hiện ra từng chữ giống ChatGPT?"**
> Em bật `stream: true` khi gọi API. OpenAI trả về response dạng **Server-Sent Events** từng chunk nhỏ. Em đọc bằng OkHttp `BufferedSource.readUtf8Line()`, parse JSON từng chunk rồi cập nhật LiveData liên tục → UI tự render lại.

**Q: "Chat có nhớ ngữ cảnh không?"**
> Có nhưng giới hạn. Mỗi request em gửi kèm 6 message gần nhất trong session → AI biết user vừa hỏi gì. Em không gửi quá nhiều để tiết kiệm token.

**Q: "User chưa đăng nhập có chat được không?"**
> Có. Khách vẫn chat được, em lưu lịch sử vào SharedPreferences (local) với giới hạn 50 message. Khi login, em sẽ có cơ chế migrate dữ liệu (chưa làm).

**Q: "Em xử lý ảnh thế nào?"**
> 3 bước: (1) đọc ảnh từ URI → Bitmap, (2) resize về tối đa 1024px, compress JPEG 80%, (3) encode Base64 nhúng thẳng vào prompt theo định dạng data URI. Mô hình gpt-4o-mini có khả năng "nhìn" ảnh nên trả lời được câu hỏi như "Đây là chó gì?". Đồng thời ảnh được upload lên Firebase Storage để lưu vào lịch sử.

**Q: "Voice nhận diện thế nào?"**
> Em dùng `RecognizerIntent` có sẵn của Android. Khi user bấm icon mic, em launch intent → hệ thống Android (Google) tự xử lý nhận diện giọng nói → trả về text. Em không cần API ngoài.

**Q: "Bảo mật API key thế nào?"**
> Em lưu trong `local.properties` (không commit Git) rồi inject vào `BuildConfig`. Tuy nhiên em thừa nhận đây vẫn là điểm yếu — ai decompile APK vẫn có thể lấy được. Để production em sẽ chuyển sang gọi OpenAI qua backend proxy của mình, client chỉ gửi message lên backend, backend mới gọi OpenAI với key giấu kín.

---

# 📌 Tóm tắt 1 dòng cho từng chủ đề

| Chủ đề | 1 câu nhớ thuộc |
|---|---|
| **Gradle build** | Sửa `local.properties` xong PHẢI Sync Gradle vì `BuildConfig` cần regenerate |
| **Firebase Security Rules** | Hiện dùng test mode, nên siết theo `request.auth.uid` + role |
| **Firestore Offline Cache** | Tự động cache, app dùng offline được mà không cần Room |
| **Auth Token Lifecycle** | idToken 1 giờ, Firebase tự refresh ngầm → user không phải re-login |
| **Address `@PropertyName`** | Tránh JavaBeans bỏ chữ "is" khi serialize boolean |
| **Notification không có FCM** | Chỉ in-app, đóng app không có push (cần FCM + Cloud Function) |
| **Chatbot — Why?** | **Context Injection** — nhồi data shop vào system prompt mỗi lần gọi |
| **Chatbot — How?** | 6 Repository → format text → OpenAI gpt-4o-mini stream → LiveData |
| **Streaming** | OpenAI trả Server-Sent Events, OkHttp readUtf8Line từng chunk |
| **Multimodal** | Resize 1024px + JPEG 80% + Base64 → nhúng vào data URI |
| **Voice** | `RecognizerIntent.ACTION_RECOGNIZE_SPEECH` — built-in Android |
