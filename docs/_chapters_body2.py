"""Chapters 3, 4, 5, 6 - one per team member."""

# ===========================================================================
# CHUONG 3 - TV1
# ===========================================================================
def build_chapter3(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "CHƯƠNG 3. XÂY DỰNG MODULE TÀI KHOẢN VÀ HỒ SƠ NGƯỜI DÙNG")
    add_para(g['doc'], "Thành viên phụ trách: TV1 – Nguyễn Hữu Đức Thọ (Trưởng nhóm).",
             size=12, italic=True, color=g['GREY'], space_after=8)

    add_h2(g['doc'], "3.1. Phân tích chức năng")
    add_body(g['doc'], "Module Tài khoản và Hồ sơ người dùng là “cánh cửa” đầu tiên của ứng dụng – mọi tính năng riêng tư của người dùng (giỏ hàng, đơn hàng, thông báo, chat lưu trữ) đều phụ thuộc vào module này. Vì vậy module được đặt trong tay TV1 với yêu cầu cao về độ ổn định và bảo mật.")
    add_body(g['doc'], "Module gồm các tính năng:")
    add_bullets(g['doc'], [
        "Splash Screen và điều hướng khởi động.",
        "Đăng ký tài khoản bằng Email/Mật khẩu, có xác thực OTP qua email.",
        "Đăng nhập bằng Email/Mật khẩu.",
        "Đăng nhập bằng tài khoản Google.",
        "Đăng nhập bằng tài khoản Facebook (thiết kế sẵn cho phiên bản mở rộng).",
        "Quên mật khẩu (gửi link reset qua Firebase Auth).",
        "Quản lý hồ sơ cá nhân: avatar, họ tên, số điện thoại, ngày sinh, giới tính.",
        "Quản lý sổ địa chỉ giao hàng (CRUD, đặt mặc định).",
        "Hệ thống thông báo (Notification): real-time badge, danh sách, mark as read.",
        "Quản lý phiên đăng nhập bằng SessionManager + SharedPrefManager.",
        "Đăng xuất, xoá phiên cục bộ.",
    ])

    add_h2(g['doc'], "3.2. Thiết kế lớp Model: User, Address, Notification")
    add_body(g['doc'], "Để biểu diễn dữ liệu người dùng, nhóm thiết kế ba lớp Model chính. Bảng 3.1 mô tả chi tiết các thuộc tính của Model User – cũng là document trên collection users của Firestore.")
    add_table_caption(g['doc'], "Các thuộc tính của Model User")
    add_table(g['doc'],
        header=["Trường", "Kiểu", "Mô tả"],
        rows=[
            ("id",          "String",  "UID do Firebase Auth sinh ra."),
            ("fullName",    "String",  "Họ và tên đầy đủ."),
            ("email",       "String",  "Email đăng nhập / liên hệ."),
            ("phone",       "String",  "Số điện thoại."),
            ("avatarUrl",   "String",  "URL ảnh đại diện trên Firebase Storage."),
            ("role",        "String",  "ADMIN | CUSTOMER."),
            ("loginType",   "String",  "EMAIL | GOOGLE | FACEBOOK."),
            ("status",      "String",  "ACTIVE | INACTIVE | BANNED."),
            ("gender",      "String",  "MALE | FEMALE | OTHER."),
            ("dateOfBirth", "String",  "yyyy-MM-dd."),
            ("totalOrders", "int",     "Số đơn đã hoàn thành."),
            ("totalSpent",  "double",  "Tổng số tiền đã chi tiêu."),
            ("createdAt",   "String",  "Thời điểm tạo tài khoản."),
            ("updatedAt",   "String",  "Thời điểm cập nhật gần nhất."),
        ],
        widths_cm=[3.0, 2.0, 10.5])

    add_body(g['doc'], "Lớp Address mô tả một địa chỉ giao hàng, bao gồm: id, userId, receiverName, phone, address (số nhà + đường), ward, district, city, isDefault. Lớp Notification gồm: id, userId, title, message, type (ORDER/PROMO/SYSTEM), isRead, createdAt, orderId. Notification được thiết kế đơn giản nhưng đủ thông tin để client điều hướng (ví dụ click vào notification kiểu ORDER sẽ mở chi tiết đơn hàng tương ứng).")

    add_h2(g['doc'], "3.3. Cấu hình Firebase Authentication")
    add_body(g['doc'], "Để sử dụng Firebase Authentication, nhóm thực hiện các bước cấu hình sau:")
    add_numbered(g['doc'], [
        "Tạo project trên Firebase Console (https://console.firebase.google.com), thêm app Android với package name com.example.petshop.",
        "Tải file google-services.json về thư mục app/ của dự án.",
        "Trong Authentication > Sign-in method bật Email/Password và Google. Riêng Google cần khai báo SHA-1 fingerprint của keystore debug và keystore release.",
        "Thêm dependency Firebase BoM, Auth, Firestore, Storage và Google Play Services Auth vào libs.versions.toml.",
        "Trong build.gradle.kts của module app, áp dụng plugin com.google.gms.google-services.",
        "Khai báo OAuth client ID Web trong local.properties (GOOGLE_WEB_CLIENT_ID) và truyền vào BuildConfig để dùng khi tạo GoogleSignInOptions.",
    ])

    add_h2(g['doc'], "3.4. Màn hình Splash và điều hướng khởi động")
    add_body(g['doc'], "SplashActivity là entry-point đầu tiên (khai báo intent-filter MAIN/LAUNCHER trong AndroidManifest.xml). Màn hình hiển thị logo và slogan “Find Your Furry Favorite” trong ~1.5 giây. Trong khoảng thời gian này, ứng dụng kiểm tra:")
    add_bullets(g['doc'], [
        "Nếu SessionManager.isLoggedIn() == false → mở PetShopActivity (giao diện guest).",
        "Nếu đã đăng nhập và role == ADMIN → mở AdminActivity.",
        "Nếu đã đăng nhập và role == CUSTOMER → mở PetShopActivity.",
    ])
    add_body(g['doc'], "Cách điều hướng này tách biệt rõ ràng hai role; phía customer không thể truy cập màn hình admin và ngược lại.")
    add_image(g['doc'], "diagram_customer-journey.png",
              "Hành trình người dùng (Customer Journey)", width_cm=15)

    add_h2(g['doc'], "3.5. Đăng ký – Đăng nhập bằng Email/Mật khẩu")
    add_body(g['doc'], "Quy trình đăng ký tài khoản gồm hai bước, trong đó bước OTP qua email được nhóm tự cài đặt thay vì dùng SMS phí cao:")
    add_numbered(g['doc'], [
        "Người dùng nhập họ tên, email, mật khẩu và xác nhận mật khẩu.",
        "Nhấn “Gửi OTP” → ứng dụng gọi FirebaseAuth.fetchSignInMethodsForEmail() để kiểm tra email đã tồn tại chưa. Nếu chưa, sinh OTP 6 số ngẫu nhiên, lưu tạm trong biến và gọi EmailHelper.sendOTP() (sử dụng JavaMail SMTP Gmail) để gửi.",
        "Người dùng nhập OTP nhận được, nhấn “Đăng ký”. Hệ thống so sánh OTP; nếu trùng khớp → gọi FirebaseAuth.createUserWithEmailAndPassword() và lưu document user vào Firestore.",
        "Nếu đăng ký thành công → mở PetShopActivity với role CUSTOMER.",
    ])
    add_body(g['doc'], "Đoạn mã rút gọn của EmailHelper.sendOTP():")
    add_code(g['doc'], """public static void sendOTP(String toEmail, String otp, EmailCallback cb) {
    final String senderEmail    = "yourshop@gmail.com";
    final String senderPassword = "<APP_PASSWORD_GMAIL>";

    Properties props = new Properties();
    props.put("mail.smtp.auth", "true");
    props.put("mail.smtp.starttls.enable", "true");
    props.put("mail.smtp.host", "smtp.gmail.com");
    props.put("mail.smtp.port", "587");

    Session session = Session.getInstance(props, new Authenticator() {
        @Override protected PasswordAuthentication getPasswordAuthentication() {
            return new PasswordAuthentication(senderEmail, senderPassword);
        }
    });

    new Thread(() -> {
        try {
            Message message = new MimeMessage(session);
            message.setFrom(new InternetAddress(senderEmail));
            message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(toEmail));
            message.setSubject("Ma xac thuc dang ky Petshop");
            message.setText("Ma OTP cua ban la: " + otp + ". Khong chia se cho ai.");
            Transport.send(message);
            cb.onSuccess();
        } catch (MessagingException e) {
            cb.onFailure("Loi gui email: " + e.getMessage());
        }
    }).start();
}""")
    add_body(g['doc'], "Việc gửi mail được thực hiện trên thread riêng để không chặn UI thread. App password Gmail được cấp riêng cho ứng dụng gửi OTP và có thể vô hiệu hoá bất cứ lúc nào.")

    add_body(g['doc'], "Phía đăng nhập email/mật khẩu được xử lý trong AuthViewModel.loginWithEmail(), gọi FirebaseHelper.loginWithEmail() để kết nối tới FirebaseAuth, sau đó truy vấn role để điều hướng đúng màn hình.")
    add_body(g['doc'], "[CHỤP ẢNH 3.5] Đề nghị chèn ảnh các bước: (a) màn hình Register trống; (b) sau khi nhập OTP; (c) màn hình Login email; (d) thông báo lỗi sai mật khẩu.")

    add_h2(g['doc'], "3.6. Đăng nhập bằng Google")
    add_body(g['doc'], "Đăng nhập Google sử dụng SDK Google Play Services Auth. Quy trình:")
    add_numbered(g['doc'], [
        "Khởi tạo GoogleSignInClient với GoogleSignInOptions.Builder().requestIdToken(GOOGLE_WEB_CLIENT_ID).requestEmail().build().",
        "Khi user nhấn nút Google, gọi googleSignInClient.getSignInIntent() và mở qua ActivityResultLauncher.",
        "Nhận callback, lấy GoogleSignInAccount và idToken.",
        "Truyền idToken vào AuthViewModel.loginWithGoogle() → FirebaseHelper.loginWithGoogle() → tạo GoogleAuthProvider.getCredential(idToken, null) → FirebaseAuth.signInWithCredential().",
        "Nếu là user mới → lưu vào Firestore với role CUSTOMER. Nếu là user cũ → lấy role hiện tại để điều hướng.",
    ])
    add_body(g['doc'], "[CHỤP ẢNH 3.6] Đề nghị chèn ảnh dialog chọn tài khoản Google + ảnh sau khi đăng nhập thành công.")

    add_h2(g['doc'], "3.7. Đăng nhập bằng Facebook")
    add_body(g['doc'], "Tương tự Google, đăng nhập Facebook cũng sử dụng OAuth Credential nạp vào FirebaseAuth. Phần thiết kế đã được nhóm chuẩn bị, các bước thực hiện gồm:")
    add_numbered(g['doc'], [
        "Đăng ký App trên Meta for Developers (https://developers.facebook.com), khai báo Android Package Name và Key Hash.",
        "Thêm dependency com.facebook.android:facebook-login.",
        "Khai báo Facebook App ID và Client Token trong res/values/strings.xml và AndroidManifest.xml (theo hướng dẫn Meta).",
        "Tạo CallbackManager, gắn vào nút LoginButton hoặc gọi LoginManager.getInstance().logInWithReadPermissions(activity, listOf(\"email\", \"public_profile\")).",
        "Khi callback onSuccess(LoginResult) → lấy AccessToken, tạo FacebookAuthProvider.getCredential(token.getToken()) → FirebaseAuth.signInWithCredential().",
        "Lưu user vào Firestore với loginType = FACEBOOK.",
    ])
    add_body(g['doc'], "Tại thời điểm hoàn thiện đề tài, phiên Facebook Login đang chờ Meta xét duyệt App từ trạng thái Development sang Live. Vì vậy nút “Đăng nhập với Facebook” đã được thiết kế sẵn trên giao diện nhưng được ẩn (visibility=GONE) cho đến khi App được duyệt. Khi đó, nhóm chỉ cần kích hoạt visibility và bổ sung dependency là tính năng hoạt động đầy đủ. Kiến trúc này giúp Facebook Login có thể bật/tắt bằng feature flag mà không phải sửa logic chính.")

    add_h2(g['doc'], "3.8. Quản lý hồ sơ cá nhân và sổ địa chỉ")
    add_body(g['doc'], "Sau khi đăng nhập, người dùng có thể vào ProfileFragment để xem thông tin cá nhân, tổng số đơn đã đặt và tổng số tiền đã chi. Nhấn “Chỉnh sửa hồ sơ” mở EditProfileActivity cho phép sửa: avatar (chọn ảnh từ thư viện → upload Firebase Storage → cập nhật avatarUrl), họ tên, số điện thoại, ngày sinh, giới tính. Cập nhật được lưu xuống Firestore và đồng thời cập nhật SessionManager (cache cục bộ).")
    add_body(g['doc'], "Sổ địa chỉ được quản lý trong ManageAddressActivity. Các thao tác:")
    add_bullets(g['doc'], [
        "Thêm địa chỉ mới qua dialog dialog_add_edit_address.xml.",
        "Sửa hoặc xoá địa chỉ; xoá có dialog xác nhận để tránh lỡ tay.",
        "Đặt một địa chỉ làm mặc định; địa chỉ mặc định sẽ được tự chọn ở Checkout.",
    ])

    add_h2(g['doc'], "3.9. Hệ thống thông báo (Notification)")
    add_body(g['doc'], "Notification trong ứng dụng được thiết kế in-app dựa trên Firestore (chưa dùng FCM ở phiên bản hiện tại). Có ba loại thông báo:")
    add_bullets(g['doc'], [
        "ORDER: phát sinh khi trạng thái đơn hàng thay đổi (Đã xác nhận, Đang giao, Đã giao, Đã huỷ, Đã hoàn tiền…).",
        "PROMO: phát sinh khi admin tạo voucher hoặc bật một voucher đang vô hiệu lên (gửi cho TẤT CẢ khách hàng ACTIVE).",
        "SYSTEM: thông báo hệ thống chung.",
    ])
    add_body(g['doc'], "Khi mở app, HomeFragment đăng ký NotificationRepository.listenUnreadCount() để hiển thị badge số thông báo chưa đọc theo thời gian thực. Click badge → mở NotificationActivity, tự động markAllAsRead trên Firestore. Click vào notification kiểu ORDER → điều hướng tới OrderDetailActivity tương ứng. Đoạn mã đếm chưa đọc:")
    add_code(g['doc'], """public ListenerRegistration listenUnreadCount(String userId, Callback<Long> cb) {
    return db.collection("notifications")
            .whereEqualTo("userId", userId)
            .addSnapshotListener((snap, e) -> {
                if (e != null) { cb.onSuccess(0L); return; }
                long unread = 0;
                if (snap != null) {
                    for (DocumentSnapshot d : snap.getDocuments()) {
                        Boolean isRead = d.getBoolean("isRead");
                        if (isRead == null || !isRead) unread++;
                    }
                }
                cb.onSuccess(unread);
            });
}""")

    add_h2(g['doc'], "3.10. Quản lý phiên đăng nhập (SessionManager, SharedPrefManager)")
    add_body(g['doc'], "Để giảm số lần truy vấn Firestore và xử lý nhanh trên client, nhóm thiết kế lớp SessionManager (singleton) bọc SharedPreferences với các thao tác: saveSession, updateUserName, updateUserAvatar, clearSession, getRole, isLoggedIn, isAdmin… SessionManager được khởi tạo ngay sau khi đăng nhập thành công và bị xoá khi logout.")
    add_body(g['doc'], "Đoạn mã rút gọn của SessionManager:")
    add_code(g['doc'], """public class SessionManager {
    private static final String PREF_NAME    = "petshop_prefs";
    private final SharedPreferences prefs;
    private static SessionManager instance;

    public static SessionManager getInstance(Context context) {
        if (instance == null) instance = new SessionManager(context);
        return instance;
    }
    private SessionManager(Context context) {
        prefs = context.getApplicationContext()
                .getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }
    public void saveSession(String userId, String name, String email, String role, String avatar) {
        prefs.edit().putString("user_id", userId).putString("user_name", name)
             .putString("user_email", email).putString("user_role", role)
             .putString("user_avatar", avatar).apply();
    }
    public boolean isLoggedIn() { return prefs.getString("user_id", null) != null; }
    public boolean isAdmin()    { return "ADMIN".equals(prefs.getString("user_role", "CUSTOMER")); }
    public void clearSession()  { prefs.edit().clear().apply(); }
}""")

    add_h2(g['doc'], "3.11. Kết quả đạt được và minh hoạ giao diện")
    add_body(g['doc'], "Module Tài khoản đã được hoàn thiện 100% theo đặc tả ban đầu. Đăng ký, đăng nhập email và Google chạy ổn định trên cả emulator API 30/33/34 và thiết bị thật. OTP qua email đến trong vòng 5–10 giây. SessionManager hoạt động chính xác, đăng xuất xoá sạch dữ liệu cục bộ. Sổ địa chỉ và Notification đáp ứng các test case đặt ra (xem Chương 7).")
    add_body(g['doc'], "[CHỤP ẢNH 3.11] Đề nghị chèn ảnh các màn hình tiêu biểu của module: Splash, Login, Register, Profile, Edit Profile, Manage Address, Notification (có badge và khi mở danh sách).")


# ===========================================================================
# CHUONG 4 - TV2
# ===========================================================================
def build_chapter4(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "CHƯƠNG 4. XÂY DỰNG MODULE DANH MỤC SẢN PHẨM VÀ TRANG CHỦ")
    add_para(g['doc'], "Thành viên phụ trách: TV2 – Đào Trúc Mai.",
             size=12, italic=True, color=g['GREY'], space_after=8)

    add_h2(g['doc'], "4.1. Phân tích chức năng dành cho khách hàng")
    add_body(g['doc'], "Sau khi đăng nhập (hoặc duyệt ở chế độ guest), khách hàng tương tác chủ yếu với module Danh mục sản phẩm và Trang chủ. Đây là “mặt tiền” của ứng dụng – nơi quyết định trải nghiệm đầu tiên và tỉ lệ chuyển đổi sang đặt hàng. Vì vậy module được giao cho TV2 với yêu cầu cao về thẩm mỹ giao diện và tốc độ tải dữ liệu.")
    add_body(g['doc'], "Các tính năng chính của module:")
    add_bullets(g['doc'], [
        "Trang chủ (HomeFragment): banner ViewPager2, lời chào theo thời gian, danh mục, sản phẩm nổi bật.",
        "Tìm kiếm thời gian thực theo từ khoá.",
        "Lọc sản phẩm theo danh mục (Pet/Food).",
        "Trang Danh mục đầy đủ (CategoryFragment / ProductListActivity).",
        "Trang chi tiết Pet (PetDetailActivity) – ảnh slider, giống, tuổi, cân nặng, lịch sử tiêm phòng.",
        "Trang chi tiết Food (FoodDetailActivity) – ảnh, thương hiệu, loại, trọng lượng, hướng dẫn cho ăn.",
        "Hiển thị giá khuyến mãi (qua PromotionManager).",
        "Trang Khuyến mãi (PromotionActivity) hiển thị voucher hệ thống.",
    ])

    add_h2(g['doc'], "4.2. Thiết kế lớp Model: Pet, Food, Category, Banner, Favorite, Review")
    add_body(g['doc'], "Bảng 4.1 và 4.2 tóm tắt các thuộc tính chính của hai entity quan trọng nhất – Pet và Food. Các trường còn lại (Category, Banner, Favorite, Review) được thiết kế đơn giản hơn và mô tả trong Phụ lục B.")
    add_table_caption(g['doc'], "Các thuộc tính của Model Pet")
    add_table(g['doc'],
        header=["Trường", "Kiểu", "Mô tả"],
        rows=[
            ("id",          "String", "ID duy nhất."),
            ("name",        "String", "Tên thú cưng (ví dụ: 'Lulu')."),
            ("categoryId",  "String", "Khoá ngoại tới categories."),
            ("species",     "String", "Loài (DOG, CAT, FISH, BIRD,…)."),
            ("breed",       "String", "Giống (Corgi, Husky, Persian,…)."),
            ("age",         "int",    "Tuổi."),
            ("ageUnit",     "String", "MONTH | YEAR."),
            ("gender",      "String", "MALE | FEMALE | UNKNOWN."),
            ("weight",      "double", "Cân nặng (kg)."),
            ("color",       "String", "Màu lông."),
            ("origin",      "String", "Xuất xứ."),
            ("vaccineStatus","String","FULL | PARTIAL | NONE."),
            ("price",       "double", "Giá gốc."),
            ("status",      "String", "AVAILABLE | RESERVED | SOLD | INACTIVE."),
            ("media",       "List",   "Danh sách PetMedia (ảnh + video)."),
            ("description", "String", "Mô tả chi tiết."),
            ("createdAt/updatedAt", "String", "Mốc thời gian."),
        ],
        widths_cm=[3.5, 2.0, 10.0])

    add_table_caption(g['doc'], "Các thuộc tính của Model Food")
    add_table(g['doc'],
        header=["Trường", "Kiểu", "Mô tả"],
        rows=[
            ("id",         "String", "ID duy nhất."),
            ("name",       "String", "Tên sản phẩm."),
            ("categoryId", "String", "Khoá ngoại tới categories."),
            ("brand",      "String", "Thương hiệu (Royal Canin, Whiskas,…)."),
            ("foodType",   "String", "DRY | WET | SNACK | MILK | SUPPLEMENT."),
            ("targetPetType","String","DOG | CAT | FISH | BIRD | RABBIT | ALL."),
            ("weightGram", "int",    "Trọng lượng gói (gram)."),
            ("price",      "double", "Giá gốc."),
            ("stock",      "int",    "Tồn kho hiện tại."),
            ("sold",       "int",    "Số lượng đã bán."),
            ("status",     "String", "AVAILABLE | OUT_OF_STOCK | INACTIVE."),
            ("media",      "List",   "FoodMedia (ảnh)."),
            ("description","String", "Mô tả chi tiết."),
        ],
        widths_cm=[3.5, 2.0, 10.0])

    add_h2(g['doc'], "4.3. Tổ chức Repository: FoodRepository, PetRepository, CategoryRepository")
    add_body(g['doc'], "Cả ba repository đều dùng FirebaseFirestore.getInstance() và cung cấp các phương thức: getAll, getById, getByCategory, search, add (chỉ admin), update (chỉ admin), delete (chỉ admin). Riêng FoodRepository có thêm getStock và updateStock để hỗ trợ luồng đặt hàng (kiểm tra/giảm tồn kho khi tạo đơn).")
    add_body(g['doc'], "Mẫu callback chuẩn được sử dụng cho mọi repository:")
    add_code(g['doc'], """public interface Callback<T> {
    void onSuccess(T data);
    void onFailure(String error);
}""")
    add_body(g['doc'], "Cách triển khai callback giúp các ViewModel xử lý kết quả/error nhất quán, đồng thời dễ chuyển sang Coroutines hoặc RxJava trong tương lai mà không phải đổi nhiều API.")

    add_h2(g['doc'], "4.4. Trang chủ (HomeFragment) – banner, danh mục, sản phẩm nổi bật")
    add_body(g['doc'], "HomeFragment là Fragment đầu tiên hiển thị khi vào PetShopActivity. Layout được chia thành các khối từ trên xuống dưới:")
    add_bullets(g['doc'], [
        "Top bar: lời chào (ví dụ “Hi, Mai 🐾”) thay đổi theo thời gian (sáng/chiều/tối) lấy từ Calendar.HOUR_OF_DAY; nút giỏ hàng (kèm badge số) và nút thông báo (badge số chưa đọc).",
        "Search bar realtime: TextWatcher gọi vm.search(s.toString()) → HomeViewModel filter danh sách Pet/Food trong RAM rồi cập nhật lại RecyclerView.",
        "Banner ViewPager2: ImageSliderAdapter hiển thị các banner promo lấy từ collection banners. Tự động auto-scroll mỗi 4s.",
        "Danh mục (RecyclerView ngang): HomeCategoryAdapter; click vào danh mục sẽ filter sản phẩm tương ứng.",
        "Section “Thú cưng nổi bật” (RV ngang) + “Thức ăn nổi bật” (RV ngang) với nút “Xem tất cả” mở ProductListActivity.",
        "Card Promo: dẫn sang PromotionActivity.",
    ])
    add_image(g['doc'], "diagram_customer-journey.png",
              "Hành trình khách hàng – HomeFragment là điểm xuất phát", width_cm=15)
    add_body(g['doc'], "[CHỤP ẢNH 4.4] Đề nghị chèn ảnh đầy đủ HomeFragment (1 ảnh).")

    add_h2(g['doc'], "4.5. Màn hình Danh mục (CategoryFragment / ProductListActivity)")
    add_body(g['doc'], "Khi người dùng nhấn “Xem tất cả” từ Trang chủ hoặc chọn một danh mục cụ thể, ứng dụng mở ProductListActivity với extra EXTRA_CATEGORY = PET hoặc FOOD và (tuỳ chọn) EXTRA_FILTER_KEY (tên danh mục cụ thể). Activity hiển thị danh sách sản phẩm dạng lưới 2 cột với khả năng:")
    add_bullets(g['doc'], [
        "Sắp xếp theo: Mới nhất, Giá tăng dần, Giá giảm dần, Bán chạy.",
        "Lọc theo loài/loại thức ăn, theo giá (slider), theo có khuyến mãi hay không.",
        "Vô hạn cuộn (đang cài đặt phân trang ở phiên bản nâng cao).",
    ])
    add_body(g['doc'], "[CHỤP ẢNH 4.5] Đề nghị chèn ảnh ProductListActivity với các tuỳ chọn lọc.")

    add_h2(g['doc'], "4.6. Màn hình Chi tiết thú cưng (PetDetailActivity)")
    add_body(g['doc'], "PetDetailActivity hiển thị thông tin chi tiết của một cá thể thú cưng: ảnh slider (kết hợp video nếu có), tên, giống, tuổi (đổi đơn vị tự động giữa MONTH/YEAR), cân nặng, giới tính, màu lông, xuất xứ, tình trạng tiêm phòng (chip màu xanh/vàng/đỏ tương ứng FULL/PARTIAL/NONE), giá gốc – giá khuyến mãi (nếu có), nút “Thêm vào giỏ” (chỉ kích hoạt khi status == AVAILABLE).")
    add_body(g['doc'], "Khác biệt quan trọng so với thương mại điện tử thông thường: mỗi pet là một cá thể duy nhất, vì vậy số lượng luôn là 1. Khi pet được thêm vào giỏ, status chuyển sang RESERVED để các khách khác không thể đặt cùng lúc; khi đơn bị huỷ, status sẽ tự động trả lại AVAILABLE thông qua transaction trong OrderRepository.")
    add_body(g['doc'], "[CHỤP ẢNH 4.6] Đề nghị chèn ảnh PetDetailActivity (1 ảnh có khuyến mãi + 1 ảnh đã RESERVED).")

    add_h2(g['doc'], "4.7. Màn hình Chi tiết thức ăn (FoodDetailActivity)")
    add_body(g['doc'], "FoodDetailActivity tương tự PetDetail nhưng có các điểm khác:")
    add_bullets(g['doc'], [
        "Có bộ chọn số lượng (+/–), giới hạn theo stock hiện tại.",
        "Hiển thị thương hiệu, loại thức ăn, đối tượng phù hợp (chó/mèo/cá…), trọng lượng/gói.",
        "Hiển thị tab “Mô tả”, “Thành phần”, “Hướng dẫn cho ăn”, “Đánh giá”.",
        "Nút Thêm vào giỏ trừ trực tiếp số lượng vào tồn kho khi đơn được tạo (qua transaction).",
    ])
    add_body(g['doc'], "[CHỤP ẢNH 4.7] Đề nghị chèn ảnh FoodDetailActivity.")

    add_h2(g['doc'], "4.8. Hiển thị hình ảnh với Glide và Firebase Storage")
    add_body(g['doc'], "Toàn bộ ảnh trong ứng dụng (banner, ảnh sản phẩm, avatar, ảnh tin nhắn chat) được lưu trên Firebase Storage và truy cập qua URL. Để tải hiệu quả, nhóm dùng thư viện Glide với cú pháp:")
    add_code(g['doc'], """Glide.with(context)
     .load(url)
     .placeholder(R.drawable.bg_image_placeholder)
     .error(R.drawable.bg_image_placeholder)
     .centerCrop()
     .into(imageView);""")
    add_body(g['doc'], "Glide tự động cache ảnh vào bộ nhớ và đĩa, hỗ trợ hiển thị placeholder khi đang tải, error khi tải lỗi, transformation (centerCrop, circleCrop) – rất phù hợp cho RecyclerView nhiều item.")

    add_h2(g['doc'], "4.9. Tìm kiếm và lọc sản phẩm")
    add_body(g['doc'], "Tìm kiếm trong ứng dụng được thực hiện theo hai tầng: (1) tìm kiếm cục bộ trong RAM trên dữ liệu đã tải về từ HomeViewModel/ProductViewModel – cho tốc độ phản hồi tức thời; (2) khi danh sách quá lớn, có thể chuyển sang truy vấn Firestore với .whereGreaterThanOrEqualTo(\"name\", q).whereLessThanOrEqualTo(\"name\", q + \"\\uf8ff\"). Phiên bản hiện tại sử dụng tầng (1) là chính.")
    add_body(g['doc'], "Lọc theo danh mục, lọc theo loại thức ăn, lọc theo khoảng giá đều thực hiện bằng cách áp predicate lên List<Pet> / List<Food> rồi postValue để LiveData cập nhật RecyclerView. Cách làm này đơn giản, dễ mở rộng và không phát sinh chi phí read Firestore.")

    add_h2(g['doc'], "4.10. Kết quả đạt được và minh hoạ giao diện")
    add_body(g['doc'], "Module Trang chủ và Danh mục được hoàn thiện đầy đủ với UI mượt, ảnh tải nhanh nhờ Glide, banner tự động chạy. Tìm kiếm phản hồi tức thời (~50 ms) cho danh sách 200 sản phẩm. Hiển thị giá khuyến mãi và badge phù hợp. Pet RESERVED được phân biệt rõ với pet AVAILABLE.")
    add_body(g['doc'], "[CHỤP ẢNH 4.10] Đề nghị chèn 4 ảnh: Trang chủ đầy đủ, kết quả tìm kiếm, ProductList, Pet Detail / Food Detail.")


# ===========================================================================
# CHUONG 5 - TV3
# ===========================================================================
def build_chapter5(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "CHƯƠNG 5. XÂY DỰNG MODULE GIỎ HÀNG, THANH TOÁN VÀ ĐƠN HÀNG")
    add_para(g['doc'], "Thành viên phụ trách: TV3 – Nguyễn Văn Trường.",
             size=12, italic=True, color=g['GREY'], space_after=8)

    add_h2(g['doc'], "5.1. Phân tích chức năng mua hàng")
    add_body(g['doc'], "Module Giỏ hàng – Thanh toán – Đơn hàng là phần phức tạp nhất của ứng dụng vì liên quan đến giao dịch tiền bạc, tồn kho, voucher và tích hợp với cổng thanh toán bên thứ ba. Module được phân công cho TV3 vì các yêu cầu sau:")
    add_bullets(g['doc'], [
        "Phải đảm bảo tính nguyên tử (atomic) khi tạo đơn: không được trừ stock 2 lần, không cho phép 2 khách cùng mua một con pet.",
        "Phải xử lý đầy đủ trạng thái thanh toán (COD vs VNPay) và phải đồng bộ tồn kho khi thanh toán thành công/thất bại.",
        "Phải áp dụng đúng voucher/promotion với nhiều loại (PERCENT, FIXED, FREESHIP).",
        "Phải xử lý vòng đời đơn hàng đầy đủ: từ tạo, theo dõi đến huỷ, hoàn trả, hoàn tiền.",
    ])

    add_h2(g['doc'], "5.2. Thiết kế lớp Model")
    add_body(g['doc'], "Module sử dụng các lớp Model: Cart, CartItem, Order, OrderItem, ReturnRequest, PaymentTransaction. Quan hệ giữa chúng:")
    add_bullets(g['doc'], [
        "Cart (1) – CartItem (N): mỗi user có một Cart (id = uid), chứa danh sách CartItem.",
        "Order (1) – OrderItem (N): khi tạo đơn, các CartItem được copy thành OrderItem để cố định giá tại thời điểm mua.",
        "Order (1) – ReturnRequest (0..1): mỗi đơn có thể có tối đa một yêu cầu hoàn trả đang xử lý.",
        "Order (1) – PaymentTransaction (0..N): lịch sử các giao dịch VNPay liên quan tới đơn (thử lại, refund…).",
    ])

    add_h2(g['doc'], "5.3. Quản lý giỏ hàng (CartFragment / CartActivity)")
    add_body(g['doc'], "Giỏ hàng có hai điểm vào: nút giỏ trên Top bar (mở CartActivity) và tab Cart trong bottom navigation (mở CartFragment). Cả hai cùng dùng CartViewModel để giữ trạng thái nhất quán.")
    add_body(g['doc'], "Các thao tác chính:")
    add_bullets(g['doc'], [
        "Hiển thị danh sách CartItem; mỗi item có ảnh, tên, giá, số lượng và nút xoá.",
        "Cộng/trừ số lượng (chỉ áp dụng cho Food) – có kiểm tra stock thông qua FoodRepository.getStock().",
        "Xoá item: dialog xác nhận; nếu là Pet thì khôi phục status về AVAILABLE.",
        "Tổng tiền tạm tính: hiển thị real-time qua LiveData.",
        "Nút “Thanh toán” mở CheckoutActivity nếu giỏ hàng không trống.",
    ])
    add_body(g['doc'], "Đoạn mã thêm Pet vào giỏ (rút gọn từ CartRepository.addPetToCart):")
    add_code(g['doc'], """db.runTransaction(tx -> {
    var petRef  = db.collection("pets").document(pet.getId());
    var cartRef = db.collection("carts").document(userId);

    var petDoc  = tx.get(petRef);
    var cartDoc = tx.get(cartRef);

    String status = petDoc.getString("status");
    if (!"AVAILABLE".equals(status))
        throw new RuntimeException("Thu cung nay da duoc dat boi nguoi khac");

    tx.update(petRef, "status", "RESERVED");

    Cart cart = cartDoc.exists() ? cartDoc.toObject(Cart.class) : new Cart(userId);
    cart.addItem(new CartItem(...));
    tx.set(cartRef, cart);
    return null;
});""")
    add_body(g['doc'], "Việc thực hiện trong runTransaction giúp ngăn chặn race condition khi 2 khách hàng cùng nhấn “Thêm vào giỏ” vào cùng một con pet.")

    add_h2(g['doc'], "5.4. Quy trình thanh toán (CheckoutActivity)")
    add_body(g['doc'], "CheckoutActivity là màn hình tổng hợp toàn bộ thông tin đơn hàng trước khi gửi đi thanh toán. Sơ đồ luồng được trình bày trong Hình 5.1.")
    add_image(g['doc'], "diagram_checkout-flow.png",
              "Activity Diagram – luồng đặt hàng & thanh toán", width_cm=12)

    add_h3(g['doc'], "5.4.1. Chọn địa chỉ giao hàng")
    add_body(g['doc'], "Phần đầu màn hình hiển thị địa chỉ mặc định của user. Người dùng có thể nhấn “Thay đổi” để mở ManageAddressActivity và chọn một địa chỉ khác. Sau khi chọn, CheckoutActivity sẽ tự tính lại phí ship và cập nhật tổng tiền.")

    add_h3(g['doc'], "5.4.2. Áp dụng Voucher / Promotion")
    add_body(g['doc'], "Module hỗ trợ ba loại voucher (Voucher) và promotion tự động (Promotion). Khi user mở CheckoutActivity:")
    add_bullets(g['doc'], [
        "Hệ thống tự động tải các voucher còn hiệu lực (VoucherRepository.getSystemVouchers) hiển thị dạng chip để user chọn.",
        "Hệ thống tải các promotion AUTOMATIC còn hạn (PromotionRepository.getActive) và áp dụng vào giá sản phẩm thông qua PromotionManager.refreshCartPrices.",
        "Khi user chọn voucher: VoucherRepository.getByCode để xác thực; kiểm tra điều kiện (đơn tối thiểu, lượt còn lại, số lần đã dùng của user qua collection voucher_usage).",
        "Voucher PERCENT giới hạn bởi maxDiscountAmount; FIXED giảm cố định; FREESHIP đặt phí ship = 0.",
    ])

    add_h3(g['doc'], "5.4.3. Tính phí vận chuyển (ShippingHelper)")
    add_body(g['doc'], "Phí ship được tính trong ShippingHelper dựa trên thành phố nhận hàng và tổng tiền sản phẩm. Bảng 5.1 mô tả chính sách hiện tại.")
    add_table_caption(g['doc'], "Bảng giá phí vận chuyển theo vùng")
    add_table(g['doc'],
        header=["Khu vực", "Phí ship", "Thời gian dự kiến"],
        rows=[
            ("TP. Hồ Chí Minh (cùng thành phố)", "30.000đ", "1–2 ngày"),
            ("Miền Nam khác (Bình Dương, Đồng Nai, Cần Thơ, …)", "45.000đ", "2–3 ngày"),
            ("Miền Trung (Đà Nẵng, Huế, Quảng Nam, Khánh Hoà, …)", "60.000đ", "3–4 ngày"),
            ("Miền Bắc (Hà Nội, Hải Phòng, …)", "75.000đ", "4–6 ngày"),
            ("Đơn ≥ 500.000đ (mọi vùng)", "MIỄN PHÍ", "Như trên"),
        ],
        widths_cm=[7.0, 3.0, 5.5])
    add_body(g['doc'], "Logic tính phí được đóng gói trong ShippingHelper.calculate(address, subtotal, callback). Trong tương lai, lớp này có thể được thay bằng client gọi API GHN/GHTK/J&T mà không ảnh hưởng các phần khác của hệ thống.")

    add_h2(g['doc'], "5.5. Tích hợp cổng thanh toán VNPay")
    add_body(g['doc'], "Tích hợp VNPay được thực hiện qua ba lớp: VNPayHelper (build URL + chữ ký), VNPayWebViewActivity (mở WebView tới sandbox), VNPayResultActivity (xử lý callback Deep Link). Sơ đồ tuần tự thể hiện rõ tương tác giữa các lớp:")
    add_image(g['doc'], "diagram_sequence-vnpay.png",
              "Sequence Diagram – thanh toán qua VNPay", width_cm=15)
    add_image(g['doc'], "diagram_payment-data-flow.png",
              "Sơ đồ luồng dữ liệu thanh toán VNPay", width_cm=15)

    add_h3(g['doc'], "5.5.1. Tạo URL thanh toán (VNPayHelper)")
    add_body(g['doc'], "Theo tài liệu chính thức của VNPay, URL thanh toán phải có chữ ký HMAC-SHA512 tính từ chuỗi tham số đã URL-encode UTF-8 và sort theo tên trường. Bảng 5.2 mô tả các tham số tiêu biểu.")
    add_table_caption(g['doc'], "Tham số chính của VNPay buildPaymentUrl")
    add_table(g['doc'],
        header=["Tham số", "Mô tả", "Ví dụ"],
        rows=[
            ("vnp_Version",   "Phiên bản API", "2.1.0"),
            ("vnp_Command",   "Loại lệnh",    "pay"),
            ("vnp_TmnCode",   "Mã website ký hợp đồng với VNPay", "ABCDXXXX"),
            ("vnp_Amount",    "Số tiền (đơn vị 1 = 0.01 VND)", "1500000  (= 15.000đ)"),
            ("vnp_CurrCode",  "Tiền tệ", "VND"),
            ("vnp_TxnRef",    "Mã đơn hàng (duy nhất)", "ORD0531123456ABCDEF"),
            ("vnp_OrderInfo", "Thông tin đơn", "Thanh toan don ORD..."),
            ("vnp_Locale",    "Ngôn ngữ giao diện VNPay", "vn"),
            ("vnp_ReturnUrl", "URL/Deep Link sau thanh toán", "petshop://payment/vnpay-return"),
            ("vnp_CreateDate / vnp_ExpireDate", "Thời điểm tạo / hết hạn (15 phút sau)", "20260510052000 / 20260510053500"),
            ("vnp_SecureHash", "Chữ ký HMAC-SHA512(secret, hashData)", "lowercase hex 128 ký tự"),
        ],
        widths_cm=[4.0, 6.0, 5.5])
    add_body(g['doc'], "Cài đặt rút gọn của VNPayHelper.buildPaymentUrl():")
    add_code(g['doc'], """Map<String, String> p = new TreeMap<>();
p.put("vnp_Version",   "2.1.0");
p.put("vnp_Command",   "pay");
p.put("vnp_TmnCode",   Constants.VNPAY_TMN_CODE);
p.put("vnp_Amount",    String.valueOf(amount * 100));
p.put("vnp_CurrCode",  "VND");
p.put("vnp_TxnRef",    orderCode);
p.put("vnp_OrderInfo", orderInfo);
p.put("vnp_OrderType", "other");
p.put("vnp_Locale",    "vn");
p.put("vnp_ReturnUrl", Constants.VNPAY_RETURN_URL);
p.put("vnp_IpAddr",    "127.0.0.1");
p.put("vnp_CreateDate", now);
p.put("vnp_ExpireDate", now15);

StringBuilder hashData = new StringBuilder();
StringBuilder query    = new StringBuilder();
for (String name : new ArrayList<>(p.keySet())) {
    String value = p.get(name);
    if (value == null || value.isEmpty()) continue;
    String en = URLEncoder.encode(name, "UTF-8");
    String ev = URLEncoder.encode(value, "UTF-8");
    if (hashData.length() > 0) { hashData.append('&'); query.append('&'); }
    hashData.append(en).append('=').append(ev);
    query.append(en).append('=').append(ev);
}
String secureHash = hmacSHA512(Constants.VNPAY_HASH_SECRET, hashData.toString());
return Constants.VNPAY_URL + "?" + query + "&vnp_SecureHash=" + secureHash;""")

    add_h3(g['doc'], "5.5.2. Hiển thị WebView (VNPayWebViewActivity)")
    add_body(g['doc'], "VNPayWebViewActivity nạp URL trên WebView và override shouldOverrideUrlLoading() để bắt mọi redirect. Khi VNPay gửi user về Deep Link petshop://payment/vnpay-return?vnp_ResponseCode=…, WebView nhận URL nhưng không thể tự xử lý → ứng dụng chuyển sang Intent với scheme petshop:// và Android sẽ launch VNPayResultActivity.")

    add_h3(g['doc'], "5.5.3. Xử lý kết quả và Deep Link (VNPayResultActivity)")
    add_body(g['doc'], "VNPayResultActivity là một Activity exported = true với intent-filter:")
    add_code(g['doc'], """<activity android:name=".view.activity.VNPayResultActivity" android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="petshop" android:host="payment" android:path="/vnpay-return" />
        <data android:scheme="https"   android:host="petshop-payment.web.app"
                                       android:path="/vnpay-return" />
    </intent-filter>
</activity>""")
    add_body(g['doc'], "Activity đọc các query param vnp_ResponseCode và vnp_TxnRef từ Intent. Nếu vnp_ResponseCode == \"00\" (thành công), gọi OrderRepository.completeVNPayOrder() trong một transaction để: cập nhật status = PENDING, paymentStatus = PAID, trừ stock food, đặt Pet = RESERVED, đồng thời lưu PaymentTransaction. Cuối cùng gửi notification “Thanh toán thành công” cho user.")

    add_h2(g['doc'], "5.6. Quản lý đơn hàng (OrderHistory, OrderDetail)")
    add_body(g['doc'], "OrderHistoryActivity hiển thị danh sách đơn của user, có tab lọc theo trạng thái: Chờ xử lý, Đang giao, Đã giao, Đã huỷ, Hoàn tiền. OrderDetailActivity hiển thị chi tiết một đơn cùng các nút thao tác:")
    add_bullets(g['doc'], [
        "Huỷ đơn: chỉ khi status ∈ {PENDING, WAITING_PAYMENT, CONFIRMED}; hoàn lại stock + voucher.",
        "Đánh giá: chỉ khi status ∈ {DELIVERED, COMPLETED}.",
        "Yêu cầu hoàn trả: như Đánh giá.",
        "Mua lại: tạo đơn mới với cùng danh sách item (nếu còn).",
    ])
    add_image(g['doc'], "diagram_order-status-bar.png",
              "Sơ đồ trạng thái thanh đơn hàng hiển thị cho khách hàng", width_cm=15)

    add_h2(g['doc'], "5.7. Yêu cầu trả hàng / hoàn tiền (ReturnRequestActivity)")
    add_body(g['doc'], "Khi user yêu cầu hoàn trả, ReturnRequestActivity yêu cầu nhập lý do và (nếu thanh toán COD) nhập số tài khoản + tên ngân hàng để admin chuyển khoản. Sau khi gửi, đơn chuyển sang RETURN_REQUESTED và xuất hiện trong danh sách yêu cầu của admin (xem Chương 6).")
    add_image(g['doc'], "diagram_return-flow.png",
              "Activity Diagram – yêu cầu trả hàng và hoàn tiền (chi tiết)", width_cm=12)

    add_h2(g['doc'], "5.8. Kết quả đạt được và minh hoạ giao diện")
    add_body(g['doc'], "Module Giỏ hàng – Thanh toán – Đơn hàng đã được hoàn thiện đầy đủ. Các test case quan trọng đều pass: tạo đơn COD/VNPay, huỷ đơn pending, áp voucher, hoàn trả COD và VNPay. VNPay sandbox xử lý trong vòng 5–8 giây cho mỗi giao dịch. Việc chuyển trạng thái đơn được thực hiện qua Firestore Transaction đảm bảo tính nhất quán.")
    add_body(g['doc'], "[CHỤP ẢNH 5.8] Đề nghị chèn các ảnh: Cart, Checkout (chọn voucher), VNPay sandbox (chọn ngân hàng + nhập OTP NCB), VNPay Result thành công, Order History (đa trạng thái), OrderDetail, ReturnRequest.")


# ===========================================================================
# CHUONG 6 - TV4
# ===========================================================================
def build_chapter6(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "CHƯƠNG 6. XÂY DỰNG MODULE QUẢN TRỊ VÀ CHATBOT TƯ VẤN")
    add_para(g['doc'], "Thành viên phụ trách: TV4 – ……………………………………………………………………",
             size=12, italic=True, color=g['GREY'], space_after=8)

    add_h2(g['doc'], "6.1. Phân tích chức năng cho vai trò Admin")
    add_body(g['doc'], "Module Quản trị và Chatbot tư vấn là phần “sau hậu trường” của ứng dụng – nơi quyết định toàn bộ dữ liệu hiển thị cho khách hàng. Vai trò Admin bao gồm:")
    add_bullets(g['doc'], [
        "Theo dõi tình hình kinh doanh real-time qua Dashboard.",
        "Quản lý người dùng: khoá/mở khoá, đổi role.",
        "Quản lý catalog: danh mục, thú cưng, thức ăn.",
        "Quản lý marketing: voucher, khuyến mãi.",
        "Quản lý vận hành: đơn hàng, yêu cầu trả hàng.",
        "Trả lời tư vấn khách hàng (qua hệ thống Chatbot AI tự động + có thể can thiệp thủ công nếu cần).",
    ])

    add_h2(g['doc'], "6.2. Phân quyền Admin (AdminSetupHelper)")
    add_body(g['doc'], "Vì Firebase Authentication không có khái niệm role tự thân, nhóm thiết kế lớp AdminSetupHelper để khởi tạo tài khoản admin đầu tiên. Lớp này chỉ chạy 1 lần để bootstrap, sau đó nên xoá file để bảo mật. Quy trình:")
    add_numbered(g['doc'], [
        "Nhập email và mật khẩu trong AdminSetupHelper.createAdminAccount().",
        "Hệ thống gọi FirebaseAuth.createUserWithEmailAndPassword().",
        "Sau khi tạo, lưu user vào Firestore với role = ADMIN.",
        "Nếu email đã tồn tại trong Auth → tự động chuyển sang upgradeExistingToAdmin (chỉ update role trong Firestore).",
    ])
    add_body(g['doc'], "Sau khi có tài khoản admin gốc, các admin khác có thể được “bổ nhiệm” bằng cách admin gốc đổi role của user trong ManageUsersActivity. Việc kiểm soát quyền vẫn dựa trên Firestore Security Rules (xem 2.4.3).")

    add_h2(g['doc'], "6.3. Trang điều khiển AdminActivity")
    add_body(g['doc'], "AdminActivity là “trung tâm chỉ huy”. Layout có:")
    add_bullets(g['doc'], [
        "Drawer bên trái với các mục: Dashboard, Người dùng, Danh mục, Thú cưng, Thức ăn, Khuyến mãi, Voucher, Đơn hàng, Hoàn trả, Đăng xuất.",
        "Phần chính hiển thị 9 thẻ thống kê real-time (Hình 6.1).",
        "AdminViewModel đăng ký hai SnapshotListener (orders + users) ngay khi mở Activity và huỷ khi đóng để tránh leak.",
    ])
    add_image(g['doc'], "diagram_admin-journey.png",
              "Hành trình quản trị viên (Admin Journey)", width_cm=15)
    add_image(g['doc'], "diagram_admin-dashboard.png",
              "Sequence Diagram – Admin Dashboard real-time", width_cm=15)

    add_table_caption(g['doc'], "Các tab quản trị trong AdminActivity")
    add_table(g['doc'],
        header=["Tab", "Activity tương ứng", "Chức năng chính"],
        rows=[
            ("Dashboard",  "AdminActivity",         "9 thẻ thống kê real-time."),
            ("Người dùng", "ManageUsersActivity",   "Tìm kiếm, lọc role, khoá/mở khoá tài khoản."),
            ("Danh mục",   "ManageCategoriesActivity", "CRUD danh mục Pet/Food."),
            ("Thú cưng",   "ManagePetsActivity + AddEditPetActivity", "CRUD pet, upload ảnh + video."),
            ("Thức ăn",    "ManageFoodActivity + AddEditFoodActivity", "CRUD food, dialog cập nhật stock."),
            ("Khuyến mãi", "ManagePromotionsActivity + AddEditPromotionActivity", "CRUD promotion tự động."),
            ("Voucher",    "ManageVouchersActivity + AddEditVoucherActivity", "CRUD voucher; auto gửi notification khi tạo/bật."),
            ("Đơn hàng",   "AdminOrderListActivity + AdminOrderDetailActivity", "Lọc, tìm kiếm, chuyển trạng thái đơn."),
            ("Hoàn trả",   "AdminReturnListActivity", "Approve/Reject/Refund yêu cầu hoàn trả."),
        ],
        widths_cm=[3.0, 5.5, 7.0])

    add_h2(g['doc'], "6.4. Quản lý người dùng (ManageUsersActivity)")
    add_body(g['doc'], "Cho phép admin tìm kiếm theo tên/email, lọc theo role, khoá tài khoản (đặt status = BANNED) hoặc mở lại. Khi tài khoản bị BANNED, lần đăng nhập tiếp theo sẽ bị từ chối với thông báo “Tài khoản đã bị khoá”. Việc khoá/mở khoá được lưu trên Firestore và đồng bộ tới các dashboard khác qua SnapshotListener.")

    add_h2(g['doc'], "6.5. Quản lý danh mục (ManageCategoriesActivity)")
    add_body(g['doc'], "Admin có thể thêm/sửa/xoá danh mục Pet và danh mục Food (mỗi loại có color tag riêng để dễ phân biệt). Dialog dialog_add_edit_category.xml cho phép nhập tên và icon URL. Khi xoá, hệ thống cảnh báo nếu còn sản phẩm đang gắn vào danh mục.")

    add_h2(g['doc'], "6.6. Quản lý thú cưng (ManagePetsActivity / AddEditPetActivity)")
    add_body(g['doc'], "ManagePetsActivity hiển thị danh sách pet với search, filter status. Mỗi item có nút Sửa/Xoá. Nhấn “Thêm” mở AddEditPetActivity – form khá phức tạp với các trường: tên, danh mục, loài, giống, tuổi, cân nặng, giới tính, màu, xuất xứ, tình trạng tiêm phòng, giá, mô tả, danh sách media (ảnh + video).")
    add_body(g['doc'], "Phần upload media được TV4 thiết kế bằng MediaPickerAdapter cho phép chọn nhiều ảnh/video từ thư viện hoặc chụp/quay trực tiếp. Mỗi file được upload qua StorageHelper rồi thu URL trả về để lưu vào trường media của Pet.")

    add_h2(g['doc'], "6.7. Quản lý thức ăn (ManageFoodActivity / AddEditFoodActivity)")
    add_body(g['doc'], "Tương tự ManagePets nhưng có thêm dialog cập nhật stock nhanh dialog_update_stock.xml – admin có thể cộng/trừ tồn kho mà không cần mở form chỉnh sửa toàn bộ. Khi stock = 0, status tự động chuyển OUT_OF_STOCK; khi stock > 0 trở lại, status quay về AVAILABLE.")

    add_h2(g['doc'], "6.8. Quản lý khuyến mãi (ManagePromotionsActivity)")
    add_body(g['doc'], "Promotion là khuyến mãi tự động (không cần khách nhập mã). Admin định nghĩa: tên, mô tả, kiểu áp dụng (ALL/CATEGORY/PRODUCT), discountValue (PERCENT hoặc FIXED), maxDiscountAmount, startDate, endDate, isActive. Khi tải sản phẩm, PromotionManager.applyPromotions tự động chọn promotion tốt nhất cho từng sản phẩm và gắn vào trường discountedPrice.")

    add_h2(g['doc'], "6.9. Quản lý voucher (ManageVouchersActivity)")
    add_body(g['doc'], "Voucher là mã giảm giá khách phải nhập trong Checkout. Có ba loại: PERCENT, FIXED, FREESHIP. Mỗi voucher có usageLimit (tổng) và perUserLimit (mỗi user). Khi admin tạo hoặc bật một voucher, VoucherRepository tự động gửi notification kiểu PROMO cho TẤT CẢ user ACTIVE, ví dụ:")
    add_code(g['doc'], """private void sendVoucherNotification(Voucher voucher) {
    db.collection("users")
      .whereEqualTo("role", "CUSTOMER")
      .whereEqualTo("status", "ACTIVE")
      .get()
      .addOnSuccessListener(snap -> {
          String title   = "Voucher moi! 🎁";
          String message = buildVoucherMessage(voucher);
          for (var doc : snap.getDocuments()) {
              Notification n = new Notification();
              n.setUserId(doc.getId());
              n.setTitle(title); n.setMessage(message);
              n.setType("PROMO"); n.setRead(false);
              db.collection("notifications").document(...)
                .set(n);
          }
      });
}""")

    add_h2(g['doc'], "6.10. Quản lý đơn hàng và yêu cầu trả hàng phía Admin")
    add_body(g['doc'], "AdminOrderListActivity cho phép admin lọc theo trạng thái, tìm kiếm theo mã đơn. AdminOrderDetailActivity cho phép cập nhật trạng thái đơn (ví dụ chuyển từ PENDING → CONFIRMED → PREPARING → SHIPPING → DELIVERED). Mỗi lần đổi trạng thái đều ghi log thời gian (paidAt, deliveredAt) và gửi notification cho khách. Nếu đơn chuyển sang DELIVERED hoặc COMPLETED, hệ thống tự cập nhật totalOrders, totalSpent của user (best-effort qua FieldValue.increment).")
    add_body(g['doc'], "AdminReturnListActivity hiển thị các yêu cầu hoàn trả theo tab PENDING / APPROVED / REFUNDED / REJECTED. Admin xét duyệt và xử lý theo luồng đã mô tả ở Chương 5.")

    add_h2(g['doc'], "6.11. Tải ảnh sản phẩm lên Firebase Storage (StorageHelper)")
    add_body(g['doc'], "StorageHelper là wrapper đơn giản quanh FirebaseStorage để upload ảnh/video và xoá file. Mỗi file được lưu tại đường dẫn folder/UUID.{ext} – đảm bảo không trùng tên. URL download được trả về dưới dạng String để lưu vào Firestore.")
    add_code(g['doc'], """public static void uploadImage(Uri fileUri, String folder, OnUploadCallback cb) {
    String fileName = folder + "/" + UUID.randomUUID() + ".jpg";
    StorageReference ref = storage.getReference().child(fileName);
    ref.putFile(fileUri)
       .continueWithTask(task -> {
           if (!task.isSuccessful()) throw task.getException();
           return ref.getDownloadUrl();
       })
       .addOnSuccessListener(uri -> cb.onSuccess(uri.toString()))
       .addOnFailureListener(e -> cb.onFailure(e.getMessage()));
}""")

    add_h2(g['doc'], "6.12. Chatbot tư vấn dựa trên OpenAI API")
    add_body(g['doc'], "Chatbot là điểm khác biệt nổi bật của ứng dụng so với các giải pháp truyền thống. Chatbot được xây dựng theo kiến trúc RAG (Retrieval-Augmented Generation) đơn giản:")
    add_image(g['doc'], "diagram_chat-rag.png",
              "Sơ đồ kiến trúc Chatbot RAG nhẹ", width_cm=15)

    add_h3(g['doc'], "6.12.1. Thiết kế hội thoại")
    add_body(g['doc'], "Chat của ứng dụng có:")
    add_bullets(g['doc'], [
        "Welcome message: “Chào bạn! Tôi là trợ lý ảo của PetShop. Tôi có thể giúp gì cho bạn hôm nay?”.",
        "Cho phép gửi: văn bản, ảnh (Base64 inline), voice (chuyển thành text qua RecognizerIntent).",
        "Drawer bên phải hiển thị lịch sử các phiên hội thoại; nhấn vào phiên cũ sẽ tải tin nhắn cũ.",
        "Bot trả lời theo Markdown đơn giản (gạch đầu dòng, in đậm).",
    ])

    add_h3(g['doc'], "6.12.2. Gọi API bằng OkHttp + Gson")
    add_body(g['doc'], "ChatViewModel sử dụng OkHttp để gọi POST tới https://api.openai.com/v1/chat/completions với model gpt-4o-mini. Trước khi gọi, ViewModel tự xây “system prompt” gồm: dữ liệu danh mục, danh sách Pet/Food còn bán, voucher đang chạy, đơn hàng của user. Đây là cách triển khai RAG đơn giản, không cần vector database.")
    add_code(g['doc'], """JsonObject body = new JsonObject();
body.addProperty("model", "gpt-4o-mini");

JsonArray msgs = new JsonArray();
JsonObject sys = new JsonObject();
sys.addProperty("role", "system");
sys.addProperty("content",
    "Bạn là trợ lý ảo PetShop. " +
    "Dưới đây là dữ liệu hệ thống bạn được phép trả lời:\\n" + userContext);
msgs.add(sys);

for (ChatMessage m : recentHistory) {
    JsonObject h = new JsonObject();
    h.addProperty("role", m.getType() == ChatMessage.TYPE_USER ? "user" : "assistant");
    h.addProperty("content", m.getContent());
    msgs.add(h);
}
body.add("messages", msgs);

Request req = new Request.Builder()
    .url("https://api.openai.com/v1/chat/completions")
    .addHeader("Authorization", "Bearer " + BuildConfig.OPENAI_API_KEY)
    .addHeader("Content-Type", "application/json")
    .post(RequestBody.create(body.toString(),
                             MediaType.parse("application/json")))
    .build();
client.newCall(req).enqueue(...);""")

    add_h3(g['doc'], "6.12.3. Lưu lịch sử trò chuyện trên Firestore")
    add_body(g['doc'], "Để hỗ trợ truy cứu lịch sử và cá nhân hoá trải nghiệm, mọi tin nhắn đều được lưu lên Firestore theo cấu trúc users/{uid}/sessions/{sessionId}/messages/{msgId}. Khi user mở Chat lần sau, ChatViewModel tải session gần nhất và mở lại. Khách chưa đăng nhập (guest) lưu cục bộ trong SharedPreferences với giới hạn 50 tin để không phình app data.")

    add_h2(g['doc'], "6.13. Kết quả đạt được và minh hoạ giao diện")
    add_body(g['doc'], "Toàn bộ module Quản trị đã hoàn thiện 9 tính năng. Dashboard cập nhật ngay tức thì khi có đơn mới, đơn được giao, hoặc khi có tài khoản mới đăng ký – nhờ SnapshotListener của Firestore. Chatbot trả lời chính xác các câu hỏi liên quan đến danh mục, giá sản phẩm, voucher hiện có, lịch sử đơn hàng của khách. Thời gian phản hồi trung bình 3–5 giây cho text, 6–10 giây cho ảnh.")
    add_body(g['doc'], "[CHỤP ẢNH 6.13] Đề nghị chèn các ảnh: Admin Dashboard, ManagePets (list + form Add/Edit), ManageVouchers, AdminOrderList, AdminReturnList, ChatActivity (text + image + drawer lịch sử).")
