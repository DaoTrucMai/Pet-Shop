# 🔐 PETSHOP — Firebase, Phân quyền, Lưu trữ, Realtime, Hash & Bảo mật

> Tài liệu này là **phần thứ 3** trong series tài liệu Petshop. Đọc song song với:
> - `PETSHOP_EXPLAINED.md` — Tổng quan + 5 chủ đề cơ bản
> - `PETSHOP_CHATBOT_AND_DEEP_DIVE.md` — Chatbot AI + mở rộng Phần B
> - **`PETSHOP_FIREBASE_SECURITY.md`** — File này (Firebase + bảo mật chi tiết)
>
> **Mọi đoạn code trong tài liệu này đều có chú thích file path để bạn dễ tra cứu.**

---

## 📖 Mục lục

1. Firebase tổng quan trong project
2. 🔐 Phân quyền (Authorization) — Cách app phân biệt CUSTOMER vs ADMIN
3. 💾 Lưu trữ (Storage) — Firestore vs Firebase Storage vs SharedPreferences
4. ⚡ Realtime — Cơ chế hoạt động + so sánh với polling
5. # Hash & Mã hóa trong project (rất hay bị hỏi)
6. 🛡 Bảo mật toàn diện — 8 lớp phòng thủ + 5 lỗ hổng hiện tại
7. 🎯 Bộ câu hỏi giáo viên mở rộng + câu trả lời mẫu (30+ câu)

---

# 1. 🔥 Firebase tổng quan trong project

## 1.1 Project ID & cấu hình thực tế

Mở file `app/google-services.json` (file cấp bởi Firebase Console khi tạo project):

```json
// File: app/google-services.json
{
  "project_info": {
    "project_number": "15454009990",
    "project_id": "petshop-95c67",
    "storage_bucket": "petshop-95c67.firebasestorage.app"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "1:15454009990:android:194a2af6499e3fb440af07",
        "android_client_info": {
          "package_name": "com.example.petshop"
        }
      },
      "oauth_client": [
        {
          "client_id": "15454009990-1gfs6rhg6l9l0ua8qqcv1tbtlnsv7p2i.apps.googleusercontent.com",
          "client_type": 1,
          "android_info": {
            "package_name": "com.example.petshop",
            "certificate_hash": "baafd000f7a71be7e27592c67ab8c16943ed9b59"
          }
        }
      ],
      "api_key": [{"current_key": "AIzaSyBHIltk618FfBmY1-tC1mUUmlT85UqR_VM"}]
    }
  ]
}
```

**Giải thích từng trường (giáo viên có thể hỏi):**

| Trường | Ý nghĩa |
|---|---|
| `project_id: "petshop-95c67"` | ID duy nhất của Firebase project trên Google Cloud |
| `project_number` | Số dự án nội bộ (ít dùng) |
| `storage_bucket` | URL của Firebase Storage (lưu ảnh, video) |
| `package_name: "com.example.petshop"` | Phải khớp với `applicationId` trong `build.gradle.kts` |
| `certificate_hash: "baafd0...."` | **SHA-1 fingerprint** của keystore — dùng để Firebase verify app thật, chống giả mạo |
| `client_type: 1` | Android client (cho debug/release) |
| `client_type: 3` | Web client — dùng cho Google Sign-In (`requestIdToken`) |
| `api_key` | Khóa API gọi Firebase REST (KHÔNG nhạy cảm — bảo mật nằm ở Security Rules) |

> ⚠️ **Lưu ý quan trọng:** API key `AIzaSyBHIltk618...` **được phép public**. Khác với OPENAI_API_KEY, Firebase API key chỉ dùng để định danh project. Bảo mật thật sự nằm ở **Security Rules** + **certificate hash**. Đây là điểm giáo viên giỏi hay hỏi để check em hiểu.

## 1.2 3 dịch vụ Firebase đang dùng

```
┌────────────────────────────────────────────────────────┐
│              FIREBASE PROJECT (petshop-95c67)          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 1. Firebase Authentication                       │  │
│  │    - Email/Password                              │  │
│  │    - Google Sign-In                              │  │
│  │    - Cấp UID + idToken                           │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 2. Cloud Firestore (NoSQL Database)              │  │
│  │    - users, pets, foods, orders, carts...        │  │
│  │    - Realtime sync                               │  │
│  │    - Offline cache                               │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 3. Cloud Storage                                 │  │
│  │    - avatars/{uid}.jpg (avatar người dùng)       │  │
│  │    - chats/chat_{timestamp}.jpg (ảnh chat AI)    │  │
│  │    - pet_media/, food_media/                     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Khai báo dependency** trong `app/build.gradle.kts`:
```kotlin
// File: app/build.gradle.kts
implementation(platform(libs.firebase.bom))   // BOM quản lý version
implementation(libs.firebase.auth)            // Authentication
implementation(libs.firebase.firestore)       // NoSQL Database
implementation(libs.firebase.storage)         // File Storage
```

---

# 2. 🔐 PHÂN QUYỀN (Authorization)

## 2.1 Khái niệm cơ bản: Authentication vs Authorization

Sinh viên hay nhầm 2 khái niệm này:

| | Authentication | Authorization |
|---|---|---|
| Dịch | Xác **thực** | Phân **quyền** |
| Câu hỏi trả lời | "Bạn là AI?" | "Bạn có quyền gì?" |
| Firebase service | Firebase Auth | Security Rules + Role |
| Trong project | Login email/Google | Field `role` = ADMIN/CUSTOMER |

→ Authentication chỉ trả lời "user là ai", còn user đó có quyền **làm gì** là phân quyền (Authorization).

## 2.2 Phân quyền trong project có 2 lớp

```
        USER → app
          │
          ▼
┌──────────────────────────────────┐
│ LỚP 1: Phân quyền ở CLIENT       │
│   - SessionManager.isAdmin()     │
│   - Quyết định màn nào hiện      │
│   - DỄ BỊ BYPASS                 │
└─────────────┬────────────────────┘
              │ Khi user gọi Firestore
              ▼
┌──────────────────────────────────┐
│ LỚP 2: Phân quyền ở SERVER       │
│   - Firestore Security Rules     │
│   - Check request.auth.uid       │
│   - Check role trong document    │
│   - KHÔNG BỊ BYPASS              │
└──────────────────────────────────┘
```

## 2.3 Lớp 1: Phân quyền ở Client

### A) Gán role lúc đăng ký

User mới đăng ký luôn là `CUSTOMER`:

```java
// File: app/src/main/java/com/example/petshop/utils/FirebaseHelper.java
public static void registerWithEmail(String email, String password, String fullName,
                                      OnAuthCallback callback) {
    auth.createUserWithEmailAndPassword(email, password)
            .addOnSuccessListener(result -> {
                FirebaseUser user = result.getUser();
                ...
                saveUserToFirestore(user.getUid(), fullName, email,
                        User.ROLE_CUSTOMER,   // ★ Role mặc định = CUSTOMER
                        User.LOGIN_EMAIL, null,
                        () -> callback.onSuccess(user.getUid(), User.ROLE_CUSTOMER));
            })
            .addOnFailureListener(e -> callback.onFailure(parseAuthError(e.getMessage())));
}
```

### B) Tạo ADMIN bằng tay (Admin Setup Helper)

Project có 1 file đặc biệt để tạo ADMIN account lần đầu:

```java
// File: app/src/main/java/com/example/petshop/utils/AdminSetupHelper.java
public static void createAdminAccount(String email, String password,
                                       String fullName, SetupCallback cb) {
    FirebaseAuth auth = FirebaseAuth.getInstance();
    FirebaseFirestore db = FirebaseFirestore.getInstance();

    auth.createUserWithEmailAndPassword(email, password)
            .addOnSuccessListener(result -> {
                String uid = result.getUser().getUid();
                ...
                // ★ Khác với registerWithEmail: gán role = ADMIN
                Map<String, Object> data = new HashMap<>();
                data.put("id",        uid);
                data.put("role",      User.ROLE_ADMIN);   // ★★★
                data.put("loginType", User.LOGIN_EMAIL);
                ...
                db.collection("users").document(uid).set(data)
                        .addOnSuccessListener(v -> cb.onSuccess(...))
```

> Comment trong file ghi: *"Chạy 1 lần để tạo tài khoản admin... SAU KHI TẠO XONG NÊN XOÁ FILE NÀY để bảo mật."*
>
> Đây là pattern **bootstrapping** — chạy 1 lần rồi xóa.

### C) Đọc role khi login + lưu vào SessionManager

```java
// File: app/src/main/java/com/example/petshop/utils/FirebaseHelper.java
public static void getUserRole(String uid, OnRoleCallback callback) {
    db.collection(COLLECTION_USERS).document(uid).get()
            .addOnSuccessListener(doc -> {
                String role = doc.getString("role");
                callback.onResult(role != null ? role : User.ROLE_CUSTOMER);
            })
            .addOnFailureListener(e -> callback.onResult(User.ROLE_CUSTOMER));
}
```

→ Sau khi login thành công, app đọc field `role` từ Firestore. Nếu thiếu → fallback `CUSTOMER`.

### D) Cache role local qua SessionManager

```java
// File: app/src/main/java/com/example/petshop/utils/SessionManager.java
public static final String ROLE_ADMIN    = "ADMIN";
public static final String ROLE_CUSTOMER = "CUSTOMER";

public String getRole() { return prefs.getString(KEY_ROLE, ROLE_CUSTOMER); }
public boolean isAdmin() { return ROLE_ADMIN.equals(getRole()); }
public boolean isLoggedIn() { return getUserId() != null; }
```

→ Lưu role vào SharedPreferences để khỏi đọc Firestore mỗi lần. Khi user logout → `clearSession()` xóa hết.

### E) Routing dựa trên role

```java
// File: app/src/main/java/com/example/petshop/view/activity/SplashActivity.java
FirebaseUser currentUser = FirebaseHelper.getCurrentUser();
if (currentUser != null) {
    FirebaseHelper.getUserRole(currentUser.getUid(), role -> {
        Runnable action = SessionManager.ROLE_ADMIN.equals(role)
                ? this::goToAdmin : this::goToPetShop;   // ★ Phân nhánh
        navigateAfterMinDelay(action);
    });
}
```

```java
// File: app/src/main/java/com/example/petshop/view/activity/LoginActivity.java
private void navigateByRole(String role) {
    Intent intent;
    if (SessionManager.ROLE_ADMIN.equals(role)) {
        intent = new Intent(this, AdminActivity.class);   // ★ ADMIN
    } else {
        intent = new Intent(this, PetShopActivity.class); // ★ CUSTOMER
    }
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
    startActivity(intent);
    finish();
}
```

### F) Kiểm tra trước khi vào màn nhạy cảm

```java
// File: app/src/main/java/com/example/petshop/view/activity/AdminActivity.java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_admin);

    // ★ Kiểm tra: chưa login → đẩy về Login
    FirebaseUser user = FirebaseHelper.getCurrentUser();
    if (user == null) {
        startActivity(new Intent(this, LoginActivity.class));
        finish();
        return;
    }
    ...
}
```

> ⚠️ **Điểm yếu của lớp 1:** AdminActivity chỉ check **đã login chưa**, KHÔNG check role. Nếu user copy được link mở AdminActivity (vd qua deeplink), họ vào màn này được. Phân quyền thật sự nằm ở Lớp 2 (Security Rules).

## 2.4 Lớp 2: Phân quyền ở Server (Firestore Security Rules)

**Hiện project KHÔNG kèm file `firestore.rules`** trong source code (rules nằm ở Firebase Console). Đây là mẫu rules **bạn NÊN có**:

```js
// File: firestore.rules (NÊN tạo trong Firebase Console)
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Helper function check role
    function isAdmin() {
      return request.auth != null
        && get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == "ADMIN";
    }

    function isOwner(userId) {
      return request.auth != null && request.auth.uid == userId;
    }

    // Users: chính chủ đọc/ghi, admin đọc all
    match /users/{uid} {
      allow read: if isOwner(uid) || isAdmin();
      allow write: if isOwner(uid);  // user tự sửa profile

      match /addresses/{addrId} {
        allow read, write: if isOwner(uid);
      }

      match /sessions/{sessionId} {
        allow read, write: if isOwner(uid);
      }

      match /chats/{chatId} {
        allow read, write: if isOwner(uid);
      }
    }

    // Pets, Foods, Categories: ai cũng đọc, chỉ ADMIN ghi
    match /pets/{petId} {
      allow read: if true;
      allow write: if isAdmin();
    }
    match /foods/{foodId} {
      allow read: if true;
      allow write: if isAdmin();
    }
    match /categories/{catId} {
      allow read: if true;
      allow write: if isAdmin();
    }

    // Promotions, Vouchers: ai cũng đọc, chỉ ADMIN ghi
    match /promotions/{promoId} {
      allow read: if true;
      allow write: if isAdmin();
    }
    match /vouchers/{voucherId} {
      allow read: if true;
      allow write: if isAdmin();
    }

    // Carts: chỉ chính chủ
    match /carts/{uid} {
      allow read, write: if isOwner(uid);
    }

    // Orders: chính chủ đọc, admin đọc all + update status
    match /orders/{orderId} {
      allow read: if request.auth != null
                  && (resource.data.userId == request.auth.uid || isAdmin());
      allow create: if request.auth != null
                    && request.resource.data.userId == request.auth.uid;
      allow update: if isAdmin()  // admin sửa status
                    || (isOwner(resource.data.userId)
                        && request.resource.data.status == "CANCELLED");  // user chỉ huỷ
      allow delete: if false;  // không ai được xoá
    }

    // Notifications: chỉ chính chủ đọc, admin tạo
    match /notifications/{notifId} {
      allow read: if request.auth != null
                  && resource.data.userId == request.auth.uid;
      allow create: if request.auth != null;  // app tự tạo cho user
      allow update: if isOwner(resource.data.userId);  // user mark read
    }
  }
}
```

**Quan trọng:**
- `request.auth.uid` — Firebase tự inject UID của user đang đăng nhập (KHÔNG thể giả mạo).
- `get(/.../users/$(uid)).data.role` — đọc role từ document để check ADMIN.
- Rules chạy **ở server** → user dù có sửa app cũng không bypass được.

> **Trả lời mẫu khi giáo viên hỏi "Phân quyền bằng cách nào?":**
> "Em phân quyền 2 lớp. Lớp 1 ở client: app đọc field `role` từ Firestore, lưu vào SessionManager, và route Activity tương ứng. Lớp 2 ở server bằng Firestore Security Rules — kiểm tra `request.auth.uid` và đọc role trong document `users/{uid}` để cho phép hay từ chối thao tác. Lớp 1 phục vụ UX (ẩn/hiện menu), lớp 2 mới là phân quyền thật vì không thể bypass."

---

# 3. 💾 LƯU TRỮ (Storage) — 3 nơi khác nhau

Project lưu data ở **3 nơi**, mỗi nơi dùng cho mục đích khác nhau:

```
┌──────────────┬──────────────────────┬─────────────────────┐
│ NƠI LƯU      │ DÙNG CHO             │ ĐẶC ĐIỂM            │
├──────────────┼──────────────────────┼─────────────────────┤
│ Firestore    │ Data cấu trúc        │ JSON-like, sort/    │
│              │ (user, pet, food,    │ query, realtime,    │
│              │  order, cart,        │ free tier 50K       │
│              │  notification...)    │ reads/day           │
├──────────────┼──────────────────────┼─────────────────────┤
│ Firebase     │ File nhị phân        │ URL public, hoặc    │
│ Storage      │ (ảnh, video)         │ download cần auth   │
│              │                      │ (theo Storage rules)│
├──────────────┼──────────────────────┼─────────────────────┤
│ SharedPrefs  │ Cache local nhanh    │ Lưu trên thiết bị,  │
│ (Android)    │ (session, guest chat)│ mất khi xoá app     │
└──────────────┴──────────────────────┴─────────────────────┘
```

## 3.1 Firestore — Lưu data cấu trúc

Đã giải thích chi tiết ở `PETSHOP_CHATBOT_AND_DEEP_DIVE.md`. Tóm tắt nhanh:

```
firestore-root/
├── users/{uid}             ← document
│   ├── (fields: fullName, email, role...)
│   ├── addresses/{id}      ← subcollection
│   ├── sessions/{id}       ← subcollection (chat sessions)
│   └── chats/{id}          ← subcollection (chat messages)
│
├── pets/{petId}
│   └── pet_media/{id}
├── foods/{foodId}
├── categories/{id}
├── carts/{uid}              ← 1 cart per user
├── orders/{orderId}
├── notifications/{id}
├── promotions/{id}
├── vouchers/{id}
├── reviews/{id}
└── return_requests/{id}
```

## 3.2 Firebase Storage — Lưu file

Storage có cấu trúc giống **thư mục file system**:

```
firebase-storage/  (bucket: petshop-95c67.firebasestorage.app)
├── avatars/                     ← Ảnh đại diện
│   └── {uid}.jpg               (tên = UID user → tự ghi đè khi đổi avatar)
│
├── chats/                       ← Ảnh user gửi trong chat
│   └── chat_{timestamp}.jpg
│
├── pet_media/                   ← Ảnh thú cưng (ngầm — qua StorageHelper)
│   └── {uuid}.jpg
│
└── food_media/
    └── {uuid}.jpg
```

### Code upload avatar

```java
// File: app/src/main/java/com/example/petshop/view/activity/ProfileActivity.java
private void uploadAvatar(Uri uri) {
    FirebaseUser user = FirebaseHelper.getCurrentUser();
    if (user == null) return;

    Toast.makeText(this, "Đang tải ảnh lên...", Toast.LENGTH_SHORT).show();

    String uid = user.getUid();
    // ★ Tên file = uid → tự ghi đè ảnh cũ khi đổi avatar
    StorageReference ref = FirebaseStorage.getInstance().getReference("avatars/" + uid + ".jpg");

    try {
        Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), uri);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 80, baos);  // compress 80%
        byte[] data = baos.toByteArray();

        ref.putBytes(data)
                .addOnSuccessListener(task -> ref.getDownloadUrl().addOnSuccessListener(downloadUri -> {
                    String avatarUrl = downloadUri.toString();

                    // 1. Cập nhật Firebase Auth profile (photoUri)
                    user.updateProfile(new UserProfileChangeRequest.Builder()
                            .setPhotoUri(downloadUri).build())
                        .addOnSuccessListener(aVoid -> {
                            // 2. Cập nhật Firestore - QUAN TRỌNG để đồng bộ across devices
                            FirebaseFirestore.getInstance().collection("users")
                                    .document(uid)
                                    .update("avatarUrl", avatarUrl,
                                            "updatedAt", Timestamp.now().toString());

                            // 3. Cập nhật SessionManager (cache local)
                            SessionManager.getInstance(this).updateUserAvatar(avatarUrl);
                            ...
                        });
                }))
                .addOnFailureListener(e -> ...);
    ...
}
```

→ **Pattern "3 nơi sync"** rất quan trọng phải hiểu:

```
   Upload avatar
       │
       ├──► 1. Firebase Storage     (file ảnh)
       │       avatars/{uid}.jpg
       │
       ├──► 2. Firebase Auth profile (URL ảnh)
       │       user.photoUri
       │
       ├──► 3. Firestore document   (URL ảnh)
       │       users/{uid}.avatarUrl
       │
       └──► 4. SessionManager       (URL ảnh - cache local)
              prefs.user_avatar
```

**Vì sao phải sync 3 nơi?**
1. **Storage** giữ file thật.
2. **Auth profile** dùng để Firebase Auth tự đồng bộ giữa các thiết bị.
3. **Firestore document** để khi user khác xem profile (vd review), đọc được URL.
4. **SessionManager** để hiện ngay khi mở app, không cần đợi Firestore.

### Code helper upload chung

```java
// File: app/src/main/java/com/example/petshop/utils/StorageHelper.java
private static final FirebaseStorage storage = FirebaseStorage.getInstance();

public static void uploadImage(Uri fileUri, String folder, OnUploadCallback callback) {
    String fileName  = folder + "/" + UUID.randomUUID().toString() + ".jpg";
    StorageReference ref = storage.getReference().child(fileName);
    ref.putFile(fileUri)
            .continueWithTask(task -> {
                if (!task.isSuccessful()) throw task.getException();
                return ref.getDownloadUrl();
            })
            .addOnSuccessListener(uri -> callback.onSuccess(uri.toString()))
            .addOnFailureListener(e -> callback.onFailure(e.getMessage()));
}

public static void deleteFile(String downloadUrl, OnDeleteCallback callback) {
    if (downloadUrl == null || downloadUrl.isEmpty()) { callback.onComplete(); return; }
    try {
        storage.getReferenceFromUrl(downloadUrl).delete()
                .addOnCompleteListener(t -> callback.onComplete());
    } catch (Exception e) {
        callback.onComplete();
    }
}
```

→ `UUID.randomUUID()` đảm bảo tên file unique, không bị trùng giữa các user.

### Storage Security Rules (NÊN có)

```js
// File: storage.rules (Firebase Console)
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // Avatars: chỉ chính chủ ghi, ai cũng đọc
    match /avatars/{uid}.jpg {
      allow read: if true;
      allow write: if request.auth != null
                   && request.auth.uid == uid
                   && request.resource.size < 5 * 1024 * 1024  // max 5MB
                   && request.resource.contentType.matches('image/.*');
    }

    // Pet/Food media: ai cũng đọc, chỉ ADMIN ghi
    match /pet_media/{file} {
      allow read: if true;
      allow write: if firestore.get(/databases/(default)/documents/users/$(request.auth.uid)).data.role == "ADMIN";
    }

    // Chat images: chỉ chính chủ
    match /chats/{file} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 3.3 SharedPreferences — Cache local

Dùng cho 2 mục đích:

**A) Lưu session sau khi login** (`SessionManager`):

```java
// File: app/src/main/java/com/example/petshop/utils/SessionManager.java
public void saveSession(String userId, String name, String email, String role, String avatarUrl) {
    prefs.edit()
            .putString(KEY_USER_ID, userId)
            .putString(KEY_NAME, name)
            .putString(KEY_EMAIL, email)
            .putString(KEY_ROLE, role)
            .putString(KEY_AVATAR, avatarUrl)
            .apply();
}
```

→ Lưu vào file XML cục bộ: `/data/data/com.example.petshop/shared_prefs/petshop_prefs.xml`

**B) Lưu chat của khách (chưa đăng nhập)** (`ChatViewModel`):

```java
// File: app/src/main/java/com/example/petshop/viewmodel/ChatViewModel.java
private static final String PREFS_NAME = "petshop_prefs";
private static final String KEY_GUEST_MSGS = "guest_chat_messages";
private static final int GUEST_MSG_LIMIT = 50;

private void saveGuestMessages() {
    ...
    List<ChatMessage> toSave = current.size() > GUEST_MSG_LIMIT
            ? current.subList(current.size() - GUEST_MSG_LIMIT, current.size())
            : current;

    getApplication()
            .getSharedPreferences(PREFS_NAME, android.content.Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_GUEST_MSGS + "_" + sid, gson.toJson(toSave))  // ★ JSON serialize
            .apply();
    ...
}
```

> ⚠️ **Cảnh báo:** SharedPreferences **KHÔNG mã hóa**. Ai có root device sẽ đọc được file. Nếu cần lưu thông tin nhạy cảm, dùng `EncryptedSharedPreferences` (Jetpack Security library).

---

# 4. ⚡ REALTIME — Cơ chế hoạt động

## 4.1 Realtime nghĩa là gì?

Bình thường (HTTP polling): muốn biết có data mới → app phải **hỏi server** mỗi 5 giây. Tốn pin, tốn 4G.

Realtime: server **chủ động bắn data** xuống app **NGAY** khi có thay đổi. App không phải hỏi.

## 4.2 Cách Firestore làm realtime — Cơ chế bên dưới

```
APP (Android)                        FIRESTORE (Server)
   │                                       │
   │  1. Mở WebSocket connection           │
   ├──────────────────────────────────────►│
   │                                       │
   │  2. Subscribe (đăng ký) query:        │
   │     "Listen notifications              │
   │      WHERE userId = abc123"           │
   ├──────────────────────────────────────►│
   │                                       │
   │  3. Server trả về snapshot ban đầu    │
   │◄──────────────────────────────────────┤
   │                                       │
   │  4. App callback onEvent(snapshot)    │
   │                                       │
   │                                       │
   │            ... user vẫn dùng app ...  │
   │                                       │
   │                                       │
   │   [Admin tạo notification mới]        │
   │                                       │
   │  5. Server PUSH delta xuống:          │
   │     "+1 doc mới, +1 doc sửa"          │
   │◄──────────────────────────────────────┤
   │                                       │
   │  6. App callback onEvent(snapshot)    │
   │     UI tự cập nhật                    │
   │                                       │
   │  7. App gọi reg.remove()              │
   ├──────────────────────────────────────►│
   │                                       │
   │  8. Server đóng subscription          │
   │◄──────────────────────────────────────┤
```

Firebase SDK ngầm dùng **WebSocket** (giao thức 2 chiều). Sinh viên không cần code WebSocket, chỉ gọi `addSnapshotListener` là xong.

## 4.3 Code thực tế: 3 nơi dùng realtime trong project

### A) Badge thông báo chưa đọc (HomeFragment)

```java
// File: app/src/main/java/com/example/petshop/repository/NotificationRepository.java
public ListenerRegistration listenUnreadCount(String userId, Callback<Long> cb) {
    return db.collection(COL)
            .whereEqualTo("userId", userId)
            .addSnapshotListener((snap, e) -> {       // ★ Callback gọi mỗi khi data đổi
                if (e != null) {
                    cb.onSuccess(0L);
                    return;
                }
                cb.onSuccess(snap != null ? countUnread(snap.getDocuments()) : 0L);
            });
}
```

Đăng ký + gỡ:
```java
// File: app/src/main/java/com/example/petshop/view/fragment/HomeFragment.java
private void startUnreadNotificationListener() {
    ...
    unreadNotifListener = new NotificationRepository().listenUnreadCount(uid, new NotificationRepository.Callback<Long>() {
        @Override
        public void onSuccess(Long data) {
            long count = data != null ? data : 0L;
            ...
            getActivity().runOnUiThread(() -> renderUnreadBadge(count));
        }
        ...
    });
}

@Override public void onStop() {
    super.onStop();
    if (unreadNotifListener != null) {
        unreadNotifListener.remove();    // ★ GỠ khi Fragment dừng
        unreadNotifListener = null;
    }
}
```

### B) Cart realtime (CartViewModel)

```java
// File: app/src/main/java/com/example/petshop/viewmodel/CartViewModel.java
public void loadCart() {
    String uid = uid();
    if (uid == null) { cart.postValue(new Cart()); return; }

    if (cartListener != null) cartListener.remove();    // ★ Tránh duplicate listener

    isLoading.postValue(true);
    cartListener = FirebaseFirestore.getInstance()
            .collection("carts").document(uid)
            .addSnapshotListener((doc, e) -> {           // ★ Listen 1 document
                isLoading.postValue(false);
                if (e != null) {
                    error.postValue(e.getMessage());
                    return;
                }
                if (doc != null && doc.exists()) {
                    Cart c = doc.toObject(Cart.class);
                    if (c != null) cart.postValue(c);
                    else cart.postValue(new Cart(uid));
                } else {
                    cart.postValue(new Cart(uid));
                }
            });
}

@Override
protected void onCleared() {
    super.onCleared();
    if (cartListener != null) cartListener.remove();   // ★ Gỡ khi ViewModel destroy
}
```

→ **Use case thực tế:** User mở Cart trên điện thoại A. Trên điện thoại B (cùng tài khoản) thêm 1 sản phẩm → điện thoại A **tự cập nhật** giỏ hàng, không cần refresh.

### C) Admin Dashboard realtime (AdminViewModel)

```java
// File: app/src/main/java/com/example/petshop/viewmodel/AdminViewModel.java
private void startOrdersListener() {
    ordersListener = db.collection(COL_ORDERS)
            .addSnapshotListener(new EventListener<QuerySnapshot>() {
                @Override
                public void onEvent(QuerySnapshot snapshots, FirebaseFirestoreException e) {
                    if (e != null) {
                        Log.e(TAG, "Orders listener error: " + e.getMessage());
                        error.postValue("Lỗi tải đơn hàng: " + e.getMessage());
                        return;
                    }
                    // ★ Tính lại stats mỗi khi có đơn mới hoặc đổi trạng thái
                    ...
                }
            });
}

public void stopListening() {
    if (ordersListener != null) {
        ordersListener.remove();
        ordersListener = null;
    }
    ...
}
```

→ Admin mở dashboard → mỗi khi customer đặt đơn mới, số "Đơn chờ xác nhận" tăng **tức thì** trên màn admin.

## 4.4 Polling vs Realtime — So sánh

| Tiêu chí | Polling (hỏi định kỳ) | Snapshot Listener (realtime) |
|---|---|---|
| Cách hoạt động | App hỏi server mỗi N giây | Server push khi có data mới |
| Độ trễ | 5-30 giây | < 1 giây |
| Pin/Data | Tốn (gọi liên tục) | Tiết kiệm (chỉ gọi khi cần) |
| Code phức tạp | Cần `Handler.postDelayed` | 1 dòng `addSnapshotListener` |
| Backend cần làm gì | Trả toàn bộ data mỗi lần | Server tự diff + push delta |

## 4.5 Cẩn thận với realtime — 3 quy tắc vàng

1. **PHẢI gỡ listener khi không cần** → tránh leak + tốn quota.
2. **PHẢI kiểm tra null** trong snapshot callback → đôi khi `snap` rỗng.
3. **KHÔNG nên** listen 1 collection lớn (1000+ doc) toàn bộ → tốn bandwidth. Dùng `where` + `limit`.

---

# 5. 🔒 HASH & MÃ HÓA trong project (giáo viên RẤT hay hỏi)

> **Câu trả lời ngắn:** Project KHÔNG tự hash password (Firebase tự lo). Project chỉ dùng hash cho:
> 1. **HMAC-SHA512** trong VNPay (ký giao dịch thanh toán).
> 2. **SHA-1** trong certificate hash của keystore (xác thực app).
> 3. Một số nơi dùng **Base64** (không phải hash, chỉ là encoding).

## 5.1 Hash là gì? Khác Encoding/Encryption ở chỗ nào?

Đây là kiến thức cơ bản nhưng sinh viên hay nhầm:

| | Encoding | Encryption | Hashing |
|---|---|---|---|
| Mục đích | Đổi format | Giấu data | "Vân tay" dữ liệu |
| Khôi phục được? | Có | Có (cần key) | **KHÔNG** (1 chiều) |
| Ví dụ | Base64, URLEncoder | AES, RSA | MD5, SHA-256, HMAC |
| Trong project | Chat ảnh base64 | (không dùng) | VNPay HMAC-SHA512, password Firebase |

**Hash đặc trưng:**
- **Một chiều:** từ "abc" ra hash "ba7816...", không thể ngược lại từ hash về "abc".
- **Deterministic:** "abc" lúc nào hash ra cũng giống nhau.
- **Avalanche:** đổi 1 ký tự → hash hoàn toàn khác.
- **Cùng kích thước:** input bao nhiêu cũng ra hash kích thước cố định.

## 5.2 HMAC-SHA512 — Dùng trong VNPay (PHẢI HIỂU)

### HMAC là gì?

HMAC = **Hash-based Message Authentication Code** — kết hợp giữa hash function (SHA-512) và **secret key**. Dùng để:
1. **Verify integrity** — dữ liệu không bị sửa giữa đường.
2. **Verify authenticity** — chỉ bên có secret key mới tạo được hash đúng.

```
HMAC-SHA512(message, secretKey) → chuỗi 128 ký tự hex
```

### Code VNPay tạo hash

```java
// File: app/src/main/java/com/example/petshop/utils/VNPayHelper.java
public static String buildPaymentUrl(String orderCode, long amount, String orderInfo) {
    Map<String, String> vnp_Params = new TreeMap<>();   // ★ TreeMap = tự sort theo alphabet
    vnp_Params.put("vnp_Version",   "2.1.0");
    vnp_Params.put("vnp_Command",   "pay");
    vnp_Params.put("vnp_TmnCode",   Constants.VNPAY_TMN_CODE.trim());
    vnp_Params.put("vnp_Amount",    String.valueOf(amount * 100));  // ★ VNPay yêu cầu × 100
    vnp_Params.put("vnp_CurrCode",  "VND");
    vnp_Params.put("vnp_TxnRef",    orderCode);
    vnp_Params.put("vnp_OrderInfo", orderInfo);
    ...

    // Bước 1: Sort theo alphabet (TreeMap đã làm)
    List<String> fieldNames = new ArrayList<>(vnp_Params.keySet());
    Collections.sort(fieldNames);

    // Bước 2: URL-encode + ghép thành chuỗi a=b&c=d
    StringBuilder hashData = new StringBuilder();
    StringBuilder query = new StringBuilder();
    for (String fieldName : fieldNames) {
        String fieldValue = vnp_Params.get(fieldName);
        if (fieldValue == null || fieldValue.isEmpty()) continue;

        String encodedName = URLEncoder.encode(fieldName, StandardCharsets.UTF_8.toString());
        String encodedValue = URLEncoder.encode(fieldValue, StandardCharsets.UTF_8.toString());

        if (hashData.length() > 0) {
            hashData.append('&');
            query.append('&');
        }
        hashData.append(encodedName).append('=').append(encodedValue);
        query.append(encodedName).append('=').append(encodedValue);
    }

    // ★★★ Bước 3: HMAC-SHA512 với secret key
    String secureHash = hmacSHA512(Constants.VNPAY_HASH_SECRET.trim(), hashData.toString());
    query.append("&vnp_SecureHash=").append(secureHash);

    return Constants.VNPAY_URL + "?" + query;
}

public static String hmacSHA512(String key, String data) {
    try {
        Mac mac = Mac.getInstance("HmacSHA512");
        mac.init(new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "HmacSHA512"));
        byte[] result = mac.doFinal(data.getBytes(StandardCharsets.UTF_8));

        // Convert byte[] → hex string lowercase
        StringBuilder sb = new StringBuilder(2 * result.length);
        for (byte b : result) sb.append(String.format("%02x", b & 0xff));
        return sb.toString();
    } catch (Exception e) {
        return "";
    }
}
```

### Vì sao phải hash thanh toán?

**Tình huống tấn công nếu KHÔNG hash:**
```
1. App tạo URL: https://vnpay.vn/pay?amount=500000&order=ORD123
2. User chặn request → đổi thành: ?amount=1&order=ORD123
3. Gửi lên VNPay → VNPay tính tiền 1đ
4. → Cửa hàng bị hack
```

**Với HMAC:**
```
1. App tạo URL: https://vnpay.vn/pay?amount=500000&order=ORD123&secureHash=ABC...
   (ABC... = HMAC-SHA512("amount=500000&order=ORD123", SECRET_KEY))
2. User đổi: ?amount=1&order=ORD123&secureHash=ABC...
3. VNPay nhận → tự tính hash lại với amount=1
   → ra DEF... (khác ABC) → REJECT
4. → An toàn
```

**Vì sao chỉ shop biết secret key?**
- `Constants.VNPAY_HASH_SECRET` lưu trong `local.properties` (không commit Git).
- Chỉ shop + VNPay biết. User không biết → không tạo được hash hợp lệ.

> ⚠️ **Điểm yếu của project:** Secret key đang nằm trong APK (qua BuildConfig). Decompile APK là lấy được. **Cách đúng** là tạo URL VNPay ở backend của mình, app chỉ nhận URL về.

## 5.3 SHA-1 Certificate Hash — Trong google-services.json

```json
// File: app/google-services.json
"android_info": {
    "package_name": "com.example.petshop",
    "certificate_hash": "baafd000f7a71be7e27592c67ab8c16943ed9b59"
}
```

Đây là **SHA-1 fingerprint** (160 bit = 40 ký tự hex) của file keystore dùng để sign APK.

**Cách lấy:**
```bash
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```

**Mục đích:** Khi user mở Google Sign-In trong app, Google kiểm tra:
1. Package name (com.example.petshop) → khớp với cấu hình.
2. SHA-1 hash của keystore đang sign APK hiện tại → khớp với certificate_hash trong Firebase.

Nếu cả 2 khớp → cho phép idToken. Nếu không → từ chối.

→ **Tại sao quan trọng?** Để chống **fake app**. Ai đó decompile APK của bạn, rebuild với keystore khác → SHA-1 khác → Google không cho đăng nhập.

## 5.4 Password Hashing — Firebase TỰ LÀM

Firebase Auth dùng **scrypt** (1 thuật toán hash mạnh cho password). Quy trình:

```
User nhập password "abc123"
        │
        ▼ HTTPS encrypt
Gửi lên Firebase Server
        │
        ▼
Firebase: hash = scrypt("abc123", salt, work_factor)
        │
        ▼
Lưu vào internal DB: { uid: "...", passwordHash: "...", salt: "..." }
```

**Lúc login:**
```
User nhập "abc123"
        │ HTTPS
        ▼
Firebase: testHash = scrypt("abc123", stored_salt, work_factor)
        │
        ▼
testHash == passwordHash? → cấp idToken
```

**Đặc điểm:**
- **Code app KHÔNG hash gì cả** — chỉ gọi `signInWithEmailAndPassword(email, password)`. Firebase tự lo.
- Password đi qua **HTTPS** (TLS) nên giữa đường không ai đọc được.
- Firebase không lưu password gốc — kể cả admin Firebase Console cũng không xem được.

**Trả lời khi giáo viên hỏi "Em hash password thế nào?":**

> "Em KHÔNG tự hash password. Em dùng Firebase Authentication, Firebase tự hash bằng **scrypt** ở server side. Khi user đăng ký, em chỉ gọi `auth.createUserWithEmailAndPassword(email, password)` — password đi qua HTTPS đến Firebase, Firebase hash rồi lưu. Khi login, Firebase tự verify. Em không bao giờ thấy hash đó, kể cả admin Firebase Console cũng không xem được. Đây là pattern an toàn hơn tự build vì Firebase đã có chuyên gia bảo mật."

## 5.5 Base64 — Không phải hash, là ENCODING

Project dùng Base64 ở 2 chỗ:

```java
// File: app/src/main/java/com/example/petshop/viewmodel/ChatViewModel.java
byte[] bytes = outputStream.toByteArray();
return Base64.encodeToString(bytes, Base64.NO_WRAP);  // ★ Encode ảnh sang text
```

**Base64 KHÔNG bảo mật**. Nó chỉ là cách biểu diễn dữ liệu nhị phân (byte) bằng ký tự text (A-Z, a-z, 0-9, +, /). Mục đích:
- Nhúng ảnh vào JSON (vốn là text format).
- Truyền data qua URL.
- Lưu file vào field text.

→ Ai cũng decode được. Không có bảo mật.

## 5.6 Tóm tắt mọi cơ chế hash/mã hóa trong project

| Cơ chế | Dùng ở đâu | File code |
|---|---|---|
| **HMAC-SHA512** | Ký giao dịch VNPay | `VNPayHelper.java` |
| **SHA-1 fingerprint** | Verify app cho Google Sign-In | `google-services.json` |
| **scrypt** (Firebase tự dùng) | Hash password user | Không có code app — Firebase server |
| **HTTPS/TLS** | Mọi request lên Firebase, OpenAI, VNPay | Tự động (URL bắt đầu `https://`) |
| **Base64** (encoding) | Nhúng ảnh chat AI, OkHttp auth header | `ChatViewModel.java` |
| **URLEncoder** (encoding) | Tham số trong URL VNPay | `VNPayHelper.java` |

---

# 6. 🛡 BẢO MẬT TOÀN DIỆN — 8 lớp phòng thủ

Khi giáo viên hỏi "Bảo mật app em thế nào?", trả lời theo **8 lớp** sau (in ra giấy A4 cầm theo):

## Lớp 1: Bảo mật API key — `local.properties`

```kotlin
// File: app/build.gradle.kts (lines 35-55)
buildConfigField("String", "GOOGLE_WEB_CLIENT_ID", "\"${localProp("GOOGLE_WEB_CLIENT_ID")}\"")
buildConfigField("String", "VNPAY_HASH_SECRET", "\"${localProp("VNPAY_HASH_SECRET")}\"")
buildConfigField("String", "OPENAI_API_KEY", "\"${localProp("OPENAI_API_KEY")}\"")
```
→ Khóa secret lưu trong `local.properties` (file này có trong `.gitignore` → KHÔNG commit Git).

## Lớp 2: HTTPS bắt buộc

Mọi URL trong project đều `https://`:
- `https://api.openai.com/v1/chat/completions` (ChatViewModel)
- `https://sandbox.vnpayment.vn/paymentv2/vpcpay.html` (VNPayHelper)
- Firebase tự dùng HTTPS

→ Không ai đọc được data giữa đường (TLS encryption).

## Lớp 3: Firebase Authentication

```java
// File: app/src/main/java/com/example/petshop/utils/FirebaseHelper.java (line 31)
public static FirebaseUser getCurrentUser() {
    return auth.getCurrentUser();  // Token tự verify, hết hạn 1h tự refresh
}
```

## Lớp 4: Role-based Access (CUSTOMER/ADMIN)

```java
// File: app/src/main/java/com/example/petshop/utils/SessionManager.java (lines 8-9)
public static final String ROLE_ADMIN    = "ADMIN";
public static final String ROLE_CUSTOMER = "CUSTOMER";
```

## Lớp 5: Firestore Security Rules (server-side)

→ Phần 2.4 đã giải thích. **CỰC KỲ QUAN TRỌNG** — đây là phòng thủ chính chống hack data.

## Lớp 6: HMAC chữ ký số (VNPay)

→ Phần 5.2. Chống user/attacker sửa số tiền.

## Lớp 7: Certificate Hash (SHA-1)

→ Phần 5.3. Chống fake app dùng key của shop.

## Lớp 8: ProGuard minify (chưa bật)

```kotlin
// File: app/build.gradle.kts (lines 58-66)
buildTypes {
    release {
        isMinifyEnabled = false   // ★ Hiện đang FALSE — nên bật cho production
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
    }
}
```

→ Khi bật, ProGuard sẽ:
- Đổi tên class/method thành `a`, `b`, `c` → khó decompile.
- Loại bỏ code không dùng → APK nhỏ hơn.

## 🚨 5 lỗ hổng hiện tại của project (giáo viên hỏi có gì yếu?)

| # | Lỗ hổng | Cách khắc phục |
|---|---|---|
| 1 | OPENAI_API_KEY trong BuildConfig → decompile lấy được | Gọi qua backend proxy giấu key |
| 2 | VNPAY_HASH_SECRET trong APK → tự tạo URL ăn cắp | Tạo URL ở backend, app chỉ nhận về |
| 3 | OTP register sinh ở client → bypass được | Sinh OTP ở Firebase Cloud Function |
| 4 | Email + password gửi mail OTP hardcode trong `EmailHelper.java` | Dùng SendGrid/Mailgun, lưu credential ở backend |
| 5 | Chưa có Firestore Security Rules (test mode) | Viết rules theo Phần 2.4 |
| 6 | Chưa bật ProGuard | Set `isMinifyEnabled = true` trong release |

**Code lỗ hổng 4** (giáo viên có thể chỉ ra):
```java
// File: app/src/main/java/com/example/petshop/utils/EmailHelper.java (line 20-21)
final String senderEmail = "nguyenductho0411@gmail.com";
final String senderPassword = "gfvl elnj hpzw lcpu";   // ★ HARDCODE = LỖI LỚN
```

> Nếu giáo viên chỉ ra: thừa nhận và đề xuất khắc phục: "Đúng ạ, đây là điểm yếu em đã thấy. Em sẽ chuyển sang dùng SendGrid API hoặc Firebase Cloud Function để gửi email, credential giấu ở backend, không nằm trong APK."

---

# 7. 🎯 BỘ CÂU HỎI GIÁO VIÊN MỞ RỘNG (30+ câu)

## 7.1 Về Firebase

**Q1: "Firebase miễn phí à?"**
> Có gói **Spark Plan** miễn phí: Firestore 50K reads/20K writes/day, Auth không giới hạn, Storage 5GB. Đủ cho project học. Khi production em sẽ nâng lên **Blaze Plan** (trả theo lượng dùng).

**Q2: "google-services.json có lộ ra bên ngoài được không?"**
> File này được **commit Git công khai** vì nó chỉ chứa project_id, API key public. Bảo mật thật nằm ở Firestore Security Rules + Certificate Hash. Nhưng `local.properties` thì KHÔNG được commit vì chứa OPENAI/VNPAY secret.

**Q3: "Firestore khác Realtime Database thế nào?"**
> Firebase có 2 database: **Realtime Database** (cũ, JSON tree) và **Firestore** (mới, document-collection). Em chọn Firestore vì: (1) query phức tạp hơn, (2) scale tốt hơn, (3) offline cache tự nhiên, (4) cấu trúc rõ ràng theo collection.

**Q4: "Sao em dùng `set()` mà không phải `add()` khi tạo pet?"**
> `set()` lưu vào ID **mình tự chỉ định** (em dùng UUID generate ở client). `add()` để Firestore tự sinh ID. Em chọn `set()` vì cần biết ID ngay để tham chiếu chéo (vd CartItem cần `productId` của pet đó). `add()` phải đợi server trả về mới biết ID.

**Q5: "Vì sao toObject(Pet.class) hoạt động?"**
> Vì Firestore SDK dùng **reflection** — đọc field name trong document JSON rồi map vào field cùng tên trong class Pet. Class phải có:
> - Constructor không tham số: `public Pet() {}`
> - Getter/setter chuẩn JavaBeans
> - Field public hoặc có setter
> Nếu tên không khớp (vd boolean `isDefault`), dùng `@PropertyName("isDefault")`.

**Q6: "Em có index nào trong Firestore không?"**
> Firestore tự tạo **single-field index**. Nếu query với 2+ field (vd `whereEqualTo("userId", x).orderBy("timestamp")`), Firestore yêu cầu **composite index**. Em có thấy trong `ChatViewModel` có fallback nếu thiếu composite index: nếu lỗi → load lại không orderBy rồi sort tay.

**Q7: "Firestore tính tiền thế nào?"**
> Theo: (1) **document reads** (mỗi lần đọc 1 doc tính 1), (2) **writes** (mỗi set/update tính 1), (3) **deletes**, (4) **storage GB**, (5) **bandwidth**. Snapshot listener tính reads theo số doc match. Em phải tối ưu để khỏi quá free tier.

## 7.2 Về Chatbot

**Q8: "Sao AI biết shop có gì? Em training à?"**
> KHÔNG. Em dùng OpenAI ChatGPT (model `gpt-4o-mini`) qua API. Mỗi lần user hỏi, em fetch toàn bộ data shop (30 pet + 30 food + categories + orders + promotions + vouchers) từ Firestore, format thành text rồi nhồi vào `system message` của prompt. AI đọc data đó để trả lời. Đây gọi là **Context Injection**, là biến thể đơn giản của **RAG (Retrieval-Augmented Generation)**.

**Q9: "Sao chữ đánh máy từ từ giống ChatGPT?"**
> Em bật `stream: true` khi gọi API. OpenAI trả response theo giao thức **Server-Sent Events (SSE)** từng chunk nhỏ. Em đọc qua OkHttp `BufferedSource.readUtf8Line()` trong vòng lặp `while`, parse JSON từng chunk lấy `delta.content`, ghép lại rồi cập nhật LiveData → UI render lại liên tục.

**Q10: "Sao em chỉ gửi 6 message history?"**
> Tiết kiệm token (OpenAI tính tiền theo token). 6 message = ~3 lượt qua lại đủ giữ ngữ cảnh ngắn. Nếu gửi 100 message: (1) tốn $$$, (2) AI dễ "quên" system message quan trọng vì context window có hạn.

**Q11: "Nếu user hỏi sản phẩm không có trong 30 pet em fetch thì sao?"**
> AI sẽ trả lời "shop chưa có sản phẩm này nhưng sẽ cập nhật sau" — đây là quy tắc số 2 trong system message. Cải tiến: dùng **vector embedding search** để chỉ fetch pet liên quan câu hỏi, support shop lớn.

**Q12: "OPENAI_API_KEY lộ ra bị gì?"**
> Ai có key → gọi API của em → em bị charge tiền. OpenAI có limit chống abuse nhưng vẫn rủi ro. Em đang lưu trong BuildConfig nên ai decompile APK lấy được. **Cách đúng**: gọi qua backend của mình, app gửi message lên backend, backend mới forward sang OpenAI với key giấu kín.

**Q13: "Em làm sao gửi ảnh cho AI?"**
> 3 bước: (1) đọc ảnh từ URI → Bitmap, (2) resize về tối đa 1024px + compress JPEG 80% (giảm size, tiết kiệm token), (3) **Base64** encode → nhúng vào prompt theo định dạng **data URI** (`data:image/jpeg;base64,...`). Model `gpt-4o-mini` có vision capability nên đọc được ảnh. Ngoài ra ảnh còn được upload lên Firebase Storage để lưu lịch sử.

**Q14: "Voice nhận giọng thế nào?"**
> Em dùng `RecognizerIntent.ACTION_RECOGNIZE_SPEECH` có sẵn của Android. Khi user bấm mic, em launch intent → hệ thống Android (Google Speech-to-Text) tự nhận giọng → trả về text qua `ActivityResultLauncher`. Em không cần API key ngoài.

## 7.3 Về Đăng nhập / Auth

**Q15: "Em hash password thế nào?"**
> KHÔNG hash. Firebase Authentication tự hash bằng **scrypt** ở server. App em chỉ gọi `signInWithEmailAndPassword(email, password)` — password đi qua HTTPS đến Firebase, Firebase hash + lưu. Em không bao giờ thấy hash, kể cả admin Firebase Console cũng không xem được password gốc.

**Q16: "scrypt khác MD5/SHA-256 ở đâu?"**
> scrypt được thiết kế **chống brute-force**:
> - **Slow by design** — tốn CPU + RAM nhiều (work factor lớn), 1 hash mất 100ms thay vì 1µs.
> - **Salt riêng** mỗi user → không thể dùng **rainbow table** (bảng hash sẵn).
> - **Memory-hard** — cần nhiều RAM, GPU/ASIC khó tăng tốc.
> MD5/SHA-256 quá nhanh, dễ brute-force bằng GPU. Không bao giờ dùng để hash password.

**Q17: "Email login khác Google login ở quy trình nào?"**
> **Email:** App → Firebase Auth trực tiếp (1 bước).
> **Google:** App → Google Sign-In SDK → idToken → đưa cho Firebase đổi → Firebase user (3 bước).
> Google phức tạp hơn vì cần qua Google Server xác thực account trước. Lợi: user không phải nhớ password, dùng account Google sẵn có.

**Q18: "Sao em check email tồn tại trước khi register?"**
> Em dùng `auth.fetchSignInMethodsForEmail(email)` — Firebase trả về list provider đang dùng cho email đó (vd `["password"]` hoặc `["google.com"]`). Nếu list rỗng → email chưa được dùng. Em cũng có thể check ngay khi `createUserWithEmailAndPassword` báo `EMAIL_EXISTS`, nhưng kiểm trước UX tốt hơn.

**Q19: "Em có dùng Facebook login không?"**
> KHÔNG. Em chỉ làm Email/Password và Google. Em chọn Google vì tích hợp sẵn với Firebase và đa số user Việt Nam có Google account (do Android). Nếu cần Facebook em sẽ làm tương tự Google: dùng `FacebookAuthProvider.getCredential(token)` đổi sang Firebase Credential.

**Q20: "Email + Google cùng địa chỉ thì sao?"**
> Firebase có cơ chế **provider linking** — tự gộp thành 1 account khi email khớp. Code project chưa xử lý đặc biệt, nhưng user vẫn login được. Để tốt hơn nên dùng `auth.useEmailAlreadyInUseException` để hỏi user "Bạn đã đăng ký bằng Google, chuyển sang Google login nhé?".

**Q21: "Token Firebase sống bao lâu?"**
> `idToken` của Firebase Auth có hiệu lực **1 giờ**. Firebase SDK tự refresh token ngầm khi sắp hết hạn (dùng `refreshToken` sống lâu hơn). User mở app sau cả tuần vẫn login được tự động.

**Q22: "Logout có xóa session ở server không?"**
> `FirebaseAuth.signOut()` chỉ xóa **local token** trên thiết bị này. Token đang chạy vẫn valid đến khi hết 1 giờ. Để **force logout toàn thiết bị** cần dùng `revokeRefreshTokens` (chỉ qua Admin SDK ở server). Em chưa làm — đây là điểm cải tiến.

## 7.4 Về Hash / Bảo mật

**Q23: "HMAC khác hash thường ở đâu?"**
> Hash thường (SHA-256): `hash(data)` → ai cũng tính được nếu biết data.
> HMAC: `HMAC(data, secret_key)` → cần biết secret key mới tính được.
> HMAC dùng để **xác thực** (chỉ bên có key mới tạo được hash đúng), không chỉ check integrity. VNPay yêu cầu HMAC để xác thực giao dịch.

**Q24: "Sao là HMAC-SHA512 mà không phải SHA-256?"**
> Theo yêu cầu của VNPay. SHA-512 cho hash **128 ký tự hex** (so với SHA-256 là 64), bảo mật cao hơn. Cũng không chậm hơn đáng kể trên máy hiện đại.

**Q25: "TLS/HTTPS có hash không?"**
> Có nhưng ở tầng dưới. TLS dùng kết hợp:
> - **Asymmetric encryption** (RSA/ECDHE) để trao đổi key.
> - **Symmetric encryption** (AES) để mã hóa data.
> - **HMAC** để kiểm tra integrity.
> App em không phải code TLS — hệ thống Android + OkHttp + Firebase SDK tự xử lý.

**Q26: "Em có dùng JWT không?"**
> Firebase `idToken` chính là **JWT (JSON Web Token)**. Cấu trúc 3 phần `header.payload.signature` cách nhau dấu chấm. Phần signature là HMAC-SHA256 của header+payload với secret key của Firebase → không ai forge token được. Em không tự tạo JWT, Firebase tự lo.

**Q27: "Bảo mật ảnh upload thế nào?"**
> Em **chưa có Storage Security Rules**. Hiện tại bất kỳ ai có URL download cũng truy cập được file. Cải tiến: viết rules theo mẫu Phần 3.2 — chỉ chính chủ ghi avatar, ADMIN ghi pet_media, ai cũng đọc.

## 7.5 Câu hỏi tổng hợp

**Q28: "Nếu em mất file `google-services.json` thì sao?"**
> App build vẫn được nhưng Firebase **không hoạt động** (Auth, Firestore, Storage đều fail). Em phải vào Firebase Console > Project Settings > Android app > tải lại file. Hoặc tạo mới project nếu mất hết.

**Q29: "Nếu Firebase down thì app em chạy được không?"**
> Phần lớn KHÔNG. Vì:
> - Auth fail → không login được.
> - Firestore fail → không đọc/ghi data.
> - Tuy nhiên: nhờ **offline cache** của Firestore, data đã load trước đó vẫn xem được.
> Đây là nhược điểm của serverless — phụ thuộc hoàn toàn vào Google.

**Q30: "Em sẽ làm gì để bảo mật tốt hơn cho production?"**
> Theo thứ tự ưu tiên:
> 1. Viết Firestore + Storage Security Rules chặt chẽ
> 2. Bật ProGuard minify để khó decompile
> 3. Chuyển OPENAI/VNPAY/SMTP credential sang backend proxy
> 4. Thêm OTP verify ở server (Cloud Functions)
> 5. Bật App Check (Firebase) để chống bot
> 6. Tích hợp Crashlytics để monitor lỗi
> 7. Audit Firestore queries — không dùng `addSnapshotListener` trên collection lớn
> 8. Migrate sang `EncryptedSharedPreferences` cho session local
> 9. Bật **Email Verification** trước khi cho login đầy đủ
> 10. Setup **rate limiting** ở server proxy

---

# 📌 TÓM TẮT MỘT DÒNG (HỌC THUỘC)

| Chủ đề | Câu nhớ |
|---|---|
| **Firebase Auth** | Email/Google → cấp UID + idToken (JWT) — Firebase tự hash password bằng scrypt |
| **Firestore** | NoSQL document, realtime qua `addSnapshotListener`, offline cache tự nhiên |
| **Storage** | File ảnh/video, đường dẫn `avatars/{uid}.jpg`, `chats/...`, public URL |
| **Phân quyền** | 2 lớp: client (SessionManager.isAdmin) + server (Security Rules check role) |
| **Realtime** | Firestore dùng WebSocket ngầm, callback `addSnapshotListener` mỗi khi data đổi |
| **Hash password** | KHÔNG hash, Firebase tự dùng scrypt server-side |
| **Hash VNPay** | HMAC-SHA512 với secret key để chống tampering số tiền |
| **Hash app cert** | SHA-1 fingerprint trong `google-services.json` để verify app thật |
| **Bảo mật API key** | local.properties → BuildConfig → KHÔNG commit Git |
| **HTTPS** | Mọi call đều `https://` → TLS encrypt giữa đường |
| **Base64** | Encoding (không phải bảo mật), dùng nhúng ảnh chat |
| **Offline** | Firestore tự cache local, app vẫn dùng được khi mất mạng |

---

# 📁 BẢNG TỔNG HỢP FILE PATH MỌI ĐOẠN CODE QUAN TRỌNG

> Để bạn tra cứu nhanh khi báo cáo. Mọi file đều nằm trong `app/src/main/java/com/example/petshop/`.

| Tính năng | File chính | Phụ trợ |
|---|---|---|
| Launcher / Routing | `view/activity/SplashActivity.java` | `MainActivity.java` |
| Login | `view/activity/LoginActivity.java` | `viewmodel/AuthViewModel.java`, `utils/FirebaseHelper.java` |
| Register | `view/activity/RegisterActivity.java` | `utils/EmailHelper.java` (OTP) |
| Tạo Admin | `utils/AdminSetupHelper.java` | – |
| Session local | `utils/SessionManager.java` | – |
| Home tab | `view/fragment/HomeFragment.java` | `viewmodel/HomeViewModel.java` |
| Profile tab | `view/fragment/ProfileFragment.java` | `view/activity/ProfileActivity.java` |
| Cart | `view/activity/CartActivity.java` | `viewmodel/CartViewModel.java`, `repository/CartRepository.java` |
| Checkout | `view/activity/CheckoutActivity.java` | `repository/OrderRepository.java` |
| VNPay | `utils/VNPayHelper.java` | `view/activity/VNPayWebViewActivity.java`, `VNPayResultActivity.java` |
| Chat AI | `view/activity/ChatActivity.java` | `viewmodel/ChatViewModel.java` |
| Address | `view/activity/ManageAddressActivity.java` | `repository/AddressRepository.java` |
| Notification | `view/activity/NotificationActivity.java` | `repository/NotificationRepository.java`, `view/adapter/NotificationAdapter.java` |
| Admin Dashboard | `view/activity/AdminActivity.java` | `viewmodel/AdminViewModel.java` |
| Pet CRUD | `view/activity/ManagePetsActivity.java` + `AddEditPetActivity.java` | `repository/PetRepository.java` |
| Food CRUD | `view/activity/ManageFoodActivity.java` + `AddEditFoodActivity.java` | `repository/FoodRepository.java` |
| Order Admin | `view/activity/AdminOrderListActivity.java` + `AdminOrderDetailActivity.java` | – |
| Hằng số / Config | `utils/Constants.java` | `app/build.gradle.kts`, `local.properties` |
| Firebase wrapper | `utils/FirebaseHelper.java` | – |
| Upload file | `utils/StorageHelper.java` | – |
| Build config | `app/build.gradle.kts` | `app/google-services.json` |
| Manifest | `app/src/main/AndroidManifest.xml` | – |

---

🎓 **Chúc bạn bảo vệ thành công!** Khi giáo viên hỏi, bạn cứ bình tĩnh chỉ vào file path, nói tự tin, đừng học vẹt code — hiểu **vì sao** quan trọng hơn nhớ **làm sao**.
