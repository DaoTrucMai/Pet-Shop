# 📚 PETSHOP — Tài liệu giải thích chi tiết cho sinh viên

> Tài liệu này tổng hợp 2 phần giải thích:
> - **Phần A:** Giải thích tổng quan toàn bộ project (cấu trúc, kiến trúc, MVVM, flow, RecyclerView, ViewModel, Lifecycle…).
> - **Phần B:** Đi sâu vào 5 chủ đề trọng tâm: Cấu trúc dự án, Firebase, Auth (Email/Google), Facebook (KHÔNG có trong project), Address, Notification.
>
> Mục tiêu: dạy như mentor dạy sinh viên năm 2 vừa học Android — hiểu kiến trúc, hiểu code, đủ kiến thức để **bảo vệ đồ án**.

---

# PHẦN A — GIẢI THÍCH TỔNG QUAN TOÀN BỘ PROJECT

## 📖 Mục lục Phần A

1. Bức tranh tổng quan — App này làm gì?
2. Kiến trúc tổng thể (MVVM + Repository)
3. Cấu trúc thư mục & vai trò từng package
4. Các khái niệm Android nền tảng (Activity, Fragment, ViewModel, Adapter…)
5. Flow chạy của app từ lúc bấm vào icon
6. Login flow chi tiết
7. Data flow (Firestore → Repository → ViewModel → UI)
8. RecyclerView + Adapter hoạt động như thế nào
9. CRUD đầy đủ trong project
10. Cart + Checkout + Thanh toán VNPay
11. Lifecycle Android & ảnh hưởng đến ViewModel/Listener
12. Async / Thread / Callback (project KHÔNG dùng coroutine)
13. Liệt kê chi tiết từng class quan trọng
14. Câu hỏi giáo viên hay hỏi + Câu trả lời mẫu
15. Tóm tắt — Học gì trước, file quan trọng nhất

---

## 1. 🐾 Bức tranh tổng quan — App này làm gì?

Đây là app **Petshop** — cửa hàng bán thú cưng & đồ ăn cho thú cưng. App có **2 vai trò người dùng**:

| Vai trò | Tính năng |
|---|---|
| **CUSTOMER** (khách) | Xem thú cưng/đồ ăn, tìm kiếm, lọc theo danh mục, thêm vào giỏ, đặt hàng (COD/VNPay), xem đơn, yêu cầu hoàn trả, chat AI, quản lý địa chỉ, nhận thông báo, áp voucher/khuyến mãi |
| **ADMIN** | Dashboard thống kê, quản lý user, danh mục, thú cưng, đồ ăn, đơn hàng, hoàn trả, khuyến mãi, voucher |

Backend: **Firebase** (Authentication + Firestore database + Storage). Ngoài ra còn tích hợp:
- **Google Sign-In** (đăng nhập bằng Google)
- **VNPay sandbox** (thanh toán online)
- **OpenAI API** (chatbot AI tư vấn pet)
- **Glide** (load ảnh từ URL)

---

## 2. 🏛 Kiến trúc tổng thể — Project đang dùng kiến trúc gì?

**Câu trả lời chính xác: MVVM + Repository pattern (biến thể của Clean Architecture rút gọn).**

> ⚠️ Đây là câu giáo viên RẤT hay hỏi. Bạn phải thuộc câu trả lời này.

Mô hình MVVM gồm 3 tầng chính:

```
┌───────────────────────────────────────────────────────────────┐
│  VIEW   (Activity / Fragment / Adapter)                       │
│  - Hiển thị UI, nhận sự kiện click                            │
│  - KHÔNG biết về Firestore                                    │
└──────────────────────┬────────────────────────────────────────┘
                       │  observe(LiveData) / gọi hàm
                       ▼
┌───────────────────────────────────────────────────────────────┐
│  VIEWMODEL  (HomeViewModel, CartViewModel, AuthViewModel…)    │
│  - Giữ trạng thái UI (LiveData)                               │
│  - Logic nghiệp vụ "view"                                     │
│  - Sống sót khi xoay màn hình                                 │
└──────────────────────┬────────────────────────────────────────┘
                       │  gọi
                       ▼
┌───────────────────────────────────────────────────────────────┐
│  REPOSITORY  (PetRepository, CartRepository, OrderRepository…)│
│  - "Cánh cửa" duy nhất đi đến dữ liệu                         │
│  - Gọi Firebase Firestore / Storage                           │
│  - Trả kết quả qua Callback interface                         │
└──────────────────────┬────────────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────────────┐
│  DATA SOURCE  (Firebase Firestore / Storage / Auth)           │
└───────────────────────────────────────────────────────────────┘
```

**Vì sao phải tách nhiều lớp như vậy? (Câu giáo viên RẤT hay hỏi):**

1. **Tách trách nhiệm (Separation of Concerns)** — mỗi class chỉ làm 1 việc → dễ đọc, dễ sửa.
2. **Test được** — Repository có thể mock để test ViewModel không cần Firebase thật.
3. **Tái sử dụng** — `PetRepository.getAll()` dùng được ở HomeFragment, ProductListActivity, ManagePetsActivity…
4. **Lifecycle-safe** — ViewModel sống sót khi xoay màn hình; LiveData tự động hủy observer khi Activity bị destroy → không leak.
5. **Đổi backend dễ** — nếu mai mốt đổi Firestore sang REST API, chỉ cần sửa Repository, ViewModel và View **không thay đổi**.

---

## 3. 📂 Cấu trúc thư mục & vai trò từng package

```
com.example.petshop/
├── MainActivity.java            ← cửa redirect sang Splash (gần như rỗng)
│
├── model/                       ← LỚP MODEL — chỉ chứa dữ liệu
│   ├── entity/                  ← Các "đối tượng" trong app
│   │   ├── User.java, Pet.java, Food.java, Cart.java, CartItem.java
│   │   ├── Order.java, OrderItem.java, Category.java
│   │   ├── Address.java, Voucher.java, Promotion.java
│   │   ├── Notification.java, Review.java, ChatMessage.java …
│   ├── request/                 ← Object dùng để gửi đi (LoginRequest…)
│   └── response/                ← Object trả về từ server
│
├── repository/                  ← LỚP TRUY CẬP DỮ LIỆU
│   ├── PetRepository.java       ← CRUD pet trên Firestore
│   ├── FoodRepository.java      ← CRUD food
│   ├── CartRepository.java      ← CRUD giỏ hàng (có dùng Transaction)
│   ├── OrderRepository.java     ← Tạo đơn, cập nhật trạng thái
│   ├── CategoryRepository.java, UserRepository.java,
│   │   PromotionRepository.java, VoucherRepository.java,
│   │   AddressRepository.java, NotificationRepository.java,
│   │   ReturnRepository.java
│
├── viewmodel/                   ← LỚP TRUNG GIAN GIỮ STATE UI
│   ├── AuthViewModel, HomeViewModel, CartViewModel
│   ├── OrderViewModel, ProfileViewModel, AdminViewModel
│   ├── ChatViewModel, ProductViewModel
│   ├── PetManageViewModel, FoodManageViewModel,
│   │   CategoryManageViewModel, PromotionManageViewModel,
│   │   VoucherManageViewModel, UserManageViewModel
│
├── view/
│   ├── activity/                ← 34 màn hình
│   │   ├── SplashActivity, LoginActivity, RegisterActivity
│   │   ├── PetShopActivity (chứa Fragment), AdminActivity
│   │   ├── CartActivity, CheckoutActivity, OrderHistoryActivity…
│   │   └── …
│   ├── fragment/                ← Tab bên trong PetShopActivity
│   │   ├── HomeFragment, ProfileFragment, CartFragment, OrderFragment,
│   │   │   CategoryFragment, ProductDetailFragment
│   ├── adapter/                 ← Đổ dữ liệu vào RecyclerView
│   │   ├── HomePetAdapter, HomeFoodAdapter, CartItemAdapter,
│   │   │   OrderAdapter, ChatAdapter, NotificationAdapter,
│   │   │   PetAdminAdapter, FoodAdminAdapter, UserAdminAdapter …
│   └── dialog/                  ← Dialog tái sử dụng
│       ├── ConfirmDialog, LoadingDialog, DialogUtils
│
└── utils/                       ← Các "công cụ" dùng chung
    ├── FirebaseHelper           ← bọc FirebaseAuth + Firestore user
    ├── SessionManager           ← lưu thông tin user qua SharedPreferences
    ├── Constants                ← hằng số toàn app (đọc BuildConfig)
    ├── VNPayHelper              ← tạo URL thanh toán + verify SHA512
    ├── StorageHelper            ← upload ảnh lên Firebase Storage
    ├── PromotionManager         ← áp giảm giá vào danh sách pet/food
    ├── ShippingHelper           ← tính phí ship + ETA
    ├── EmailHelper, CartBadgeManager, AdminSetupHelper
```

**Lưu ý:** Một số file `AuthRepository.java`, `ProductRepository.java`, `NetworkUtils.java`, `SharedPrefManager.java` **đang rỗng (0 dòng)** — là code "dự định viết nhưng chưa làm". Bạn nên biết để khỏi tìm vô ích.

---

## 4. 🧱 Khái niệm Android nền tảng — Vai trò từng "loại class"

### 4.1 Activity — "Một màn hình"
Một Activity = 1 màn hình toàn màn hình. Vd `LoginActivity` = màn hình login. App có 34 Activity.

Lifecycle Activity (giáo viên hay hỏi):
```
onCreate()  → khởi tạo, gọi setContentView() để gắn layout XML
onStart()   → activity bắt đầu hiển thị
onResume()  → user đang tương tác
onPause()   → user chuyển sang activity khác (vẫn nhìn thấy 1 phần)
onStop()    → bị che hoàn toàn
onDestroy() → bị hủy
```

Ví dụ trong `AdminActivity.java`:
```java
@Override
protected void onStart() {
    super.onStart();
    // Bắt đầu lắng nghe real-time updates
    if (viewModel != null) {
        viewModel.startListening();
    }
}

@Override
protected void onStop() {
    super.onStop();
    // Dừng lắng nghe để tránh memory leak
    if (viewModel != null) {
        viewModel.stopListening();
    }
}
```
→ Mở listener khi `onStart`, tắt khi `onStop` để **tránh rò bộ nhớ (memory leak)**.

### 4.2 Fragment — "Mảnh ghép màn hình"
Fragment giống Activity con. Trong project này, `PetShopActivity` là **container** chứa 2 Fragment (`HomeFragment`, `ProfileFragment`) để hiển thị theo tab dưới (BottomNavigation).

Ưu điểm: chuyển tab **không tạo Activity mới** → mượt, không reload data.

### 4.3 ViewModel — "Bộ não của UI"
- Sống sót qua **xoay màn hình** (configuration change). Activity bị recreate, ViewModel KHÔNG.
- Chứa `LiveData<T>` — một "ống dẫn" data: Activity đăng ký nghe, ViewModel postValue → Activity tự động cập nhật UI.
- Lấy bằng: `new ViewModelProvider(this).get(HomeViewModel.class);`

### 4.4 Repository — "Cánh cửa data"
Là class trung gian giữa ViewModel và Firebase. Mỗi entity có 1 Repository. Tất cả Repository trong project đều có pattern:

```java
public interface Callback<T> {
    void onSuccess(T data);
    void onFailure(String error);
}
```
→ Vì Firebase trả kết quả **bất đồng bộ** (async), ta không return thẳng được, phải dùng callback.

### 4.5 Adapter — "Người dịch dữ liệu sang ô RecyclerView"
RecyclerView không biết cách hiển thị Pet/Food. Adapter sẽ:
1. Tạo "ô" (ViewHolder) khi cần (`onCreateViewHolder`)
2. Đổ dữ liệu vào ô đó (`onBindViewHolder`)
3. Trả về số lượng item (`getItemCount`)

### 4.6 LiveData — "Loa thông báo có data mới"
- `MutableLiveData<T>` — ghi được (dùng trong ViewModel)
- `LiveData<T>` — chỉ đọc (View đăng ký nghe)
- Tự động "nghe" khi Activity ở foreground, tự "ngắt" khi destroy.

### 4.7 SharedPreferences
File XML nhỏ lưu key-value. Dùng để lưu thông tin user đăng nhập. Xem `SessionManager.java` — đây là một **singleton** bao quanh SharedPreferences:

```java
private SessionManager(Context context) {
    prefs = context.getApplicationContext()
            .getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
}

public static SessionManager getInstance(Context context) {
    if (instance == null) {
        instance = new SessionManager(context);
    }
    return instance;
}
```

---

## 5. 🚦 Flow chạy của app từ A → Z

```
[User bấm icon]
       │
       ▼
SplashActivity ◄── @LAUNCHER trong AndroidManifest.xml
       │
       │ Kiểm tra: FirebaseHelper.getCurrentUser() ?
       │
   ┌───┴────────┐
   │            │
 null         có user
   │            │
   ▼            ▼
PetShop     getUserRole(uid)
Activity        │
            ┌───┴───┐
          ADMIN  CUSTOMER
            │       │
            ▼       ▼
    AdminActivity  PetShopActivity
                       │
                       ▼
                   HomeFragment (mặc định)
                   ├─ BottomNav: Home/Chat/Order/Profile
                   ├─ Hiện danh mục, thú cưng nổi bật, đồ ăn nổi bật
                   ├─ Search bar
                   └─ Badge: giỏ hàng, thông báo (lắng nghe real-time)
```

Xem code Splash:
```java
FirebaseUser currentUser = FirebaseHelper.getCurrentUser();
if (currentUser != null) {
    FirebaseHelper.getUserRole(currentUser.getUid(), role -> {
        Runnable action = SessionManager.ROLE_ADMIN.equals(role)
                ? this::goToAdmin : this::goToPetShop;
        navigateAfterMinDelay(action);
    });
} else {
    navigateAfterMinDelay(this::goToPetShop);
}
```

**Giải thích từng dòng:**
1. `getCurrentUser()` hỏi Firebase Auth: "Có ai đang đăng nhập không?". Firebase nhớ login giữa các lần mở app.
2. Nếu có → đọc Firestore `users/{uid}` lấy field `role`.
3. Nếu `role == "ADMIN"` → vào AdminActivity, ngược lại vào PetShopActivity.
4. Mọi trường hợp đều đợi tối thiểu **1.5 giây** (`MIN_SPLASH_MS`) để splash không nháy quá nhanh.

---

## 6. 🔐 Login Flow chi tiết — Sinh viên đọc kỹ phần này!

Có **3 cách đăng nhập**: Email/Password, Google Sign-In, "Quên mật khẩu" (reset).

### 6.1 Sơ đồ tổng quát

```
LoginActivity (View)
    │   user nhập email + password, bấm "Đăng nhập"
    ▼
authViewModel.loginWithEmail(email, password)
    │
    ▼
AuthViewModel.loginWithEmail()       ← isLoading = true
    │
    ▼
FirebaseHelper.loginWithEmail()
    │
    ▼
FirebaseAuth.signInWithEmailAndPassword()  ◄─── gọi Firebase (async)
    │
    ├── thành công ──► getUserRole(uid) đọc Firestore
    │                       │
    │                       ▼
    │                  loadUserDataAndSaveSession()
    │                       │
    │                       ├─► SessionManager.saveSession()  (SharedPrefs)
    │                       └─► userRole.postValue(role)      (LiveData)
    │                                    │
    │                                    ▼
    │                            LoginActivity nhận → navigateByRole()
    │                                    │
    │                                    ├─ ADMIN → AdminActivity
    │                                    └─ CUSTOMER → PetShopActivity
    │
    └── thất bại ──► errorMessage.postValue("Email hoặc mật khẩu sai")
                           │
                           ▼
                    LoginActivity hiện tvError
```

### 6.2 Đọc code thực tế

**Bước 1 — User bấm nút (LoginActivity):**
```java
private void attemptEmailLogin() {
    String email    = getEmail();
    String password = etPassword.getText() != null ? etPassword.getText().toString().trim() : "";

    if (TextUtils.isEmpty(email)) {
        tvError.setText("Vui lòng nhập email");
        tvError.setVisibility(View.VISIBLE);
        return;
    }
    if (TextUtils.isEmpty(password)) {
        tvError.setText("Vui lòng nhập mật khẩu");
        tvError.setVisibility(View.VISIBLE);
        return;
    }
    tvError.setVisibility(View.GONE);
    authViewModel.loginWithEmail(email, password);
}
```

**Bước 2 — ViewModel xử lý:**
```java
public void loginWithEmail(String email, String password) {
    setLoading(true);
    FirebaseHelper.loginWithEmail(email, password, new FirebaseHelper.OnAuthCallback() {
        @Override
        public void onSuccess(String uid, String role) {
            loadUserDataAndSaveSession(uid, role);
        }
        @Override
        public void onFailure(String errorMsg) {
            setLoading(false);
            errorMessage.postValue(errorMsg);
        }
    });
}
```

**Bước 3 — Helper gọi Firebase:**
```java
public static void loginWithEmail(String email, String password, OnAuthCallback callback) {
    auth.signInWithEmailAndPassword(email, password)
            .addOnSuccessListener(result -> {
                String uid = result.getUser().getUid();
                getUserRole(uid, role -> callback.onSuccess(uid, role));
            })
            .addOnFailureListener(e -> callback.onFailure(parseAuthError(e.getMessage())));
}
```

**Bước 4 — Lưu session + bắn LiveData:**
```java
private void loadUserDataAndSaveSession(String uid, String role) {
    FirebaseHelper.getUserData(uid, new FirebaseHelper.OnUserDataCallback() {
        @Override
        public void onSuccess(User user) {
            String fullName = user.getFullName() != null ? user.getFullName() : "";
            sessionManager.saveSession(
                    uid,
                    fullName,
                    user.getEmail() != null ? user.getEmail() : "",
                    role,
                    user.getAvatarUrl()
            );
            setLoading(false);
            userRole.postValue(role);
            userName.postValue(fullName);
        }
```

**Bước 5 — Activity quan sát kết quả & điều hướng:**
```java
authViewModel.getUserRole().observe(this, role -> {
    if (role != null) navigateByRole(role);
});
```

```java
private void navigateByRole(String role) {
    Intent intent;
    if (SessionManager.ROLE_ADMIN.equals(role)) {
        intent = new Intent(this, AdminActivity.class);
    } else {
        intent = new Intent(this, PetShopActivity.class);
    }
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
    startActivity(intent);
    finish();
}
```

`FLAG_ACTIVITY_CLEAR_TASK` → **xóa hết back stack**, người dùng không thể bấm Back quay lại Login.

### 6.3 Google Sign-In

Phức tạp hơn vì phải qua Google trước:
1. Bấm nút Google → mở `GoogleSignInClient.getSignInIntent()`
2. User chọn tài khoản trong popup hệ thống.
3. Nhận `idToken` qua `ActivityResultLauncher` (cơ chế mới thay cho `onActivityResult`).
4. Gọi `authViewModel.loginWithGoogle(idToken)` → Firebase đổi idToken sang FirebaseUser.
5. Nếu là user mới (`isNewUser`) → tạo document trong Firestore với role mặc định `CUSTOMER`.

Xem `FirebaseHelper.loginWithGoogle()`.

### 6.4 Quên mật khẩu
`FirebaseAuth.sendPasswordResetEmail(email)` → Firebase tự gửi email reset, không cần backend của mình.

---

## 7. 🌊 Data flow chi tiết — HomeFragment làm ví dụ

### 7.1 Mục tiêu UI
Màn home hiển thị:
- Lời chào "Hi, tên user 🐾"
- Danh mục (RecyclerView ngang)
- Pet nổi bật (RecyclerView ngang)
- Đồ ăn nổi bật (RecyclerView ngang)
- Search bar
- Badge giỏ hàng + chuông thông báo

### 7.2 Data flow

```
1) onViewCreated()
        │
        ▼
2) vm = ViewModelProvider(activity).get(HomeViewModel.class)
   cartVm = ViewModelProvider(activity).get(CartViewModel.class)
        │
        ▼
3) setupRecyclerViews() → tạo HomePetAdapter, HomeFoodAdapter, HomeCategoryAdapter
   gắn LayoutManager, gắn click listener
        │
        ▼
4) observeViewModel() → đăng ký nghe LiveData
        │
        ▼
5) vm.loadHomeData()                    ◄─── kích hoạt fetch
        │
        ▼
6) HomeViewModel:
     promoRepo.getActive() ─► onSuccess(promotions)
                              │
                              ▼
     loadCategories()  ──► categories.postValue(active)
     petRepo.getAll()  ──► PromotionManager.applyPromotions()
                              │
                              ▼
                          filteredPets.postValue(top 20)
     foodRepo.getAll() ──► filteredFoods.postValue(top 20)
        │
        ▼
7) HomeFragment.observeViewModel():
     vm.getCategories().observe → categoryAdapter.updateList()
     vm.getFeaturedPets().observe → renderPets() → petAdapter.updateList()
     vm.getFeaturedFoods().observe → renderFoods() → foodAdapter.updateList()
     cartVm.getCart().observe → cập nhật badge giỏ hàng
```

### 7.3 Đoạn quan trọng nhất — ràng buộc View ↔ ViewModel
```java
private void observeViewModel() {
    vm.getCategories().observe(getViewLifecycleOwner(), cats -> categoryAdapter.updateList(cats));

    vm.getFeaturedPets().observe(getViewLifecycleOwner(), this::renderPets);
    vm.getFeaturedFoods().observe(getViewLifecycleOwner(), this::renderFoods);

    vm.getIsSearching().observe(getViewLifecycleOwner(), isSearching -> updateSectionTitles());

    cartVm.getSuccess().observe(getViewLifecycleOwner(), msg -> {
        if (msg != null) {
            Toast.makeText(requireContext(), msg, Toast.LENGTH_SHORT).show();
            cartVm.loadCart();
        }
    });
```

`getViewLifecycleOwner()` (chứ không phải `this`) — đây là **trick quan trọng** với Fragment: View của Fragment có thể bị hủy mà Fragment vẫn sống → dùng lifecycleOwner của *view* an toàn hơn.

---

## 8. 🎞 RecyclerView + Adapter hoạt động như thế nào?

RecyclerView là widget hiển thị **danh sách dài hiệu năng cao**. Nó **tái sử dụng** view (vì vậy có chữ "Recycler"): bạn cuộn 1000 item, nó chỉ tạo ra ~10 ô (đủ phủ màn hình), khi cuộn xuống thì lấy ô đã trôi lên gắn data mới.

### 8.1 4 thành phần
1. **RecyclerView** — cái khung trong XML
2. **LayoutManager** — sắp xếp dọc/ngang/lưới
   - `LinearLayoutManager` — danh sách
   - `GridLayoutManager` — lưới
3. **Adapter** — tạo ô + đổ data
4. **ViewHolder** — giữ tham chiếu tới TextView, ImageView của 1 ô (để khỏi `findViewById` lại mỗi lần)

### 8.2 Phân tích `HomePetAdapter`

**Khai báo:**
```java
public class HomePetAdapter extends RecyclerView.Adapter<HomePetAdapter.VH> {
```
→ Extends `RecyclerView.Adapter` với generic là class ViewHolder của riêng nó (`VH`).

**3 phương thức bắt buộc:**

`onCreateViewHolder` — tạo 1 ô mới khi RecyclerView cần:
```java
public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
    View v = LayoutInflater.from(parent.getContext())
            .inflate(R.layout.item_pet_card, parent, false);
    return new VH(v);
}
```
→ "Thổi phồng" (inflate) layout XML `item_pet_card.xml` thành View thực, bọc trong ViewHolder.

`onBindViewHolder` — gắn dữ liệu vào ô (gọi mỗi lần ô trôi vào màn hình):
```java
public void onBindViewHolder(@NonNull VH h, int pos) {
    Pet pet = list.get(pos);

    h.tvPetName.setText("Pet: " + pet.getName());
    ...
    // Hiện sale badge nếu có khuyến mãi
    if (pet.hasPromotion() && pet.getOriginalPrice() > 0 ...) {
        h.tvSaleBadge.setVisibility(View.VISIBLE);
        ...
    }
    ...
    // Load ảnh bằng Glide
    Glide.with(h.itemView).load(thumb).centerCrop()
          .placeholder(R.mipmap.ic_launcher).into(h.ivPet);
    ...
    // Click vào ô → mở chi tiết
    h.itemView.setOnClickListener(v -> listener.onClick(pet));
    // Click nút giỏ → thêm vào giỏ
    h.ivAddToCart.setOnClickListener(v -> cartListener.onAddToCart(pet));
}
```

`getItemCount` — tổng số ô:
```java
@Override public int getItemCount() { return list.size(); }
```

**ViewHolder** — cache findViewById:
```java
static class VH extends RecyclerView.ViewHolder {
    ImageView ivPet, ivAddToCart;
    TextView  tvPetName, tvPrice, ...;

    VH(View v) {
        super(v);
        ivPet       = v.findViewById(R.id.ivPetImage);
        ivAddToCart = v.findViewById(R.id.ivAddToCart);
        ...
    }
}
```

**Update data:**
```java
public void updateList(List<Pet> newList) {
    list.clear();
    list.addAll(newList);
    notifyDataSetChanged();
}
```
`notifyDataSetChanged()` báo cho RecyclerView vẽ lại. Đây là cách **đơn giản nhất** (giáo viên nâng cao có thể chê: nên dùng `DiffUtil`/`ListAdapter` để mượt hơn).

### 8.3 Pattern callback giữa Adapter và Fragment
Adapter **không nên** tự mình `startActivity` (vì Adapter không biết Context của Activity). Cách project làm:
```java
public interface OnPetClick { void onClick(Pet pet); }
public interface OnCartClick { void onAddToCart(Pet pet); }
```
Fragment truyền lambda khi tạo adapter:
```java
petAdapter = new HomePetAdapter(new ArrayList<>(), this::openPetDetail, pet -> cartVm.addPet(pet));
rvPets.setAdapter(petAdapter);
```
→ **Inversion of Control**: Adapter chỉ phát sự kiện, Fragment quyết định làm gì.

---

## 9. 🔄 CRUD đầy đủ trong project

CRUD = **C**reate **R**ead **U**pdate **D**elete. Hầu hết các entity đều có 4 thao tác này:

| Entity | Repository | Màn hình admin |
|---|---|---|
| **User** | `UserRepository` | `ManageUsersActivity` |
| **Pet** | `PetRepository` | `ManagePetsActivity` + `AddEditPetActivity` |
| **Food** | `FoodRepository` | `ManageFoodActivity` + `AddEditFoodActivity` |
| **Category** | `CategoryRepository` | `ManageCategoriesActivity` |
| **Order** | `OrderRepository` | `AdminOrderListActivity` + `AdminOrderDetailActivity` |
| **Promotion** | `PromotionRepository` | `ManagePromotionsActivity` + `AddEditPromotionActivity` |
| **Voucher** | `VoucherRepository` | `ManageVouchersActivity` + `AddEditVoucherActivity` |
| **Address** | `AddressRepository` | `ManageAddressActivity` |
| **Cart** | `CartRepository` | `CartActivity` (customer) |
| **Return** | `ReturnRepository` | `AdminReturnListActivity` |
| **Notification** | `NotificationRepository` | `NotificationActivity` |

### Ví dụ CRUD `Pet` (file `PetRepository.java`)

**CREATE:**
```java
public void add(Pet pet, Callback<String> cb) {
    String id = UUID.randomUUID().toString();
    pet.setId(id);
    pet.setCreatedAt(now());
    pet.setUpdatedAt(now());
    if (pet.getStatus() == null) pet.setStatus(Pet.STATUS_AVAILABLE);
    db.collection(COL).document(id).set(pet)
            .addOnSuccessListener(v -> cb.onSuccess(id))
            .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}
```

**READ all:**
```java
public void getAll(Callback<List<Pet>> cb) {
    db.collection(COL)
            .orderBy("createdAt", Query.Direction.DESCENDING)
            .get()
            .addOnSuccessListener(snap -> {
                List<Pet> list = new ArrayList<>();
                for (var doc : snap.getDocuments()) {
                    Pet pet = doc.toObject(Pet.class);
                    if (pet != null) {
                        pet.setId(doc.getId());
                        list.add(pet);
                    }
                }
                cb.onSuccess(list);
            })
            .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}
```
- `db.collection("pets")` — chọn collection
- `orderBy(...).get()` — truy vấn
- `doc.toObject(Pet.class)` — tự động map JSON → object Java (nhờ tên field giống nhau hoặc nhờ `@SerializedName`)

**UPDATE:** dùng `set(..., merge())` để không ghi đè field bị thiếu.
```java
public void update(Pet pet, Callback<Void> cb) {
    pet.setUpdatedAt(now());
    db.collection(COL).document(pet.getId())
            .set(pet, com.google.firebase.firestore.SetOptions.merge())
            .addOnSuccessListener(v -> cb.onSuccess(null))
            .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}
```

**DELETE:**
```java
public void delete(String id, Callback<Void> cb) {
    db.collection(COL).document(id).delete()
            .addOnSuccessListener(v -> cb.onSuccess(null))
            .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}
```

---

## 10. 🛒 Cart + Checkout + Thanh toán VNPay — Flow phức tạp nhất

### 10.1 Sơ đồ luồng

```
[Home] bấm "Thêm vào giỏ" trên pet/food
   │
   ▼
HomeFragment → cartVm.addPet(pet)  hoặc  cartVm.addFood(food, 1)
   │
   ▼
CartViewModel.addPet()
   │
   ▼
CartRepository.addPetToCart(uid, pet)
   │  dùng Firestore Transaction:
   │  1. Đọc pets/{id} → check status = AVAILABLE?
   │  2. Cập nhật pets/{id} → status = RESERVED  (giữ chỗ)
   │  3. Đọc/ghi carts/{uid} → thêm CartItem
   │
   ▼
[CartActivity] hiển thị giỏ
   │  - Mỗi item là 1 row trong RecyclerView (CartItemAdapter)
   │  - Nút +/- cho Food (không cho Pet vì pet là duy nhất)
   │  - Nút Xóa → trả pet về AVAILABLE
   │
   ▼ Bấm "Đặt hàng"
   │
[CheckoutActivity]
   │  - Hiện địa chỉ giao hàng (lấy từ AddressRepository)
   │  - Tính phí ship (ShippingHelper)
   │  - Áp voucher (PromotionRepository / VoucherRepository)
   │  - Chọn COD hoặc VNPay
   │
   ▼ Bấm "Đặt hàng"
   │
OrderRepository.createOrder(order, cartItems)
   │  Firestore Transaction:
   │  - Nếu COD: trừ stock food, mark pet = RESERVED
   │  - Nếu VNPay: chỉ tạo order trạng thái WAITING_PAYMENT
   │  - Tạo doc orders/{orderId}
   │
   ▼
   ├── COD → openOrderSuccess(orderId) → OrderDetailActivity
   │
   └── VNPay → VNPayHelper.buildPaymentUrl()
                  │  - Build query params + sort + URLEncode
                  │  - Tạo SecureHash HMAC-SHA512
                  ▼
                VNPayWebViewActivity (mở WebView trang VNPay)
                  │  user thanh toán xong → VNPay redirect về:
                  │  petshop://payment/vnpay-return?vnp_ResponseCode=00...
                  ▼
                VNPayResultActivity (nhận deeplink, đọc params)
                  │  - Nếu vnp_ResponseCode = "00" → orderRepo.completeVNPayOrder(orderId)
                  │  - Ngược lại → status FAILED
```

### 10.2 Code phần Transaction (đoạn HAY BỊ HỎI)

Firestore Transaction yêu cầu: **đọc trước, ghi sau**. Xem `addPetToCart`:
```java
public void addPetToCart(String userId, Pet pet, Callback<Cart> cb) {
    db.runTransaction((Transaction.Function<Void>) transaction -> {
        var petRef = db.collection(COL_PETS).document(pet.getId());
        var cartRef = db.collection(COL_CARTS).document(userId);

        // Step 1: All Reads first
        var petDoc = transaction.get(petRef);
        var cartDoc = transaction.get(cartRef);

        // Step 2: Validate
        String status = petDoc.getString("status");
        if (!Pet.STATUS_AVAILABLE.equals(status)) {
            throw new RuntimeException("Thú cưng này đã được đặt trước bởi người khác");
        }

        // Step 3: All Writes
        transaction.update(petRef, "status", Pet.STATUS_RESERVED);
        ...
        transaction.set(cartRef, cart);
        return null;
    })
    .addOnSuccessListener(v -> getCart(userId, cb))
    .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}
```

**Vì sao cần Transaction?** Hai user cùng bấm "Thêm vào giỏ" cùng lúc trên cùng 1 pet → nếu không có transaction, cả 2 đều thấy `AVAILABLE` và cùng thêm → trùng. Transaction bảo đảm: **đọc + check + ghi diễn ra nguyên tử**.

### 10.3 VNPay — Tạo chữ ký số

```java
public static String buildPaymentUrl(String orderCode, long amount, String orderInfo) {
    Map<String, String> vnp_Params = new TreeMap<>();
    vnp_Params.put("vnp_Version",   "2.1.0");
    ...
    vnp_Params.put("vnp_Amount",    String.valueOf(amount * 100)); // VNPay yêu cầu nhân 100
    ...
    // Sort theo alphabet → ghép thành chuỗi a=b&c=d&...
    // Ký HMAC-SHA512 với secret key
    String secureHash = hmacSHA512(Constants.VNPAY_HASH_SECRET.trim(), hashData.toString());
    query.append("&vnp_SecureHash=").append(secureHash);
    ...
}
```

**Vì sao phải ký?** Tránh user (hoặc attacker) sửa `vnp_Amount` từ 500.000đ → 1đ rồi gửi link đó cho VNPay. Server VNPay verify chữ ký → nếu sửa params thì hash sai → reject.

---

## 11. 🔁 Lifecycle Android ảnh hưởng gì?

### 11.1 Vì sao quan trọng?

Xét `HomeFragment` đăng ký listener real-time tới Firestore để đếm thông báo chưa đọc:
```java
private void startUnreadNotificationListener() {
    ...
    unreadNotifListener = new NotificationRepository().listenUnreadCount(uid, new NotificationRepository.Callback<Long>() {
        @Override
        public void onSuccess(Long data) { ... }
        @Override
        public void onFailure(String error) { ... }
    });
}
```

Nếu KHÔNG gỡ listener khi Fragment dừng → app vẫn nhận update → leak bộ nhớ + tốn quota Firebase. Code đã xử lý:
```java
@Override public void onStop() {
    super.onStop();
    if (unreadNotifListener != null) {
        unreadNotifListener.remove();
        unreadNotifListener = null;
    }
}
```

### 11.2 ViewModel sống sót xoay màn hình

Khi xoay từ dọc sang ngang, Android **destroy + recreate** Activity. Nhưng:
- ViewModel **không bị destroy** (sống chung với `ViewModelStore`).
- `LiveData` cũ tự động re-deliver giá trị mới nhất cho Activity mới.

→ Đó là lý do tại sao dùng `ViewModelProvider(this).get(...)` thay vì `new HomeViewModel()`.

### 11.3 onCleared() — Dọn dẹp ViewModel
```java
@Override
protected void onCleared() {
    super.onCleared();
    if (cartListener != null) cartListener.remove();
}
```
Khi Activity bị destroy **vĩnh viễn** (finish), ViewModel mới được hủy → đây là chỗ gỡ listener Firestore.

---

## 12. ⚡ Async / Thread / Callback — Project KHÔNG dùng Coroutine

> ⚠️ Đây là điểm **rất quan trọng** sinh viên hay nhầm. Project viết bằng **Java**, KHÔNG dùng Kotlin Coroutine. Nếu giáo viên hỏi "Project dùng coroutine không?" → trả lời **KHÔNG**.

### 12.1 Cách project xử lý bất đồng bộ

Mọi cuộc gọi Firebase đều **không trả về ngay** (chạy ngầm trên thread khác). Có 2 cơ chế:

**A) Firebase Task API (`addOnSuccessListener` / `addOnFailureListener`):**
```java
auth.sendPasswordResetEmail(email)
        .addOnSuccessListener(v -> callback.onSuccess(null, null))
        .addOnFailureListener(e -> callback.onFailure(parseAuthError(e.getMessage())));
```

**B) Callback interface tự định nghĩa** (mỗi Repository có 1):
```java
public interface Callback<T> {
    void onSuccess(T data);
    void onFailure(String error);
}
```

**C) LiveData postValue / setValue:**
- `setValue()` — chỉ gọi từ Main thread (UI thread)
- `postValue()` — có thể gọi từ background thread (Firebase callback thường ở thread UI rồi, nhưng để an toàn vẫn dùng `postValue`).

### 12.2 OkHttp (gọi OpenAI) — background thread thật sự

Trong `ChatViewModel`, gọi OpenAI bằng OkHttp — thư viện này tự chạy thread mạng:
```
client.newCall(request).enqueue(new Callback() {
   onResponse() { ... runOnUiThread(...) }
   onFailure() { ... }
});
```

→ Nhớ phải `runOnUiThread()` khi update UI từ thread mạng.

### 12.3 Tóm tắt: Project KHÔNG dùng

- ❌ `Thread`, `Handler` (chỉ dùng `Handler` 1 lần ở SplashActivity để delay)
- ❌ `AsyncTask` (deprecated)
- ❌ `ExecutorService`
- ❌ Kotlin `suspend` / `Coroutine`
- ❌ RxJava

→ Cả app dùng **callback-style asynchronous programming**.

---

## 13. 📋 Vai trò chi tiết từng class quan trọng

### 13.1 Utils (8 class chính)

| Class | Vai trò |
|---|---|
| `FirebaseHelper` | Bọc FirebaseAuth + Firestore user. Cung cấp loginWithEmail/Google, getUserRole, getUserData, sendPasswordReset, parseAuthError |
| `SessionManager` | Singleton bọc SharedPreferences. Lưu userId/name/email/role/avatar để dùng offline |
| `Constants` | Đọc giá trị từ `local.properties` qua `BuildConfig`: GOOGLE_WEB_CLIENT_ID, VNPAY_*, BASE_URL, OPENAI_API_KEY. Cũng định nghĩa tên collection: `COL_USERS`, `COL_PETS`,… |
| `VNPayHelper` | Tạo URL thanh toán + ký HMAC-SHA512, validate response code "00" |
| `StorageHelper` | Upload ảnh/video lên Firebase Storage, trả URL download |
| `ShippingHelper` | Tính phí ship dựa trên địa chỉ và subtotal |
| `PromotionManager` | Áp khuyến mãi vào list Pet/Food trước khi hiển thị |
| `AdminSetupHelper` | Khởi tạo tài khoản admin mặc định (tự gán role = ADMIN trong Firestore) |

### 13.2 Entity (20 class trong `model/entity`)

Tất cả đều là **POJO** (Plain Old Java Object): chỉ chứa field + getter/setter, có annotation `@SerializedName` (Gson) và một số `@Exclude` (Firestore không serialize).

| Class | Vai trò |
|---|---|
| `User` | Có role (ADMIN/CUSTOMER), loginType (EMAIL/GOOGLE), avatarUrl, status |
| `Pet` | name, species, breed, age, gender, price, status (AVAILABLE/RESERVED/SOLD/INACTIVE), thumbnailUrl, mediaList, promotion |
| `Food` | name, brand, foodType, targetPetType, price, stock, status, expiryDate |
| `Cart` | userId, items, totalItems, subtotal. Có method `calculateSubtotal()`, `calculateTotalItems()`, `isEmpty()` |
| `CartItem` | productType (PET/FOOD), productId, productName, unitPrice, originalPrice, quantity, subtotal |
| `Order` | orderCode, items, receiverName, shippingAddress, subtotal, shippingFee, voucherDiscount, totalAmount, status, paymentMethod, paymentStatus |
| `OrderItem` | Snapshot của CartItem tại thời điểm đặt (không thay đổi nếu sản phẩm bị xóa sau này) |
| `Category` | name, type (PET/FOOD), active |
| `Voucher` | code, type, discountValue, minOrderAmount, usageLimit, usageCount, expiryDate |
| `Promotion` | name, discountType, discountValue, startDate, endDate, voucherCode (optional), applicableProducts |
| `Address` | receiverName, receiverPhone, addressLine, ward, district, city, isDefault |
| `Notification` | userId, title, message, type, orderId, isRead, createdAt |
| `Review` | userId, productId, rating, comment, mediaList |
| `ChatMessage`, `ChatSession` | Lịch sử chat AI |
| `ReturnRequest` | orderId, reason, status, refundAmount |

### 13.3 Repository (13 class)

Tất cả đều có pattern giống nhau (CRUD + đặc biệt). Đặc điểm nổi bật:

- `CartRepository` — dùng **Firestore Transaction** để tránh race condition khi 2 user cùng thêm 1 pet.
- `OrderRepository` — dùng **Transaction** để giảm stock + tạo order đồng thời + cập nhật trạng thái pet.
- `NotificationRepository` — dùng **`addSnapshotListener`** (lắng nghe real-time) cho badge thông báo.
- `PromotionRepository` — có `incrementUsageCount` dùng `FieldValue.increment(1)` (Firestore atomic increment).

### 13.4 ViewModel (14 class)

| ViewModel | Phục vụ màn hình |
|---|---|
| `AuthViewModel` | LoginActivity, RegisterActivity |
| `HomeViewModel` | HomeFragment |
| `CartViewModel` | CartActivity, CheckoutActivity, các nơi cần thêm vào giỏ |
| `OrderViewModel` | OrderHistoryActivity, OrderDetailActivity |
| `ProfileViewModel` | ProfileFragment, EditProfileActivity |
| `AdminViewModel` | AdminActivity (dashboard) — có `startListening/stopListening` real-time |
| `ChatViewModel` | ChatActivity — gọi OpenAI API |
| `ProductViewModel` | ProductListActivity, PetDetail, FoodDetail |
| `PetManageViewModel`, `FoodManageViewModel`, `CategoryManageViewModel`, `PromotionManageViewModel`, `VoucherManageViewModel`, `UserManageViewModel` | Các màn hình admin |

### 13.5 Activity (34 class)

Phân loại theo vai trò:

- **Authentication (3):** Splash, Login, Register
- **Customer (15):** PetShop, Home (Fragment), Profile (Fragment), Cart, Checkout, OrderHistory, OrderDetail, ReturnRequest, EditProfile, ManageAddress, Notification, Promotion, ProductList, PetDetail, FoodDetail
- **Chat:** ChatActivity
- **Payment:** VNPayWebViewActivity, VNPayResultActivity
- **Admin Dashboard (1):** AdminActivity
- **Admin Quản lý (12):** ManageUsers, ManageCategories, ManagePets, AddEditPet, ManageFood, AddEditFood, ManagePromotions, AddEditPromotion, ManageVouchers, AddEditVoucher, AdminOrderList, AdminOrderDetail, AdminReturnList

### 13.6 Adapter (19 class)

Chia 2 nhóm:
- **Home/customer adapters:** `HomePetAdapter`, `HomeFoodAdapter`, `HomeCategoryAdapter`, `CartAdapter`, `CartItemAdapter`, `OrderAdapter`, `NotificationAdapter`, `ProductAdapter`, `PromotionAdapter`, `ChatAdapter`, `ChatSessionAdapter`, `ImageSliderAdapter`, `MediaPickerAdapter`, `CategoryAdapter`
- **Admin adapters:** `PetAdminAdapter`, `FoodAdminAdapter`, `UserAdminAdapter`, `PromotionAdminAdapter`, `VoucherAdminAdapter`

---

## 14. 🎯 Câu hỏi giáo viên hay hỏi + Câu trả lời mẫu

### Q1: "Project em dùng kiến trúc gì?"
> **Em sử dụng kiến trúc MVVM kết hợp Repository Pattern.**
> - **Model**: các class trong `model/entity` chứa dữ liệu thuần (POJO).
> - **View**: các Activity và Fragment, chỉ hiển thị UI và bắt sự kiện.
> - **ViewModel**: các class trong `viewmodel/`, chứa trạng thái UI dạng `LiveData` và logic nghiệp vụ, không phụ thuộc vào Android Framework.
> - **Repository**: lớp trung gian giữa ViewModel và Firebase Firestore, đóng vai trò "single source of truth" cho data.
>
> Em chọn MVVM vì: (1) tách trách nhiệm rõ ràng, (2) ViewModel sống sót khi xoay màn hình, (3) LiveData tự động đồng bộ UI ↔ data, (4) dễ test, (5) dễ thay backend mà không cần sửa UI.

### Q2: "Vì sao có ViewModel? `new HomeViewModel()` được không?"
> Không nên. ViewModel phải được lấy qua `ViewModelProvider` vì:
> 1. Khi Activity bị recreate (xoay màn hình), `new` sẽ tạo instance mới, mất hết state. ViewModelProvider lưu instance trong `ViewModelStore` nên giữ nguyên data đã load.
> 2. ViewModel có `onCleared()` được gọi tự động khi Activity finish hẳn → dùng để dọn dẹp listener.

### Q3: "LiveData khác Observer thông thường ở đâu?"
> LiveData là Observer **gắn với Lifecycle**. Nó chỉ gửi data khi observer đang ở trạng thái `STARTED` hoặc `RESUMED`, và **tự động hủy đăng ký** khi observer bị destroy. Vì vậy:
> - Không bao giờ crash do update UI trên Activity đã destroy.
> - Không leak memory vì observer không tự hủy.

### Q4: "Tại sao dùng Repository? Sao không gọi Firebase thẳng trong Activity?"
> Để **tách lớp**: Activity chỉ lo UI, không biết data đến từ Firestore hay REST API. Nếu sau này đổi sang dùng REST API hay Room database, em chỉ cần sửa Repository, không phải đụng vào 34 Activity.

### Q5: "Firestore Transaction là gì? Vì sao dùng?"
> Transaction là một chuỗi đọc/ghi **nguyên tử** trên Firestore. Nếu giữa lúc đọc và ghi có người khác sửa cùng document, Firestore sẽ retry transaction tự động.
> Em dùng trong `CartRepository.addPetToCart()` để tránh trường hợp 2 user cùng thêm 1 con thú cưng vào giỏ — chỉ 1 người thành công, người kia nhận lỗi "đã được đặt".

### Q6: "Xoay màn hình thì data có mất không?"
> Không. Vì em dùng ViewModel để giữ data. Activity bị recreate nhưng ViewModel vẫn sống, LiveData re-deliver giá trị mới nhất sang Activity mới. Vì vậy em không phải load lại từ Firestore.

### Q7: "Em xử lý bất đồng bộ thế nào?"
> Em dùng **callback** (vì project viết bằng Java thuần, không phải Kotlin Coroutine).
> - Firebase trả `Task` → em dùng `.addOnSuccessListener` / `.addOnFailureListener`.
> - Em bọc lại thành interface `Callback<T>` trong mỗi Repository, có 2 method `onSuccess(T)` / `onFailure(String)`.
> - ViewModel sau khi nhận callback sẽ `postValue()` lên LiveData để UI cập nhật.

### Q8: "RecyclerView khác ListView ở chỗ nào?"
> 1. RecyclerView **bắt buộc dùng ViewHolder pattern** → không phải `findViewById` mỗi lần bind.
> 2. Tách rõ Adapter / LayoutManager / ItemDecoration → linh hoạt hơn (Grid, Linear, Staggered…).
> 3. Tái sử dụng view hiệu quả hơn → cuộn mượt, ít tốn RAM.
> 4. Hỗ trợ animation built-in, DiffUtil để chỉ update item thay đổi.

### Q9: "ViewBinding hay findViewById?"
> Project em **bật ViewBinding trong `build.gradle.kts`** (`buildFeatures { viewBinding = true }`) nhưng đa số file vẫn dùng `findViewById` vì code có sẵn. ViewBinding chỉ generate class binding tự động, tránh `findViewById` lặp lại và tránh `NullPointerException` do gõ sai id. Trong project tương lai em sẽ refactor sang ViewBinding hết.

### Q10: "Login bằng Google làm sao?"
> 4 bước:
> 1. Cấu hình `GoogleSignInOptions` với `requestIdToken(WEB_CLIENT_ID)` (lấy từ Firebase Console).
> 2. Mở intent đăng nhập của Google → user chọn tài khoản.
> 3. Nhận `idToken` qua `ActivityResultLauncher`.
> 4. Đổi idToken sang Firebase Credential bằng `GoogleAuthProvider.getCredential(idToken, null)` → `FirebaseAuth.signInWithCredential()`.
> Nếu là user mới (`AdditionalUserInfo.isNewUser()`) thì em tạo document trong Firestore với role mặc định CUSTOMER.

### Q11: "Bảo mật của VNPay đảm bảo bằng cách nào?"
> Bằng **chữ ký HMAC-SHA512**:
> 1. Em sort các tham số theo alphabet, URL-encode rồi nối lại thành chuỗi.
> 2. Ký chuỗi đó bằng HMAC-SHA512 với secret key (cấp bởi VNPay).
> 3. Gắn chữ ký vào URL dưới key `vnp_SecureHash`.
> Server VNPay verify lại chữ ký → nếu user/attacker sửa amount thì hash sai → reject.

### Q12: "ProfileFragment và HomeFragment dùng chung Activity, có khác gì khi switch tab?"
> Em dùng pattern **`hide()` / `show()`** thay vì `replace()`:
> ```
> fm.beginTransaction()
>   .add(container, profileFragment).hide(profileFragment)
>   .add(container, homeFragment)
>   .commit();
> ```
> Khi switch tab chỉ ẩn/hiện, không destroy fragment → giữ nguyên state (vị trí scroll, dữ liệu) và không phải reload data → mượt hơn `replace()`.

### Q13: "Có dependency injection (Dagger/Hilt) không?"
> Không. Em dùng cách đơn giản: trong ViewModel khai báo `new XxxRepository()` trực tiếp. Đối với project lớn hơn em sẽ dùng Hilt để inject Repository (dễ test mock).

### Q14: "Real-time update ở đâu?"
> Em dùng `addSnapshotListener` của Firestore tại:
> - Badge thông báo chưa đọc trong HomeFragment.
> - Dashboard thống kê đơn hàng trong AdminActivity.
> - Cart trong CartViewModel.
> Khi data trên Firestore thay đổi (admin đổi trạng thái đơn, có thông báo mới...) UI tự cập nhật, không cần user kéo refresh.

### Q15: "Em làm sao tránh memory leak?"
> 1. Mọi `addSnapshotListener` đều giữ `ListenerRegistration` và `.remove()` trong `onStop()` (Fragment) hoặc `onCleared()` (ViewModel).
> 2. Dùng `getViewLifecycleOwner()` thay cho `this` khi observe LiveData trong Fragment.
> 3. Adapter giữ list bằng `final` reference, không lưu Context của Activity.

---

## 15. 📌 Tổng kết — Học gì trước, file nào quan trọng nhất

### 15.1 Sơ đồ flow tổng quát của app

```
                 ┌──────────────────┐
                 │  SplashActivity  │ ← launcher
                 └────────┬─────────┘
              chưa login  │  đã login
                  ┌───────┴────────┐
                  ▼                ▼
         PetShopActivity     getUserRole
        (Bottom Navigation)         │
            │                  ┌────┴─────┐
   ┌─────┬──┴──┬──────┐      CUSTOMER  ADMIN
   ▼     ▼     ▼      ▼         │        │
 Home  Chat Orders Profile      ▼        ▼
   │           │       │   PetShopAct  AdminActivity
   │           │       │                   │
   │           │       │            ┌──────┴───────┐
   │           │       │       Manage*           Dashboard
   │           ▼       │       (Users/Pets/Foods/
   ▼      ChatActivity ▼        Orders/Promos…)
PetDetail / FoodDetail
  → CartActivity
  → CheckoutActivity
  → OrderRepository.createOrder
  → (COD) OrderDetailActivity
    (VNPay) VNPayWebViewActivity → VNPayResultActivity
```

### 15.2 Top 12 file QUAN TRỌNG NHẤT (đọc trước)

| # | File | Vì sao quan trọng |
|---|---|---|
| 1 | `AndroidManifest.xml` | Khai báo toàn bộ Activity, permission, launcher, deeplink VNPay |
| 2 | `SplashActivity.java` | Entry point thực sự — quyết định route |
| 3 | `FirebaseHelper.java` | Toàn bộ logic auth: login email/Google, check role |
| 4 | `SessionManager.java` | Quản lý session local qua SharedPreferences |
| 5 | `AuthViewModel.java` | Pattern MVVM tiêu biểu cho login |
| 6 | `LoginActivity.java` | Bộ ba View ↔ ViewModel ↔ FirebaseHelper |
| 7 | `PetShopActivity.java` | Cách tổ chức BottomNav + Fragment hide/show |
| 8 | `HomeFragment.java` | Ví dụ điển hình Fragment dùng MVVM + RecyclerView |
| 9 | `HomeViewModel.java` | LiveData, gọi Repository, search/filter logic |
| 10 | `PetRepository.java` | CRUD chuẩn trên Firestore |
| 11 | `CartRepository.java` | Firestore Transaction (advanced) |
| 12 | `CheckoutActivity.java` + `OrderRepository.java` + `VNPayHelper.java` | Flow đặt hàng & thanh toán |

### 15.3 Lộ trình học để hiểu project nhanh nhất

**Giai đoạn 1 — Nền tảng Android (nếu chưa biết):**
- Activity Lifecycle (`onCreate`, `onStart`, `onResume`, `onPause`, `onStop`, `onDestroy`)
- Intent + cách chuyển Activity
- View, ViewGroup, layout XML (LinearLayout, ConstraintLayout)
- `findViewById`, `setOnClickListener`
- Fragment cơ bản

**Giai đoạn 2 — RecyclerView & Adapter:**
- Đọc kỹ `HomePetAdapter.java` và `item_pet_card.xml`
- Tự tạo 1 RecyclerView nhỏ hiển thị list String để hiểu pattern
- Glide load ảnh từ URL

**Giai đoạn 3 — ViewModel + LiveData:**
- Đọc `AuthViewModel.java` rồi đọc `LoginActivity.java` để thấy chúng nối với nhau qua `observe()`
- Học khái niệm `MutableLiveData` vs `LiveData`

**Giai đoạn 4 — Firebase:**
- Firebase Auth: login/register/Google
- Firestore: collection/document, `get()`, `set()`, `update()`, `delete()`, `addSnapshotListener`
- Storage: upload file
- Đọc `FirebaseHelper.java`, `PetRepository.java`, `StorageHelper.java`

**Giai đoạn 5 — Tổng hợp + Đặc biệt:**
- Đọc `CartRepository.java` để hiểu Transaction
- Đọc `CheckoutActivity.java` + `VNPayHelper.java` để hiểu payment flow
- Đọc `ChatViewModel.java` để xem cách gọi REST API bằng OkHttp

### 15.4 Những thứ project CHƯA có (giáo viên có thể hỏi để gợi ý cải tiến)

- Không có **Hilt/Dagger** (DI)
- Không có **Room** (cache offline)
- Không có **Retrofit** (BASE_URL trong Constants chưa được dùng đến)
- Không có **DiffUtil** trong adapter → cuộn list dài có thể giật
- Một số file repository còn rỗng (`AuthRepository`, `ProductRepository`)
- Đa số dùng `findViewById`, chưa migrate sang ViewBinding dù đã enable
- Không có Unit Test / Instrumentation Test (folder `test/` và `androidTest/` đang rỗng)

---

# PHẦN B — ĐI SÂU VÀO 5 CHỦ ĐỀ TRỌNG TÂM

> ⚠️ **Lưu ý quan trọng từ đầu:** Project này **KHÔNG có đăng nhập bằng Facebook**. Search toàn bộ source code, không có file nào chứa từ "facebook". Project chỉ hỗ trợ **Email/Password** + **Google Sign-In**. Nếu giáo viên hỏi "Có Facebook login không?" → phải trả lời **KHÔNG**, đừng nói có rồi giáo viên mở code ra check là chết.

---

# PHẦN 1️⃣ — CẤU TRÚC DỰ ÁN (chi tiết)

## 1.1 Sơ đồ tầng vật lý (physical layers) của project

Một project Android Studio luôn có **3 cấp** thư mục bạn cần phân biệt:

```
Petshop/                       ← PROJECT ROOT (mở bằng Android Studio)
│
├── build.gradle.kts           ← Cấu hình cho TOÀN BỘ project (top-level)
├── settings.gradle.kts        ← Khai báo các module con (ở đây chỉ có :app)
├── gradle.properties          ← Cấu hình JVM, dùng để bật/tắt feature
├── local.properties           ← FILE BÍ MẬT chứa API key (KHÔNG commit Git!)
├── gradlew / gradlew.bat      ← Script chạy build mà không cần cài Gradle
│
└── app/                       ← MODULE "app" (chứa toàn bộ code app)
    │
    ├── build.gradle.kts       ← Cấu hình riêng cho module này
    ├── google-services.json   ← File cấu hình Firebase (tải từ Firebase Console)
    ├── proguard-rules.pro     ← Quy tắc minify khi build release
    │
    └── src/
        ├── main/              ← CODE CHÍNH của app
        │   ├── AndroidManifest.xml   ← "Mục lục" app: khai báo Activity, permission
        │   ├── java/com/example/petshop/   ← Source code Java
        │   └── res/                   ← Tài nguyên (XML, ảnh, màu, string)
        │
        ├── test/              ← Unit test (trong project này đang rỗng)
        └── androidTest/       ← Test trên máy thật/giả lập (đang rỗng)
```

**Giải thích các file gradle (giáo viên hay hỏi):**

| File | Vai trò ví dụ thực tế |
|---|---|
| `build.gradle.kts` (root) | Như "danh sách thư viện chung" cho cả nhà — chỉ định plugin Android, plugin Google Services |
| `settings.gradle.kts` | Như "danh sách các phòng trong nhà" — ở đây có 1 phòng tên `:app` |
| `app/build.gradle.kts` | Cấu hình riêng "phòng app": minSdk, targetSdk, dependencies, buildFeatures... |
| `local.properties` | Ghi giá trị bí mật (API key Google, VNPay secret, OpenAI key). KHÔNG được commit Git. |
| `google-services.json` | Firebase cấp — chứa thông tin project Firebase (project_id, app_id). |

Mở file `app/build.gradle.kts` xem **3 dòng then chốt** sau:

```kotlin
buildFeatures {
    viewBinding = true
    buildConfig = true
}
```
- `viewBinding = true` → cho phép truy cập view qua biến thay vì `findViewById`.
- `buildConfig = true` → cho phép sinh class `BuildConfig.java` chứa biến đọc từ `local.properties`.

Và đoạn này:
```kotlin
buildConfigField("String", "GOOGLE_WEB_CLIENT_ID",
    "\"${localProp("GOOGLE_WEB_CLIENT_ID")}\"")
buildConfigField("String", "BASE_URL",
    "\"${localProp("BASE_URL", "https://your-api.com/api/v1/")}\"")
buildConfigField("String", "VNPAY_TMN_CODE",
    "\"${localProp("VNPAY_TMN_CODE")}\"")
...
buildConfigField("String", "OPENAI_API_KEY",
    "\"${localProp("OPENAI_API_KEY")}\"")
```
→ Lúc build, Gradle đọc `local.properties` rồi inject vào class `BuildConfig`. Code app dùng qua `BuildConfig.GOOGLE_WEB_CLIENT_ID`.

**Vì sao làm vậy? (giáo viên hay hỏi)** → Để KHÔNG commit API key lên Git. File `local.properties` được liệt kê trong `.gitignore` nên không bị đẩy lên GitHub. Mỗi developer có file riêng.

## 1.2 Cấu trúc package Java — tổ chức theo "layer"

Sơ đồ tổ chức theo **chiều dọc theo tầng MVVM**:

```
com.example.petshop
│
│  ─── TẦNG 1: MODEL (dữ liệu thuần) ───
├── model/
│   ├── entity/        ← Các "danh từ" của app: User, Pet, Food, Cart, Order…
│   ├── request/       ← Object để gửi đi (hiện chỉ có LoginRequest, RegisterRequest)
│   └── response/      ← Object trả về từ API (hiện chỉ có 2 file)
│
│  ─── TẦNG 2: DATA ACCESS ───
├── repository/        ← Mỗi entity 1 file, làm CRUD trên Firestore
│   ├── PetRepository, FoodRepository, CartRepository, OrderRepository
│   ├── CategoryRepository, UserRepository
│   ├── AddressRepository, NotificationRepository
│   ├── PromotionRepository, VoucherRepository, ReturnRepository
│
│  ─── TẦNG 3: STATE / LOGIC ───
├── viewmodel/         ← Mỗi màn hình lớn có 1 ViewModel
│   ├── AuthViewModel, HomeViewModel, CartViewModel, OrderViewModel
│   ├── ProfileViewModel, AdminViewModel, ChatViewModel
│   ├── PetManageViewModel, FoodManageViewModel… (cho admin)
│
│  ─── TẦNG 4: UI ───
├── view/
│   ├── activity/      ← 34 màn hình toàn màn hình
│   ├── fragment/      ← 6 tab nằm trong PetShopActivity
│   ├── adapter/       ← 19 adapter cho RecyclerView
│   └── dialog/        ← 4 dialog tái sử dụng
│
│  ─── TẦNG 5: HELPER / DỊCH VỤ NỀN ───
├── utils/             ← Các "trợ lý" dùng chung
│   ├── FirebaseHelper, SessionManager, Constants
│   ├── VNPayHelper, EmailHelper, StorageHelper
│   ├── PromotionManager, ShippingHelper, CartBadgeManager
│   ├── AdminSetupHelper
│
└── MainActivity.java  ← (gần như rỗng, chỉ redirect sang SplashActivity)
```

**Quy tắc phụ thuộc (dependency rule):**

```
View → ViewModel → Repository → Firebase
  ↓        ↓            ↓
utils    utils       utils
  ↓
model (entity)
```

- View **được phép** import: ViewModel, Model, utils
- ViewModel **được phép** import: Repository, Model, utils
- Repository **được phép** import: Firebase, Model, utils
- Model **chỉ import**: thư viện chuẩn (Gson, Firestore annotation)
- **CẤM:** ViewModel import View; Repository import View hay ViewModel; Model import gì khác.

Vẽ ra giấy mũi tên này, giáo viên hỏi "kiến trúc tách thế nào?" → bạn vẽ luôn → ăn điểm cao.

## 1.3 Thư mục `res/` — tài nguyên

```
res/
├── layout/        ← XML giao diện (60+ file)
│   ├── activity_*.xml      ← Layout của Activity
│   ├── fragment_*.xml      ← Layout của Fragment
│   ├── item_*.xml          ← Layout của 1 row trong RecyclerView
│   ├── dialog_*.xml        ← Layout của Dialog
│
├── drawable/      ← Background, shape, icon vector
├── menu/          ← bottom_nav_menu.xml (4 tab dưới)
├── mipmap-*/      ← Icon app theo độ phân giải
├── values/
│   ├── colors.xml         ← Bảng màu
│   ├── strings.xml        ← Văn bản (để dịch đa ngôn ngữ)
│   └── themes.xml         ← Theme (sáng)
├── values-night/          ← Theme tối
└── xml/                   ← backup_rules.xml
```

> **Mẹo đọc tên file:** Tên Activity Java và tên layout XML đặt theo quy ước: `LoginActivity.java` ↔ `activity_login.xml`. Cứ đổi camelCase → snake_case, thêm prefix `activity_`/`fragment_`/`item_` là ra layout tương ứng.

---

# PHẦN 2️⃣ — FIREBASE TRONG PROJECT

Firebase là **backend dịch vụ** của Google. Project này dùng **3 dịch vụ Firebase**:

```
┌──────────────────────────────────────────────────────┐
│                    FIREBASE PROJECT                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. Authentication      → Quản lý đăng nhập          │
│     - Email/Password                                 │
│     - Google                                         │
│                                                      │
│  2. Firestore           → Database NoSQL (cloud DB)  │
│     - Lưu user, pet, food, order, cart, address,     │
│       notification, voucher, promotion…              │
│                                                      │
│  3. Storage             → Lưu file (ảnh, video)      │
│     - Avatar user                                    │
│     - Ảnh pet, ảnh food                              │
│     - Media trong review                             │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 2.1 Firebase được "cắm" vào app như thế nào?

Quy trình kết nối Firebase (giáo viên có thể hỏi):

```
1. Vào https://console.firebase.google.com → tạo project
2. Add Android app → nhập package "com.example.petshop"
3. Tải file google-services.json về → đặt vào thư mục app/
4. Trong build.gradle:
     - plugin: com.google.gms.google-services
     - dependency: firebase-bom, firebase-auth, firebase-firestore, firebase-storage
5. Lúc build, plugin google-services tự đọc google-services.json
   và sinh ra mã kết nối Firebase
6. Trong code chỉ cần gọi: FirebaseAuth.getInstance(), FirebaseFirestore.getInstance()...
   không cần config gì thêm
```

Xem `app/build.gradle.kts`:
```kotlin
implementation(platform(libs.firebase.bom))
implementation(libs.firebase.auth)
implementation(libs.firebase.firestore)
implementation(libs.firebase.storage)
```

> **BOM là gì?** "Bill of Materials" — một file metadata khai báo phiên bản. Khi import `firebase-bom`, các thư viện `firebase-auth`, `firebase-firestore`… tự lấy version tương thích, không phải khai báo tay từng cái. Lợi: tránh xung đột version.

## 2.2 Cấu trúc Firestore của project này

Firestore là **NoSQL document database**. Cấu trúc giống cây thư mục, gồm:
- **Collection** (giống thư mục) → chứa nhiều Document
- **Document** (giống file) → chứa các field (key-value)
- Một Document có thể chứa **subcollection** bên trong

Theo code mà tôi đọc, project có cấu trúc Firestore như sau:

```
firestore-root/
│
├── users/                          ← Collection "users"
│   └── {uid}/                      ← Document (id = Firebase Auth UID)
│       ├── id: "abc123"
│       ├── fullName: "Nguyễn Văn A"
│       ├── email: "a@gmail.com"
│       ├── role: "CUSTOMER" hoặc "ADMIN"
│       ├── loginType: "EMAIL" hoặc "GOOGLE"
│       ├── avatarUrl: "https://..."
│       ├── status: "ACTIVE"
│       ├── createdAt: "..."
│       │
│       └── addresses/              ← Subcollection
│           └── {addrId}/           ← Document địa chỉ
│               ├── receiverName, receiverPhone
│               ├── addressLine, ward, district, city
│               └── isDefault
│
├── pets/                           ← Collection thú cưng
│   └── {petId}/
│       ├── id, name, species, breed, age, gender, weight
│       ├── price, originalPrice, discountedPrice, promotionId
│       ├── thumbnailUrl, status (AVAILABLE/RESERVED/SOLD/INACTIVE)
│       ├── description, careGuide, vaccineStatus…
│       │
│       └── pet_media/              ← Subcollection (ảnh phụ)
│           └── {mediaId}: { url, sortOrder, type }
│
├── foods/                          ← Collection đồ ăn
│   └── {foodId}: { name, brand, foodType, stock, price… }
│
├── categories/                     ← Danh mục pet/food
│   └── {catId}: { name, type ("PET"/"FOOD"), active }
│
├── carts/                          ← Collection giỏ hàng
│   └── {uid}/                      ← 1 user = 1 document cart
│       ├── userId, totalItems, subtotal
│       └── items: [ { productType, productId, productName,
│                       unitPrice, originalPrice, quantity, subtotal } ]
│
├── orders/                         ← Đơn hàng
│   └── {orderId}/
│       ├── orderCode: "ORD..."
│       ├── userId, items, receiverName, shippingAddress
│       ├── subtotal, shippingFee, voucherDiscount, totalAmount
│       ├── status (PENDING/CONFIRMED/SHIPPING/DELIVERED/CANCELLED/…)
│       ├── paymentMethod (COD/VNPAY), paymentStatus
│
├── notifications/                  ← Thông báo
│   └── {notifId}/
│       ├── userId         ← Người nhận
│       ├── title, message, type ("ORDER"/"PROMO"/"SYSTEM")
│       ├── orderId        ← Link tới đơn (nếu có)
│       ├── isRead: false  ← Trạng thái đọc
│       └── createdAt
│
├── promotions/                     ← Khuyến mãi (giảm giá sản phẩm)
│   └── {promoId}: { name, discountValue, startDate, endDate,
│                     voucherCode (optional), applicableProducts… }
│
├── vouchers/                       ← Voucher rời
│   └── {voucherId}: { code, discountValue, minOrderAmount, expiryDate… }
│
├── reviews/                        ← Đánh giá sản phẩm
└── return_requests/                ← Yêu cầu hoàn trả
```

> **Quy ước quan trọng:** Document `users/{uid}` dùng đúng **UID từ Firebase Auth** làm ID. Document `carts/{uid}` cũng vậy. Lợi: không cần thêm field nữa để tra cứu, query nhanh.

## 2.3 Pattern Firestore mọi Repository đều dùng

Mọi Repository trong project đều theo 4 thao tác cơ bản này:

**1) READ một document:**
```java
db.collection("pets").document(petId).get()
    .addOnSuccessListener(doc -> {
        Pet pet = doc.toObject(Pet.class);  // tự động map JSON → object
        pet.setId(doc.getId());
        callback.onSuccess(pet);
    })
    .addOnFailureListener(e -> callback.onFailure(e.getMessage()));
```

**2) READ nhiều document (query):**
```java
db.collection("notifications")
    .whereEqualTo("userId", uid)           // điều kiện WHERE
    .orderBy("createdAt", Query.Direction.DESCENDING)  // ORDER BY
    .limit(50)                              // LIMIT
    .get()
    .addOnSuccessListener(snap -> {
        for (var doc : snap.getDocuments()) { ... }
    });
```

**3) CREATE / UPDATE:**
```java
db.collection("pets").document(petId).set(pet);         // ghi đè toàn bộ
db.collection("pets").document(petId)
    .set(pet, SetOptions.merge());                       // chỉ ghi field có giá trị
db.collection("pets").document(petId)
    .update("status", "SOLD", "updatedAt", now());       // update vài field
```

**4) DELETE:**
```java
db.collection("pets").document(petId).delete();
```

**5) REAL-TIME listener:**
```java
ListenerRegistration reg = db.collection("notifications")
    .whereEqualTo("userId", uid)
    .addSnapshotListener((snap, e) -> {
        // Gọi MỖI KHI có thay đổi trên Firestore
    });
// Khi không cần nữa: reg.remove();
```

**6) TRANSACTION (đọc + ghi nguyên tử):**
```java
db.runTransaction(transaction -> {
    var doc = transaction.get(ref);   // đọc trước
    transaction.update(ref, "field", newValue);  // ghi sau
    return null;
});
```

**7) BATCH (ghi nhiều cùng lúc):**
```java
WriteBatch batch = db.batch();
for (Address a : list) {
    batch.update(ref, "isDefault", false);
}
batch.commit();   // commit cùng lúc
```

## 2.4 Vì sao chọn Firestore?

| Ưu điểm | Giải thích |
|---|---|
| Realtime | `addSnapshotListener` → app tự update khi data đổi, không cần kéo refresh |
| Không cần backend tự build | Khỏi phải viết Node.js, Spring Boot, MySQL… |
| Authentication tích hợp sẵn | Tự xử lý token, refresh, không cần code |
| Free tier rộng | Đủ cho project học |
| Offline cache | App vẫn chạy được khi mất mạng (tự sync khi có lại) |

**Nhược điểm (giáo viên có thể hỏi để check em hiểu):**
- Query phức tạp hạn chế (không JOIN được như SQL).
- Chi phí tính theo số lần đọc/ghi → nếu thiết kế sai có thể tốn tiền.
- Khó migration nếu sau này đổi backend.

---

# PHẦN 3️⃣ — AUTH BẰNG EMAIL/PASSWORD (chi tiết flow)

## 3.1 Tổng quan 2 flow: Đăng ký vs Đăng nhập

```
┌──────────────────────────┐   ┌──────────────────────────┐
│   ĐĂNG KÝ (Register)     │   │   ĐĂNG NHẬP (Login)      │
│                          │   │                          │
│ 1. Nhập email            │   │ 1. Nhập email + password │
│ 2. Bấm "Gửi mã" → OTP    │   │ 2. Bấm "Đăng nhập"       │
│ 3. Nhập OTP              │   │                          │
│ 4. Nhập password         │   │                          │
│ 5. Bấm "Đăng ký"         │   │                          │
└──────────┬───────────────┘   └──────────┬───────────────┘
           ▼                              ▼
      Firebase Auth                  Firebase Auth
   createUser...                  signInWith...
           │                              │
           ▼                              ▼
   Tạo document trong              Đọc role từ
   Firestore users/{uid}           Firestore users/{uid}
           │                              │
           └──────────┬───────────────────┘
                      ▼
              SessionManager.saveSession()
                      │
                      ▼
              Mở PetShop hoặc Admin
```

## 3.2 Đăng ký — Flow chi tiết 7 bước

> Project này có thêm **xác thực OTP qua email** trước khi register (không bắt buộc, do team tự viết bằng JavaMail). Đây là điểm cộng khi báo cáo!

**Bước 1: User nhập email, bấm "Gửi mã"**
```java
private void sendOtp() {
    String email = getText(etEmail);
    if (TextUtils.isEmpty(email) || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
        showError("Vui lòng nhập email hợp lệ");
        return;
    }
    setLoading(true);
    // Bước 1: Kiểm tra email đã tồn tại trong hệ thống chưa
    FirebaseAuth.getInstance().fetchSignInMethodsForEmail(email)
            .addOnCompleteListener(task -> {
                if (task.isSuccessful()) {
                    List<String> methods = task.getResult().getSignInMethods();
                    if (methods != null && !methods.isEmpty()) {
                        setLoading(false);
                        showError("Email này đã được đăng ký cho tài khoản khác");
                    } else {
                        performSendEmail(email);
                    }
                } else { ... }
            });
}
```
→ Gọi `fetchSignInMethodsForEmail()` của Firebase Auth để hỏi: "Email này đã có ai dùng chưa?".

**Bước 2: Sinh OTP 6 số + gửi email qua SMTP Gmail**
```java
private void performSendEmail(String email) {
    generatedOtp = String.valueOf((int) (Math.random() * 900000 + 100000));

    EmailHelper.sendOTP(email, generatedOtp, new EmailHelper.EmailCallback() {
        @Override
        public void onSuccess() {
            runOnUiThread(() -> {
                setLoading(false);
                tilOtp.setVisibility(View.VISIBLE);
                btnSendOtp.setText("Gửi lại mã");
                ...
            });
        }
```

`EmailHelper` dùng **JavaMail** + tài khoản Gmail có App Password để gửi email:
```java
public static void sendOTP(String toEmail, String otp, EmailCallback callback) {
    final String senderEmail = "nguyenductho0411@gmail.com";
    final String senderPassword = "gfvl elnj hpzw lcpu";
    ...
    Session session = Session.getInstance(props, new Authenticator() { ... });
    new Thread(() -> {
        try {
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(senderEmail));
            message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(toEmail));
            message.setSubject("Mã xác thực đăng ký Petshop");
            message.setText("Mã OTP của bạn là: " + otp + "\n\n...");
            Transport.send(message);
            ...
```

> 💡 **Chú ý điểm yếu:** OTP được sinh và lưu trong biến `generatedOtp` ngay tại Activity — tức là **client tự verify**. Đây là lỗ hổng (ai biết cách edit memory app có thể fake OTP). Giáo viên giỏi sẽ hỏi: "Sao em không verify OTP ở server?" → Trả lời thẳng thắn: "Project học của em chưa có backend riêng, OTP chỉ làm rào cản UX cơ bản. Nếu production em sẽ chuyển sang Firebase Cloud Functions để verify server-side."

**Bước 3: User nhập OTP + password → bấm "Đăng ký"**

Activity verify OTP cục bộ (so sánh với `generatedOtp`):
```java
if (TextUtils.isEmpty(userOtp)) {
    showError("Vui lòng nhập mã OTP");
    return;
}
if (!userOtp.equals(generatedOtp)) {
    showError("Mã OTP không chính xác");
    return;
}
if (TextUtils.isEmpty(password) || password.length() < 6) {
    showError("Mật khẩu phải có ít nhất 6 ký tự");
    return;
}
if (!password.equals(confirmPwd)) {
    showError("Mật khẩu xác nhận không khớp");
    return;
}

tvError.setVisibility(View.GONE);
authViewModel.registerWithEmail(email, password, fullName);
```

**Bước 4: ViewModel gọi `FirebaseHelper.registerWithEmail`**
```java
public void registerWithEmail(String email, String password, String fullName) {
    setLoading(true);
    FirebaseHelper.registerWithEmail(email, password, fullName, new FirebaseHelper.OnAuthCallback() {
        @Override
        public void onSuccess(String uid, String role) {
            loadUserDataAndSaveSession(uid, role);
        }
        @Override
        public void onFailure(String errorMsg) {
            setLoading(false);
            errorMessage.postValue(errorMsg);
        }
    });
}
```

**Bước 5: Helper tạo user ở Firebase Auth + Firestore**
```java
public static void registerWithEmail(String email, String password, String fullName,
                                      OnAuthCallback callback) {
    auth.createUserWithEmailAndPassword(email, password)
            .addOnSuccessListener(result -> {
                FirebaseUser user = result.getUser();
                if (user == null) {
                    callback.onFailure("Lỗi tạo tài khoản");
                    return;
                }
                UserProfileChangeRequest profileUpdate = new UserProfileChangeRequest.Builder()
                        .setDisplayName(fullName)
                        .build();
                user.updateProfile(profileUpdate);

                saveUserToFirestore(user.getUid(), fullName, email,
                        User.ROLE_CUSTOMER, User.LOGIN_EMAIL, null,
                        () -> callback.onSuccess(user.getUid(), User.ROLE_CUSTOMER));
            })
            .addOnFailureListener(e -> callback.onFailure(parseAuthError(e.getMessage())));
}
```

→ 3 việc tuần tự:
1. Firebase Auth: `createUserWithEmailAndPassword()` → tạo tài khoản, có UID
2. Update displayName trong Firebase Auth profile
3. Tạo document `users/{uid}` trong Firestore với role mặc định `CUSTOMER`

**Bước 6 & 7: Lưu session local + chuyển sang PetShopActivity** (xem `AuthViewModel.loadUserDataAndSaveSession`).

## 3.3 Đăng nhập — Flow chi tiết

Đơn giản hơn register, **4 bước**:

```
LoginActivity.attemptEmailLogin()
        │
        ▼
AuthViewModel.loginWithEmail(email, password)
        │
        ▼
FirebaseHelper.loginWithEmail()
        │
        ▼
FirebaseAuth.signInWithEmailAndPassword(email, password)
        │
        ├─ thành công → result.getUser().getUid()
        │       │
        │       ▼
        │   getUserRole(uid) → đọc Firestore field "role"
        │       │
        │       ▼
        │   callback.onSuccess(uid, role)
        │       │
        │       ▼
        │   AuthViewModel.loadUserDataAndSaveSession(uid, role)
        │       │
        │       ├─► SessionManager.saveSession(uid, name, email, role, avatar)
        │       └─► userRole.postValue(role)
        │              │
        │              ▼
        │      LoginActivity.observe → navigateByRole()
        │              │
        │              ├─ ADMIN  → AdminActivity
        │              └─ CUSTOMER → PetShopActivity
        │
        └─ thất bại → errorMessage.postValue("Sai mật khẩu")
```

## 3.4 Quên mật khẩu

Đơn giản: gọi `FirebaseAuth.sendPasswordResetEmail()` → Firebase **tự gửi email reset**, mình không cần backend.

```java
public static void sendPasswordReset(String email, OnAuthCallback callback) {
    if (email == null || email.isEmpty()) {
        callback.onFailure("Vui lòng nhập email trước");
        return;
    }
    auth.sendPasswordResetEmail(email)
            .addOnSuccessListener(v -> callback.onSuccess(null, null))
            .addOnFailureListener(e -> callback.onFailure(parseAuthError(e.getMessage())));
}
```

## 3.5 Bảng đối chiếu xử lý lỗi
```java
private static String parseAuthError(String error) {
    if (error == null) return "Có lỗi xảy ra";
    if (error.contains("INVALID_EMAIL"))      return "Email không hợp lệ";
    if (error.contains("WRONG_PASSWORD") || error.contains("INVALID_LOGIN_CREDENTIALS"))
        return "Email hoặc mật khẩu không đúng";
    if (error.contains("EMAIL_NOT_FOUND"))    return "Tài khoản không tồn tại";
    if (error.contains("EMAIL_EXISTS") || error.contains("email address is already"))
        return "Email đã được sử dụng";
    if (error.contains("WEAK_PASSWORD"))      return "Mật khẩu quá yếu (tối thiểu 6 ký tự)";
    if (error.contains("TOO_MANY_REQUESTS"))  return "Quá nhiều lần thử. Vui lòng thử lại sau";
    ...
```
→ Trick hay: dịch lỗi Firebase tiếng Anh sang tiếng Việt thân thiện trước khi đưa lên UI.

---

# PHẦN 4️⃣ — AUTH BẰNG GOOGLE (chi tiết)

Google Sign-In phức tạp hơn email vì có **3 bên** tham gia:

```
                 ┌──────────────┐
                 │  Google      │
                 │  Server      │
                 └───┬──────────┘
                     │ 3. Cấp idToken
   ┌─────────┐       │       ┌──────────────┐
   │   App   │◄──────┘──────►│   Firebase   │
   │ Android │  4. Đổi token │   Auth       │
   └─────────┘    sang user  └──────────────┘
        ▲
        │ 1. Mở popup chọn account
        │ 2. User chọn account
   ┌─────────┐
   │  User   │
   └─────────┘
```

## 4.1 Chuẩn bị (giáo viên có thể hỏi)

Trước khi viết code Android, phải làm 3 việc:

1. Vào **Google Cloud Console** → tạo OAuth 2.0 Client ID **loại "Web application"** (không phải Android).
2. Lấy chuỗi Client ID đó (có dạng `xxx.apps.googleusercontent.com`).
3. Lưu vào `local.properties`:
   ```
   GOOGLE_WEB_CLIENT_ID=xxx.apps.googleusercontent.com
   ```
4. Vào **Firebase Console** → Authentication → Sign-in method → Enable **Google provider**.
5. Trong Firebase Console → Project Settings → thêm **SHA-1 fingerprint** của file keystore Android.

> Quan trọng: Vì sao là **Web Client ID** mà không phải Android Client ID? → Vì Google Sign-In trả về `idToken` (JWT chuẩn OAuth), Firebase chỉ chấp nhận idToken được issue cho Web Client ID. Đây là quirk nhưng giáo viên giỏi sẽ hỏi.

## 4.2 Flow đầy đủ 6 bước trong code

**Bước 1: User bấm nút Google → LoginActivity khởi tạo client**
```java
private void initGoogleSignIn() {
    GoogleSignInOptions.Builder builder = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestEmail();

    if (Constants.GOOGLE_WEB_CLIENT_ID != null && !Constants.GOOGLE_WEB_CLIENT_ID.trim().isEmpty()) {
        builder.requestIdToken(Constants.GOOGLE_WEB_CLIENT_ID);
    }

    googleSignInClient = GoogleSignIn.getClient(this, builder.build());
}
```
- `requestEmail()` → yêu cầu Google trả email
- `requestIdToken(clientId)` → yêu cầu Google trả idToken (đây mới là cái Firebase cần)

**Bước 2: Bấm nút → mở intent đăng nhập của Google**
```java
private void startGoogleSignIn() {
    googleSignInClient.signOut().addOnCompleteListener(task ->
            googleSignInLauncher.launch(googleSignInClient.getSignInIntent()));
}
```
- `signOut()` trước → ép user chọn lại tài khoản (tránh tự đăng nhập tài khoản cũ).
- `signInIntent` → popup chọn account của Google.

**Bước 3: User chọn account → kết quả về qua `ActivityResultLauncher`**
```java
private final ActivityResultLauncher<Intent> googleSignInLauncher =
        registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
            Task<GoogleSignInAccount> task = GoogleSignIn.getSignedInAccountFromIntent(result.getData());
            try {
                GoogleSignInAccount account = task.getResult(ApiException.class);
                authViewModel.loginWithGoogle(account.getIdToken());
            } catch (ApiException e) {
                showError("Google sign-in thất bại: " + e.getMessage());
            }
        });
```

> 💡 **Điểm KỸ THUẬT MỚI:** `ActivityResultLauncher` là API mới thay thế `onActivityResult` (đã deprecated). Đăng ký 1 launcher, gọi `launch()`, kết quả về qua callback. An toàn về lifecycle hơn.

**Bước 4: AuthViewModel chuyển sang FirebaseHelper**
```java
public void loginWithGoogle(String idToken) {
    setLoading(true);
    FirebaseHelper.loginWithGoogle(idToken, new FirebaseHelper.OnAuthCallback() {
        @Override
        public void onSuccess(String uid, String role) {
            loadUserDataAndSaveSession(uid, role);
        }
        @Override
        public void onFailure(String errorMsg) {
            setLoading(false);
            errorMessage.postValue(errorMsg);
        }
    });
}
```

**Bước 5: FirebaseHelper đổi idToken sang Firebase user**
```java
public static void loginWithGoogle(String idToken, OnAuthCallback callback) {
    AuthCredential credential = GoogleAuthProvider.getCredential(idToken, null);
    auth.signInWithCredential(credential)
            .addOnSuccessListener(result -> {
                FirebaseUser user = result.getUser();
                if (user == null) { callback.onFailure("Lỗi đăng nhập Google"); return; }
                boolean isNewUser = result.getAdditionalUserInfo() != null
                        && result.getAdditionalUserInfo().isNewUser();
                if (isNewUser) {
                    saveUserToFirestore(
                            user.getUid(),
                            user.getDisplayName() != null ? user.getDisplayName() : "",
                            user.getEmail(),
                            User.ROLE_CUSTOMER,
                            User.LOGIN_GOOGLE,
                            user.getPhotoUrl() != null ? user.getPhotoUrl().toString() : null,
                            () -> callback.onSuccess(user.getUid(), User.ROLE_CUSTOMER)
                    );
                } else {
                    getUserRole(user.getUid(), role -> callback.onSuccess(user.getUid(), role));
                }
            })
            .addOnFailureListener(e -> callback.onFailure("Google: " + parseAuthError(e.getMessage())));
}
```

→ **Điểm hay đáng nói khi báo cáo:** Phân biệt user mới và cũ.
- User **mới** (lần đầu login Google) → tạo document `users/{uid}` với role `CUSTOMER`, loginType `GOOGLE`, lấy avatar từ Google luôn.
- User **cũ** (đã từng login) → chỉ đọc role từ Firestore.

`result.getAdditionalUserInfo().isNewUser()` là API của Firebase để phân biệt 2 trường hợp.

**Bước 6: Giống email login** → save session → navigate.

## 4.3 So sánh Email vs Google

| | Email/Password | Google Sign-In |
|---|---|---|
| Số bước | 2 (nhập → submit) | 3 (mở popup → chọn → callback) |
| Lưu password? | Có (Firebase mã hóa) | Không, dùng idToken |
| Cần OTP? | Project tự thêm | Không cần (Google verify rồi) |
| Tốc độ login lại | Nhanh | Nhanh hơn (1 click) |
| Phụ thuộc bên ngoài | Chỉ Firebase | Google + Firebase |
| Có avatar mặc định? | Không | Có (lấy từ Google profile) |

---

# PHẦN 5️⃣ — FACEBOOK LOGIN (KHÔNG CÓ TRONG PROJECT)

Tôi đã search toàn bộ source: **không có 1 dòng code nào về Facebook**. Lý do có thể là:
- Facebook Login yêu cầu app phải được **review** bởi Facebook trước khi public (nhiều thủ tục).
- Cần thêm SDK `facebook-android-sdk`, phải đăng ký app ở Facebook Developers.
- Hầu hết user Việt Nam dùng Google account, ít dùng Facebook để login app.

## 🛡️ Cách trả lời nếu giáo viên hỏi:

**Nếu giáo viên hỏi "Sao không có Facebook login?":**
> Dạ, em chỉ làm 2 phương thức: Email/Password và Google. Em chọn Google vì:
> 1. Tích hợp sẵn với Firebase, không cần qua bước review của Facebook.
> 2. Đa số user Việt Nam có Google account (do Android).
> 3. Trong phạm vi đồ án, em ưu tiên hoàn thiện flow chính (mua hàng, thanh toán VNPay) hơn là làm thêm provider.

**Nếu giáo viên hỏi "Nếu thêm Facebook thì làm thế nào?":**
> Tương tự Google, em sẽ:
> 1. Thêm dependency `facebook-android-sdk` và `firebase-auth`.
> 2. Đăng ký app trên Facebook Developers, lấy App ID.
> 3. Cấu hình `LoginManager` + `CallbackManager` của Facebook SDK.
> 4. Khi user login Facebook xong, lấy `AccessToken` rồi gọi `FacebookAuthProvider.getCredential(token)`.
> 5. Đổi credential sang Firebase: `auth.signInWithCredential(credential)` — y hệt flow Google.
>
> Code chỉ khác đoạn lấy token từ provider, còn phần Firebase/Firestore tái sử dụng được hết.

→ Câu trả lời này cho thấy **em hiểu pattern**, không phải đối phó.

---

# PHẦN 6️⃣ — ADDRESS (ĐỊA CHỈ GIAO HÀNG)

## 6.1 Tổng quan

Mỗi user có thể có **nhiều địa chỉ** (nhà, công ty, nhà bố mẹ…). Mỗi địa chỉ có thể được đánh dấu là **mặc định** (`isDefault`). Khi checkout, app tự load địa chỉ default.

## 6.2 Cấu trúc dữ liệu

**Entity `Address` (Java POJO):**
```java
public class Address {
    private String id;
    private String userId;
    private String label;                // Nhà, Công ty, ...
    private String receiverName;
    private String receiverPhone;
    private String addressLine;          // số nhà, tên đường
    private String ward;                 // phường/xã
    private String wardCode;
    private String district;             // quận/huyện
    private String districtCode;
    private String city;                 // tỉnh/thành phố
    private String cityCode;
    private boolean isDefault;
    private String createdAt;
```

**Trên Firestore:** Address là **subcollection** của user (không phải collection riêng):
```
users/{uid}/addresses/{addrId}
```

→ Vì sao chọn subcollection? Tôi suy ra từ code `AddressRepository`:
- Mỗi địa chỉ chỉ thuộc về 1 user → quan hệ "có" tự nhiên (composition).
- Khi xóa user, có thể dễ dàng cascade delete cả subcollection.
- Query "lấy tất cả địa chỉ của user X" → KHÔNG cần `whereEqualTo("userId", X)` vì path đã tự gắn user.

## 6.3 Repository — Đầy đủ CRUD + đặc biệt

**GET ALL:**
```java
public void getAddresses(String userId, Callback<List<Address>> cb) {
    db.collection(COL_USERS).document(userId)
            .collection(COL_ADDR).get()
            .addOnSuccessListener(snap -> {
                List<Address> list = new ArrayList<>();
                for (var doc : snap.getDocuments()) {
                    Address addr = doc.toObject(Address.class);
                    if (addr != null) {
                        addr.setId(doc.getId());
                        list.add(addr);
                    }
                }
                cb.onSuccess(list);
            })
            .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}
```

**ADD:**
```java
public void addAddress(String userId, Address address, Callback<String> cb) {
    String id = UUID.randomUUID().toString();
    address.setId(id);
    address.setUserId(userId);
    address.setCreatedAt(Timestamp.now().toString());
    db.collection(COL_USERS).document(userId)
            .collection(COL_ADDR).document(id).set(address)
            .addOnSuccessListener(v -> cb.onSuccess(id))
            .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}
```

**SET DEFAULT (sử dụng BATCH — ăn điểm khi báo cáo):**
```java
public void setDefault(String userId, String addressId, Callback<Void> cb) {
    getAddresses(userId, new Callback<List<Address>>() {
        public void onSuccess(List<Address> list) {
            var batch = db.batch();
            for (Address a : list) {
                var ref = db.collection(COL_USERS).document(userId)
                        .collection(COL_ADDR).document(a.getId());
                batch.update(ref, "isDefault", a.getId().equals(addressId));
            }
            batch.commit()
                    .addOnSuccessListener(v -> cb.onSuccess(null))
                    .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
        }
        public void onFailure(String err) { cb.onFailure(err); }
    });
}
```

→ **Điểm cần nhớ giải thích:**
- Quy tắc nghiệp vụ: chỉ **1 địa chỉ** được làm default.
- Cách giải: dùng **WriteBatch** — nhóm nhiều update thành 1 commit nguyên tử.
- Nếu KHÔNG dùng batch: gọi `update` riêng cho từng địa chỉ → 5 địa chỉ = 5 round-trip mạng, rủi ro nếu giữa chừng mạng đứt → có thể có 2 địa chỉ cùng `isDefault=true`.
- Dùng batch: hoặc tất cả thành công, hoặc không có gì thay đổi (atomicity).

## 6.4 Flow 4 use case của Address

### Use case A: Quản lý địa chỉ (từ Profile)

```
ProfileFragment
   │ bấm "Địa chỉ giao hàng"
   ▼
ManageAddressActivity (mode thường, pickMode = false)
   │
   ├─ loadAddresses() → AddressRepository.getAddresses()
   ▼
RecyclerView hiển thị danh sách
   │
   ├─ FAB "+" → showDialog(null) → tạo mới
   ├─ Click item → showDialog(addr) → sửa
   ├─ Nút "Mặc định" → repo.setDefault()
   └─ Nút "Xóa" → confirmDeleteAddress() → repo.deleteAddress()
```

### Use case B: Thêm địa chỉ mới

```
Bấm FAB "+"
   │
   ▼
showDialog(null)  ← truyền null = thêm mới
   │
   ▼
Dialog hiện 6 ô input (Tên, SĐT, Đường, Phường, Quận, Thành phố)
   │
   ▼ Bấm Save
Validate (Tên, SĐT, Đường bắt buộc)
   │
   ▼
new Address() + set field
   │
   ▼ Nếu là địa chỉ ĐẦU TIÊN → setDefault(true) tự động
addr.setDefault(addresses.isEmpty());
   │
   ▼
repo.addAddress(uid, addr) → Firestore
   │
   ▼ onSuccess
loadAddresses() → refresh list
```

Code:
```java
btnSave.setOnClickListener(v -> {
    String name = get(etName); if (TextUtils.isEmpty(name)) { etName.setError("Bắt buộc"); return; }
    String phone= get(etPhone); if (TextUtils.isEmpty(phone)) { etPhone.setError("Bắt buộc"); return; }
    String line = get(etLine);  if (TextUtils.isEmpty(line)) { etLine.setError("Bắt buộc"); return; }

    Address addr = existing != null ? existing : new Address();
    addr.setReceiverName(name);
    addr.setReceiverPhone(phone);
    addr.setAddressLine(line);
    addr.setWard(get(etWard));
    addr.setDistrict(get(etDist));
    addr.setCity(get(etCity));

    if (existing == null) {
        addr.setDefault(addresses.isEmpty());
        repo.addAddress(uid(), addr, new AddressRepository.Callback<>() { ... });
    } else {
        repo.updateAddress(uid(), addr, new AddressRepository.Callback<>() { ... });
    }
});
```

### Use case C: Chọn địa chỉ khi Checkout (Pick mode)

Đây là điểm THÔNG MINH của project:

```
CheckoutActivity
   │ User bấm "Đổi địa chỉ"
   ▼
Intent có flag "pick_mode = true"
   │
   ▼
ManageAddressActivity (pickMode = TRUE)
   │
   ▼ User click vào 1 địa chỉ
   │   (KHÔNG mở dialog edit như mode thường)
   ▼
setResult(RESULT_OK, intent with "selected_address_id")
finish()
   │
   ▼
CheckoutActivity.onActivityResult()
   │
   ▼
loadAddress(addrId) → cập nhật địa chỉ giao hàng + tính lại phí ship
```

Code phần "pick mode" trong ManageAddressActivity:
```java
v.setOnClickListener(x -> {
    if (pickMode) {
        Intent result = new Intent();
        result.putExtra("selected_address_id", addr.getId());
        setResult(RESULT_OK, result);
        finish();
    } else {
        showDialog(addr);
    }
});
```

Code CheckoutActivity mở manager với cờ pick_mode:
```java
View.OnClickListener changeAddressListener = v -> {
    Intent i = new Intent(this, ManageAddressActivity.class);
    i.putExtra("pick_mode", true);
    startActivityForResult(i, 100);
};
```

Code nhận kết quả về:
```java
@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    super.onActivityResult(requestCode, resultCode, data);

    if (requestCode == 100 && resultCode == RESULT_OK && data != null) {
        String addrId = data.getStringExtra("selected_address_id");
        loadAddress(addrId);
    }
}
```

→ **Đây là pattern "Activity for Result" cổ điển**, dùng để giao tiếp 2 chiều giữa 2 Activity. Mới hơn người ta dùng `ActivityResultLauncher`, nhưng pattern này vẫn dùng được (deprecated chứ chưa bỏ).

### Use case D: Tự load default khi mở Checkout
```java
private void loadAddress(String specificId) {
    String uid = ...;
    new AddressRepository().getAddresses(uid, new AddressRepository.Callback<>() {
        @Override
        public void onSuccess(List<Address> list) {
            if (list == null || list.isEmpty()) { ... return; }

            Address toSet = null;

            if (specificId != null) {                          // ưu tiên id chỉ định (từ pick mode)
                for (Address a : list) {
                    if (specificId.equals(a.getId())) { toSet = a; break; }
                }
            }

            if (toSet == null) {                               // không có chỉ định → tìm default
                for (Address a : list) {
                    if (a.isDefault()) { toSet = a; break; }
                }
            }

            if (toSet == null) toSet = list.get(0);            // không có default → lấy địa chỉ đầu

            final Address finalToSet = toSet;
            runOnUiThread(() -> setAddress(finalToSet));
        }
```

→ Thuật toán **3 mức ưu tiên** rất rõ ràng:
1. ID được chỉ định (user vừa pick)
2. Địa chỉ `isDefault = true`
3. Địa chỉ đầu tiên trong list (fallback)

---

# PHẦN 7️⃣ — NOTIFICATION (THÔNG BÁO)

Đây là phần **kỹ thuật nhất** ngoài VNPay, vì có **real-time listener** với Firestore.

## 7.1 Tổng quan

Có 3 chỗ tạo notification trong project:
1. **Khi customer đặt hàng** → notify chính customer "Đặt hàng thành công"
2. **Khi admin thay đổi trạng thái đơn** (xác nhận/giao hàng/hủy) → notify customer
3. **Khi admin gửi thông báo hệ thống** → broadcast tới tất cả customer

App có **3 chỗ HIỂN THỊ** notification:
1. **Badge đỏ trên icon chuông** ở HomeFragment (số chưa đọc, real-time)
2. **Toast notification "Có thông báo mới"** (nếu code thêm — hiện chưa có)
3. **Màn hình `NotificationActivity`** liệt kê chi tiết

## 7.2 Cấu trúc dữ liệu

**Entity `Notification`:**
```java
public class Notification {
    private String id;
    private String userId;          // người nhận
    private String title;
    private String message;
    private String type;            // ORDER, PROMO, SYSTEM
    private boolean isRead;
    private String createdAt;
    private String orderId;         // nếu là thông báo về đơn
```

**Firestore:** collection PHẲNG (không phải subcollection):
```
notifications/{notifId}
    ├── userId: "abc123"      ← người nhận
    ├── title: "Đặt hàng thành công"
    ├── message: "Đơn hàng ORD123 đã được tạo..."
    ├── type: "ORDER"
    ├── isRead: false
    ├── orderId: "uuid..."
    └── createdAt: "..."
```

→ Vì sao KHÔNG dùng subcollection `users/{uid}/notifications/{notifId}`?

Tôi đoán: vì cần **broadcast** (admin gửi cho tất cả user) — nếu là subcollection thì phải duyệt từng user mới ghi được. Dùng collection phẳng + query `whereEqualTo("userId", uid)` thì linh hoạt hơn.

## 7.3 Flow A: Tạo thông báo khi đặt hàng

Sau khi `OrderRepository.createOrder` thành công, `CheckoutActivity` tự bắn thông báo cho user:

```java
private void sendOrderCreatedNotification(String userId, String orderId, String orderCode) {
    Notification notif = new Notification();
    notif.setUserId(userId);
    notif.setTitle("Đặt hàng thành công");
    notif.setMessage("Đơn hàng " + orderCode + " đã được tạo và đang chờ xác nhận.");
    notif.setType("ORDER");
    notif.setOrderId(orderId);

    new NotificationRepository().createNotificationAsync(notif);
}
```

`createNotificationAsync` là phiên bản **"fire-and-forget"** — không cần callback (vì nếu lỡ thất bại, user vẫn đặt hàng thành công, không nên báo lỗi):
```java
public void createNotificationAsync(Notification notification) {
    String id = UUID.randomUUID().toString() + "_" + notification.getUserId();
    notification.setId(id);
    notification.setCreatedAt(Timestamp.now().toString());
    notification.setRead(false);
    db.collection(COL).document(id).set(notification)
            .addOnSuccessListener(v ->
                    Log.d("NotificationRepo", "createNotificationAsync OK: id=" + id))
            .addOnFailureListener(e ->
                    Log.e("NotificationRepo", "createNotificationAsync FAILED: " + e.getMessage()));
}
```

> Quy ước ID: `UUID + "_" + userId` → vừa unique, vừa dễ debug nhìn vào ID biết của ai.

## 7.4 Flow B: Real-time badge số chưa đọc

Đây là chỗ **kỹ thuật xịn nhất**. Khi có người tạo notification mới trong Firestore, badge ở HomeFragment **tự động tăng** mà không cần user mở app lại.

**Bước 1: Bắt đầu lắng nghe khi Fragment hiển thị**
```java
private void startUnreadNotificationListener() {
    if (tvNotificationBadge == null) return;
    String uid = FirebaseHelper.getCurrentUser() != null ? FirebaseHelper.getCurrentUser().getUid() : null;
    if (uid == null) {
        tvNotificationBadge.setVisibility(View.GONE);
        return;
    }

    if (unreadNotifListener != null) return;       // tránh đăng ký 2 lần

    unreadNotifListener = new NotificationRepository().listenUnreadCount(uid, new NotificationRepository.Callback<Long>() {
        @Override
        public void onSuccess(Long data) {
            long count = data != null ? data : 0L;
            if (getActivity() == null) return;
            getActivity().runOnUiThread(() -> renderUnreadBadge(count));
        }

        @Override
        public void onFailure(String error) {
            if (getActivity() == null) return;
            getActivity().runOnUiThread(() -> tvNotificationBadge.setVisibility(View.GONE));
        }
    });
}
```

**Bước 2: Repository đăng ký Snapshot Listener với Firestore**
```java
public ListenerRegistration listenUnreadCount(String userId, Callback<Long> cb) {
    return db.collection(COL)
            .whereEqualTo("userId", userId)
            .addSnapshotListener((snap, e) -> {
                if (e != null) {
                    cb.onSuccess(0L);
                    return;
                }
                cb.onSuccess(snap != null ? countUnread(snap.getDocuments()) : 0L);
            });
}
```

→ `addSnapshotListener` khác `get()` ở điểm: **không chỉ chạy 1 lần**. Mỗi khi data thay đổi trên Firestore, callback `(snap, e) -> { ... }` được gọi lại → tự đếm lại số chưa đọc → bắn về UI.

**Bước 3: Đếm số chưa đọc (có hỗ trợ data cũ)**
```java
private long countUnread(List<? extends DocumentSnapshot> docs) {
    long unreadCount = 0L;
    for (DocumentSnapshot doc : docs) {
        if (isUnread(doc)) unreadCount++;
    }
    return unreadCount;
}

private boolean isUnread(DocumentSnapshot doc) {
    Boolean isRead = doc.getBoolean("isRead");
    if (isRead != null) return !isRead;

    Boolean legacyRead = doc.getBoolean("read");
    if (legacyRead != null) return !legacyRead;

    // Backward compatibility: old docs without read flags are treated as unread.
    return true;
}
```

→ **Điểm hay đáng nói trong báo cáo:** Code support **2 tên field** (`isRead` mới và `read` cũ). Đây là kỹ thuật **backward compatibility** — nếu có data cũ trong database không có field `isRead`, code vẫn không crash.

**Bước 4: Render badge**
```java
private void renderUnreadBadge(long count) {
    if (tvNotificationBadge == null) return;
    if (count <= 0) {
        tvNotificationBadge.setVisibility(View.GONE);
        return;
    }

    tvNotificationBadge.setVisibility(View.VISIBLE);
    tvNotificationBadge.setText(count > 9 ? "9+" : String.valueOf(count));
}
```

**Bước 5: GỠ listener khi Fragment dừng → tránh leak**
```java
@Override public void onStop() {
    super.onStop();
    if (unreadNotifListener != null) {
        unreadNotifListener.remove();
        unreadNotifListener = null;
    }
}
```

→ **CỰC KỲ QUAN TRỌNG.** Nếu quên gỡ:
- App vẫn tiêu thụ quota Firebase mỗi giây.
- Khi user mở app lại, đăng ký listener mới → có 2 listener cùng chạy → badge tăng gấp đôi mỗi lần có update.
- Listener giữ reference đến Fragment đã destroy → memory leak.

## 7.5 Flow C: Đánh dấu đã đọc

Trong HomeFragment, khi bấm icon chuông:
```java
root.findViewById(R.id.btnNotification).setOnClickListener(v -> {
    // Hide badge immediately when user opens notification screen
    if (tvNotificationBadge != null) tvNotificationBadge.setVisibility(View.GONE);

    // Mark all as read (best effort)
    String uid = FirebaseHelper.getCurrentUser() != null ? FirebaseHelper.getCurrentUser().getUid() : null;
    if (uid != null) {
        new NotificationRepository().markAllAsRead(uid, new NotificationRepository.Callback<Void>() {
            @Override public void onSuccess(Void data) { /* no-op */ }
            @Override public void onFailure(String error) { /* no-op */ }
        });
    }

    startActivity(new Intent(requireContext(), NotificationActivity.class));
});
```

→ Pattern **Optimistic UI**: ẨN BADGE NGAY LẬP TỨC (không đợi Firestore), rồi mới gọi `markAllAsRead`. Lợi: UX mượt, không có độ trễ.

`markAllAsRead`:
```java
public void markAllAsRead(String userId, Callback<Void> cb) {
    db.collection(COL)
            .whereEqualTo("userId", userId)
            .get()
            .addOnSuccessListener(snap -> {
                long unreadCount = 0L;
                for (var doc : snap.getDocuments()) {
                    if (isUnread(doc)) {
                        unreadCount++;
                        doc.getReference().update("isRead", true, "read", true);
                    }
                }
                cb.onSuccess(null);
            })
```

→ Lưu ý: code đang `update` từng document riêng → nếu user có 100 thông báo chưa đọc thì là 100 round-trip. **Cải tiến:** nên dùng `WriteBatch.update(...)` rồi `commit()` 1 lần (giống `setDefault` ở Address). Đây là điểm bạn có thể nói khi giáo viên hỏi "có gì cần cải thiện?".

## 7.6 Flow D: Liệt kê chi tiết — NotificationActivity

Cách hiển thị **không** dùng real-time, mà dùng `get()` 1 lần (đủ rồi vì user đang ở màn này):

```java
private void loadNotifications() {
    String uid = FirebaseHelper.getCurrentUser() != null ? FirebaseHelper.getCurrentUser().getUid() : null;
    if (uid == null) {
        ...
        return;
    }
    ...
    repo.getNotifications(uid, new NotificationRepository.Callback<List<Notification>>() {
        @Override
        public void onSuccess(List<Notification> list) {
            runOnUiThread(() -> {
                progressBar.setVisibility(View.GONE);
                if (list == null || list.isEmpty()) {
                    ...
                    tvEmpty.setText("Chưa có thông báo nào");
                } else {
                    ...
                    adapter.updateData(list);
                }
            });
        }
```

Lưu ý: `getNotifications` sort theo `createdAt` **trong code Java** (chứ không dùng `orderBy` của Firestore):
```java
list.sort((n1, n2) -> {
    try {
        long ts1 = extractTimestamp(n1.getCreatedAt());
        long ts2 = extractTimestamp(n2.getCreatedAt());
        return Long.compare(ts2, ts1); // ts2 - ts1 for descending (newest first)
    } catch (Exception e) {
        return 0;
    }
});
```

→ Vì sao? Vì field `createdAt` được lưu dạng **String** (`Timestamp.now().toString()`) thay vì kiểu `Timestamp` native của Firestore → `orderBy` của Firestore không sort đúng. Đây là **điểm yếu thiết kế** — nếu giáo viên hỏi, bạn có thể nói: "Em sẽ refactor cho lưu Timestamp gốc để dùng `orderBy` server-side, đỡ phải load hết 50 docs về client mới sort."

## 7.7 Flow E: Broadcast tới tất cả customer

Repository có sẵn hàm này:
```java
public void sendToAllCustomers(String title, String message, String type, String orderId, List<User> customers) {
    if (customers == null || customers.isEmpty()) return;
    String createdAt = Timestamp.now().toString();
    ...
    for (User user : customers) {
        WriteBatch batch = db.batch();
        String notifId = UUID.randomUUID().toString() + "_" + user.getId();
        Notification notif = new Notification();
        notif.setId(notifId);
        notif.setUserId(user.getId());
        notif.setTitle(title);
        ...
        batch.set(db.collection(COL).document(notifId), notif);
        batch.commit();
    }
}
```

## 7.8 Sơ đồ tổng quát flow Notification

```
┌──────────────────────────────────────────────────────────────┐
│                   SỰ KIỆN PHÁT SINH                          │
│  - User đặt hàng → CheckoutActivity                          │
│  - Admin đổi trạng thái → AdminOrderDetailActivity           │
│  - (Tương lai) Admin broadcast → AdminActivity               │
└──────────────────────────┬───────────────────────────────────┘
                           ▼
                NotificationRepository.createNotification()
                hoặc createNotificationAsync()
                           │
                           ▼
                ┌────────────────────────┐
                │  Firestore:            │
                │  notifications/{id}    │  ← Tạo document mới
                │  { userId, title,      │
                │    message, isRead,    │
                │    createdAt, ... }    │
                └──────────┬─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
   [HomeFragment]   [NotificationActivity]
   listenUnreadCount     getNotifications
   (real-time)              (1 lần)
              │                  │
              ▼                  ▼
       badge tăng         hiển thị list
              │
              │ User bấm chuông
              ▼
       markAllAsRead → update isRead=true
       (badge tự ẩn nhờ real-time)
```

---

# 🎯 CÂU HỎI GIÁO VIÊN CÓ THỂ HỎI (về 4 phần Phần B)

### Về cấu trúc:
**Q:** "Vì sao em chia thành nhiều package mà không gộp vào 1 chỗ?"
> **A:** Để **separation of concerns**. Mỗi package có 1 vai trò: `model` chỉ giữ dữ liệu, `repository` chỉ truy cập data source, `viewmodel` chỉ giữ state UI, `view` chỉ hiển thị. Khi sửa lỗi UI em chỉ vào `view`, không lo ảnh hưởng logic database. Khi đổi backend (Firestore → REST API) em chỉ sửa `repository`, không cần đụng `view`.

### Về Firebase:
**Q:** "Firestore khác MySQL ở chỗ nào?"
> **A:** Firestore là **NoSQL** dạng document (giống JSON), không có bảng cứng. Ưu điểm: realtime listener (`addSnapshotListener`), tự sync offline, không cần dựng server, scale tự động. Nhược: không JOIN được như SQL, query phức tạp bị hạn chế. Em chọn Firestore vì project là đồ án, không có thời gian build backend riêng.

**Q:** "Sao address là subcollection mà notification là collection phẳng?"
> **A:** Address luôn thuộc về **đúng 1 user** và không cần broadcast → dùng subcollection để path tự gắn user, query "addresses của user X" nhanh và rõ ràng. Notification cần hỗ trợ **broadcast tới nhiều user** + cần query "tất cả thông báo chưa đọc trong toàn hệ thống" (cho admin) → dùng collection phẳng + `whereEqualTo("userId", X)` linh hoạt hơn.

### Về Auth:
**Q:** "Sao login Google cần Web Client ID chứ không phải Android Client ID?"
> **A:** Vì luồng đăng nhập là: Google trả `idToken` → đưa cho Firebase verify. `idToken` này phải được issue cho Web Client ID (chuẩn OAuth của Google Identity). Android Client ID dùng để xác thực SHA-1 của app, không cấp idToken.

**Q:** "OTP em tự sinh ở client có an toàn không?"
> **A:** Em thừa nhận đây là **điểm yếu**. OTP đang được sinh và verify ngay tại Activity, attacker có khả năng đọc memory hoặc decompile APK để lấy OTP. Trong production em sẽ chuyển logic sinh OTP sang **Firebase Cloud Functions** (server-side), client chỉ gửi email lên, server sinh OTP + lưu vào Firestore + gửi mail. Client gửi OTP user nhập lên server để verify. Như vậy mới chống được tấn công.

**Q:** "Project có thêm Facebook login được không?"
> **A:** Được. Em đã design pattern chung: View → ViewModel → FirebaseHelper. Để thêm Facebook em chỉ cần: (1) thêm SDK Facebook, (2) viết hàm `loginWithFacebook(token)` trong `FirebaseHelper` tương tự `loginWithGoogle()`, dùng `FacebookAuthProvider.getCredential(token)`, (3) thêm nút trong `LoginActivity`. Phần Firestore và navigation tái sử dụng được hoàn toàn.

### Về Address:
**Q:** "Vì sao dùng WriteBatch ở `setDefault`?"
> **A:** Vì nghiệp vụ yêu cầu **chỉ 1 địa chỉ default**. Nếu update từng địa chỉ tuần tự, giữa chừng mất mạng có thể có 2 địa chỉ cùng default (race condition). WriteBatch gom tất cả update thành **1 commit nguyên tử** — hoặc tất cả thành công, hoặc không có gì thay đổi.

**Q:** "Pick mode khi checkout là gì?"
> **A:** Là cờ `pick_mode = true` em truyền qua Intent khi mở `ManageAddressActivity` từ Checkout. Khi cờ này bật, click vào địa chỉ không mở dialog edit mà `setResult(RESULT_OK)` + `finish()`. Checkout nhận result qua `onActivityResult` rồi load lại địa chỉ. Đây là pattern "Activity for Result" cổ điển.

### Về Notification:
**Q:** "Real-time badge hoạt động thế nào?"
> **A:** Em dùng `addSnapshotListener` của Firestore. Khác `get()` ở chỗ nó **không chạy 1 lần** mà gọi callback **mỗi khi data thay đổi** trên server. Em đăng ký listener trong `HomeFragment.startUnreadNotificationListener()`, lưu `ListenerRegistration`, và **gỡ trong onStop()** để tránh leak. Khi có thông báo mới được tạo trên Firestore, badge tự tăng số mà user không cần làm gì.

**Q:** "Vì sao phải gỡ listener?"
> **A:** Vì 3 lý do: (1) listener vẫn ngốn quota Firebase ngay cả khi user không xem màn này, (2) khi user mở lại Fragment, đăng ký listener mới → có 2 listener cùng chạy gây nhân đôi sự kiện, (3) listener giữ reference đến Fragment đã destroy → memory leak. Em gỡ trong `onStop()` để chỉ active khi user đang xem.

**Q:** "Optimistic UI là gì? Em dùng ở đâu?"
> **A:** Là pattern UI **không đợi server**: làm UI thay đổi trước, gọi server sau. Em dùng khi user bấm chuông: em ẨN badge ngay lập tức (`setVisibility(GONE)`) rồi mới gọi `markAllAsRead` lên Firestore. Lợi: UX mượt, user không cảm thấy lag. Rủi ro nhỏ: nếu Firestore update fail, badge tạm thời ẩn nhưng lần sau mở lại sẽ hiện đúng lại (vì real-time listener đếm thật).

---

# 📌 TÓM TẮT NHANH ĐỂ HỌC THUỘC

| Chủ đề | 1 câu nhớ | Lệnh/API chính |
|---|---|---|
| **Cấu trúc** | View → ViewModel → Repository → Firebase | – |
| **Firebase** | 3 dịch vụ: Auth + Firestore + Storage, kết nối qua `google-services.json` | `FirebaseAuth.getInstance()`, `FirebaseFirestore.getInstance()` |
| **Login Email** | `signInWithEmailAndPassword` → đọc role → save session → navigate | `auth.signInWithEmailAndPassword(email, pwd)` |
| **Register Email** | `createUser...` + tạo doc Firestore + xác thực OTP qua JavaMail | `auth.createUserWithEmailAndPassword(email, pwd)` |
| **Login Google** | Lấy idToken từ Google → đổi qua Firebase Credential → signIn | `GoogleAuthProvider.getCredential(idToken, null)` |
| **Facebook** | **KHÔNG có** trong project. Nếu hỏi: pattern giống Google, chỉ đổi provider | – |
| **Address** | Subcollection của user, có 1 default, set default dùng WriteBatch | `users/{uid}/addresses/{id}` |
| **Notification** | Collection phẳng, real-time bằng `addSnapshotListener`, gỡ trong onStop | `addSnapshotListener`, `ListenerRegistration.remove()` |

---

# 🎓 Lời khuyên cuối cùng (mentor → sinh viên)

1. **Khi giáo viên hỏi, đừng đọc code — hãy giải thích flow.** Vẽ sơ đồ trên giấy: View → ViewModel → Repository → Firebase. Mọi tính năng đều theo flow này.

2. **Thuộc 3 câu trả lời mẫu:**
   - "Em dùng MVVM + Repository Pattern."
   - "View không biết về Firebase, chỉ biết ViewModel."
   - "LiveData giúp UI tự cập nhật mà không cần code đồng bộ tay."

3. **Chạy thử app + debug breakpoint** ở 3 chỗ:
   - `LoginActivity.attemptEmailLogin()` → bấm F8 step-by-step xem flow chạy đâu.
   - `HomeViewModel.loadHomeData()` → xem LiveData được set khi nào.
   - `CartRepository.addPetToCart()` → xem Transaction chạy ra sao.

4. **Trước khi bảo vệ:** in ra 2 tờ A4 — một là sơ đồ MVVM, một là sơ đồ flow đặt hàng. Cầm theo, vừa nói vừa chỉ.

5. **Nếu giáo viên hỏi "Em viết bao nhiêu %?"** — đừng nói "em viết tất cả". Hãy nói trung thực: "Em hiểu rõ phần X, Y; phần Z em tham khảo từ tài liệu/template và chỉnh sửa". Giáo viên không trừ điểm nếu bạn hiểu rõ những gì mình trình bày.

Chúc bạn bảo vệ thành công! 🎉
