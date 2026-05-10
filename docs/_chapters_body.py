"""Body chapters of BAO_CAO.docx - imported by build_report.py.

This file expects the following names in scope when imported:
    doc, add_h1, add_h2, add_h3, add_body, add_para, add_bullets,
    add_numbered, add_table, add_table_caption, add_image, add_code,
    page_break, add_centered_text, PRIMARY, GREY, DARK
"""

# ===========================================================================
# MO DAU
# ===========================================================================

def build_intro(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "MỞ ĐẦU")

    add_h2(g['doc'], "1. Lý do chọn đề tài")
    add_body(g['doc'], "Trong những năm gần đây, song song với sự phát triển nhanh chóng của nền kinh tế và mức sống ngày càng được nâng cao, nhu cầu nuôi thú cưng tại Việt Nam, đặc biệt ở các đô thị lớn, đã có sự gia tăng rõ rệt. Theo nhiều khảo sát thị trường, có khoảng 35–40% hộ gia đình thành thị đang nuôi ít nhất một thú cưng (chó, mèo, cá, chim, hamster, …). Kéo theo đó là một thị trường khổng lồ về thú cưng giống, thức ăn chuyên biệt, phụ kiện chăm sóc, dịch vụ thú y, làm đẹp, gửi thú… với tốc độ tăng trưởng hai con số mỗi năm.")
    add_body(g['doc'], "Tuy nhiên, ở thị trường trong nước, đa số giao dịch mua bán thú cưng và thức ăn cho thú cưng vẫn diễn ra theo các kênh truyền thống: cửa hàng vật lý, các bài đăng tự phát trên mạng xã hội (Facebook, Zalo, Chợ Tốt). Người dùng gặp một số khó khăn điển hình: (1) khó tìm đúng giống, đúng độ tuổi, đúng nguồn gốc thú cưng phù hợp với gia đình; (2) khó so sánh giá và xác minh chất lượng thức ăn theo loài, độ tuổi và cân nặng; (3) thiếu cơ chế bảo vệ giao dịch, không có lịch sử đơn hàng, không có quy trình hoàn trả/hoàn tiền minh bạch; (4) thiếu kênh tư vấn 24/7 cho người mới nuôi thú lần đầu.")
    add_body(g['doc'], "Trong khi đó, các nền tảng thương mại điện tử lớn như Shopee, Lazada, Tiki tuy có bán đồ thú cưng nhưng không chuyên biệt, không tối ưu trải nghiệm tìm kiếm theo loài/giống/tuổi, không hỗ trợ đăng tin bán thú cưng theo từng cá thể (mỗi pet là một sản phẩm độc nhất với tình trạng AVAILABLE/RESERVED/SOLD), và không có chatbot tư vấn chuyên sâu về thú cưng.")
    add_body(g['doc'], "Xuất phát từ thực tiễn đó, nhóm chọn đề tài “Xây dựng ứng dụng PetShop trên nền tảng Android” nhằm đề xuất một giải pháp ứng dụng di động chuyên biệt cho lĩnh vực thú cưng. Ứng dụng vừa giải quyết các bài toán nghiệp vụ của một website thương mại điện tử thông thường (đăng nhập, sản phẩm, giỏ hàng, thanh toán, đơn hàng), vừa bổ sung các tính năng đặc thù của ngành thú cưng (mỗi pet là một cá thể duy nhất, theo dõi tình trạng đặt giữ, phân loại thức ăn theo loài và lứa tuổi, chatbot tư vấn). Đề tài cũng là cơ hội để các thành viên vận dụng tổng hợp kiến thức về kiến trúc MVVM, Firebase, OAuth 2.0 (Google Sign-In), HMAC-SHA512 (VNPay), tích hợp REST API bên ngoài (OpenAI), thiết kế UI/UX theo Material Design.")

    add_h2(g['doc'], "2. Mục tiêu của đề tài")
    add_body(g['doc'], "Đề tài hướng tới các mục tiêu cụ thể sau:")
    add_numbered(g['doc'], [
        "Xây dựng được một ứng dụng Android hoàn chỉnh cho hai vai trò người dùng – Khách hàng (Customer) và Quản trị viên (Admin) – với điều hướng tách biệt rõ ràng.",
        "Quản lý được hai loại sản phẩm đặc thù của ngành: thú cưng (Pet, mỗi pet là một cá thể) và thức ăn cho thú cưng (Food, có tồn kho).",
        "Triển khai trọn vẹn luồng nghiệp vụ thương mại điện tử end-to-end: đăng ký → đăng nhập → duyệt sản phẩm → giỏ hàng → đặt hàng → thanh toán → giao hàng → đánh giá / hoàn trả.",
        "Tích hợp Firebase Authentication (Email/Password, Google Sign-In; thiết kế sẵn kết cấu cho Facebook Login) và Cloud Firestore làm cơ sở dữ liệu real-time.",
        "Tích hợp cổng thanh toán điện tử VNPay (Sandbox) sử dụng chữ ký HMAC-SHA512 đúng chuẩn tài liệu chính thức.",
        "Tích hợp Chatbot tư vấn dựa trên OpenAI Chat Completions API (gpt-4o-mini), hỗ trợ gửi văn bản, ảnh và voice-to-text.",
        "Áp dụng nhất quán mẫu kiến trúc MVVM kết hợp Repository Pattern; tổ chức mã nguồn rõ ràng theo từng layer; sử dụng ViewBinding và LiveData.",
        "Sản phẩm cuối có giao diện thân thiện, hỗ trợ tiếng Việt đầy đủ, đáp ứng yêu cầu phi chức năng cơ bản về hiệu năng (load < 2s) và bảo mật (không lưu mật khẩu local).",
    ])

    add_h2(g['doc'], "3. Đối tượng và phạm vi nghiên cứu")
    add_h3(g['doc'], "3.1. Đối tượng nghiên cứu")
    add_bullets(g['doc'], [
        "Quy trình mua bán thú cưng và thức ăn cho thú cưng tại các cửa hàng vừa và nhỏ ở Việt Nam.",
        "Các nghiệp vụ thương mại điện tử cơ bản: catalog sản phẩm, giỏ hàng, đặt hàng, thanh toán, vận chuyển, hoàn trả.",
        "Kiến trúc Model-View-ViewModel (MVVM) kết hợp Repository Pattern trên nền tảng Android.",
        "Hệ sinh thái Firebase (Authentication, Cloud Firestore, Storage) và cách thức xây dựng ứng dụng real-time bằng SnapshotListener.",
        "Cổng thanh toán VNPay (sandbox) với cơ chế chữ ký HMAC-SHA512 và Deep Link redirect.",
        "Mô hình ngôn ngữ lớn (Large Language Model) thông qua OpenAI Chat Completions API và kỹ thuật Retrieval-Augmented Generation (RAG) đơn giản.",
    ])
    add_h3(g['doc'], "3.2. Phạm vi nghiên cứu")
    add_bullets(g['doc'], [
        "Nền tảng: Android, ngôn ngữ Java; minSdk = 24 (Android 7.0), targetSdk = 36.",
        "Backend: Firebase (BaaS) – không xây server riêng; chỉ sử dụng Cloud Functions ở mức đề xuất tương lai.",
        "Thanh toán: VNPay Sandbox (chưa đưa lên môi trường production).",
        "Hỗ trợ tiếng Việt; các văn bản trong app đều bằng tiếng Việt.",
        "Phạm vi địa lý mô phỏng: Việt Nam, với phí vận chuyển chia theo bốn vùng (TP.HCM, Miền Nam, Miền Trung, Miền Bắc).",
        "Đối tượng người dùng giả định: khách hàng cá nhân và quản trị viên cửa hàng – chưa hỗ trợ tài khoản B2B.",
    ])

    add_h2(g['doc'], "4. Phương pháp thực hiện")
    add_body(g['doc'], "Để hoàn thành đề tài, nhóm áp dụng phối hợp nhiều phương pháp nghiên cứu và phát triển phần mềm:")
    add_bullets(g['doc'], [
        "Phương pháp khảo sát: nhóm khảo sát một số ứng dụng/website pet shop trong và ngoài nước (Pet Mart, Petsy, Chewy, PetSmart, các bài đăng MXH) để rút ra ưu/nhược điểm và đề xuất tính năng riêng.",
        "Phương pháp phân tích – thiết kế: vận dụng UML (Use Case, Activity, Sequence, State, ER) để mô hình hoá hệ thống trước khi viết code.",
        "Phương pháp phát triển lặp tăng dần (Incremental & Iterative): chia hệ thống thành 4 module độc lập, mỗi thành viên phụ trách 1 module và tích hợp dần.",
        "Phương pháp lập trình theo mẫu kiến trúc MVVM + Repository Pattern, kết hợp ViewBinding và LiveData.",
        "Phương pháp kiểm thử: kết hợp manual test (kịch bản chi tiết) và unit test cho các util thuần Java (VNPayHelper, ShippingHelper, PromotionManager).",
        "Phương pháp quản lý mã nguồn: sử dụng Git/GitHub, mỗi thành viên làm việc trên nhánh riêng, merge qua Pull Request.",
        "Phương pháp tham khảo: đọc và áp dụng tài liệu chính thức của Android Developers, Firebase, VNPay, OpenAI; tham khảo các bài viết kỹ thuật trên Medium, Stack Overflow.",
    ])

    add_h2(g['doc'], "5. Bố cục báo cáo")
    add_body(g['doc'], "Báo cáo được trình bày trong bảy chương chính (ngoài phần Mở đầu, Kết luận, Tài liệu tham khảo và các phụ lục), trong đó các Chương 3, 4, 5, 6 tương ứng với bốn module phụ trách bởi bốn thành viên trong nhóm:")
    add_bullets(g['doc'], [
        "Chương 1 – Tổng quan đề tài và công nghệ sử dụng: trình bày bối cảnh, khảo sát hiện trạng, mô tả bài toán, yêu cầu chức năng/phi chức năng và các công nghệ then chốt.",
        "Chương 2 – Phân tích và thiết kế hệ thống: Use Case, Activity Diagram, thiết kế CSDL Cloud Firestore, kiến trúc tổng thể MVVM và thiết kế UI/UX.",
        "Chương 3 – Xây dựng module Tài khoản và Hồ sơ người dùng (TV1).",
        "Chương 4 – Xây dựng module Danh mục sản phẩm và Trang chủ (TV2).",
        "Chương 5 – Xây dựng module Giỏ hàng, Thanh toán và Đơn hàng (TV3).",
        "Chương 6 – Xây dựng module Quản trị và Chatbot tư vấn (TV4).",
        "Chương 7 – Kiểm thử, triển khai và đánh giá: kế hoạch kiểm thử, bảng test case theo từng module, hiệu năng – bảo mật và hướng dẫn build.",
    ])


# ===========================================================================
# CHUONG 1
# ===========================================================================
def build_chapter1(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ CÔNG NGHỆ SỬ DỤNG")

    add_h2(g['doc'], "1.1. Khảo sát hiện trạng các ứng dụng pet shop trên thị trường")
    add_body(g['doc'], "Trước khi đặc tả yêu cầu cho ứng dụng PetShop, nhóm tiến hành khảo sát một số ứng dụng và website cùng lĩnh vực, đặc biệt tập trung vào trải nghiệm người dùng cuối, tính năng đặc thù cho thú cưng và mức độ chuyên biệt của giải pháp. Bảng 1.1 dưới đây tổng hợp ưu/nhược điểm của các giải pháp tham khảo:")
    add_table_caption(g['doc'], "So sánh các giải pháp Pet shop hiện có trên thị trường")
    add_table(g['doc'],
        header=["Tên / Loại", "Ưu điểm", "Nhược điểm"],
        rows=[
            ("Pet Mart, Petsy (Website thuần)",
             "Sản phẩm phong phú, có hệ thống cửa hàng vật lý hỗ trợ.",
             "Chỉ có web, chưa tối ưu cho mobile; UX chậm; thanh toán hạn chế; không có app native; thiếu chatbot tư vấn."),
            ("Chewy, PetSmart (US)",
             "Hệ sinh thái lớn, chương trình thành viên, giao hàng định kỳ, phục vụ rất chuyên nghiệp.",
             "Không phục vụ thị trường Việt Nam; giao diện và phương thức thanh toán không phù hợp người dùng VN."),
            ("Bài đăng MXH (Facebook, Zalo, Chợ Tốt)",
             "Dễ đăng tin, tiếp cận nhanh, cộng đồng người chơi sẵn có.",
             "Không có quản lý đơn hàng, không có cơ chế bảo vệ giao dịch, không có hồ sơ thú cưng đầy đủ, không hoàn trả/hoàn tiền."),
            ("Shopee, Lazada, Tiki",
             "Hệ thống thanh toán/giao hàng hoàn thiện; nhiều người bán.",
             "Không chuyên về thú cưng; mỗi cá thể pet không quản lý đúng theo trạng thái AVAILABLE/RESERVED/SOLD; không có tư vấn chuyên sâu."),
        ],
        widths_cm=[4.0, 6.0, 5.5])
    add_body(g['doc'], "Từ kết quả khảo sát, nhóm rút ra hai nhóm cơ hội mà ứng dụng PetShop cần khai thác: (1) cung cấp một nền tảng tập trung, chuyên biệt cho lĩnh vực thú cưng, có quản lý từng cá thể pet; và (2) tích hợp một trợ lý AI tư vấn về chăm sóc, dinh dưỡng, lựa chọn giống – điều mà các đối thủ chưa làm. Đây cũng là hai điểm khác biệt quan trọng được nhóm đặt làm trọng tâm khi đặc tả yêu cầu.")

    add_h2(g['doc'], "1.2. Mô tả bài toán và yêu cầu chức năng")
    add_body(g['doc'], "Ứng dụng PetShop đóng vai trò là nền tảng kết nối hai nhóm người dùng chính:")
    add_bullets(g['doc'], [
        "Khách hàng (Customer): có thể duyệt sản phẩm, đặt mua, thanh toán, theo dõi đơn hàng, trao đổi với chatbot, quản lý hồ sơ và sổ địa chỉ.",
        "Quản trị viên (Admin): chịu trách nhiệm cập nhật sản phẩm, danh mục, khuyến mãi, voucher; phê duyệt đơn hàng, xử lý yêu cầu hoàn trả; theo dõi doanh thu thực tế qua bảng điều khiển real-time.",
    ])

    add_h3(g['doc'], "1.2.1. Yêu cầu chức năng (Functional Requirements)")
    add_body(g['doc'], "Bảng 1.2 và Bảng 1.3 mô tả chi tiết các yêu cầu chức năng cho hai vai trò.")
    add_table_caption(g['doc'], "Yêu cầu chức năng (FR) cho khách hàng")
    add_table(g['doc'],
        header=["Mã", "Tên chức năng", "Mô tả ngắn"],
        rows=[
            ("FC-01", "Đăng ký tài khoản", "Đăng ký Email/Mật khẩu, xác thực bằng OTP gửi qua email; tự động tạo bản ghi user trên Firestore với role = CUSTOMER."),
            ("FC-02", "Đăng nhập",       "Hỗ trợ Email/Password, Google Sign-In (đăng ký Facebook Login đã được thiết kế sẵn cho phiên bản mở rộng)."),
            ("FC-03", "Quên mật khẩu",  "Gửi email đặt lại mật khẩu thông qua Firebase Auth."),
            ("FC-04", "Trang chủ",      "Hiển thị banner, lời chào theo thời gian, danh mục, sản phẩm nổi bật, ô tìm kiếm, badge giỏ hàng và thông báo."),
            ("FC-05", "Duyệt & lọc sản phẩm", "Duyệt thú cưng và thức ăn theo danh mục; tìm kiếm theo từ khoá; lọc theo loài/loại/giá."),
            ("FC-06", "Chi tiết sản phẩm", "Xem ảnh slideshow, mô tả, giá, tình trạng tiêm phòng (Pet) hoặc trọng lượng/loại (Food)."),
            ("FC-07", "Giỏ hàng",       "Thêm/xoá/đổi số lượng, tự động tính tiền; mỗi pet chỉ thêm được 1 lần (cá thể duy nhất)."),
            ("FC-08", "Voucher / Khuyến mãi", "Áp dụng voucher PERCENT/FIXED/FREESHIP và promotion tự động."),
            ("FC-09", "Thanh toán",     "Chọn địa chỉ, tính phí ship theo vùng, chọn COD hoặc VNPay."),
            ("FC-10", "Lịch sử đơn hàng", "Lọc theo trạng thái; xem chi tiết; huỷ đơn khi còn ở trạng thái cho phép."),
            ("FC-11", "Hoàn trả / Hoàn tiền", "Yêu cầu trả hàng sau khi nhận; nhập số TK ngân hàng nếu COD."),
            ("FC-12", "Thông báo",      "Real-time badge; danh sách thông báo (đơn hàng, khuyến mãi, hệ thống)."),
            ("FC-13", "Chat hỗ trợ AI", "Chat với GPT-4o-mini, gửi văn bản/ảnh/voice; lưu lịch sử phiên."),
            ("FC-14", "Quản lý hồ sơ",  "Sửa thông tin cá nhân, upload avatar, quản lý sổ địa chỉ."),
        ],
        widths_cm=[1.6, 4.0, 9.9])

    add_table_caption(g['doc'], "Yêu cầu chức năng (FR) cho quản trị viên")
    add_table(g['doc'],
        header=["Mã", "Tên chức năng", "Mô tả ngắn"],
        rows=[
            ("FA-01", "Dashboard",          "9 thẻ thống kê real-time: doanh thu, tổng đơn, người dùng, đơn theo trạng thái."),
            ("FA-02", "Quản lý người dùng", "Khoá/mở khoá tài khoản, đổi role."),
            ("FA-03", "Quản lý danh mục",   "CRUD danh mục Pet và Food."),
            ("FA-04", "Quản lý thú cưng",   "CRUD pet với upload nhiều ảnh + video."),
            ("FA-05", "Quản lý thức ăn",    "CRUD food, cập nhật tồn kho nhanh qua dialog."),
            ("FA-06", "Quản lý đơn hàng",   "Cập nhật trạng thái: PENDING → CONFIRMED → … → DELIVERED."),
            ("FA-07", "Duyệt hoàn trả",     "Approve / Reject / Refund yêu cầu trả hàng của khách."),
            ("FA-08", "Quản lý voucher",    "CRUD voucher; auto gửi notification khi tạo/bật."),
            ("FA-09", "Quản lý khuyến mãi", "CRUD promotion; áp dụng % giảm giá theo sản phẩm/danh mục."),
        ],
        widths_cm=[1.6, 4.0, 9.9])

    add_h3(g['doc'], "1.2.2. Yêu cầu phi chức năng (Non-Functional Requirements)")
    add_table_caption(g['doc'], "Yêu cầu phi chức năng (NFR)")
    add_table(g['doc'],
        header=["Tiêu chí", "Mức yêu cầu"],
        rows=[
            ("Tương thích",  "Android 7.0 trở lên (API 24+); thiết kế responsive với màn hình từ 4.7 inch đến 7 inch."),
            ("Hiệu năng",    "Trang chủ load < 2s; SnapshotListener phản hồi < 500 ms; kích thước APK < 30 MB."),
            ("Bảo mật",      "Sử dụng Firebase Auth (mã hoá phía Google); HMAC-SHA512 cho VNPay; không lưu mật khẩu local; khoá API đặt trong local.properties."),
            ("Khả năng sử dụng", "UI Material Design, hỗ trợ tiếng Việt đầy đủ, các thao tác chính không quá 3 lần chạm."),
            ("Khả năng mở rộng", "Dễ dàng thay shipping API (hiện hardcode bằng ShippingHelper) bằng GHN/GHTK; dễ tích hợp FCM cho push notification."),
            ("Bảo trì",      "Mã nguồn chia layer rõ ràng (model/repository/viewmodel/view/utils); đặt tên nhất quán."),
            ("Khả năng kiểm thử", "ViewModel tách rời View, có thể test bằng JUnit; util thuần Java có thể test offline."),
        ],
        widths_cm=[4.0, 11.5])

    add_h2(g['doc'], "1.3. Công nghệ sử dụng")
    add_h3(g['doc'], "1.3.1. Ngôn ngữ Java và nền tảng Android")
    add_body(g['doc'], "Nhóm chọn ngôn ngữ Java cho dự án vì các lý do: (1) Java là ngôn ngữ chính thức đầu tiên của Android, có cộng đồng lớn nhất, tài liệu phong phú, dễ dàng tìm kiếm khi gặp vấn đề; (2) các thành viên trong nhóm đã có nền tảng tốt từ các môn học trước (Lập trình hướng đối tượng, Lập trình Java, Lập trình Android căn bản); (3) Java vẫn là lựa chọn ổn định cho các dự án thương mại lớn, đặc biệt với hệ sinh thái Spring/Android.")
    add_body(g['doc'], "Dự án được build với Android Gradle Plugin 8.x, sử dụng Gradle Kotlin DSL (build.gradle.kts), compileSdk = 36, minSdk = 24, targetSdk = 36. Tệp cấu hình version-catalog (libs.versions.toml) được sử dụng để khai báo dependency tập trung, dễ nâng cấp.")

    add_h3(g['doc'], "1.3.2. Kiến trúc MVVM, ViewBinding, LiveData, ViewModel")
    add_body(g['doc'], "MVVM (Model – View – ViewModel) là kiến trúc được Google chính thức khuyến nghị cho Android (theo Android Architecture Components). Ưu điểm chính:")
    add_bullets(g['doc'], [
        "Tách bạch logic UI khỏi logic dữ liệu: View (Activity/Fragment) chỉ hiển thị; ViewModel giữ trạng thái và xử lý logic; Model/Repository chịu trách nhiệm I/O.",
        "ViewModel sống theo lifecycle Activity/Fragment, tự động giữ trạng thái khi cấu hình thay đổi (xoay màn hình).",
        "LiveData là một observable lifecycle-aware: View đăng ký quan sát, khi data thay đổi UI tự cập nhật và tự huỷ listener khi View bị destroy → tránh memory leak.",
        "ViewBinding giúp truy xuất View bằng tham chiếu type-safe thay cho findViewById, giảm sai sót và NullPointerException.",
    ])
    add_body(g['doc'], "Trong dự án PetShop, mỗi tính năng có một cặp Activity/Fragment + ViewModel + Repository. Các Repository đại diện cho lớp truy cập dữ liệu (Firestore, Storage, REST API). Mô hình kiến trúc tổng thể được trình bày chi tiết ở Chương 2.")

    add_h3(g['doc'], "1.3.3. Firebase (Authentication, Cloud Firestore, Storage)")
    add_body(g['doc'], "Firebase là nền tảng Backend-as-a-Service (BaaS) của Google được nhóm sử dụng làm backend chính, gồm ba dịch vụ:")
    add_bullets(g['doc'], [
        "Firebase Authentication: quản lý xác thực với nhiều phương thức (Email/Password, Google, Phone, Facebook…). Trong dự án dùng Email/Password và Google Sign-In; Facebook Login được thiết kế sẵn kết cấu, sẵn sàng kích hoạt.",
        "Cloud Firestore: cơ sở dữ liệu NoSQL real-time, dạng document/collection. Hỗ trợ truy vấn phức tạp, transaction, snapshot listener, security rules. Đáp ứng tốt yêu cầu real-time của module Admin Dashboard và Notification.",
        "Firebase Storage: lưu trữ file (ảnh, video). Sử dụng để lưu ảnh banner, ảnh sản phẩm, video giới thiệu thú cưng và avatar.",
    ])
    add_body(g['doc'], "Các lý do nhóm chọn Firebase: (1) miễn phí trong giai đoạn phát triển; (2) tích hợp sẵn SDK Android, cấu hình bằng google-services.json; (3) cho phép xây dựng nhanh các ứng dụng real-time mà không cần dựng server riêng; (4) hệ sinh thái Google có hỗ trợ Cloud Functions, Cloud Messaging cho hướng phát triển tiếp theo.")

    add_h3(g['doc'], "1.3.4. Đăng nhập mạng xã hội: Google Sign-In, Facebook Login")
    add_body(g['doc'], "Để tăng trải nghiệm đăng ký/đăng nhập cho người dùng, ứng dụng hỗ trợ đăng nhập bằng tài khoản mạng xã hội:")
    add_bullets(g['doc'], [
        "Google Sign-In: sử dụng SDK Google Play Services Auth. Người dùng nhấn nút “Đăng nhập với Google”, ứng dụng mở Intent chọn tài khoản Google trên thiết bị; sau khi user xác nhận, Google trả về ID token; ID token được đẩy lên Firebase Auth để lấy phiên đăng nhập. Nếu là user mới, hệ thống tự tạo bản ghi trong Firestore với role = CUSTOMER.",
        "Facebook Login: được thiết kế đồng dạng (cũng dùng OAuth credential nạp vào Firebase Auth). Cấu trúc lớp đã sẵn sàng, chỉ cần cấp App ID/App Secret từ Meta for Developers và bổ sung Facebook SDK để kích hoạt. Phiên bản hiện tại nhóm chưa kích hoạt do giới hạn thời gian xét duyệt App từ Meta; xem mục 3.7 trong Chương 3.",
    ])

    add_h3(g['doc'], "1.3.5. Cổng thanh toán VNPay")
    add_body(g['doc'], "VNPay là một trong những cổng thanh toán điện tử phổ biến nhất tại Việt Nam, hỗ trợ thanh toán qua tài khoản ngân hàng nội địa, thẻ ATM, QR Code, ví VNPay-QR. Nhóm sử dụng môi trường Sandbox của VNPay để demo, gồm:")
    add_bullets(g['doc'], [
        "URL thanh toán: https://sandbox.vnpayment.vn/paymentv2/vpcpay.html",
        "Mã hash secret và Terminal Code (TMN) lưu trong local.properties.",
        "Chữ ký HMAC-SHA512 để bảo đảm tính toàn vẹn của tham số gửi sang VNPay.",
        "Deep Link callback theo lược đồ petshop://payment/vnpay-return → VNPayResultActivity.",
    ])
    add_body(g['doc'], "Quy trình tích hợp được cài đặt trong lớp VNPayHelper.java và mô tả chi tiết trong Chương 5.")

    add_h3(g['doc'], "1.3.6. OpenAI API (chatbot tư vấn)")
    add_body(g['doc'], "OpenAI cung cấp các API mô hình ngôn ngữ lớn (LLM). Nhóm sử dụng endpoint /v1/chat/completions với model gpt-4o-mini – cho chất lượng tốt với chi phí thấp và hỗ trợ vision (gửi ảnh). Ứng dụng PetShop dùng API này cho tính năng Chatbot tư vấn:")
    add_bullets(g['doc'], [
        "Người dùng nhập câu hỏi (gõ phím hoặc voice-to-text) và có thể đính kèm ảnh.",
        "Trước khi gọi API, ChatViewModel tự động tổng hợp “context” từ Firestore (danh mục, pet, food, voucher, đơn hàng của user) và prepend vào prompt – đây là kỹ thuật RAG (Retrieval-Augmented Generation) đơn giản giúp bot trả lời chính xác về sản phẩm hiện có.",
        "Lịch sử hội thoại được lưu vào Firestore (users/{uid}/sessions/{sessionId}/messages); khách chưa đăng nhập lưu cục bộ trong SharedPreferences với giới hạn 50 tin.",
    ])

    add_h3(g['doc'], "1.3.7. Thư viện hỗ trợ: Glide, OkHttp, Gson, Material…")
    add_body(g['doc'], "Bên cạnh các nền tảng chính, dự án sử dụng nhiều thư viện hỗ trợ để tăng tốc phát triển và ổn định sản phẩm:")
    add_bullets(g['doc'], [
        "Glide: tải và cache ảnh từ URL/Storage hiệu quả, tự động xử lý vòng đời, hỗ trợ placeholder/error.",
        "OkHttp: client HTTP nhỏ gọn, được dùng để gọi OpenAI API và bất kỳ REST endpoint nào trong tương lai.",
        "Gson: chuyển đổi JSON ⇄ POJO, dùng cho parse response OpenAI và serialize/deserialize Firestore document.",
        "Material Components for Android: bộ component tuân theo Material Design 3 (BottomNavigationView, TextInputLayout, MaterialButton, …).",
        "ViewPager2: cho banner trượt ở Trang chủ.",
        "RecyclerView, CardView: hiển thị danh sách và bố cục thẻ.",
        "CircleImageView: avatar tròn.",
        "JavaMail (javax.mail): gửi email OTP qua SMTP Gmail trong RegisterActivity.",
        "Lifecycle ViewModel + LiveData (androidx.lifecycle:*): cốt lõi của MVVM.",
    ])

    add_h2(g['doc'], "1.4. Công cụ phát triển và quản lý dự án")
    add_h3(g['doc'], "1.4.1. Android Studio, Gradle (Kotlin DSL)")
    add_body(g['doc'], "Toàn bộ quá trình phát triển được thực hiện trên Android Studio (phiên bản Hedgehog 2023.x trở lên), kết hợp Gradle 8 với cú pháp Kotlin DSL (build.gradle.kts) – có lợi thế hơn Groovy về kiểm tra cú pháp và auto-complete. Tệp libs.versions.toml dùng để khai báo dependency tập trung, đảm bảo tất cả module dùng chung phiên bản.")

    add_h3(g['doc'], "1.4.2. Git, GitHub, quản lý nhánh")
    add_body(g['doc'], "Mã nguồn được quản lý bằng Git và lưu trên GitHub. Nhóm sử dụng quy trình Git-flow rút gọn: nhánh chính main giữ trạng thái ổn định; mỗi tính năng phát triển trên một nhánh feature/<tên-tính-năng>; sau khi hoàn thành sẽ mở Pull Request để review trước khi merge. Quy ước commit ngắn gọn theo dạng “fix:” / “feat:” / “docs:” giúp truy vết lịch sử dễ dàng.")

    add_h3(g['doc'], "1.4.3. Figma cho thiết kế giao diện")
    add_body(g['doc'], "Nhóm sử dụng Figma để vẽ wireframe và mockup các màn hình trước khi viết XML layout. Việc thống nhất bộ màu (cam #F5A623, nâu nhạt #FFF8F2, trắng), font, icon trên Figma giúp các thành viên không cần trao đổi nhiều mà vẫn cho ra giao diện đồng nhất. Một số màn hình tiêu biểu (Splash, Login, Home, Cart, Checkout) được prototype trên Figma để demo cho giảng viên trước khi triển khai chính thức.")

    add_image(g['doc'], "diagram_architecture.png",
              "Sơ đồ kiến trúc MVVM + Repository + Firebase của ứng dụng PetShop", width_cm=15)
    add_image(g['doc'], "diagram_package-layout.png",
              "Mô hình tổ chức package mã nguồn theo MVVM", width_cm=15)


# ===========================================================================
# CHUONG 2
# ===========================================================================
def build_chapter2(g):
    add_h1, add_h2, add_h3 = g['add_h1'], g['add_h2'], g['add_h3']
    add_body, add_para     = g['add_body'], g['add_para']
    add_bullets, add_numbered = g['add_bullets'], g['add_numbered']
    add_table, add_table_caption = g['add_table'], g['add_table_caption']
    add_image, add_code    = g['add_image'], g['add_code']

    add_h1(g['doc'], "CHƯƠNG 2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")

    add_h2(g['doc'], "2.1. Sơ đồ Use Case tổng quát")
    add_body(g['doc'], "Sơ đồ Use Case tổng quát của ứng dụng PetShop được trình bày trong Hình 1.1 (đã đặt tại Chương 1). Sơ đồ thể hiện rõ hai tác nhân của hệ thống và các Use Case mà mỗi tác nhân tương tác.")
    add_image(g['doc'], "diagram_usecase.png",
              "Sơ đồ Use Case tổng quát của ứng dụng PetShop", width_cm=15)

    add_h3(g['doc'], "2.1.1. Tác nhân Khách hàng")
    add_body(g['doc'], "Khách hàng là tác nhân chính, đại diện cho người dùng cuối có nhu cầu mua thú cưng và thức ăn. Một khách hàng có thể đăng ký tài khoản hoặc duyệt sản phẩm ở trạng thái guest (chưa đăng nhập). Tuy nhiên, các thao tác liên quan đến giỏ hàng, đơn hàng, thông báo cá nhân, chat lưu trữ phiên… đều yêu cầu đăng nhập. Khách hàng có thể giữ nhiều địa chỉ giao hàng khác nhau và chọn địa chỉ mặc định.")

    add_h3(g['doc'], "2.1.2. Tác nhân Quản trị viên")
    add_body(g['doc'], "Quản trị viên là người được cấp role = ADMIN trên Firestore. Sau khi đăng nhập, hệ thống điều hướng admin tới giao diện AdminActivity (khác hoàn toàn với giao diện của khách hàng). Admin chịu trách nhiệm vận hành cửa hàng: cập nhật catalog, duyệt đơn, giải quyết hoàn trả, theo dõi doanh thu. Hệ thống không cho phép admin tự đặt hàng cho mình – tách biệt rõ vai trò.")

    add_h2(g['doc'], "2.2. Đặc tả các Use Case chính")
    add_body(g['doc'], "Để minh hoạ chi tiết, nhóm trình bày đặc tả của hai Use Case quan trọng nhất: Đặt hàng & Thanh toán (Customer) và Yêu cầu trả hàng / hoàn tiền (Customer–Admin).")

    add_table_caption(g['doc'], "Mô tả Use Case 'Đặt hàng và thanh toán'")
    add_table(g['doc'],
        header=["Trường", "Nội dung"],
        rows=[
            ("Tên Use Case",       "UC-05: Đặt hàng và thanh toán"),
            ("Mô tả",              "Khách hàng tạo đơn hàng từ giỏ hàng, chọn địa chỉ, phương thức thanh toán và xác nhận thanh toán."),
            ("Tác nhân",           "Customer"),
            ("Tiền điều kiện",     "Đã đăng nhập; giỏ hàng có ít nhất 1 sản phẩm; có ít nhất 1 địa chỉ."),
            ("Hậu điều kiện",      "Đơn hàng được tạo ở trạng thái PENDING (COD) hoặc WAITING_PAYMENT (VNPay); tồn kho food được trừ; pet chuyển sang RESERVED khi PAID."),
            ("Luồng chính",
             "1) Mở giỏ hàng → nhấn Thanh toán.\n"
             "2) CheckoutActivity hiển thị danh sách sản phẩm, địa chỉ, phí ship.\n"
             "3) Khách chọn voucher (tùy chọn) và phương thức thanh toán.\n"
             "4) Nếu COD → OrderRepo.createOrder(); chuyển sang OrderDetail.\n"
             "5) Nếu VNPay → tạo URL bằng VNPayHelper, mở VNPayWebView; sau khi thanh toán → completeVNPayOrder() chốt đơn."),
            ("Luồng phụ",
             "A1: Voucher quá hạn / vượt giới hạn → báo lỗi, không áp dụng.\n"
             "A2: VNPay thất bại → đơn vẫn ở WAITING_PAYMENT, khách có thể thanh toán lại.\n"
             "A3: Mất kết nối → giao dịch tạo đơn rollback nhờ Firestore Transaction."),
            ("Ngoại lệ",
             "E1: Pet đã bị reserved/sold trong lúc thanh toán → transaction fail, báo lỗi tới khách.\n"
             "E2: Stock food không đủ → báo lỗi, đề nghị giảm số lượng."),
        ],
        widths_cm=[3.5, 12.0])

    add_table_caption(g['doc'], "Mô tả Use Case 'Yêu cầu trả hàng / hoàn tiền'")
    add_table(g['doc'],
        header=["Trường", "Nội dung"],
        rows=[
            ("Tên Use Case",   "UC-09: Yêu cầu trả hàng và hoàn tiền"),
            ("Mô tả",          "Khách hàng yêu cầu trả hàng/hoàn tiền sau khi nhận hàng; admin duyệt và xử lý hoàn tiền."),
            ("Tác nhân",       "Customer (gửi yêu cầu); Admin (xử lý)"),
            ("Tiền điều kiện", "Đơn hàng đã ở trạng thái DELIVERED hoặc COMPLETED."),
            ("Hậu điều kiện",  "Đơn chuyển sang RETURN_REQUESTED → RETURN_APPROVED → REFUNDED; doanh thu hệ thống tự giảm tương ứng."),
            ("Luồng chính",
             "1) Customer mở chi tiết đơn → nhấn 'Yêu cầu hoàn trả'.\n"
             "2) Nhập lý do; nếu COD bắt buộc nhập số tài khoản + tên ngân hàng.\n"
             "3) OrderRepo.requestReturn() cập nhật trạng thái; ReturnRepo.create() lưu yêu cầu.\n"
             "4) Notification gửi đến admin (qua tile real-time).\n"
             "5) Admin mở AdminReturnList → Approve / Reject.\n"
             "6) Nếu Approve → admin chuyển khoản (COD) hoặc gọi API refund VNPay (tương lai), sau đó cập nhật REFUNDED."),
            ("Luồng phụ", "A1: Admin từ chối → đơn quay lại COMPLETED + ghi adminNote."),
            ("Ngoại lệ",  "E1: Yêu cầu trả hàng quá thời hạn quy định → ẩn nút."),
        ],
        widths_cm=[3.5, 12.0])

    add_h2(g['doc'], "2.3. Sơ đồ hoạt động (Activity Diagram) các luồng nghiệp vụ tiêu biểu")
    add_h3(g['doc'], "2.3.1. Luồng Đăng ký – Đăng nhập")
    add_body(g['doc'], "Luồng đăng ký – đăng nhập của ứng dụng được mô tả trong Hình kèm theo. Hệ thống hỗ trợ ba con đường vào: (a) đăng nhập email/mật khẩu; (b) đăng nhập Google; (c) đăng ký mới có xác thực OTP qua email. Sau khi xác thực thành công, hệ thống đọc role từ Firestore để điều hướng tới giao diện Admin hoặc Customer.")
    add_image(g['doc'], "diagram_auth-flow.png",
              "Activity Diagram – luồng đăng ký, đăng nhập", width_cm=15)

    add_h3(g['doc'], "2.3.2. Luồng Mua hàng – Thanh toán VNPay")
    add_body(g['doc'], "Luồng mua hàng được tổ chức theo các bước: chọn địa chỉ → tính phí ship → áp voucher/promotion → chọn phương thức thanh toán. Riêng luồng VNPay phức tạp hơn vì phải tạo URL có chữ ký HMAC-SHA512, mở WebView, đợi VNPay redirect về deep link và chốt đơn bằng transaction. Chi tiết được mô tả trong Hình kèm theo.")
    add_image(g['doc'], "diagram_checkout-flow.png",
              "Activity Diagram – luồng đặt hàng & thanh toán", width_cm=12)

    add_h3(g['doc'], "2.3.3. Luồng Yêu cầu trả hàng")
    add_body(g['doc'], "Luồng yêu cầu trả hàng có hai giai đoạn: (1) phía khách hàng tạo yêu cầu, hệ thống cập nhật trạng thái đơn sang RETURN_REQUESTED; (2) phía admin xử lý: Approve → Refund hoặc Reject. Khi Refund, hệ thống tự động trừ doanh thu khỏi dashboard và gửi notification cho khách.")
    add_image(g['doc'], "diagram_return-flow.png",
              "Activity Diagram – yêu cầu trả hàng và hoàn tiền", width_cm=12)

    add_h2(g['doc'], "2.4. Thiết kế cơ sở dữ liệu trên Cloud Firestore")
    add_h3(g['doc'], "2.4.1. Sơ đồ collection / document")
    add_body(g['doc'], "Khác với các CSDL quan hệ truyền thống, Cloud Firestore là một CSDL NoSQL tổ chức theo mô hình collection/document. Mỗi collection chứa các document, mỗi document có thể chứa các sub-collection. Sơ đồ dưới đây thể hiện toàn bộ collection của ứng dụng PetShop.")
    add_image(g['doc'], "diagram_firestore-collections.png",
              "Sơ đồ collection Firestore của ứng dụng PetShop", width_cm=15)
    add_body(g['doc'], "Một số collection có sub-collection:")
    add_bullets(g['doc'], [
        "users/{uid}/sessions/{sessionId}/messages – lưu lịch sử chat từng phiên hội thoại.",
        "vouchers/{voucherId}/voucher_usage – lưu lịch sử lượt sử dụng voucher của từng user.",
    ])

    add_h3(g['doc'], "2.4.2. Mô tả các collection")
    add_table_caption(g['doc'], "Cấu trúc các collection chính trên Firestore")
    add_table(g['doc'],
        header=["Collection", "Mô tả ngắn", "Trường tiêu biểu"],
        rows=[
            ("users",         "Tài khoản người dùng (CUSTOMER/ADMIN).",
             "id, fullName, email, role, status, totalOrders, totalSpent, avatarUrl"),
            ("pets",          "Thú cưng đăng bán (mỗi pet là một cá thể).",
             "id, name, species, breed, age, gender, price, status (AVAILABLE/RESERVED/SOLD), media[]"),
            ("foods",         "Sản phẩm thức ăn cho thú cưng.",
             "id, name, brand, foodType, targetPetType, weightGram, price, stock, sold"),
            ("categories",    "Danh mục Pet/Food.",
             "id, name, type (PET/FOOD), iconUrl, isActive"),
            ("carts",         "Giỏ hàng (mỗi user có document cùng id = uid).",
             "userId, items[], subtotal, totalItems, updatedAt"),
            ("orders",        "Đơn hàng đã đặt.",
             "id, orderCode, userId, items[], shippingAddress, totalAmount, status, paymentMethod, paymentStatus"),
            ("notifications", "Thông báo gửi cho user.",
             "id, userId, type (ORDER/PROMO/SYSTEM), title, message, isRead, createdAt, orderId"),
            ("vouchers",      "Mã giảm giá hệ thống.",
             "id, code, type (PERCENT/FIXED/FREESHIP), discountValue, usageLimit, usedCount"),
            ("promotions",    "Khuyến mãi áp dụng tự động cho sản phẩm.",
             "id, name, applyType (ALL/CATEGORY/PRODUCT), discountValue, startDate, endDate"),
            ("return_requests", "Yêu cầu trả hàng & hoàn tiền.",
             "id, orderId, userId, reason, paymentMethod, bankAccount, status, refundAmount"),
            ("addresses",     "Sổ địa chỉ giao hàng.",
             "id, userId, receiverName, phone, address, ward, district, city, isDefault"),
            ("banners",       "Banner trang chủ.",
             "id, imageUrl, link, sortOrder, isActive"),
            ("reviews",       "Đánh giá sản phẩm sau khi mua.",
             "id, productId, userId, rating, comment, media[], createdAt"),
        ],
        widths_cm=[3.0, 5.5, 7.0])

    add_h3(g['doc'], "2.4.3. Quy tắc bảo mật (Security Rules)")
    add_body(g['doc'], "Việc đặt Cloud Firestore Security Rules đúng và chặt chẽ là yếu tố then chốt để bảo vệ dữ liệu khi client truy cập trực tiếp Firestore. Nhóm thiết kế Security Rules theo nguyên tắc “mặc định từ chối, chỉ cho phép có chủ đích”, được khái quát trong Hình kèm theo.")
    add_image(g['doc'], "diagram_security-rules.png",
              "Tóm tắt logic Firestore Security Rules", width_cm=15)
    add_body(g['doc'], "Một số luật chính (rút gọn, cú pháp Firestore Rules):")
    add_code(g['doc'], """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    function isSignedIn()  { return request.auth != null; }
    function isOwner(uid)  { return isSignedIn() && request.auth.uid == uid; }
    function isAdmin()     {
      return isSignedIn()
        && get(/databases/$(database)/documents/users/$(request.auth.uid))
             .data.role == 'ADMIN';
    }

    // users/{uid}: customer chi sua duoc cua minh; admin co toan quyen
    match /users/{uid} {
      allow read, write: if isOwner(uid) || isAdmin();
      match /sessions/{sid}/messages/{mid} {
        allow read, write: if isOwner(uid);
      }
    }

    // pets, foods, categories, vouchers, promotions: customer chi READ
    match /{col=pets|foods|categories|vouchers|promotions|banners}/{id} {
      allow read:  if isSignedIn();
      allow write: if isAdmin();
    }

    // carts/{uid}: chi cua minh
    match /carts/{uid} {
      allow read, write: if isOwner(uid);
    }

    // orders: customer tao moi don cua minh, READ cua minh; admin toan quyen
    match /orders/{oid} {
      allow read:   if isAdmin() || (isSignedIn() && resource.data.userId == request.auth.uid);
      allow create: if isSignedIn() && request.resource.data.userId == request.auth.uid;
      allow update: if isAdmin();
    }

    // notifications: chi nguoi nhan READ va mark isRead; admin write
    match /notifications/{nid} {
      allow read:   if isAdmin() || (isSignedIn() && resource.data.userId == request.auth.uid);
      allow create: if isAdmin();
      allow update: if isAdmin() || (isSignedIn() && resource.data.userId == request.auth.uid);
    }

    // return_requests: customer tao cua minh; admin xu ly
    match /return_requests/{rid} {
      allow read:   if isAdmin() || (isSignedIn() && resource.data.userId == request.auth.uid);
      allow create: if isSignedIn() && request.resource.data.userId == request.auth.uid;
      allow update: if isAdmin();
    }

    // addresses: chi cua minh
    match /addresses/{aid} {
      allow read, write: if isSignedIn() && resource.data.userId == request.auth.uid;
      allow create:      if isSignedIn() && request.resource.data.userId == request.auth.uid;
    }
  }
}""")
    add_body(g['doc'], "Bộ rules trên đảm bảo: (1) khách hàng tuyệt đối không truy cập được dữ liệu của người khác; (2) khách không thể tự cập nhật trạng thái đơn (chỉ admin); (3) admin có toàn quyền nhưng phải đăng nhập; (4) các collection danh mục có thể đọc tự do (đã đăng nhập) nhưng chỉ admin được sửa. Bộ rules đầy đủ được lưu trong Phụ lục C.")

    add_h2(g['doc'], "2.5. Kiến trúc tổng thể của ứng dụng")
    add_h3(g['doc'], "2.5.1. Mô hình MVVM trong dự án")
    add_body(g['doc'], "Như đã trình bày ở Chương 1, dự án áp dụng nhất quán mô hình MVVM kết hợp Repository Pattern. Cụ thể trong dự án PetShop, vai trò các tầng như sau:")
    add_bullets(g['doc'], [
        "Model (model/entity, model/request, model/response): các POJO ánh xạ document Firestore và DTO nội bộ. Ví dụ: User, Pet, Food, Cart, Order, Voucher, Notification…",
        "Repository (repository/): chịu trách nhiệm I/O với Firestore (CRUD, transaction, snapshot listener), Storage (upload ảnh) và REST API (OkHttp). Mỗi repository chỉ phụ thuộc Firestore SDK, không phụ thuộc Android UI.",
        "ViewModel (viewmodel/): giữ trạng thái màn hình bằng MutableLiveData; gọi Repository, transform/aggregate dữ liệu rồi postValue. ViewModel KHÔNG biết tới Activity/Fragment cụ thể.",
        "View (view/activity, view/fragment, view/adapter, view/dialog): hiển thị UI và observe LiveData; chỉ gọi method của ViewModel khi người dùng tương tác.",
        "Utils (utils/): các lớp hỗ trợ chung như VNPayHelper (build URL HMAC-SHA512), EmailHelper (gửi OTP), ShippingHelper (tính phí ship), PromotionManager, StorageHelper…",
    ])

    add_h3(g['doc'], "2.5.2. Sơ đồ luồng dữ liệu giữa các tầng")
    add_image(g['doc'], "diagram_mvvm-dataflow.png",
              "Sơ đồ luồng dữ liệu giữa các tầng trong MVVM", width_cm=15)
    add_body(g['doc'], "Sơ đồ thể hiện chu trình dữ liệu chuẩn: View → ViewModel → Repository → Firebase/API → callback ngược lại → ViewModel → LiveData → View. Cả chu trình diễn ra bất đồng bộ; LiveData đảm bảo việc cập nhật UI luôn xảy ra trên main thread và an toàn lifecycle.")

    add_h3(g['doc'], "2.5.3. Tổ chức package và quy ước đặt tên")
    add_image(g['doc'], "diagram_package-layout.png",
              "Tổ chức package mã nguồn theo MVVM và Repository", width_cm=15)
    add_body(g['doc'], "Các quy ước đặt tên trong dự án:")
    add_bullets(g['doc'], [
        "Activity: <Tên>Activity.java (vd: LoginActivity, CheckoutActivity).",
        "Fragment: <Tên>Fragment.java.",
        "ViewModel: <Tên>ViewModel.java – mỗi tính năng/module một ViewModel.",
        "Repository: <Tên>Repository.java – tách theo domain.",
        "Adapter: <Tên>Adapter.java – kèm interface OnItemClickListener nếu cần.",
        "Layout XML: activity_<ten>.xml / fragment_<ten>.xml / item_<ten>.xml / dialog_<ten>.xml.",
        "Resource id: theo dạng tvName, etEmail, btnLogin, ivAvatar, rvList…",
        "Hằng số: viết HOA_GẠCH_DƯỚI, đặt trong Constants.java hoặc trong chính lớp sở hữu.",
    ])

    add_h2(g['doc'], "2.6. Thiết kế giao diện (UI/UX)")
    add_h3(g['doc'], "2.6.1. Bộ màu, font, icon, theme")
    add_body(g['doc'], "Giao diện được thiết kế theo phong cách Material Design 3 với bảng màu lấy cảm hứng từ tông cam ấm – gợi cảm giác thân thiện, gần gũi với thú cưng (file colors.xml):")
    add_bullets(g['doc'], [
        "Primary: #F5A623 (cam đậm), Primary Dark: #E09010, Primary Light: #FFD580.",
        "Background chính: #FFF8F2 (kem nhạt), Card: #FFFFFF.",
        "Text Primary: #1A1A1A, Text Secondary: #888888, Hint: #AEAEB2.",
        "Status: Success #34C759, Error #FF3B30, Warning #FF9500.",
        "Font: Roboto (hệ thống) cho UI, Times New Roman cho báo cáo.",
        "Icon: Material Icons + một số icon vẽ riêng (ic_paw, ic_cart, ic_chat,...).",
    ])

    add_h3(g['doc'], "2.6.2. Wireframe / Mockup các màn hình chính")
    add_body(g['doc'], "Trước khi viết XML layout, nhóm vẽ wireframe các màn hình chính trên Figma, bao gồm: Splash, Login, Register, Home, Pet/Food Detail, Cart, Checkout, Order, Profile (cho Customer); Dashboard, Manage Users/Pets/Foods/Vouchers (cho Admin). Wireframe được giảng viên duyệt trước khi nhóm bắt tay vào code, giúp giảm thiểu việc phải sửa giao diện sau này. Một số ảnh chụp màn hình thực tế của ứng dụng được trình bày trong Phụ lục D.")
    add_body(g['doc'], "[CHỤP ẢNH 2.6] Đề nghị nhóm chèn 1–2 mockup tiêu biểu của Figma tại đây để minh hoạ giai đoạn thiết kế.")
