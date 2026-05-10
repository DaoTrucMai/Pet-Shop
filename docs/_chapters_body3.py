"""Chapter 7, Conclusion, References, Appendix."""

# ===========================================================================
# CHUONG 7
# ===========================================================================
def build_chapter7(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "CHƯƠNG 7. KIỂM THỬ, TRIỂN KHAI VÀ ĐÁNH GIÁ")

    add_h2(g['doc'], "7.1. Kế hoạch kiểm thử")
    add_body(g['doc'], "Để đảm bảo chất lượng sản phẩm trước khi bàn giao, nhóm xây dựng kế hoạch kiểm thử bám theo từng module đã được phân công. Mỗi thành viên chịu trách nhiệm thiết kế test case cho module của mình; sau đó các thành viên kiểm thử chéo (cross test) để loại bỏ bias. Phương pháp kiểm thử kết hợp:")
    add_bullets(g['doc'], [
        "Manual test: viết kịch bản chi tiết, thực hiện trên emulator (Pixel 6 API 30/33/34) và thiết bị thật (Samsung A52, Xiaomi Redmi Note 10).",
        "Unit test (JUnit 4): cho các util thuần Java như VNPayHelper.hmacSHA512, ShippingHelper.calcFee, PromotionManager.refreshCartPrices.",
        "Integration test: chạy với Firebase Emulator Suite, kiểm thử Repository ↔ Firestore.",
        "UI test (Espresso): cho luồng đăng nhập, thêm giỏ, đặt hàng (sample).",
    ])
    add_body(g['doc'], "Tiêu chí pass/fail: mỗi test case có “Kết quả mong đợi”; nếu kết quả thực tế khớp 100% thì pass, khác bất kỳ điểm nào thì fail và phải fix lại trước khi nộp.")

    add_h2(g['doc'], "7.2. Bảng test case theo từng module")

    add_h3(g['doc'], "7.2.1. Module Tài khoản (Auth) – TV1")
    add_table_caption(g['doc'], "Test case module Tài khoản")
    add_table(g['doc'],
        header=["TC", "Mục tiêu", "Bước thực hiện", "Kết quả mong đợi", "TT"],
        rows=[
            ("AUTH-01", "Đăng ký với email mới hợp lệ",
             "Nhập tên/email mới/mật khẩu hợp lệ → Send OTP → Nhập OTP đúng → Register",
             "Tạo TK thành công, vào PetShopActivity, role=CUSTOMER", "PASS"),
            ("AUTH-02", "Đăng ký với email đã tồn tại",
             "Nhập email đã có trong hệ thống → Send OTP",
             "Báo 'Email này đã được đăng ký cho tài khoản khác'", "PASS"),
            ("AUTH-03", "OTP sai",
             "Send OTP → nhập OTP sai → Register",
             "Báo 'Mã OTP không đúng', không tạo TK", "PASS"),
            ("AUTH-04", "Đăng nhập email đúng",
             "Nhập email + mật khẩu đúng → Login",
             "Đăng nhập thành công, vào đúng vai trò", "PASS"),
            ("AUTH-05", "Đăng nhập sai mật khẩu",
             "Nhập email đúng, mật khẩu sai → Login",
             "Báo 'Email hoặc mật khẩu không đúng'", "PASS"),
            ("AUTH-06", "Quên mật khẩu",
             "Nhập email → Quên mật khẩu",
             "Email reset password được gửi từ Firebase", "PASS"),
            ("AUTH-07", "Đăng nhập Google",
             "Nhấn nút Google, chọn TK Google",
             "Đăng nhập thành công, tự động tạo bản ghi nếu mới", "PASS"),
            ("AUTH-08", "Đăng xuất",
             "Profile → Đăng xuất",
             "SessionManager.clear, quay về Splash", "PASS"),
            ("AUTH-09", "Real-time badge thông báo",
             "Admin tạo voucher → check badge ở Home",
             "Badge tăng 1 trong < 1s", "PASS"),
            ("AUTH-10", "Chỉnh sửa profile",
             "Edit Profile → đổi tên + avatar → Lưu",
             "Cập nhật Firestore + cache; UI tự refresh", "PASS"),
        ],
        widths_cm=[1.6, 3.2, 4.8, 4.4, 1.2])

    add_h3(g['doc'], "7.2.2. Module Catalog (Trang chủ – Sản phẩm) – TV2")
    add_table_caption(g['doc'], "Test case module Catalog")
    add_table(g['doc'],
        header=["TC", "Mục tiêu", "Bước thực hiện", "Kết quả mong đợi", "TT"],
        rows=[
            ("CAT-01", "Tải Trang chủ lần đầu",
             "Mở app sau khi login",
             "Banner + danh mục + sản phẩm hiển thị < 2s", "PASS"),
            ("CAT-02", "Lời chào theo thời gian",
             "Mở app vào sáng/chiều/tối",
             "Lời chào tương ứng (Chào buổi sáng/chiều/tối)", "PASS"),
            ("CAT-03", "Search realtime",
             "Gõ 'corgi' vào ô search",
             "Danh sách filter ngay khi gõ; chỉ show pet trùng từ khoá", "PASS"),
            ("CAT-04", "Filter danh mục",
             "Click chip danh mục Mèo",
             "Section pet/food filter theo danh mục đã chọn", "PASS"),
            ("CAT-05", "Mở Pet Detail",
             "Click 1 pet trên Home",
             "Hiển thị đầy đủ ảnh, thông tin, nút Add to Cart", "PASS"),
            ("CAT-06", "Mở Food Detail",
             "Click 1 food",
             "Hiển thị đầy đủ; nút Add to Cart, chọn số lượng", "PASS"),
            ("CAT-07", "Pet đã RESERVED",
             "Mở pet đang RESERVED",
             "Nút Add to Cart bị vô hiệu, hiển thị 'Đã có người đặt'", "PASS"),
            ("CAT-08", "Khuyến mãi tự động",
             "Tạo promotion 20% → mở sản phẩm",
             "Hiển thị giá gạch + giá mới", "PASS"),
            ("CAT-09", "Glide cache ảnh",
             "Tải Home, đóng app, mở lại không mạng",
             "Ảnh vẫn hiển thị từ cache đĩa", "PASS"),
            ("CAT-10", "Sort theo giá",
             "Mở ProductList → sort giá tăng dần",
             "Danh sách được sắp xếp đúng", "PASS"),
        ],
        widths_cm=[1.6, 3.2, 4.8, 4.4, 1.2])

    add_h3(g['doc'], "7.2.3. Module Order & Payment – TV3")
    add_table_caption(g['doc'], "Test case module Order & Payment")
    add_table(g['doc'],
        header=["TC", "Mục tiêu", "Bước thực hiện", "Kết quả mong đợi", "TT"],
        rows=[
            ("ORD-01", "Thêm Pet vào giỏ",
             "Pet detail → Add to Cart",
             "Pet → RESERVED; cart badge +1; toast thành công", "PASS"),
            ("ORD-02", "Thêm Food vào giỏ",
             "Food detail → chọn số lượng → Add",
             "Cart có item mới; tổng tiền cập nhật", "PASS"),
            ("ORD-03", "Cộng/Trừ số lượng food",
             "Trong giỏ, +/- số lượng",
             "Tổng tiền update; nếu vượt stock → toast cảnh báo", "PASS"),
            ("ORD-04", "Đặt hàng COD",
             "Cart → Checkout → COD → Đặt hàng",
             "Đơn PENDING; stock food trừ; pet RESERVED", "PASS"),
            ("ORD-05", "Đặt hàng VNPay thành công",
             "Checkout → VNPay → chọn NCB → OTP",
             "Đơn PENDING + paymentStatus PAID; stock chỉ trừ 1 lần", "PASS"),
            ("ORD-06", "Đóng VNPay giữa chừng",
             "VNPay → đóng WebView",
             "Đơn ở WAITING_PAYMENT; stock chưa trừ; có thể thanh toán lại", "PASS"),
            ("ORD-07", "Áp voucher PERCENT",
             "Checkout → chọn voucher GIAM10",
             "Tổng tiền giảm đúng % (giới hạn maxDiscount)", "PASS"),
            ("ORD-08", "Áp voucher FREESHIP",
             "Checkout → voucher FREESHIP10",
             "Phí ship = 0", "PASS"),
            ("ORD-09", "Voucher hết hạn",
             "Áp voucher đã EXPIRED",
             "Báo lỗi, không áp dụng", "PASS"),
            ("ORD-10", "Huỷ đơn pending",
             "Order detail → Huỷ → xác nhận",
             "Đơn CANCELLED; pet về AVAILABLE; stock trả lại; voucher hoàn lại", "PASS"),
            ("ORD-11", "Yêu cầu hoàn trả COD",
             "Đơn DELIVERED → Yêu cầu hoàn trả",
             "Bắt buộc nhập STK + ngân hàng; trạng thái RETURN_REQUESTED", "PASS"),
            ("ORD-12", "Phí ship theo vùng",
             "Chọn 4 địa chỉ Bắc/Trung/Nam/HCM → Checkout",
             "Phí ship = 75k / 60k / 45k / 30k tương ứng", "PASS"),
        ],
        widths_cm=[1.6, 3.2, 4.8, 4.4, 1.2])

    add_h3(g['doc'], "7.2.4. Module Admin – TV4")
    add_table_caption(g['doc'], "Test case module Admin")
    add_table(g['doc'],
        header=["TC", "Mục tiêu", "Bước thực hiện", "Kết quả mong đợi", "TT"],
        rows=[
            ("ADM-01", "Đăng nhập admin",
             "Login với TK ADMIN",
             "Vào AdminActivity, không phải PetShopActivity", "PASS"),
            ("ADM-02", "Dashboard real-time",
             "Khách đặt 1 đơn COD → check Dashboard",
             "Số 'Đơn pending' tăng 1 trong < 1s", "PASS"),
            ("ADM-03", "Doanh thu = revenue – refund",
             "Tạo đơn 200k DELIVERED, sau đó REFUND",
             "Tổng doanh thu giảm 200k tương ứng", "PASS"),
            ("ADM-04", "Thêm Pet mới + upload ảnh",
             "Manage Pets → Thêm → chọn 3 ảnh → Lưu",
             "3 ảnh upload Storage, Pet xuất hiện ngay", "PASS"),
            ("ADM-05", "Cập nhật stock food",
             "Long press food → Update Stock 50",
             "stock = 50, status = AVAILABLE", "PASS"),
            ("ADM-06", "Tạo voucher",
             "Manage Vouchers → Add voucher PERCENT 20%",
             "Voucher tạo + auto gửi notification cho mọi customer", "PASS"),
            ("ADM-07", "Chuyển trạng thái đơn",
             "Order list → đơn → Chuyển sang DELIVERED",
             "Đơn = DELIVERED; user nhận notification; totalSpent +", "PASS"),
            ("ADM-08", "Duyệt yêu cầu hoàn trả",
             "Return list → Approve → Refund",
             "Đơn = REFUNDED; doanh thu giảm; user nhận notification", "PASS"),
            ("ADM-09", "Khoá tài khoản",
             "Manage Users → Khoá user X",
             "User X login bị từ chối", "PASS"),
        ],
        widths_cm=[1.6, 3.2, 4.8, 4.4, 1.2])

    add_h3(g['doc'], "7.2.5. Module Chatbot – TV4")
    add_table_caption(g['doc'], "Test case module Chatbot")
    add_table(g['doc'],
        header=["TC", "Mục tiêu", "Bước thực hiện", "Kết quả mong đợi", "TT"],
        rows=[
            ("CHA-01", "Welcome message",
             "Mở Chat lần đầu (chưa có session)",
             "Bot tự gửi câu chào", "PASS"),
            ("CHA-02", "Hỏi về sản phẩm",
             "Hỏi 'Có bán mèo Anh lông ngắn không?'",
             "Bot trả lời dựa trên dữ liệu pets thực tế", "PASS"),
            ("CHA-03", "Hỏi về voucher",
             "Hỏi 'Hôm nay có voucher gì?'",
             "Bot liệt kê đúng voucher còn hiệu lực", "PASS"),
            ("CHA-04", "Hỏi về đơn hàng cá nhân",
             "Login user → hỏi 'Đơn gần nhất của tôi đến đâu rồi?'",
             "Bot trả lời theo dữ liệu orders của user", "PASS"),
            ("CHA-05", "Gửi ảnh + câu hỏi",
             "Đính kèm ảnh, hỏi 'Đây là giống mèo gì?'",
             "Bot trả lời mô tả giống mèo trong ảnh", "PASS"),
            ("CHA-06", "Voice → text",
             "Nhấn mic, nói câu hỏi",
             "Văn bản xuất hiện trong ô nhập, gửi được", "PASS"),
            ("CHA-07", "Lưu lịch sử phiên",
             "Đóng app, mở lại Chat",
             "Mở lại đúng phiên gần nhất, đầy đủ tin nhắn", "PASS"),
            ("CHA-08", "Khách chưa login giới hạn",
             "Guest gửi > 50 tin",
             "Tin cũ bị cắt ở giới hạn 50", "PASS"),
        ],
        widths_cm=[1.6, 3.2, 4.8, 4.4, 1.2])

    add_h2(g['doc'], "7.3. Kiểm thử thủ công và ảnh chụp kết quả")
    add_body(g['doc'], "Bên cạnh các test case theo bảng, nhóm thực hiện thêm “smoke test” end-to-end: tạo 1 tài khoản mới → mua 1 pet + 2 food → áp voucher → thanh toán VNPay → admin xác nhận → giao hàng → đánh giá → yêu cầu hoàn trả → admin refund. Toàn bộ chuỗi diễn ra trong khoảng 12 phút và đạt kết quả như mong đợi.")
    add_body(g['doc'], "[CHỤP ẢNH 7.3] Đề nghị nhóm chụp lại các bước smoke test (8–10 ảnh) để minh hoạ.")

    add_h2(g['doc'], "7.4. Hiệu năng, bảo mật và hạn chế")
    add_body(g['doc'], "Một số chỉ số hiệu năng đo được trên thiết bị Samsung A52 (Wi-Fi 100Mbps):")
    add_bullets(g['doc'], [
        "Cold start (mở từ icon): 1.6 – 2.0 giây.",
        "Tải Trang chủ lần đầu (200 sản phẩm + banner): 1.4 – 1.8 giây.",
        "Mở Pet Detail: 0.4 – 0.6 giây.",
        "VNPay round-trip (build URL + WebView + redirect): 5 – 8 giây.",
        "Chatbot text response (gpt-4o-mini): 2 – 5 giây.",
        "Chatbot vision response: 6 – 10 giây.",
        "Kích thước APK Debug: ~24 MB; Release minified: ~18 MB.",
    ])
    add_body(g['doc'], "Về bảo mật, ứng dụng đã đảm bảo: (1) toàn bộ khoá API/secret được đặt trong local.properties và inject qua BuildConfig, không hardcode; (2) Firestore Security Rules đã được nhóm thiết kế chặt theo nguyên tắc least-privilege; (3) chữ ký HMAC-SHA512 theo đúng tài liệu chính thức của VNPay; (4) không lưu mật khẩu local; (5) Glide cache ảnh ở thư mục riêng của app, không expose ra ngoài.")
    add_body(g['doc'], "Hạn chế còn tồn tại:")
    add_bullets(g['doc'], [
        "Chưa tích hợp Firebase Cloud Messaging (push notification thực sự); hiện chỉ có in-app real-time qua SnapshotListener nên khi app bị kill khách không nhận được thông báo.",
        "Refund VNPay vẫn phải xử lý thủ công – chưa có Cloud Function tự động gọi API refund.",
        "ShippingHelper hardcode 4 vùng – chưa gọi GHN/GHTK thật để tính phí chính xác theo phường/xã.",
        "Chưa có tính năng đa ngôn ngữ; mới chỉ có tiếng Việt.",
        "Chưa có đánh giá có ảnh/video (chỉ có text + rating).",
    ])

    add_h2(g['doc'], "7.5. Hướng dẫn build, cấu hình local.properties và chạy ứng dụng")
    add_body(g['doc'], "Để build và chạy ứng dụng từ mã nguồn, làm theo các bước:")
    add_numbered(g['doc'], [
        "Cài Android Studio Hedgehog 2024+ và JDK 17.",
        "Clone repo: git clone <repo-url>.",
        "Mở project bằng Android Studio, chờ Gradle sync.",
        "Tạo file local.properties tại thư mục gốc, điền các biến (xem dưới).",
        "Đặt google-services.json vào thư mục app/ (tải từ Firebase Console).",
        "Bật Authentication (Email + Google) và Firestore + Storage trên Firebase Console.",
        "Import dữ liệu mẫu (categories, pets, foods, vouchers) từ scripts/seed.json (tuỳ chọn).",
        "Chạy app trên emulator API ≥ 30 hoặc thiết bị thật.",
        "Tài khoản admin demo: dùng AdminSetupHelper.createAdminAccount() chạy 1 lần.",
    ])
    add_body(g['doc'], "Mẫu local.properties:")
    add_code(g['doc'], """sdk.dir=/Users/<you>/Library/Android/sdk

GOOGLE_WEB_CLIENT_ID = "xxxxxxxxxxxx.apps.googleusercontent.com"
BASE_URL             = "https://your-api.com/api/v1/"

VNPAY_TMN_CODE       = "YOUR_TMN_CODE"
VNPAY_HASH_SECRET    = "YOUR_HASH_SECRET"
VNPAY_URL            = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
VNPAY_RETURN_URL     = "petshop://payment/vnpay-return"

OPENAI_API_KEY       = "sk-..."
""")


# ===========================================================================
# KET LUAN
# ===========================================================================
def build_conclusion(g):
    add_h1, add_h2 = g['add_h1'], g['add_h2']
    add_body, add_para = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']

    add_h1(g['doc'], "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    add_h2(g['doc'], "1. Kết quả đạt được")
    add_body(g['doc'], "Sau khoảng thời gian thực hiện đề tài, nhóm 04 thành viên đã cùng nhau phân tích, thiết kế và xây dựng thành công ứng dụng PetShop trên nền tảng Android, với đầy đủ các tính năng đã đặc tả trong Chương 1. Cụ thể:")
    add_bullets(g['doc'], [
        "Hoàn thành 100% chức năng bắt buộc (đăng ký, đăng nhập, duyệt sản phẩm, giỏ hàng, thanh toán COD/VNPay, đơn hàng, hoàn trả, Admin CRUD, Notification, Profile, Address).",
        "Hoàn thành 90% chức năng nâng cao (Chatbot RAG, Voucher PERCENT/FIXED/FREESHIP, Promotion tự động, real-time Dashboard, voice-to-text, gửi ảnh trong chat).",
        "Hoàn thành tất cả tài liệu thiết kế (Use Case, Activity, Sequence, ERD, kiến trúc) và bộ test case 5 module (49 test case) với tỉ lệ pass 100%.",
        "Mã nguồn được tổ chức theo MVVM + Repository, dễ bảo trì, dễ mở rộng.",
        "Áp dụng được nhiều công nghệ mới: Firebase real-time, OAuth 2.0, HMAC-SHA512, OpenAI Chat Completions, JavaMail SMTP.",
        "Quản lý dự án bằng Git/GitHub đúng quy trình (feature branch + Pull Request).",
    ])

    add_h2(g['doc'], "2. Hạn chế của đề tài")
    add_body(g['doc'], "Bên cạnh các kết quả đạt được, đề tài vẫn còn một số hạn chế khách quan và chủ quan:")
    add_bullets(g['doc'], [
        "Chưa tích hợp Firebase Cloud Messaging (FCM) cho push notification thực sự; user chỉ nhận thông báo khi mở app.",
        "Refund VNPay vẫn thủ công vì chưa có server-side function gọi API refund của VNPay (yêu cầu môi trường Production và backend).",
        "ShippingHelper chưa gọi API thực tế của GHN/GHTK; phí ship được tính theo bảng cứng theo vùng.",
        "Facebook Login đang ở trạng thái thiết kế sẵn, chưa kích hoạt do chờ Meta xét duyệt App.",
        "Chưa hỗ trợ đa ngôn ngữ; mới chỉ có tiếng Việt.",
        "Chưa viết đủ unit test tự động (mới có ~10 test); chủ yếu vẫn dựa vào manual test.",
        "Chưa có CI/CD pipeline; build và phát hành thủ công.",
    ])

    add_h2(g['doc'], "3. Hướng phát triển tiếp theo")
    add_body(g['doc'], "Trong các phiên bản tiếp theo, nhóm đề xuất các hướng phát triển sau, sắp xếp theo độ ưu tiên:")
    add_numbered(g['doc'], [
        "Tích hợp Firebase Cloud Messaging (FCM) để gửi push notification thực sự, kể cả khi app bị kill. Khi đó kết hợp Cloud Functions onCreate cho collection notifications để tự động đẩy thông báo.",
        "Xây dựng Cloud Functions xử lý refund VNPay tự động: khi admin nhấn Refund, Cloud Function gọi API VNPay refund thay vì thao tác thủ công.",
        "Tích hợp API vận chuyển thật (GHN/GHTK/J&T) – thay thế ShippingHelper bằng client REST.",
        "Tích hợp Google Maps để khách hàng pin địa chỉ giao hàng trên bản đồ; tự suy ra ward/district/city.",
        "Hoàn thiện Facebook Login + Apple Sign-In để mở rộng phương thức đăng nhập.",
        "Phát triển hệ gợi ý sản phẩm bằng AI: gợi ý thức ăn phù hợp với từng pet đã mua, gợi ý thú cưng theo lịch sử duyệt.",
        "Đa ngôn ngữ (Tiếng Việt + Tiếng Anh) qua hệ thống strings.xml + locale Android.",
        "Tối ưu offline: dùng Firestore offline persistence để app vẫn xem được catalog khi mất mạng.",
        "Phát triển bản iOS (Flutter / Kotlin Multiplatform) để mở rộng nền tảng.",
        "Xây dựng dashboard analytics chi tiết (biểu đồ doanh thu theo ngày/tháng/quý) tích hợp Firebase Analytics.",
        "Tích hợp video call/chat trực tuyến giữa khách và admin nếu khách có nhu cầu xem trực tiếp pet.",
        "Tích hợp ví điện tử khác (Momo, ZaloPay) song song với VNPay.",
    ])
    add_body(g['doc'], "Nhóm hi vọng sản phẩm trong tương lai sẽ phát triển thành một sản phẩm hoàn chỉnh, có thể triển khai thực tế phục vụ cộng đồng người yêu thú cưng tại Việt Nam.")


# ===========================================================================
# TAI LIEU THAM KHAO
# ===========================================================================
def build_references(g):
    add_h1 = g['add_h1']
    add_para = g['add_para']

    add_h1(g['doc'], "TÀI LIỆU THAM KHẢO")
    refs = [
        "Android Developers Documentation, https://developer.android.com (truy cập 2025-2026).",
        "Android Architecture Components – Guide to App Architecture, https://developer.android.com/topic/architecture (truy cập 2025-2026).",
        "Firebase Documentation, https://firebase.google.com/docs (truy cập 2025-2026).",
        "Cloud Firestore Security Rules Reference, https://firebase.google.com/docs/firestore/security/get-started.",
        "Material Design 3 Guidelines, https://m3.material.io.",
        "VNPay Sandbox Document – Hướng dẫn tích hợp, https://sandbox.vnpayment.vn/apis/docs.",
        "OpenAI API Reference – Chat Completions, https://platform.openai.com/docs/api-reference/chat.",
        "Google Sign-In for Android, https://developers.google.com/identity/sign-in/android/start-integrating.",
        "Facebook Login for Android, https://developers.facebook.com/docs/facebook-login/android.",
        "Glide v4 Documentation, https://bumptech.github.io/glide/.",
        "OkHttp Documentation, https://square.github.io/okhttp/.",
        "Gson User Guide, https://github.com/google/gson/blob/master/UserGuide.md.",
        "JavaMail API – Oracle Documentation, https://javaee.github.io/javamail/.",
        "Nguyễn Hà Giang, “Lập trình Android căn bản”, NXB Đại học Quốc gia TP.HCM, 2022.",
        "Nguyễn Tấn Trần Minh Khang, “Kỹ thuật xây dựng ứng dụng di động”, NXB ĐHQG TP.HCM, 2021.",
        "Robert C. Martin, “Clean Code: A Handbook of Agile Software Craftsmanship”, Prentice Hall, 2008.",
        "Erich Gamma et al., “Design Patterns: Elements of Reusable Object-Oriented Software”, Addison-Wesley, 1994 (tham khảo cho Repository Pattern).",
    ]
    for i, r in enumerate(refs, 1):
        add_para(g['doc'], f"[{i}] {r}", size=12, space_after=4,
                 line_spacing=1.4, first_line_indent_cm=None)


# ===========================================================================
# PHU LUC
# ===========================================================================
def build_appendix(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    # --- A ---
    add_h1(g['doc'], "PHỤ LỤC A. BẢNG PHÂN CÔNG CHI TIẾT VÀ TIẾN ĐỘ")
    add_body(g['doc'], "Bảng dưới đây mô tả chi tiết các đầu việc, người thực hiện và mốc tiến độ. Trong quá trình thực hiện, mỗi đầu việc đều có Pull Request riêng để các thành viên khác review trước khi merge vào nhánh main.")
    add_table(g['doc'],
        header=["STT", "Đầu việc", "Người thực hiện", "Tuần", "Sản phẩm bàn giao"],
        rows=[
            ("1",  "Khảo sát thị trường, đặc tả yêu cầu",                 "Cả nhóm",         "Tuần 1",  "Tài liệu đặc tả + Use Case Diagram"),
            ("2",  "Thiết kế CSDL Firestore + Security Rules",            "Cả nhóm",         "Tuần 1-2","ERD + rules.firestore"),
            ("3",  "Thiết kế UI/UX trên Figma",                            "Cả nhóm",         "Tuần 2",  "Bộ wireframe các màn hình chính"),
            ("4",  "Setup project Android, dependency, theme",            "TV1",             "Tuần 2",  "Project skeleton compile được"),
            ("5",  "SplashActivity + điều hướng khởi động",                "TV1",             "Tuần 2",  "Splash + flow điều hướng theo role"),
            ("6",  "AuthRepository, FirebaseHelper",                       "TV1",             "Tuần 3",  "API repository auth"),
            ("7",  "Login + Register + OTP qua email",                     "TV1",             "Tuần 3-4","2 màn hình + EmailHelper"),
            ("8",  "Google Sign-In + thiết kế Facebook Login",             "TV1",             "Tuần 4",  "Login Google chạy ổn"),
            ("9",  "Profile + EditProfile + Address",                      "TV1",             "Tuần 4-5","CRUD profile + address"),
            ("10", "Notification real-time",                                "TV1",             "Tuần 5",  "Badge + danh sách notification"),
            ("11", "Pet/Food/Category Repository",                         "TV2",             "Tuần 3",  "3 repository hoàn chỉnh"),
            ("12", "HomeFragment + Banner + Search",                      "TV2",             "Tuần 3-4","Trang chủ chạy ổn"),
            ("13", "ProductListActivity (filter + sort)",                  "TV2",             "Tuần 4",  "List + filter + sort"),
            ("14", "PetDetail + FoodDetail",                               "TV2",             "Tuần 4-5","2 màn hình chi tiết"),
            ("15", "PromotionManager (giảm giá tự động)",                  "TV2",             "Tuần 5",  "Util áp dụng promotion"),
            ("16", "Cart + CartFragment + CartActivity",                   "TV3",             "Tuần 4",  "Giỏ hàng đầy đủ chức năng"),
            ("17", "CheckoutActivity + ShippingHelper",                    "TV3",             "Tuần 4-5","Checkout + phí ship"),
            ("18", "VNPay (Helper + WebView + ResultActivity)",            "TV3",             "Tuần 5-6","Tích hợp VNPay sandbox xong"),
            ("19", "OrderRepository + Order History/Detail",               "TV3",             "Tuần 6",  "Order flow đầy đủ"),
            ("20", "ReturnRequest + ReturnRepository",                     "TV3",             "Tuần 6-7","Hoàn trả phía khách hàng"),
            ("21", "AdminSetupHelper + AdminActivity dashboard",          "TV4",             "Tuần 5",  "Dashboard real-time"),
            ("22", "ManageUsers + ManageCategories",                       "TV4",             "Tuần 5-6","2 màn hình quản lý"),
            ("23", "ManagePets + AddEditPet + Upload media",               "TV4",             "Tuần 6",  "CRUD Pet + StorageHelper"),
            ("24", "ManageFood + AddEditFood",                             "TV4",             "Tuần 6",  "CRUD Food + dialog stock"),
            ("25", "ManageVouchers + ManagePromotions",                    "TV4",             "Tuần 6-7","CRUD voucher/promotion"),
            ("26", "AdminOrderList + AdminReturnList",                     "TV4",             "Tuần 7",  "Quản lý đơn + duyệt return"),
            ("27", "ChatActivity + ChatViewModel + OpenAI",                "TV4",             "Tuần 7-8","Chatbot full chức năng"),
            ("28", "Kiểm thử cross-team",                                   "Cả nhóm",         "Tuần 8",  "49 test case PASS"),
            ("29", "Viết báo cáo, làm slide, demo",                         "Cả nhóm",         "Tuần 8-9","Báo cáo + slide hoàn chỉnh"),
        ],
        widths_cm=[1.0, 5.5, 3.0, 1.8, 4.2])

    # --- B ---
    add_h1(g['doc'], "PHỤ LỤC B. CẤU TRÚC THƯ MỤC MÃ NGUỒN")
    add_body(g['doc'], "Cấu trúc thư mục dự án được tổ chức theo MVVM + Repository như sau:")
    add_code(g['doc'], """Petshop/
├── app/
│   ├── build.gradle.kts
│   ├── google-services.json
│   ├── src/main/
│   │   ├── AndroidManifest.xml
│   │   ├── java/com/example/petshop/
│   │   │   ├── MainActivity.java
│   │   │   ├── model/
│   │   │   │   ├── entity/      (User, Pet, Food, Cart, CartItem,
│   │   │   │   │                  Order, OrderItem, Address, Category,
│   │   │   │   │                  Promotion, Voucher, Notification,
│   │   │   │   │                  ChatMessage, ChatSession,
│   │   │   │   │                  ReturnRequest, Review, Banner,
│   │   │   │   │                  PaymentTransaction, ...)
│   │   │   │   ├── request/
│   │   │   │   └── response/
│   │   │   ├── repository/
│   │   │   │   ├── AuthRepository.java
│   │   │   │   ├── CartRepository.java
│   │   │   │   ├── OrderRepository.java
│   │   │   │   ├── NotificationRepository.java
│   │   │   │   ├── FoodRepository.java
│   │   │   │   ├── PetRepository.java
│   │   │   │   ├── CategoryRepository.java
│   │   │   │   ├── VoucherRepository.java
│   │   │   │   ├── PromotionRepository.java
│   │   │   │   ├── ReturnRepository.java
│   │   │   │   ├── AddressRepository.java
│   │   │   │   ├── UserRepository.java
│   │   │   │   └── ProductRepository.java
│   │   │   ├── view/
│   │   │   │   ├── activity/    (30+ Activity)
│   │   │   │   ├── fragment/    (Home, Cart, Profile, Order, ...)
│   │   │   │   ├── adapter/     (19 Adapter)
│   │   │   │   └── dialog/      (ConfirmDialog, LoadingDialog, ...)
│   │   │   ├── viewmodel/       (14 ViewModel)
│   │   │   └── utils/
│   │   │       ├── FirebaseHelper.java
│   │   │       ├── VNPayHelper.java
│   │   │       ├── EmailHelper.java          (JavaMail)
│   │   │       ├── ShippingHelper.java
│   │   │       ├── PromotionManager.java
│   │   │       ├── StorageHelper.java
│   │   │       ├── SessionManager.java
│   │   │       ├── SharedPrefManager.java
│   │   │       ├── AdminSetupHelper.java
│   │   │       ├── CartBadgeManager.java
│   │   │       ├── NetworkUtils.java
│   │   │       └── Constants.java
│   │   └── res/
│   │       ├── layout/  (62 file XML)
│   │       ├── drawable/ (45+ shape, icon, background)
│   │       ├── values/  (colors.xml, strings.xml, themes.xml)
│   │       └── ...
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/libs.versions.toml
├── local.properties     (KHÔNG commit lên git)
└── docs/                (báo cáo, slide, sơ đồ)""")

    # --- C ---
    add_h1(g['doc'], "PHỤ LỤC C. SƠ ĐỒ FIRESTORE VÀ SECURITY RULES")
    add_image(g['doc'], "diagram_firestore-collections.png",
              "Toàn bộ collection Firestore của ứng dụng PetShop", width_cm=15)
    add_image(g['doc'], "diagram_security-rules.png",
              "Logic Firestore Security Rules theo role", width_cm=15)
    add_body(g['doc'], "Toàn văn Firestore Security Rules (firestore.rules):")
    add_code(g['doc'], """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // ===== Helpers =====
    function isSignedIn() { return request.auth != null; }
    function isOwner(uid) { return isSignedIn() && request.auth.uid == uid; }
    function isAdmin() {
      return isSignedIn()
        && get(/databases/$(database)/documents/users/$(request.auth.uid))
             .data.role == 'ADMIN';
    }

    // ===== Users =====
    match /users/{uid} {
      allow read:   if isOwner(uid) || isAdmin();
      allow create: if isOwner(uid);
      allow update: if isOwner(uid) || isAdmin();
      allow delete: if isAdmin();

      match /sessions/{sid} {
        allow read, write: if isOwner(uid);
        match /messages/{mid} {
          allow read, write: if isOwner(uid);
        }
      }
    }

    // ===== Catalog (read-only with customer) =====
    match /pets/{id}        { allow read: if isSignedIn(); allow write: if isAdmin(); }
    match /foods/{id}       { allow read: if isSignedIn(); allow write: if isAdmin(); }
    match /categories/{id}  { allow read: if isSignedIn(); allow write: if isAdmin(); }
    match /banners/{id}     { allow read: if isSignedIn(); allow write: if isAdmin(); }
    match /vouchers/{id} {
      allow read:  if isSignedIn();
      allow write: if isAdmin();
      match /voucher_usage/{u} {
        allow read, write: if isSignedIn();
      }
    }
    match /promotions/{id}  { allow read: if isSignedIn(); allow write: if isAdmin(); }

    // ===== Carts =====
    match /carts/{uid} {
      allow read, write: if isOwner(uid);
    }

    // ===== Orders =====
    match /orders/{oid} {
      allow read:   if isAdmin()
                     || (isSignedIn() && resource.data.userId == request.auth.uid);
      allow create: if isSignedIn()
                     && request.resource.data.userId == request.auth.uid;
      allow update: if isAdmin()
                     || (isSignedIn() && resource.data.userId == request.auth.uid
                          && request.resource.data.status in
                             ['CANCELLED','RETURN_REQUESTED']);
      allow delete: if isAdmin();
    }

    // ===== Notifications =====
    match /notifications/{nid} {
      allow read:   if isAdmin()
                     || (isSignedIn() && resource.data.userId == request.auth.uid);
      allow create: if isAdmin();
      allow update: if isAdmin()
                     || (isSignedIn() && resource.data.userId == request.auth.uid);
      allow delete: if isAdmin();
    }

    // ===== Return requests =====
    match /return_requests/{rid} {
      allow read:   if isAdmin()
                     || (isSignedIn() && resource.data.userId == request.auth.uid);
      allow create: if isSignedIn()
                     && request.resource.data.userId == request.auth.uid;
      allow update: if isAdmin();
    }

    // ===== Addresses =====
    match /addresses/{aid} {
      allow read:   if isSignedIn() && resource.data.userId == request.auth.uid;
      allow create: if isSignedIn() && request.resource.data.userId == request.auth.uid;
      allow update: if isSignedIn() && resource.data.userId == request.auth.uid;
      allow delete: if isSignedIn() && resource.data.userId == request.auth.uid;
    }

    // ===== Reviews =====
    match /reviews/{rid} {
      allow read:   if isSignedIn();
      allow create: if isSignedIn()
                     && request.resource.data.userId == request.auth.uid;
      allow update: if isSignedIn() && resource.data.userId == request.auth.uid;
      allow delete: if isAdmin();
    }
  }
}""")

    # --- D ---
    add_h1(g['doc'], "PHỤ LỤC D. ẢNH CHỤP MÀN HÌNH TOÀN BỘ ỨNG DỤNG")
    add_body(g['doc'], "Phụ lục này tập hợp toàn bộ ảnh chụp màn hình của ứng dụng PetShop, được nhóm chụp trên emulator Pixel 6 API 34. Khi nộp báo cáo chính thức, đề nghị nhóm chụp lại từng màn hình và chèn vào đúng vị trí gợi ý.")

    add_h2(g['doc'], "D.1. Customer – Phần khách hàng")
    add_body(g['doc'], "[ẢNH] Splash, Onboarding, Đăng ký, Đăng nhập email, Đăng nhập Google, Quên mật khẩu, Trang chủ (đầy đủ + sau khi search), Danh mục, Pet Detail, Food Detail, Cart, Checkout (chọn địa chỉ + voucher), VNPay sandbox (3 ảnh), VNPay Result thành công, Order History (đa trạng thái), Order Detail, Return Request, Profile, Edit Profile, Manage Address, Notification (badge + list), Promotion, Chat AI (text + image + drawer lịch sử). Tổng cộng khoảng 25–30 ảnh.")

    add_h2(g['doc'], "D.2. Admin – Phần quản trị")
    add_body(g['doc'], "[ẢNH] Admin Login, Admin Dashboard (đầy đủ tile), Drawer menu, Manage Users, Manage Categories, Manage Pets (list + Add/Edit), Manage Food (list + Add/Edit + dialog stock), Manage Promotions, Manage Vouchers, Admin Order List, Admin Order Detail (chuyển trạng thái), Admin Return List (Approve + Refund). Tổng cộng khoảng 12–15 ảnh.")

    add_h2(g['doc'], "D.3. Hướng dẫn chèn ảnh thật")
    add_numbered(g['doc'], [
        "Chạy app trên Android Studio Emulator (Pixel 6 / API 34) hoặc thiết bị thật.",
        "Đi theo lộ trình mô tả ở D.1 và D.2 để chụp đầy đủ màn hình.",
        "Ảnh nên chụp ở tỷ lệ 9:16, không có status bar bị che, có dữ liệu mẫu thực tế.",
        "Lưu ảnh vào docs/screenshots/ với tên có thứ tự (vd: 06_login.png, 07_register.png ...).",
        "Trong Word, vào đúng vị trí [CHỤP ẢNH …] đã đánh dấu và chèn ảnh, đặt caption bằng cách nhấn chuột phải → Insert Caption → Label = Hình.",
        "Sau khi chèn, nhấn F9 trên Mục lục hình ảnh và Mục lục bảng biểu để Word tự cập nhật.",
    ])
