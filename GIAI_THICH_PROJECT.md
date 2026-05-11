# 📚 PHÂN TÍCH TOÀN BỘ PROJECT PETSHOP ANDROID
## Giải thích chi tiết dành cho sinh viên mới học

---

## MỤC LỤC
1. [Cấu trúc project tổng quan](#1-cấu-trúc-project-tổng-quan)
2. [Kiến trúc project (MVVM)](#2-kiến-trúc-project-mvvm)
3. [Flow hoạt động tổng thể](#3-flow-hoạt-động-tổng-thể)
4. [Data flow](#4-data-flow)
5. [Vai trò từng package](#5-vai-trò-từng-package)
6. [Vai trò từng class](#6-vai-trò-từng-class)
7. [Vai trò từng hàm quan trọng](#7-vai-trò-từng-hàm-quan-trọng)
8. [UI hoạt động thế nào](#8-ui-hoạt-động-thế-nào)
9. [Firebase hoạt động ra sao](#9-firebase-hoạt-động-ra-sao)
10. [Navigation giữa các màn hình](#10-navigation-giữa-các-màn-hình)
11. [Login flow chi tiết](#11-login-flow-chi-tiết)
12. [CRUD flow và toàn bộ tính năng](#12-crud-flow-và-toàn-bộ-tính-năng)
13. [RecyclerView hoạt động](#13-recyclerview-hoạt-động)
14. [Adapter hoạt động](#14-adapter-hoạt-động)
15. [ViewBinding hoạt động](#15-viewbinding-hoạt-động)
16. [ViewModel và Repository](#16-viewmodel-và-repository)
17. [Async và Callback hoạt động](#17-async-và-callback-hoạt-động)
18. [Lifecycle Android](#18-lifecycle-android)
19. [Kiến trúc MVVM chi tiết](#19-kiến-trúc-mvvm-chi-tiết)
20. [Vai trò Activity/Fragment/Adapter/ViewModel/Repository](#20-vai-trò-từng-thành-phần)
21. [Tại sao phải tách nhiều lớp](#21-tại-sao-phải-tách-nhiều-lớp)
22. [Dependency giữa các module](#22-dependency-giữa-các-module)
23. [Câu hỏi giáo viên có thể hỏi](#23-câu-hỏi-giáo-viên-có-thể-hỏi)
24. [Câu trả lời mẫu](#24-câu-trả-lời-mẫu)
25. [Tóm tắt và file quan trọng nhất](#25-tóm-tắt-và-file-quan-trọng-nhất)

---

## 1. CẤU TRÚC PROJECT TỔNG QUAN

Hãy tưởng tượng project này như một cửa hàng thú cưng thật sự. Trong cửa hàng đó có:
- **Khu bán hàng** (màn hình cho khách hàng)
- **Khu quản lý** (màn hình dành cho admin)
- **Kho hàng** (Firebase Firestore - lưu dữ liệu)
- **Thu ngân** (xử lý đơn hàng, thanh toán)
- **Trợ lý AI** (chat bot OpenAI)

### Cây thư mục:

```
app/src/main/java/com/example/petshop/
│
├── MainActivity.java              ← Cửa vào (chỉ redirect sang Splash)
│
├── model/entity/                  ← Các "khuôn" dữ liệu (21 class)
│   ├── Pet.java                   ← Thú cưng
│   ├── Food.java                  ← Đồ ăn
│   ├── User.java                  ← Người dùng
│   ├── Order.java                 ← Đơn hàng
│   ├── Cart.java / CartItem.java  ← Giỏ hàng
│   ├── Category.java              ← Danh mục
│   ├── Promotion.java             ← Khuyến mãi
│   ├── Voucher.java               ← Mã giảm giá
│   ├── ChatMessage.java           ← Tin nhắn chat
│   ├── Address.java               ← Địa chỉ giao hàng
│   └── Notification.java          ← Thông báo
│
├── repository/                    ← Tầng giao tiếp với Firebase (11 class)
│   ├── PetRepository.java
│   ├── FoodRepository.java
│   ├── CartRepository.java
│   ├── OrderRepository.java
│   └── ...
│
├── viewmodel/                     ← Tầng logic xử lý (11 class)
│   ├── AuthViewModel.java         ← Đăng nhập/đăng ký
│   ├── HomeViewModel.java         ← Trang chủ
│   ├── CartViewModel.java         ← Giỏ hàng
│   ├── ChatViewModel.java         ← Chat AI
│   └── ...
│
├── view/
│   ├── activity/                  ← Các màn hình (34 class)
│   │   ├── SplashActivity.java    ← Màn hình chào
│   │   ├── LoginActivity.java     ← Đăng nhập
│   │   ├── RegisterActivity.java  ← Đăng ký
│   │   ├── PetShopActivity.java   ← Màn hình chính khách hàng
│   │   ├── AdminActivity.java     ← Màn hình chính admin
│   │   ├── CheckoutActivity.java  ← Thanh toán
│   │   ├── ChatActivity.java      ← Chat với AI
│   │   └── ...
│   ├── fragment/                  ← Mảnh giao diện (2 class)
│   │   ├── HomeFragment.java      ← Tab trang chủ
│   │   └── ProfileFragment.java   ← Tab hồ sơ
│   ├── adapter/                   ← Quản lý danh sách (16 class)
│   └── dialog/                    ← Hộp thoại (4 class)
│
└── utils/                         ← Công cụ hỗ trợ (10 class)
    ├── FirebaseHelper.java        ← Giao tiếp Firebase
    ├── SessionManager.java        ← Lưu thông tin đăng nhập
    ├── Constants.java             ← Hằng số
    ├── VNPayHelper.java           ← Thanh toán VNPay
    └── EmailHelper.java           ← Gửi email OTP
```

---

## 2. KIẾN TRÚC PROJECT (MVVM)

Project này dùng kiến trúc **MVVM** (Model - View - ViewModel).

### MVVM là gì? Hãy dùng ví dụ thực tế:

Tưởng tượng bạn đặt món ăn ở nhà hàng:
- **Model** = Nhà bếp (nơi có nguyên liệu, chế biến đồ ăn - tức là dữ liệu Firebase)
- **ViewModel** = Bồi bàn (nhận yêu cầu từ khách, gọi vào bếp, mang đồ ra) 
- **View** = Bàn của khách (màn hình hiển thị cho người dùng)

```
VIEW (Activity/Fragment)
    |  "Tôi muốn xem danh sách thú cưng"
    ↓  gọi hàm trong ViewModel
VIEWMODEL (HomeViewModel)
    |  "OK, tôi sẽ lấy từ Repository"
    ↓  gọi Repository
REPOSITORY (PetRepository)
    |  "Để tôi lấy từ Firebase"
    ↓  truy vấn Firestore
FIREBASE FIRESTORE
    |  trả về dữ liệu
    ↑  thông qua Callback
REPOSITORY  →  VIEWMODEL  →  VIEW (tự động cập nhật qua LiveData)
```

### Sơ đồ chi tiết hơn:

```
┌─────────────────────────────────────────────────────────┐
│                      VIEW LAYER                          │
│  Activity / Fragment  ←──── observe ────  LiveData      │
│  (Hiển thị UI, nhận sự kiện từ người dùng)              │
└────────────────┬────────────────────────────────────────┘
                 │ gọi hàm (vd: vm.loadHomeData())
┌────────────────▼────────────────────────────────────────┐
│                   VIEWMODEL LAYER                        │
│  Chứa logic xử lý, giữ dữ liệu qua xoay màn hình       │
│  Không được import Context hay Activity                  │
└────────────────┬────────────────────────────────────────┘
                 │ gọi Repository
┌────────────────▼────────────────────────────────────────┐
│                  REPOSITORY LAYER                        │
│  Giao tiếp với Firebase Firestore                       │
│  Trả kết quả qua Callback interface                     │
└────────────────┬────────────────────────────────────────┘
                 │ get/set
┌────────────────▼────────────────────────────────────────┐
│                   DATA LAYER                             │
│  Firebase Firestore (NoSQL database trên cloud)         │
│  Firebase Auth (đăng nhập/đăng ký)                      │
│  Firebase Storage (lưu ảnh)                             │
└─────────────────────────────────────────────────────────┘
```

---

## 3. FLOW HOẠT ĐỘNG TỔNG THỂ

### Khi người dùng mở app lần đầu:

```
Mở App
  ↓
MainActivity.java
  → Ngay lập tức redirect sang SplashActivity
  → finish() (đóng MainActivity lại, không dùng nữa)
  ↓
SplashActivity.java
  → Hiện logo/splash trong 1.5 giây (MIN_SPLASH_MS = 1500)
  → Đồng thời kiểm tra: "Người dùng đã đăng nhập chưa?"
     - FirebaseHelper.getCurrentUser() khác null → đã đăng nhập
     - null → chưa đăng nhập
  ↓
Nếu đã đăng nhập:
  → Kiểm tra role (ADMIN hay CUSTOMER)
  → ADMIN → AdminActivity
  → CUSTOMER → PetShopActivity
Nếu chưa đăng nhập:
  → PetShopActivity (vẫn có thể xem, nhưng chức năng bị hạn chế)
```

### Flow khách hàng mua hàng:

```
PetShopActivity (BottomNavigation với 4 tab)
  ↓
HomeFragment (Tab Trang chủ)
  → Xem danh mục, thú cưng, đồ ăn, banner
  → Tìm kiếm sản phẩm
  → Click vào thú cưng → PetDetailActivity
  → Click "Thêm vào giỏ" → CartViewModel.addPet()
  ↓
CartActivity (khi bấm icon giỏ hàng)
  → Xem danh sách sản phẩm trong giỏ
  → Tăng/giảm số lượng đồ ăn
  → Xóa sản phẩm
  → Bấm "Thanh toán" → CheckoutActivity
  ↓
CheckoutActivity
  → Chọn địa chỉ giao hàng
  → Nhập/chọn mã voucher
  → Chọn phương thức thanh toán (COD hoặc VNPay)
  → Bấm "Đặt hàng"
  ↓
Nếu COD:
  → Tạo Order trong Firestore
  → Xóa giỏ hàng
  → Chuyển sang OrderDetailActivity (hiện thành công)
Nếu VNPay:
  → Tạo URL thanh toán → VNPayWebViewActivity
  → Sau khi thanh toán xong → VNPayResultActivity
  → Cập nhật trạng thái đơn hàng
```

---

## 4. DATA FLOW

### Ví dụ: Người dùng xem trang chủ

```
HomeFragment.onViewCreated()
  │
  ├─ vm = new ViewModelProvider(requireActivity()).get(HomeViewModel.class)
  │       (Lấy hoặc tạo ViewModel, dùng chung trong cùng Activity)
  │
  ├─ observeViewModel()  ← Đăng ký lắng nghe dữ liệu
  │   ├─ vm.getFeaturedPets().observe(...) → khi có pets mới → renderPets()
  │   └─ vm.getFeaturedFoods().observe(...) → khi có foods mới → renderFoods()
  │
  └─ vm.loadHomeData()  ← Ra lệnh "hãy tải dữ liệu về"
        │
        └─ HomeViewModel.loadHomeData()
              │
              ├─ promoRepo.getActive() → lấy khuyến mãi đang chạy
              ├─ petRepo.getAll() → lấy danh sách thú cưng từ Firestore
              └─ foodRepo.getAll() → lấy danh sách đồ ăn từ Firestore
                    │
                    └─ PetRepository.getAll()
                          │
                          └─ db.collection("pets").orderBy("createdAt").get()
                                │
                                └─ Firestore trả về kết quả
                                      │
                                      └─ filteredPets.postValue(allPets)
                                            │
                                            └─ HomeFragment.renderPets() TỰ ĐỘNG CHẠY
                                                  │
                                                  └─ petAdapter.updateList(pets)
                                                        │
                                                        └─ RecyclerView hiển thị danh sách
```

### Tại sao tự động cập nhật được?

Đây là sức mạnh của **LiveData + Observer pattern**:

```java
// Trong HomeFragment - đăng ký lắng nghe
vm.getFeaturedPets().observe(getViewLifecycleOwner(), pets -> {
    // Hàm này sẽ tự động chạy mỗi khi pets thay đổi
    petAdapter.updateList(pets);
});

// Trong HomeViewModel - khi có dữ liệu mới
filteredPets.postValue(newPetList); // Thông báo cho tất cả observers
```

Giống như bạn đăng ký nhận thông báo email. Khi có email mới, hệ thống TỰ ĐỘNG gửi thông báo cho bạn, bạn không cần ngồi F5 liên tục.

---

## 5. VAI TRÒ TỪNG PACKAGE

### `model/entity/` - "Bản thiết kế dữ liệu"

Đây là các **Data Class** - mô tả hình dạng của dữ liệu. Giống như bản vẽ thiết kế:

```java
// Pet.java - Khuôn của một con thú cưng
public class Pet {
    private String id;          // Mã định danh
    private String name;        // Tên ("Mochi")
    private String species;     // Loài ("DOG", "CAT")
    private String breed;       // Giống ("Corgi", "Husky")
    private double price;       // Giá gốc
    private double discountedPrice; // Giá sau giảm
    private String status;      // Trạng thái: AVAILABLE/SOLD/RESERVED
    // ... và nhiều trường khác
    
    // getEffectivePrice() - tính giá thực tế có tính khuyến mãi
    public double getEffectivePrice() {
        if (promotionId != null && promotion != null && promotion.isActive()) {
            return promotion.applyDiscount(price); // Trả về giá đã giảm
        }
        return price; // Trả về giá gốc nếu không có KM
    }
}
```

Firestore tự động chuyển đổi JSON ↔ Object Java nhờ các class này.

### `repository/` - "Nhân viên kho hàng"

Mỗi Repository chịu trách nhiệm với một loại dữ liệu:

```
PetRepository       → đọc/ghi thú cưng
FoodRepository      → đọc/ghi đồ ăn
CartRepository      → đọc/ghi giỏ hàng
OrderRepository     → đọc/ghi đơn hàng
UserRepository      → đọc/ghi thông tin người dùng
AddressRepository   → đọc/ghi địa chỉ
NotificationRepository → đọc/ghi thông báo
VoucherRepository   → đọc/ghi voucher
PromotionRepository → đọc/ghi khuyến mãi
CategoryRepository  → đọc/ghi danh mục
ReturnRepository    → đọc/ghi yêu cầu đổi trả
```

### `viewmodel/` - "Bộ não xử lý"

```
AuthViewModel       → Xử lý đăng nhập, đăng ký, logout
HomeViewModel       → Xử lý dữ liệu trang chủ, tìm kiếm, lọc danh mục
CartViewModel       → Xử lý giỏ hàng (thêm/xóa/cập nhật)
ChatViewModel       → Xử lý chat AI (OpenAI GPT-4o-mini)
AdminViewModel      → Xử lý thống kê cho admin dashboard
PetManageViewModel  → Xử lý CRUD thú cưng (admin)
FoodManageViewModel → Xử lý CRUD đồ ăn (admin)
CategoryManageViewModel → Xử lý CRUD danh mục (admin)
PromotionManageViewModel → Xử lý CRUD khuyến mãi (admin)
UserManageViewModel → Xử lý quản lý người dùng (admin)
VoucherManageViewModel  → Xử lý CRUD voucher (admin)
```

### `view/activity/` - "Các màn hình"

34 màn hình, chia thành 3 nhóm:

**Nhóm Auth (xác thực):**
- `SplashActivity` → Màn hình chào
- `LoginActivity` → Đăng nhập
- `RegisterActivity` → Đăng ký

**Nhóm Customer (khách hàng):**
- `PetShopActivity` → Màn hình chính (container cho Fragment)
- `PetDetailActivity` → Xem chi tiết thú cưng
- `FoodDetailActivity` → Xem chi tiết đồ ăn
- `CartActivity` → Giỏ hàng
- `CheckoutActivity` → Thanh toán
- `OrderHistoryActivity` → Lịch sử đơn hàng
- `ChatActivity` → Chat với AI
- `ProfileActivity` → Hồ sơ cá nhân
- `NotificationActivity` → Thông báo
- ...

**Nhóm Admin:**
- `AdminActivity` → Dashboard admin
- `ManagePetsActivity` → Quản lý thú cưng
- `ManageFoodActivity` → Quản lý đồ ăn
- `ManageUsersActivity` → Quản lý người dùng
- `AdminOrderListActivity` → Quản lý đơn hàng
- ...

### `utils/` - "Hộp công cụ"

```
FirebaseHelper   → Tất cả thao tác Firebase Auth
SessionManager   → Lưu/đọc thông tin đăng nhập trong SharedPreferences
Constants        → Các hằng số (tên collection, intent key, ...)
VNPayHelper      → Tạo URL thanh toán VNPay, tạo chữ ký HMAC-SHA512
EmailHelper      → Gửi email OTP qua JavaMail
StorageHelper    → Upload ảnh lên Firebase Storage
ShippingHelper   → Tính phí vận chuyển
CartBadgeManager → Cập nhật badge số lượng giỏ hàng
PromotionManager → Áp dụng khuyến mãi vào danh sách sản phẩm
AdminSetupHelper → Tạo tài khoản admin lần đầu
```

---

## 6. VAI TRÒ TỪNG CLASS QUAN TRỌNG

### `MainActivity.java` - "Cửa ra vào"

```java
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        startActivity(new Intent(this, SplashActivity.class)); // Chuyển sang Splash
        finish(); // Đóng chính nó lại
    }
}
```

**Tại sao cần class này?** Vì `AndroidManifest.xml` yêu cầu phải có một Activity với `LAUNCHER` intent-filter. Tuy nhiên launcher thực sự là `SplashActivity`, `MainActivity` chỉ là "bảng chỉ đường".

### `SplashActivity.java` - "Cổng vào thực sự"

Nhiệm vụ:
1. Hiện logo/splash screen
2. Kiểm tra đăng nhập (Firebase Auth)
3. Phân quyền (ADMIN → AdminActivity, CUSTOMER → PetShopActivity)
4. Đảm bảo hiện ít nhất 1.5 giây để người dùng nhìn thấy splash

### `PetShopActivity.java` - "Khung chứa màn hình khách hàng"

```java
// Chứa BottomNavigationView với 4 tab:
// 🏠 Home    →  HomeFragment
// 💬 Chat    →  ChatActivity (mở Activity mới)
// 📦 Đơn    →  OrderHistoryActivity (mở Activity mới)
// 👤 Profile →  ProfileFragment
```

Dùng kỹ thuật **hide/show Fragment** thay vì replace để giữ state khi chuyển tab.

### `HomeFragment.java` - "Trang chủ"

Là fragment phức tạp nhất phía customer:
- Hiển thị lời chào theo thời gian (Sáng/Chiều/Tối)
- Danh sách danh mục (horizontal RecyclerView)
- Danh sách thú cưng nổi bật (horizontal RecyclerView)
- Danh sách đồ ăn nổi bật (horizontal RecyclerView)
- Tìm kiếm real-time
- Badge thông báo chưa đọc (real-time Firestore listener)
- Badge số lượng giỏ hàng

### `AuthViewModel.java` - "Bộ xử lý đăng nhập"

```java
// 3 phương thức đăng nhập:
loginWithEmail(email, password)    // Email + Password
loginWithGoogle(idToken)           // Google Sign-In
registerWithEmail(email, pwd, name) // Tạo tài khoản mới

// 3 LiveData để UI lắng nghe:
isLoading    // true/false - hiện/ẩn loading
errorMessage // thông báo lỗi
userRole     // "ADMIN" hoặc "CUSTOMER" → điều hướng
```

### `CartRepository.java` - "Kho giỏ hàng"

Class này rất thú vị vì dùng **Firestore Transaction** để đảm bảo tính nhất quán:

```java
// Khi thêm thú cưng vào giỏ:
// 1. Kiểm tra trạng thái pet (phải là AVAILABLE)
// 2. Đổi trạng thái pet thành RESERVED (để người khác không mua nữa)
// 3. Thêm vào giỏ hàng
// Tất cả 3 bước phải thành công cùng lúc, không thì không làm gì cả
db.runTransaction(transaction -> {
    // ĐỌC TRƯỚC, GHI SAU (quy tắc bắt buộc của Firestore)
    var petDoc = transaction.get(petRef);
    var cartDoc = transaction.get(cartRef);
    
    // Kiểm tra
    if (!"AVAILABLE".equals(petDoc.getString("status"))) {
        throw new RuntimeException("Thú cưng đã được đặt bởi người khác");
    }
    
    // Ghi (chỉ ghi khi đọc xong hết)
    transaction.update(petRef, "status", "RESERVED");
    transaction.set(cartRef, updatedCart);
    return null;
})
```

### `ChatViewModel.java` - "Bộ xử lý chat AI"

Kết nối với **OpenAI GPT-4o-mini** qua OkHttp:
1. Lấy context (danh sách pets, foods, orders, vouchers) từ Firestore
2. Gửi yêu cầu đến `https://api.openai.com/v1/chat/completions`
3. Nhận phản hồi theo **streaming** (từng từ xuất hiện dần như ChatGPT)
4. Lưu lịch sử chat vào Firestore (nếu đăng nhập) hoặc SharedPreferences (nếu khách)

---

## 7. VAI TRÒ TỪNG HÀM QUAN TRỌNG

### Trong `HomeViewModel.java`:

```java
// loadHomeData() - Tải toàn bộ dữ liệu trang chủ
public void loadHomeData() {
    isLoading.setValue(true);
    // Bước 1: Lấy khuyến mãi đang chạy
    promoRepo.getActive(new Callback<>() {
        void onSuccess(List<Promotion> promos) {
            loadMainData(promos); // Bước 2
        }
    });
}

// search() - Tìm kiếm real-time
public void search(String query) {
    // Bình thường hoá text (bỏ dấu tiếng Việt để tìm kiếm dễ hơn)
    // "mèo" → "meo", "chó" → "cho"
    String q = normalizeSearchText(query);
    
    // Lọc thú cưng theo tên, giống, loài
    filteredPets.setValue(allPets.stream()
        .filter(pet -> containsNormalized(pet.getName(), q))
        .collect(Collectors.toList()));
    
    // Lọc đồ ăn theo tên, thương hiệu, loại
    filteredFoods.setValue(allFoods.stream()
        .filter(food -> containsNormalized(food.getName(), q))
        .collect(Collectors.toList()));
}

// normalizeSearchText() - Bình thường hoá để tìm kiếm
// "Mèo Ba Tư" → "meo ba tu" (bỏ dấu, thành chữ thường)
private String normalizeSearchText(String value) {
    String s = value.trim().toLowerCase();
    // Tách dấu tiếng Việt thành ký tự riêng rồi xóa đi
    s = Normalizer.normalize(s, Normalizer.Form.NFD)
            .replaceAll("\\p{InCombiningDiacriticalMarks}+", "");
    s = s.replace("đ", "d"); // "đ" không bị tách được nên xử lý riêng
    return s;
}
```

### Trong `OrderRepository.java`:

```java
// createOrder() - Tạo đơn hàng (rất phức tạp)
public void createOrder(Order order, List<CartItem> cartItems, Callback<String> cb) {
    // 1. Tạo mã đơn hàng duy nhất: "ORD" + ngày giờ + uuid ngắn
    String orderCode = "ORD" + new SimpleDateFormat("MMddHHmmss").format(new Date())
                    + orderId.substring(0, 6).toUpperCase();
    
    // 2. Nếu COD → PENDING (đang chờ xử lý)
    //    Nếu VNPay → WAIT_PAY (chờ thanh toán)
    
    // 3. Transaction để đảm bảo an toàn:
    db.runTransaction(tx -> {
        // Trừ stock của đồ ăn
        // Đổi status pet thành RESERVED
        // Lưu đơn hàng vào Firestore
        return null;
    });
}
```

### Trong `FirebaseHelper.java`:

```java
// loginWithEmail() - Đăng nhập bằng email
public static void loginWithEmail(String email, String password, OnAuthCallback callback) {
    // Gọi Firebase Auth để đăng nhập
    auth.signInWithEmailAndPassword(email, password)
        .addOnSuccessListener(result -> {
            String uid = result.getUser().getUid();
            // Sau khi đăng nhập xong, lấy role từ Firestore
            getUserRole(uid, role -> callback.onSuccess(uid, role));
        })
        .addOnFailureListener(e -> {
            // Chuyển lỗi thành tiếng Việt dễ hiểu
            callback.onFailure(parseAuthError(e.getMessage()));
        });
}

// parseAuthError() - Chuyển lỗi Firebase thành tiếng Việt
private static String parseAuthError(String error) {
    if (error.contains("WRONG_PASSWORD")) return "Email hoặc mật khẩu không đúng";
    if (error.contains("EMAIL_EXISTS"))   return "Email đã được sử dụng";
    // ...
}
```

---

## 8. UI HOẠT ĐỘNG THẾ NÀO

### Layout XML và Java kết nối với nhau:

```
res/layout/activity_login.xml     ←→   LoginActivity.java
res/layout/activity_pet_shop.xml  ←→   PetShopActivity.java
res/layout/fragment_home.xml      ←→   HomeFragment.java
res/layout/item_pet_card.xml      ←→   HomePetAdapter.java (dùng trong RecyclerView)
```

### Cách tìm View trong code:

```java
// Cách truyền thống (dùng trong project này):
TextView tvGreeting = root.findViewById(R.id.tvGreeting);
// R.id.tvGreeting là ID được khai báo trong XML:
// <TextView android:id="@+id/tvGreeting" ... />
```

### Cách hiện/ẩn View:

```java
// Hiện
tvCartBadge.setVisibility(View.VISIBLE);
// Ẩn nhưng vẫn chiếm chỗ
tvCartBadge.setVisibility(View.INVISIBLE);
// Ẩn hoàn toàn, không chiếm chỗ
tvCartBadge.setVisibility(View.GONE);
```

### Cách load ảnh từ URL (dùng Glide):

```java
// Glide là thư viện load ảnh phổ biến
// Tự động cache, xử lý lỗi, hiện placeholder
Glide.with(context)
    .load(pet.getThumbnailUrl())       // URL ảnh từ Firebase Storage
    .centerCrop()                       // Cắt ảnh cho vừa ô
    .placeholder(R.mipmap.ic_launcher) // Ảnh mặc định khi đang tải
    .into(imageView);                   // ImageView để hiện
```

### BottomNavigationView hoạt động:

```java
// PetShopActivity.java
bottomNavView.setOnItemSelectedListener(item -> {
    int id = item.getItemId();
    
    if (id == R.id.nav_home) {
        showFragment(homeFragment);   // Hiện HomeFragment
        return true;
    } else if (id == R.id.nav_chat) {
        startActivity(new Intent(this, ChatActivity.class)); // Mở Activity mới
        return true;
    }
    // ...
});
```

---

## 9. FIREBASE HOẠT ĐỘNG RA SAO

### Firebase có 3 dịch vụ trong project này:

#### 1. Firebase Authentication (quản lý tài khoản)
```
Lưu: email, password (được mã hoá), uid (mã định danh duy nhất)
Không lưu: tên, số điện thoại, vai trò (những thứ này lưu ở Firestore)

Luồng đăng nhập:
User nhập email/pass → Firebase Auth kiểm tra → Trả về uid
uid → Truy vấn Firestore → Lấy thêm thông tin (tên, role, ...)
```

#### 2. Firebase Firestore (cơ sở dữ liệu NoSQL)
Giống như Excel nhưng không có bảng, có **Collection** (tập hợp) và **Document** (tài liệu):

```
firestore/
├── users/                    ← Collection
│   ├── uid123/               ← Document (ID = Firebase UID)
│   │   ├── fullName: "Nguyễn Văn A"
│   │   ├── email: "a@gmail.com"
│   │   ├── role: "CUSTOMER"
│   │   └── totalSpent: 500000
│   └── uid456/
│       └── ...
├── pets/
│   ├── pet_uuid_abc/         ← Document (ID tự tạo)
│   │   ├── name: "Mochi"
│   │   ├── species: "DOG"
│   │   ├── price: 5000000
│   │   └── status: "AVAILABLE"
│   └── ...
├── foods/
├── orders/
├── carts/
│   └── uid123/               ← Mỗi user có 1 document giỏ hàng
│       ├── items: [...]       ← Mảng CartItem
│       └── subtotal: 200000
├── categories/
├── promotions/
├── vouchers/
├── banners/
└── reviews/
```

**Cách đọc dữ liệu từ Firestore:**
```java
// Lấy tất cả thú cưng, sắp xếp theo ngày tạo
db.collection("pets")
    .orderBy("createdAt", Query.Direction.DESCENDING)
    .get()
    .addOnSuccessListener(querySnapshot -> {
        // querySnapshot chứa tất cả documents
        for (DocumentSnapshot doc : querySnapshot.getDocuments()) {
            Pet pet = doc.toObject(Pet.class); // Tự động chuyển JSON → Object
            pet.setId(doc.getId());             // Gán ID (không có trong object)
            list.add(pet);
        }
        callback.onSuccess(list);
    });
```

**Transaction - đảm bảo tính toàn vẹn:**
```java
// Nếu App crashed giữa chừng, Firestore sẽ tự rollback
db.runTransaction(tx -> {
    // Phải đọc TẤT CẢ trước, rồi mới ghi
    DocumentSnapshot snap = tx.get(petRef);
    
    // Validate
    if (!"AVAILABLE".equals(snap.getString("status")))
        throw new RuntimeException("Pet đã được đặt");
    
    // Ghi (chỉ thực hiện nếu không có exception)
    tx.update(petRef, "status", "RESERVED");
    tx.set(cartRef, updatedCart);
    return null;
});
```

#### 3. Firebase Storage (lưu ảnh/file)
```
firebase-storage/
├── pets/         ← Ảnh thú cưng
├── foods/        ← Ảnh đồ ăn
├── users/        ← Avatar người dùng
└── chats/        ← Ảnh gửi trong chat
```

---

## 10. NAVIGATION GIỮA CÁC MÀN HÌNH

Project **KHÔNG dùng Navigation Component** (không có `nav_graph.xml`). Thay vào đó dùng Intent truyền thống:

### Cách chuyển màn hình:

```java
// Đơn giản nhất - mở Activity mới
startActivity(new Intent(this, PetDetailActivity.class));

// Mở và truyền dữ liệu
Intent intent = new Intent(this, PetDetailActivity.class);
intent.putExtra("pet_id", pet.getId()); // Truyền ID
startActivity(intent);

// Nhận dữ liệu trong Activity mới
String petId = getIntent().getStringExtra("pet_id");

// Mở và xóa stack (không thể Back về)
Intent intent = new Intent(this, PetShopActivity.class);
intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
startActivity(intent);
finish();

// Mở và chờ kết quả trả về
startActivityForResult(intent, REQUEST_CODE_100);
// Nhận kết quả trong onActivityResult()
@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    if (requestCode == 100 && resultCode == RESULT_OK) {
        String addressId = data.getStringExtra("selected_address_id");
    }
}
```

### Sơ đồ navigation đầy đủ:

```
SplashActivity
    ├── → AdminActivity (nếu là Admin)
    └── → PetShopActivity (mặc định)
        │
        ├─ [Tab Home] → HomeFragment
        │   ├── → PetDetailActivity
        │   │       └── → CartActivity
        │   ├── → FoodDetailActivity
        │   │       └── → CartActivity
        │   ├── → ProductListActivity
        │   ├── → NotificationActivity
        │   └── → PromotionActivity
        │
        ├─ [Tab Chat] → ChatActivity
        │
        ├─ [Tab Orders] → OrderHistoryActivity
        │   └── → OrderDetailActivity
        │       └── → ReturnRequestActivity
        │
        └─ [Tab Profile] → ProfileFragment
            ├── → ProfileActivity
            │   ├── → EditProfileActivity
            │   └── → ManageAddressActivity
            └── → LoginActivity (nếu chưa đăng nhập)

LoginActivity
    ├── → RegisterActivity
    ├── → PetShopActivity (đăng nhập thành công, CUSTOMER)
    └── → AdminActivity (đăng nhập thành công, ADMIN)

CartActivity
    └── → CheckoutActivity
            ├── → ManageAddressActivity (chọn địa chỉ)
            ├── → OrderDetailActivity (COD thành công)
            └── → VNPayWebViewActivity (VNPay)
                    └── → VNPayResultActivity

AdminActivity
    ├── → ManageUsersActivity
    ├── → ManagePetsActivity → AddEditPetActivity
    ├── → ManageFoodActivity → AddEditFoodActivity
    ├── → ManageCategoriesActivity
    ├── → ManagePromotionsActivity → AddEditPromotionActivity
    ├── → ManageVouchersActivity → AddEditVoucherActivity
    ├── → AdminOrderListActivity → AdminOrderDetailActivity
    └── → AdminReturnListActivity
```

---

## 11. LOGIN FLOW CHI TIẾT

### Flow 1: Đăng nhập bằng Email/Password

```
User nhập email + password
    ↓ Click "Đăng nhập"
LoginActivity.attemptEmailLogin()
    → Validate: email không rỗng, password không rỗng
    → authViewModel.loginWithEmail(email, password)
        ↓
AuthViewModel.loginWithEmail()
    → isLoading.postValue(true) // Hiện loading
    → FirebaseHelper.loginWithEmail(email, password, callback)
        ↓
FirebaseHelper.loginWithEmail()
    → auth.signInWithEmailAndPassword(email, password)
        ↓
    [Firebase Auth kiểm tra trên server]
        ↓
    THÀNH CÔNG:
        → Lấy uid từ kết quả
        → getUserRole(uid) → truy vấn Firestore lấy role
            ↓
        callback.onSuccess(uid, role)
            ↓
        AuthViewModel.loadUserDataAndSaveSession(uid, role)
            → FirebaseHelper.getUserData(uid) → lấy thêm tên, avatar
            → sessionManager.saveSession(...) // Lưu vào SharedPreferences
            → isLoading.postValue(false)
            → userRole.postValue(role) // Thông báo cho LoginActivity
                ↓
        LoginActivity.observeViewModel() nhận được role
            → navigateByRole(role)
                → ADMIN: startActivity(AdminActivity)
                → CUSTOMER: startActivity(PetShopActivity)
                → finish() // Đóng LoginActivity
    
    THẤT BẠI:
        → parseAuthError(e.getMessage()) // Chuyển thành tiếng Việt
        → errorMessage.postValue(msg)
        → LoginActivity hiện thông báo lỗi
```

### Flow 2: Đăng nhập bằng Google

```
User click "Đăng nhập với Google"
    ↓
LoginActivity.startGoogleSignIn()
    → googleSignInClient.signOut() // Đảm bảo chọn tài khoản mới
    → googleSignInLauncher.launch(signInIntent) // Mở cửa sổ chọn Google account
        ↓
    [Android hiện popup chọn tài khoản Google]
        ↓
    User chọn tài khoản
        ↓
googleSignInLauncher.onActivityResult()
    → task.getResult(ApiException.class) → lấy GoogleSignInAccount
    → authViewModel.loginWithGoogle(account.getIdToken())
        ↓
FirebaseHelper.loginWithGoogle(idToken)
    → GoogleAuthProvider.getCredential(idToken, null)
    → auth.signInWithCredential(credential)
        ↓
    [Firebase xác thực với Google]
        ↓
    THÀNH CÔNG + User mới:
        → saveUserToFirestore(...) // Tạo document trong Firestore
        → callback.onSuccess(uid, ROLE_CUSTOMER)
    
    THÀNH CÔNG + User cũ:
        → getUserRole(uid) // Lấy role đã có
        → callback.onSuccess(uid, role)
```

### Flow 3: Đăng ký

```
User nhập thông tin → Click "Gửi mã OTP"
    ↓
RegisterActivity.sendOtp()
    → Kiểm tra email hợp lệ
    → Firebase.fetchSignInMethodsForEmail(email) // Kiểm tra email đã tồn tại chưa
        ↓
    Email đã tồn tại → Hiện lỗi
    Email chưa tồn tại:
        → Tạo OTP 6 số ngẫu nhiên: Math.random() * 900000 + 100000
        → EmailHelper.sendOTP(email, otp) // Gửi email qua JavaMail
        → Hiện ô nhập OTP

User nhập OTP → Click "Đăng ký"
    ↓
RegisterActivity.attemptRegister()
    → Validate tất cả trường
    → Kiểm tra OTP nhập có khớp không (so sánh với generatedOtp)
    → authViewModel.registerWithEmail(email, password, fullName)
        ↓
FirebaseHelper.registerWithEmail()
    → auth.createUserWithEmailAndPassword(email, password)
    → Cập nhật displayName trong Firebase Auth
    → saveUserToFirestore(uid, fullName, email, ROLE_CUSTOMER, ...)
        ↓
    → callback.onSuccess(uid, ROLE_CUSTOMER)
        ↓
    → PetShopActivity (khách hàng mới)
```

---

## 12. CRUD FLOW VÀ TOÀN BỘ TÍNH NĂNG

### CRUD là gì?
- **C**reate = Tạo mới
- **R**ead = Đọc/Xem
- **U**pdate = Cập nhật
- **D**elete = Xóa

### CRUD Thú cưng (Admin):

```
[READ] ManagePetsActivity
    → PetManageViewModel.loadPets()
    → PetRepository.getAll()
    → Firestore: db.collection("pets").get()
    → Hiện danh sách trong RecyclerView (PetAdminAdapter)

[CREATE] AddEditPetActivity (mode = "add")
    → Admin nhập thông tin
    → Chọn ảnh từ thư viện → upload lên Firebase Storage
    → PetManageViewModel.addPet(pet)
    → PetRepository.add(pet)
    → Firestore: db.collection("pets").document(uuid).set(pet)

[UPDATE] AddEditPetActivity (mode = "edit", truyền petId)
    → Load thông tin pet hiện tại
    → Admin sửa thông tin
    → PetRepository.update(pet)
    → Firestore: db.collection("pets").document(petId).set(pet, MERGE)

[DELETE] ManagePetsActivity → click delete trên item
    → Hiện ConfirmDialog "Bạn có chắc muốn xóa?"
    → Xác nhận → PetRepository.delete(petId)
    → Firestore: db.collection("pets").document(petId).delete()
```

### CRUD Đơn hàng (Admin + Customer):

```
[CREATE] CheckoutActivity.placeOrder()
    → Tạo object Order với đầy đủ thông tin
    → OrderRepository.createOrder(order, cartItems)
    → Firestore Transaction:
        → Trừ stock đồ ăn
        → Đổi status pet → RESERVED
        → Lưu đơn hàng
    → Xóa giỏ hàng
    → Gửi notification

[READ - Customer] OrderHistoryActivity
    → OrderRepository.getOrdersByUser(userId)
    → Firestore: db.collection("orders").whereEqualTo("userId", uid)

[READ - Admin] AdminOrderListActivity
    → OrderRepository.getAllOrders()
    → Firestore: db.collection("orders").orderBy("createdAt")

[UPDATE - Admin] AdminOrderDetailActivity
    → Cập nhật trạng thái: PENDING → CONFIRMED → SHIPPING → DELIVERED
    → OrderRepository.updateStatus(orderId, newStatus)
    → Firestore Transaction:
        → Cập nhật status đơn hàng
        → Tính toán số liệu thống kê user (totalOrders, totalSpent)

[UPDATE - Customer] OrderDetailActivity
    → Huỷ đơn (nếu được phép): OrderRepository.cancelOrder()
    → Yêu cầu đổi trả: OrderRepository.requestReturn()

[DELETE - Admin] AdminOrderDetailActivity
    → OrderRepository.deleteOrder(orderId) (chỉ admin mới có)
```

### Toàn bộ tính năng của app:

**Phía Khách hàng:**
- Xem trang chủ (danh mục, sản phẩm nổi bật, banner)
- Tìm kiếm sản phẩm (có bình thường hóa tiếng Việt)
- Lọc theo danh mục
- Xem chi tiết thú cưng / đồ ăn
- Thêm vào giỏ hàng (có kiểm tra stock)
- Quản lý giỏ hàng (tăng/giảm số lượng, xóa)
- Thanh toán (COD hoặc VNPay)
- Áp dụng voucher / mã khuyến mãi
- Xem lịch sử đơn hàng
- Huỷ đơn hàng / yêu cầu đổi trả
- Mua lại đơn hàng cũ
- Chat với AI (GPT-4o-mini) có gửi ảnh
- Quản lý hồ sơ cá nhân
- Quản lý địa chỉ giao hàng (thêm/sửa/xóa/đặt mặc định)
- Xem thông báo
- Đăng nhập/đăng ký (Email, Google)
- Quên mật khẩu (gửi email reset)

**Phía Admin:**
- Dashboard thống kê (doanh thu, đơn hàng, người dùng)
- Quản lý thú cưng (CRUD + upload ảnh)
- Quản lý đồ ăn (CRUD + upload ảnh)
- Quản lý danh mục
- Quản lý người dùng (xem, khoá/mở khoá)
- Quản lý đơn hàng (xem, cập nhật trạng thái, xoá)
- Quản lý khuyến mãi (CRUD)
- Quản lý voucher (CRUD)
- Quản lý yêu cầu đổi trả

---

## 13. RECYCLERVIEW HOẠT ĐỘNG

### RecyclerView là gì?

Hãy tưởng tượng bạn cần hiển thị 1000 sản phẩm. Nếu tạo 1000 ô UI cùng lúc → điện thoại sẽ bị lag/hết RAM.

RecyclerView thông minh hơn: chỉ tạo **đúng số ô vừa hiển thị trên màn hình** (khoảng 5-7 ô), và khi người dùng scroll, nó **tái sử dụng (recycle)** các ô vừa biến mất để hiển thị dữ liệu mới.

```
Màn hình (hiển thị 5 item):
┌─────────────────┐
│   Item 1 - Mochi│  ← VH (ViewHolder) số 1
├─────────────────┤
│   Item 2 - Lulu │  ← VH số 2
├─────────────────┤
│   Item 3 - Koko │  ← VH số 3
├─────────────────┤
│   Item 4 - Max  │  ← VH số 4
└─────────────────┘

Người dùng scroll lên:
- VH số 1 (Mochi) biến mất khỏi màn hình
- RecyclerView lấy VH số 1, đổi dữ liệu thành Item 6, đưa xuống dưới
→ Chỉ cần ~5-7 ViewHolder cho 1000 item!
```

### Cách RecyclerView hoạt động trong project:

```java
// Trong HomeFragment.setupRecyclerViews()

// Bước 1: Tạo RecyclerView
RecyclerView rvPets = root.findViewById(R.id.rvFeaturedPets);

// Bước 2: Đặt LayoutManager (cách sắp xếp)
// LinearLayoutManager: danh sách thẳng hàng
// HORIZONTAL: cuộn ngang (như carousel)
rvPets.setLayoutManager(
    new LinearLayoutManager(requireContext(), LinearLayoutManager.HORIZONTAL, false)
);

// Bước 3: Tạo và gán Adapter
petAdapter = new HomePetAdapter(
    new ArrayList<>(),           // dữ liệu ban đầu (rỗng)
    this::openPetDetail,         // callback khi click item
    pet -> cartVm.addPet(pet)    // callback khi click "Thêm vào giỏ"
);
rvPets.setAdapter(petAdapter);

// Bước 4: Khi dữ liệu về → cập nhật
vm.getFeaturedPets().observe(getViewLifecycleOwner(), pets -> {
    petAdapter.updateList(pets); // Adapter tự reload
});
```

---

## 14. ADAPTER HOẠT ĐỘNG

### Adapter làm cầu nối giữa dữ liệu và RecyclerView

```java
// HomePetAdapter.java - Phân tích từng phần

public class HomePetAdapter extends RecyclerView.Adapter<HomePetAdapter.VH> {
    // VH = ViewHolder, chứa các View của một item
    
    private final List<Pet> list;      // Dữ liệu
    private final OnPetClick listener; // Callback khi click
    
    // ===== 3 hàm BẮT BUỘC phải override =====
    
    // 1. onCreateViewHolder() - Tạo ViewHolder (tạo ô UI)
    // Chỉ chạy ~5-7 lần (số ô trên màn hình)
    @Override
    public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // Inflate (phồng/tạo) layout XML thành View Java
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_pet_card, parent, false);
        // item_pet_card.xml = một ô thú cưng trong danh sách
        return new VH(v); // Bọc View vào ViewHolder
    }
    
    // 2. onBindViewHolder() - Gắn dữ liệu vào ViewHolder
    // Chạy mỗi khi item xuất hiện trên màn hình (kể cả tái sử dụng)
    @Override
    public void onBindViewHolder(@NonNull VH h, int pos) {
        Pet pet = list.get(pos); // Lấy dữ liệu tại vị trí pos
        
        h.tvPetName.setText("Pet: " + pet.getName());
        
        // Hiện giá
        double price = pet.getEffectivePrice();
        h.tvPrice.setText(VND.format((long)price) + "đ");
        
        // Hiện badge giảm giá nếu có
        if (pet.hasPromotion() && pet.getOriginalPrice() > pet.getEffectivePrice()) {
            int pct = (int)((1 - price/pet.getOriginalPrice()) * 100);
            h.tvSaleBadge.setText("-" + pct + "%"); // "-30%"
            h.tvSaleBadge.setVisibility(View.VISIBLE);
        } else {
            h.tvSaleBadge.setVisibility(View.GONE);
        }
        
        // Load ảnh
        Glide.with(h.itemView).load(pet.getThumbnailUrl()).into(h.ivPet);
        
        // Gán sự kiện click
        h.itemView.setOnClickListener(v -> listener.onClick(pet));
        h.ivAddToCart.setOnClickListener(v -> cartListener.onAddToCart(pet));
    }
    
    // 3. getItemCount() - Trả về số lượng item
    @Override
    public int getItemCount() { return list.size(); }
    
    // Cập nhật danh sách (trigger reload toàn bộ)
    public void updateList(List<Pet> newList) {
        list.clear();
        list.addAll(newList);
        notifyDataSetChanged(); // Báo cho RecyclerView biết dữ liệu đã thay đổi
    }
    
    // ===== ViewHolder - chứa reference đến các View =====
    static class VH extends RecyclerView.ViewHolder {
        ImageView ivPet, ivAddToCart;
        TextView tvPetName, tvPrice, tvSaleBadge;
        
        VH(View v) {
            super(v);
            // Tìm và giữ reference đến các View
            // (để không phải tìm lại mỗi lần bind)
            ivPet = v.findViewById(R.id.ivPetImage);
            tvPetName = v.findViewById(R.id.tvPetName);
            tvPrice = v.findViewById(R.id.tvPrice);
            tvSaleBadge = v.findViewById(R.id.tvSaleBadge);
        }
    }
}
```

### Tại sao dùng ViewHolder?

```java
// KHÔNG dùng ViewHolder (chậm):
public void onBindViewHolder(View view, int pos) {
    // Mỗi lần bind đều gọi findViewById() → tốn thời gian
    TextView tv = view.findViewById(R.id.tvPetName); // Chậm!
    tv.setText(list.get(pos).getName());
}

// DÙNG ViewHolder (nhanh):
// ViewHolder lưu reference một lần trong constructor
// Sau đó chỉ cần gọi h.tvPetName trực tiếp → nhanh hơn nhiều
```

---

## 15. VIEWBINDING HOẠT ĐỘNG

Project này **BẬT ViewBinding** trong `build.gradle.kts`:
```kotlin
buildFeatures {
    viewBinding = true
}
```

Tuy nhiên, nhìn vào code thực tế, phần lớn vẫn dùng `findViewById()` truyền thống, chỉ một số nơi dùng ViewBinding. Đây là điểm có thể cải thiện.

### ViewBinding là gì?

Thay vì viết:
```java
// Cách cũ - dễ bị lỗi khi sai ID
TextView tvName = findViewById(R.id.tvName);
```

ViewBinding tự động tạo class binding:
```java
// Trong Activity với ViewBinding:
ActivityLoginBinding binding = ActivityLoginBinding.inflate(getLayoutInflater());
setContentView(binding.getRoot());

// Truy cập view trực tiếp qua binding, kiểm tra lỗi lúc compile
binding.tvName.setText("Xin chào");
binding.btnLogin.setOnClickListener(v -> login());
```

**Ưu điểm:** Không thể sai ID (lỗi lúc compile, không phải lúc chạy), không cần ép kiểu.

---

## 16. VIEWMODEL VÀ REPOSITORY

### Tại sao cần ViewModel?

**Vấn đề:** Khi người dùng xoay điện thoại, Android sẽ:
1. Destroy Activity/Fragment
2. Tạo lại Activity/Fragment mới
→ Mất hết dữ liệu đang có!

**Giải pháp:** ViewModel tồn tại qua quá trình recreate:

```
Xoay màn hình:
┌─────────────────┐    ┌─────────────────┐
│  Activity       │    │  Activity MỚI   │
│  (sắp bị destroy)│   │  (vừa được tạo) │
└────────┬────────┘    └────────┬────────┘
         │                      │
         └──────── ViewModel ───┘
                  (VẪN CÒN SỐNG)
                  (dữ liệu không mất)
```

```java
// Trong HomeFragment:
// ViewModelProvider tìm ViewModel hiện có hoặc tạo mới
vm = new ViewModelProvider(requireActivity()).get(HomeViewModel.class);
//   ↑ requireActivity() = dùng scope của Activity
//   → Tất cả Fragment trong Activity dùng CÙNG một HomeViewModel
//   → HomeFragment và ProfileFragment có thể share dữ liệu

// Trong LoginActivity:
authViewModel = new ViewModelProvider(this).get(AuthViewModel.class);
//   ↑ this = chỉ Activity này dùng
```

### Tại sao cần Repository?

**Không có Repository (tệ):**
```java
// Trong ViewModel - phụ thuộc trực tiếp vào Firebase
// Nếu sau này đổi sang Retrofit/Room → phải sửa ViewModel
class HomeViewModel extends ViewModel {
    void loadPets() {
        FirebaseFirestore.getInstance()
            .collection("pets").get()
            .addOnSuccessListener(...);
    }
}
```

**Có Repository (tốt):**
```java
// ViewModel không biết nguồn dữ liệu là Firebase hay REST API hay Room
class HomeViewModel extends ViewModel {
    private final PetRepository petRepo = new PetRepository();
    
    void loadPets() {
        petRepo.getAll(new PetRepository.Callback<>() {
            void onSuccess(List<Pet> pets) { ... }
        });
    }
}

// Repository là lớp duy nhất biết Firebase
class PetRepository {
    void getAll(Callback<List<Pet>> cb) {
        // Chỉ có đây mới biết đây là Firestore
        FirebaseFirestore.getInstance()...
    }
}
```

---

## 17. ASYNC VÀ CALLBACK HOẠT ĐỘNG

### Tại sao cần Async?

Điện thoại có **Main Thread** (luồng chính) chạy UI. Nếu bạn làm thứ mất thời gian trên Main Thread:
```java
// SAI - Freezes UI!
Pet pet = firestore.collection("pets").document("id").get(); // Có thể mất 2-3 giây
tvName.setText(pet.getName()); // UI bị đơ trong 2-3 giây
```

Android sẽ báo lỗi "ANR - Application Not Responding".

**Giải pháp: Callback pattern**

```java
// ĐÚNG - Async, không block UI
petRepo.getById(petId, new PetRepository.Callback<Pet>() {
    @Override
    public void onSuccess(Pet pet) {
        // Hàm này chạy SAU KHI có kết quả (trên Main Thread)
        tvName.setText(pet.getName()); // UI cập nhật bình thường
    }
    @Override
    public void onFailure(String error) {
        Toast.makeText(context, error, Toast.LENGTH_SHORT).show();
    }
});
// Code tiếp tục chạy NGAY, không đợi Firebase trả về
```

### Firebase Tasks hoạt động:

```java
// Khi gọi Firebase, nó trả về Task (tác vụ bất đồng bộ)
db.collection("pets").get()    // Bắt đầu tác vụ, trả về Task
    .addOnSuccessListener(snap -> { // Callback khi thành công
        // Chạy trên Main Thread
    })
    .addOnFailureListener(e -> { // Callback khi thất bại
        // Chạy trên Main Thread
    });
// Dòng này chạy NGAY, không đợi Firebase
```

### Streaming trong ChatViewModel:

```java
// Khác với callback thông thường, streaming trả về từng phần
// Chạy trên OkHttp background thread
client.newCall(request).enqueue(new Callback() {
    @Override
    public void onResponse(Call call, Response response) throws IOException {
        StringBuilder fullText = new StringBuilder();
        
        // Đọc từng dòng từ response (server-sent events)
        okio.BufferedSource source = response.body().source();
        while (true) {
            String line = source.readUtf8Line(); // Đọc một dòng
            // Line có dạng: "data: {"choices":[{"delta":{"content":"Chào"}}]}"
            
            if (line.startsWith("data: ")) {
                // Parse JSON, lấy nội dung mới
                String newContent = parseChunk(line);
                fullText.append(newContent);
                
                // Cập nhật UI với text đang tăng dần
                // postValue chạy callback trên Main Thread
                messages.postValue(updatedList);
            }
        }
    }
});
```

---

## 18. LIFECYCLE ANDROID ẢNH HƯỞNG GÌ

### Vòng đời Activity:

```
onCreate()    ← Tạo layout, khởi tạo ViewModel, ánh xạ View
onStart()     ← Activity hiện ra
onResume()    ← Người dùng đang tương tác (focus)
onPause()     ← Mất focus (popup xuất hiện, chuyển app khác)
onStop()      ← Activity khuất (chuyển màn hình)
onRestart()   ← Quay lại sau khi stop
onDestroy()   ← Activity bị huỷ hoàn toàn
```

### Vòng đời Fragment:

```
onAttach()       ← Fragment gắn vào Activity
onCreate()
onCreateView()   ← Tạo layout cho Fragment
onViewCreated()  ← Sau khi View đã sẵn sàng (bắt đầu code UI ở đây)
onStart()
onResume()       ← HomeFragment.onResume() gọi updateTopBar()
onPause()
onStop()         ← HomeFragment.onStop() xóa Firestore listener
onDestroyView()  ← View bị huỷ (nhưng Fragment vẫn tồn tại)
onDetach()       ← Fragment tách khỏi Activity
```

### Ảnh hưởng thực tế trong project:

```java
// HomeFragment.java
@Override
public void onResume() {
    super.onResume();
    updateTopBar(); // Cập nhật tên người dùng khi quay lại tab
    // Ví dụ: User vừa đăng nhập ở tab khác, quay lại Home → hiện tên
}

@Override
public void onStop() {
    super.onStop();
    // XÓA Firestore real-time listener khi không dùng nữa
    // Nếu không xóa → tiếp tục nhận data → tốn pin/băng thông/crash
    if (unreadNotifListener != null) {
        unreadNotifListener.remove();
        unreadNotifListener = null;
    }
}

// CartViewModel.java
@Override
protected void onCleared() {
    super.onCleared();
    // Gọi khi ViewModel bị huỷ (Activity bị destroy hẳn, không phải xoay màn hình)
    if (cartListener != null) {
        cartListener.remove(); // Xóa Firestore listener
    }
}
```

### LiveData và Lifecycle:

```java
// observe() với getViewLifecycleOwner() (trong Fragment)
vm.getFeaturedPets().observe(getViewLifecycleOwner(), pets -> {
    petAdapter.updateList(pets);
});
// getViewLifecycleOwner() = tự động dừng observe khi Fragment không hiện
// → Không bị crash khi Fragment đã bị destroy mà vẫn có callback
```

---

## 19. KIẾN TRÚC MVVM CHI TIẾT

### So sánh các kiến trúc:

| Kiến trúc | Ai xử lý logic? | Ưu điểm | Nhược điểm |
|-----------|-----------------|---------|------------|
| MVC | Controller (Activity) | Đơn giản | Activity quá to, khó test |
| MVP | Presenter | Test được | Nhiều interface, code nhiều |
| **MVVM** | **ViewModel** | **Test dễ, tách biệt tốt** | **Cần hiểu LiveData** |
| Clean Arch | UseCase + Presenter | Rất linh hoạt | Phức tạp, nhiều file |

### Project này dùng MVVM "đơn giản hóa":

```
Thuần MVVM:
View → ViewModel ← Model
       (LiveData)

Project này:
View → ViewModel → Repository → Firebase
       (LiveData)     (Callback)
```

**Không có Use Case layer** (Clean Architecture thêm Use Case ở giữa ViewModel và Repository). Project này bỏ qua lớp đó cho đơn giản.

### Tại sao MVVM tốt?

```java
// Test ViewModel mà không cần chạy app:
class HomeViewModelTest {
    @Test
    void testSearch() {
        HomeViewModel vm = new HomeViewModel();
        vm.loadHomeData(); // Cần mock Repository
        vm.search("mèo");
        // Kiểm tra filteredPets chỉ chứa mèo
        assertEquals(filteredPets.getValue().stream()
            .allMatch(p -> p.getSpecies().equals("CAT")), true);
    }
}
// Activity/Fragment không thể test tương tự vì phụ thuộc Android framework
```

---

## 20. VAI TRÒ TỪNG THÀNH PHẦN

### Activity
**Là gì:** Một màn hình độc lập, có vòng đời riêng.

**Trong project:**
- Nhận Intent từ màn hình khác
- Khởi tạo ViewModel
- Thiết lập RecyclerView và Adapter
- Lắng nghe LiveData từ ViewModel
- Xử lý tương tác người dùng (click, input)
- Chuyển sang màn hình khác bằng Intent

**Ví dụ:** `LoginActivity` → Xử lý form đăng nhập, quan sát `AuthViewModel`

### Fragment
**Là gì:** Một "mảnh" giao diện, sống bên trong Activity.

**Trong project:** Chỉ có 2 Fragment:
- `HomeFragment` → Tab trang chủ trong `PetShopActivity`
- `ProfileFragment` → Tab hồ sơ trong `PetShopActivity`

**Lý do dùng Fragment ở đây:** Để khi đổi tab, trạng thái (scroll position, dữ liệu đã load) không bị mất. Activity dùng hide/show Fragment thay vì replace.

### Adapter
**Là gì:** Cầu nối giữa dữ liệu và RecyclerView.

**Trong project:** 16 Adapter, mỗi loại danh sách có 1 Adapter riêng:
- `HomePetAdapter` → Danh sách thú cưng ở Home (horizontal scroll)
- `CartItemAdapter` → Danh sách item trong giỏ hàng
- `ChatAdapter` → Danh sách tin nhắn chat
- `ProductAdapter` → Danh sách sản phẩm ở ProductListActivity
- ...

### ViewModel
**Là gì:** Lớp giữ dữ liệu và logic xử lý, sống qua xoay màn hình.

**Trong project:** Mỗi màn hình/tính năng có 1 ViewModel:
- `AuthViewModel` → Dùng ở LoginActivity, RegisterActivity
- `HomeViewModel` → Dùng ở HomeFragment
- `CartViewModel` → Dùng ở HomeFragment, CartActivity, CheckoutActivity
- `ChatViewModel` → Dùng ở ChatActivity

**Lưu ý quan trọng:** `CartViewModel` được tạo với scope `requireActivity()` trong Fragment → HomeFragment và PetShopActivity share cùng 1 CartViewModel → Cart badge cập nhật đồng bộ

### Repository
**Là gì:** Lớp truy cập dữ liệu, trừu tượng hoá nguồn dữ liệu (Firestore).

**Trong project:** 11 Repository, mỗi loại entity có 1 Repository.

**Quy tắc:** Repository không giữ state. Mỗi lần gọi hàm là một lần query Firestore độc lập.

### API Service
Project này **không dùng Retrofit hay REST API** cho dữ liệu chính. Firebase Firestore là "database" trực tiếp.

Ngoại lệ: `ChatViewModel` dùng OkHttp để gọi **OpenAI API** (`api.openai.com/v1/chat/completions`).

### Database
**Firebase Firestore** là NoSQL cloud database:
- Không có schema cứng
- Document-based (giống JSON)
- Real-time sync (tự cập nhật khi có thay đổi)
- Offline support (cache data)
- Transaction support (đảm bảo tính toàn vẹn)

---

## 21. TẠI SAO PHẢI TÁCH NHIỀU LỚP NHƯ VẬY

### Ví dụ không tách lớp (Anti-pattern):

```java
// ALL-IN-ONE Activity (cách người mới thường làm)
public class HomeActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Trực tiếp query Firebase trong Activity
        FirebaseFirestore.getInstance()
            .collection("pets").get()
            .addOnSuccessListener(snap -> {
                List<Pet> pets = new ArrayList<>();
                for (DocumentSnapshot doc : snap.getDocuments()) {
                    pets.add(doc.toObject(Pet.class));
                }
                // Trực tiếp cập nhật UI
                adapter.updateList(pets);
            });
    }
    
    // + Tất cả logic xử lý
    // + Tất cả code UI
    // → Activity có thể lên tới 2000 dòng code!
}
```

**Vấn đề của cách này:**
1. **Không test được:** Activity phụ thuộc Android framework
2. **Khó bảo trì:** 2000 dòng code, muốn tìm bug rất khó
3. **Xoay màn hình mất data:** Activity bị recreate → mất list đã load
4. **Không tái sử dụng:** Nếu Fragment khác cũng cần list pets → phải copy code

### Với MVVM:

```
Activity (100 dòng)     → Chỉ UI + navigation
ViewModel (150 dòng)    → Logic xử lý
Repository (100 dòng)   → Truy cập data
Model (50 dòng)         → Cấu trúc data
```

Mỗi lớp có một trách nhiệm duy nhất (Single Responsibility Principle).

---

## 22. DEPENDENCY GIỮA CÁC MODULE

### Sơ đồ dependency (ai phụ thuộc vào ai):

```
View (Activity/Fragment)
    │ dùng
    ↓
ViewModel
    │ dùng
    ↓
Repository
    │ dùng
    ↓
Firebase SDK / OkHttp / Gson
    
Model (Entity classes)
    ↑ tất cả đều dùng
```

### Nguyên tắc quan trọng: "Dependency đi một chiều"

- View biết ViewModel nhưng ViewModel KHÔNG biết View
- ViewModel biết Repository nhưng Repository KHÔNG biết ViewModel
- Repository biết Model nhưng Model KHÔNG biết Repository

```java
// ĐÚNG - ViewModel không biết Activity nào đang dùng nó
class HomeViewModel extends ViewModel {
    void loadPets() {
        petRepo.getAll(new Callback<>() {
            void onSuccess(List<Pet> pets) {
                filteredPets.postValue(pets); // Cập nhật LiveData
                // Không biết ai đang observe
            }
        });
    }
}

// SAI - ViewModel biết Activity → Coupling!
class HomeViewModelBAD extends ViewModel {
    HomeActivity activity; // ❌ Không bao giờ làm thế này!
    void loadPets() {
        petRepo.getAll(new Callback<>() {
            void onSuccess(List<Pet> pets) {
                activity.showPets(pets); // ❌ Memory leak nguy hiểm!
            }
        });
    }
}
```

### Thư viện bên ngoài được dùng:

```
Firebase BOM (32.7.4)
├── firebase-auth      → Xác thực
├── firebase-firestore → Database
└── firebase-storage   → Lưu file

Google Play Services
└── play-services-auth → Google Sign-In

UI Libraries
├── material (1.12.0)  → Material Design components
├── glide (4.16.0)     → Load ảnh
├── circleimageview    → Ảnh tròn (avatar)
├── cardview           → Card layout
└── viewpager2         → Swipe giữa các trang

Network
├── okhttp (4.12.0)    → HTTP client (dùng cho OpenAI)
└── gson (2.10.1)      → Parse JSON

Email
└── android-mail       → Gửi email OTP (JavaMail)

Lifecycle (MVVM)
├── lifecycle-viewmodel → ViewModel base class
└── lifecycle-livedata  → LiveData
```

---

## 23. CÂU HỎI GIÁO VIÊN CÓ THỂ HỎI

### Câu hỏi về Kiến trúc:

1. **"Project dùng kiến trúc gì? Tại sao chọn kiến trúc đó?"**
2. **"MVVM khác MVC ở điểm nào?"**
3. **"ViewModel giải quyết vấn đề gì?"**
4. **"Tại sao Repository tách biệt khỏi ViewModel?"**
5. **"LiveData là gì? Tại sao dùng thay vì Callback thông thường?"**

### Câu hỏi về Firebase:

6. **"Firebase Firestore khác Firebase Realtime Database như thế nào?"**
7. **"Transaction trong Firestore dùng để làm gì? Khi nào cần dùng?"**
8. **"Tại sao phải đọc hết, rồi mới ghi trong Transaction?"**
9. **"Khi nào dùng addSnapshotListener() thay vì get()?"**
10. **"Firebase Authentication lưu gì? Firestore lưu gì thêm?"**

### Câu hỏi về Code:

11. **"RecyclerView.ViewHolder giải quyết vấn đề gì?"**
12. **"Tại sao Adapter cần implement 3 hàm bắt buộc?"**
13. **"Intent là gì? Sự khác biệt startActivity() và startActivityForResult()?"**
14. **"Fragment khác Activity như thế nào? Khi nào dùng Fragment?"**
15. **"Tại sao không nên giữ reference đến Activity trong ViewModel?"**

### Câu hỏi về Tính năng:

16. **"Khi thêm thú cưng vào giỏ, code làm gì để đảm bảo không bị mua trùng?"**
17. **"Giải thích flow thanh toán VNPay từ đầu đến cuối"**
18. **"Chat AI hoạt động thế nào? Streaming là gì?"**
19. **"Khi hủy đơn hàng, code cần làm gì để rollback dữ liệu?"**
20. **"OTP được tạo và xác thực như thế nào?"**

### Câu hỏi về Lifecycle:

21. **"Vòng đời Activity gồm những giai đoạn nào?"**
22. **"onResume() và onStart() khác nhau thế nào?"**
23. **"Khi xoay màn hình, điều gì xảy ra với Activity? Với ViewModel?"**
24. **"Tại sao phải remove Firestore listener trong onStop()?"**

---

## 24. CÂU TRẢ LỜI MẪU

### Q1: "Project dùng kiến trúc gì?"

> "Project dùng kiến trúc MVVM (Model-View-ViewModel). Cụ thể:
> - **Model** gồm các class entity trong `model/entity/` như `Pet.java`, `Order.java`, và các Repository trong `repository/` giao tiếp với Firebase Firestore.
> - **ViewModel** trong package `viewmodel/` chứa toàn bộ business logic. Ví dụ `HomeViewModel` xử lý việc tải dữ liệu, tìm kiếm, lọc theo danh mục, và expose kết quả qua `MutableLiveData`.
> - **View** là các Activity và Fragment trong `view/` chỉ chịu trách nhiệm hiển thị UI và gửi user action đến ViewModel.
> 
> Tôi chọn MVVM vì nó giải quyết vấn đề mất dữ liệu khi xoay màn hình (ViewModel tồn tại qua configuration change), và tách biệt rõ ràng giữa UI và logic giúp code dễ bảo trì hơn."

### Q2: "Transaction Firestore dùng để làm gì?"

> "Transaction trong Firestore đảm bảo tính nguyên tử (atomicity) - tức là tất cả các thao tác trong transaction phải thành công cùng lúc, hoặc không cái nào được thực hiện.
>
> Trong project, tôi dùng Transaction ở hai nơi quan trọng:
> 1. **Khi thêm thú cưng vào giỏ** (`CartRepository.addPetToCart()`): Cần đọc trạng thái pet, kiểm tra còn AVAILABLE không, sau đó đổi thành RESERVED và cập nhật giỏ hàng - tất cả trong một transaction. Nếu không dùng transaction, có thể xảy ra race condition: 2 người cùng mua 1 con mèo cùng lúc, cả 2 đều thấy AVAILABLE và đều thêm vào giỏ.
> 2. **Khi tạo đơn hàng** (`OrderRepository.createOrder()`): Phải đồng thời trừ stock đồ ăn, cập nhật trạng thái pet, và lưu đơn hàng. Nếu app crash giữa chừng, Firestore tự rollback, không xảy ra tình trạng stock bị trừ nhưng đơn hàng không được tạo."

### Q3: "Giải thích RecyclerView và Adapter"

> "RecyclerView là một widget hiển thị danh sách hiệu quả. Thay vì tạo View cho tất cả item (có thể là 1000 item), nó chỉ tạo đủ số View vừa hiện trên màn hình (khoảng 5-7 item). Khi người dùng scroll, các View cũ bị 'tái sử dụng' (recycle) để hiển thị dữ liệu mới - đây là ý nghĩa của tên 'Recycler'.
>
> Adapter là cầu nối giữa dữ liệu và RecyclerView. Adapter cần implement 3 hàm:
> - `onCreateViewHolder()`: Tạo một ViewHolder mới (inflate layout XML)
> - `onBindViewHolder()`: Gắn dữ liệu tại position vào ViewHolder
> - `getItemCount()`: Trả về tổng số item
>
> ViewHolder giữ reference đến các View trong một item để tránh gọi `findViewById()` mỗi lần bind - điều này tăng hiệu suất đáng kể vì `findViewById()` duyệt cây View để tìm."

### Q4: "ViewModel giải quyết vấn đề gì?"

> "ViewModel giải quyết hai vấn đề chính:
> 1. **Mất dữ liệu khi xoay màn hình**: Khi người dùng xoay điện thoại, Android destroy và recreate Activity. Nếu chứa dữ liệu trong Activity, ta phải tải lại từ đầu. ViewModel được Android giữ trong memory qua quá trình này, nên dữ liệu không mất.
> 2. **Separation of concerns (tách mối quan tâm)**: ViewModel không được import Context, Activity, hay Fragment. Điều này buộc developer tách business logic ra khỏi UI logic, code dễ test và bảo trì hơn.
>
> Trong project, ví dụ `HomeViewModel` giữ list `allPets` và `allFoods`. Khi xoay màn hình, HomeFragment được recreate nhưng nó lấy lại cùng một `HomeViewModel` đã có dữ liệu → không phải query Firestore lại."

### Q5: "Giải thích Login flow"

> "Login flow có 3 bước chính:
> 1. **Xác thực**: `LoginActivity` gọi `authViewModel.loginWithEmail(email, password)`. ViewModel gọi `FirebaseHelper.loginWithEmail()`, Firebase Auth kiểm tra credentials trên server và trả về UID.
> 2. **Lấy role**: Dùng UID vừa có, query Firestore để lấy field 'role' (ADMIN hoặc CUSTOMER). Logic này nằm trong `getUserRole()`.
> 3. **Lưu session và điều hướng**: `AuthViewModel.loadUserDataAndSaveSession()` lấy đầy đủ thông tin user, lưu vào `SharedPreferences` thông qua `SessionManager`, sau đó `userRole.postValue(role)`. `LoginActivity` đang observe `userRole`, nhận được giá trị này và gọi `navigateByRole()` để chuyển sang `AdminActivity` hoặc `PetShopActivity`.
>
> Tôi dùng MVVM ở đây để đảm bảo nếu có lỗi mạng giữa chừng (ví dụ query Firestore thất bại), `errorMessage.postValue()` sẽ thông báo cho Activity hiện thông báo lỗi mà không cần truyền reference Activity vào."

---

## 25. TÓM TẮT VÀ FILE QUAN TRỌNG NHẤT

### Tóm tắt toàn bộ flow app:

```
1. APP MỞ
   SplashActivity → kiểm tra Firebase Auth → điều hướng theo role

2. TRANG CHỦ (Customer)
   PetShopActivity (container) → HomeFragment (tab chính)
   HomeViewModel load data từ Firestore → LiveData → Adapter → RecyclerView hiện UI

3. XEM SẢN PHẨM
   Tap item → PetDetailActivity/FoodDetailActivity → load thêm chi tiết từ Firestore

4. GIỎ HÀNG
   Tap "Thêm vào giỏ" → CartViewModel.addPet/addFood()
   CartRepository.addPetToCart() → Firestore Transaction (RESERVED + thêm vào giỏ)
   CartActivity → CartItemAdapter hiện danh sách

5. THANH TOÁN
   CheckoutActivity → chọn địa chỉ + voucher + phương thức
   Tap "Đặt hàng" → OrderRepository.createOrder() → Firestore Transaction
   COD → OrderDetailActivity
   VNPay → VNPayHelper tạo URL → WebView → VNPayResultActivity → cập nhật order

6. CHAT AI
   ChatActivity → ChatViewModel → build context từ Firestore data
   OkHttp POST đến OpenAI API → streaming response → cập nhật UI từng từ

7. ADMIN
   AdminActivity → Dashboard thống kê
   Manage* Activities → CRUD với Firestore
```

### File quan trọng nhất (nên đọc theo thứ tự này):

**Bước 1: Hiểu cấu trúc cơ bản**
1. `AndroidManifest.xml` → Danh sách Activity, permissions
2. `app/build.gradle.kts` → Dependencies, cấu hình
3. `utils/Constants.java` → Các hằng số quan trọng

**Bước 2: Hiểu Authentication**
4. `utils/SessionManager.java` → Lưu session
5. `utils/FirebaseHelper.java` → Giao tiếp Firebase Auth
6. `viewmodel/AuthViewModel.java` → Logic đăng nhập
7. `view/activity/SplashActivity.java` → Điểm vào
8. `view/activity/LoginActivity.java` → UI đăng nhập

**Bước 3: Hiểu MVVM pattern**
9. `model/entity/Pet.java` → Ví dụ entity
10. `repository/PetRepository.java` → Ví dụ Repository
11. `viewmodel/HomeViewModel.java` → Ví dụ ViewModel
12. `view/fragment/HomeFragment.java` → Ví dụ Fragment/View

**Bước 4: Hiểu tính năng phức tạp**
13. `repository/CartRepository.java` → Transaction Firestore
14. `repository/OrderRepository.java` → Tạo đơn hàng phức tạp
15. `view/activity/CheckoutActivity.java` → Checkout flow
16. `viewmodel/ChatViewModel.java` → OpenAI streaming

**Bước 5: Hiểu RecyclerView**
17. `view/adapter/HomePetAdapter.java` → Adapter đơn giản nhất
18. `view/adapter/CartItemAdapter.java` → Adapter có interaction

### Những phần cần học trước để hiểu project nhanh nhất:

1. **Java cơ bản** - Class, interface, anonymous class, lambda
2. **Android Activity Lifecycle** - onCreate, onResume, onStop
3. **Intent** - Cách chuyển màn hình, truyền dữ liệu
4. **RecyclerView + Adapter** - Cách hiển thị danh sách
5. **LiveData + Observer** - Cốt lõi của MVVM
6. **Callback Pattern** - Xử lý bất đồng bộ
7. **Firebase Firestore** - Collection, Document, Query
8. **Firebase Auth** - signIn, createUser, getCurrentUser

---

## PHỤ LỤC: SƠ ĐỒ FIRESTORE DATA MODEL

```
Firestore Collections:

users/{uid}
├── id, fullName, email, phone
├── role: "ADMIN" | "CUSTOMER"
├── loginType: "EMAIL" | "GOOGLE"
├── status: "ACTIVE" | "BANNED"
├── avatarUrl, totalOrders, totalSpent
└── chats/{chatId}, sessions/{sessionId}  ← subcollections

pets/{petId}
├── name, species, breed, age, gender
├── price, discountedPrice, promotionId
├── status: "AVAILABLE" | "SOLD" | "RESERVED"
└── pet_media/{mediaId}  ← subcollection

foods/{foodId}
├── name, brand, foodType, targetPetType
├── price, stock, sold
└── status: "AVAILABLE" | "OUT_OF_STOCK"

carts/{userId}  ← userId làm document ID
└── items: [{productType, productId, quantity, unitPrice}]

orders/{orderId}
├── userId, status, paymentMethod, paymentStatus
├── subtotal, shippingFee, voucherDiscount, totalAmount
├── shippingAddress, receiverName, receiverPhone
└── items: [{productType, productId, quantity, unitPrice}]

categories/{categoryId}
├── name, type: "PET" | "FOOD"
└── isActive

promotions/{promoId}
├── name, discountType, discountValue
├── isVoucher, voucherCode
└── startDate, endDate, usageLimit, usageCount

vouchers/{voucherId}
├── code, discountType, discountValue
├── minOrderAmount, usageLimit, usageCount
└── startDate, endDate, isActive

notifications/{notifId}
├── userId, title, message, type
└── isRead, createdAt
```

---

*Tài liệu được tạo tự động bằng cách phân tích toàn bộ source code của project PetShop Android.*
*Ngày tạo: 2026-05-11*
