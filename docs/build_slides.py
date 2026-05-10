"""Generate BAO_CAO_SLIDES.pptx for PetShop project.

Heavy on visuals (diagrams already rendered to docs/images/diagram_*.png),
light on text – per stakeholder request.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Cm, Inches, Pt

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "images"
OUT = ROOT / "BAO_CAO_SLIDES.pptx"

# 16:9
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# ---- Brand palette (đồng bộ với colors.xml của app) ------------------------
PRIMARY      = RGBColor(0xF5, 0xA6, 0x23)  # cam
PRIMARY_DARK = RGBColor(0xE0, 0x90, 0x10)
PRIMARY_LITE = RGBColor(0xFF, 0xD5, 0x80)
BG_MAIN      = RGBColor(0xFF, 0xF8, 0xF2)
BG_CARD      = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK    = RGBColor(0x1A, 0x1A, 0x1A)
TEXT_GREY    = RGBColor(0x55, 0x55, 0x55)
GREEN        = RGBColor(0x34, 0xC7, 0x59)
RED          = RGBColor(0xFF, 0x3B, 0x30)
BLUE         = RGBColor(0x00, 0x7A, 0xFF)
PURPLE       = RGBColor(0x66, 0x33, 0xCC)
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)


def setup_prs() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_blank(prs):
    blank_layout = prs.slide_layouts[6]  # blank
    s = prs.slides.add_slide(blank_layout)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_MAIN
    bg.line.fill.background()
    return s


def add_text(slide, text, left, top, width, height,
             size=18, bold=False, color=TEXT_DARK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Cm(0.1)
    tf.margin_right = Cm(0.1)
    tf.margin_top = Cm(0.05)
    tf.margin_bottom = Cm(0.05)
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font
    return tb


def add_bullets(slide, items, left, top, width, height,
                size=18, color=TEXT_DARK, line_spacing=1.15, font="Calibri"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, line in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(4)
        run = p.add_run()
        run.text = "•  " + line
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.name = font
    return tb


def add_pill(slide, text, left, top, width, height, fill, fg=WHITE, size=14, bold=True):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    s.adjustments[0] = 0.5
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    tf = s.text_frame
    tf.margin_left = Cm(0.2); tf.margin_right = Cm(0.2)
    tf.margin_top = Cm(0.05); tf.margin_bottom = Cm(0.05)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = fg; r.font.name = "Calibri"


def add_card(slide, title, body, left, top, width, height,
             accent=PRIMARY, body_size=13, title_size=16):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.adjustments[0] = 0.06
    card.fill.solid(); card.fill.fore_color.rgb = BG_CARD
    card.line.color.rgb = PRIMARY_LITE
    card.line.width = Pt(0.75)

    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 left, top, Cm(0.25), height)
    bar.adjustments[0] = 0.5
    bar.fill.solid(); bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    add_text(slide, title,
             left + Cm(0.5), top + Cm(0.2),
             width - Cm(0.6), Cm(0.9),
             size=title_size, bold=True, color=accent)
    add_bullets(slide, body if isinstance(body, list) else [body],
                left + Cm(0.5), top + Cm(0.95),
                width - Cm(0.6), height - Cm(1.0),
                size=body_size, color=TEXT_DARK)


def add_header(slide, eyebrow, title, page_no=None, total=None):
    # Top accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Cm(0.35))
    bar.fill.solid(); bar.fill.fore_color.rgb = PRIMARY
    bar.line.fill.background()

    add_text(slide, eyebrow, Cm(1), Cm(0.55), Cm(20), Cm(0.7),
             size=12, bold=True, color=PRIMARY_DARK)
    add_text(slide, title, Cm(1), Cm(1.05), SLIDE_W - Cm(2), Cm(1.3),
             size=28, bold=True, color=TEXT_DARK)
    # underline
    ul = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(1), Cm(2.3), Cm(2.5), Cm(0.12))
    ul.fill.solid(); ul.fill.fore_color.rgb = PRIMARY
    ul.line.fill.background()

    if page_no and total:
        add_text(slide, f"{page_no} / {total}",
                 SLIDE_W - Cm(3), Cm(0.55), Cm(2), Cm(0.7),
                 size=11, color=TEXT_GREY, align=PP_ALIGN.RIGHT)


def add_footer(slide, text="PetShop – Đồ án Phát triển Ứng dụng Di động • Nhóm 3 thành viên"):
    add_text(slide, text, Cm(1), SLIDE_H - Cm(0.9),
             SLIDE_W - Cm(2), Cm(0.6),
             size=10, color=TEXT_GREY, align=PP_ALIGN.LEFT)


def add_image(slide, path, left, top, width=None, height=None):
    p = IMG / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return None
    return slide.shapes.add_picture(str(p), left, top, width=width, height=height)


def add_image_fit(slide, path, left, top, max_w, max_h, center=True, border=False):
    """Fit image inside (max_w, max_h) preserving aspect ratio.

    Auto-centers within the box. Returns (left, top, w, h) of placed picture.
    """
    p = IMG / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return None
    from PIL import Image as PILImage
    with PILImage.open(p) as im:
        iw, ih = im.size
    ratio = iw / ih
    box_ratio = max_w / max_h
    if ratio > box_ratio:
        w = max_w
        h = int(max_w / ratio)
    else:
        h = max_h
        w = int(max_h * ratio)
    cx = left + (max_w - w) // 2 if center else left
    cy = top + (max_h - h) // 2 if center else top
    pic = slide.shapes.add_picture(str(p), cx, cy, width=w, height=h)
    if border:
        bd = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, cy, w, h)
        bd.fill.background()
        bd.line.color.rgb = PRIMARY_LITE
        bd.line.width = Pt(0.75)
    return pic


# ===========================================================================
# Build slides
# ===========================================================================
prs = setup_prs()
TOTAL = 28  # planned slide count

# ---------- 1. COVER --------------------------------------------------------
s = add_blank(prs)
# Half-height accent
hero = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Cm(11))
hero.fill.solid(); hero.fill.fore_color.rgb = PRIMARY
hero.line.fill.background()
# diagonal decoration
deco = s.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE,
                          SLIDE_W - Cm(8), 0, Cm(8), Cm(11))
deco.fill.solid(); deco.fill.fore_color.rgb = PRIMARY_DARK
deco.line.fill.background()
deco2 = s.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE,
                           SLIDE_W - Cm(4), 0, Cm(4), Cm(11))
deco2.fill.solid(); deco2.fill.fore_color.rgb = PRIMARY_LITE
deco2.line.fill.background()

add_text(s, "ĐỒ ÁN PHÁT TRIỂN ỨNG DỤNG DI ĐỘNG",
         Cm(1.5), Cm(2.5), Cm(20), Cm(1),
         size=18, bold=True, color=WHITE)
add_text(s, "PETSHOP",
         Cm(1.5), Cm(3.4), Cm(20), Cm(2.5),
         size=72, bold=True, color=WHITE)
add_text(s, "Ứng dụng cửa hàng thú cưng & thức ăn trên Android",
         Cm(1.5), Cm(6.5), Cm(20), Cm(1),
         size=22, color=WHITE)
add_pill(s, "Java • Firebase • VNPay • OpenAI",
         Cm(1.5), Cm(8.0), Cm(11), Cm(1.0),
         fill=WHITE, fg=PRIMARY_DARK, size=15)

add_text(s, "Thực hiện bởi:", Cm(1.5), Cm(12.0), Cm(8), Cm(0.8),
         size=14, bold=True, color=TEXT_DARK)
add_text(s, "Nguyễn Văn Trường   •   Đào Trúc Mai   •   Nguyễn Hữu Đức Thọ",
         Cm(1.5), Cm(12.7), Cm(20), Cm(0.8),
         size=14, color=TEXT_DARK)
add_text(s, "GVHD: ………… • Năm học 2025-2026",
         Cm(1.5), Cm(13.5), Cm(20), Cm(0.8),
         size=12, color=TEXT_GREY)

# ---------- 2. AGENDA -------------------------------------------------------
s = add_blank(prs); add_header(s, "MỞ ĐẦU", "Nội dung trình bày", 2, TOTAL)
agenda = [
    ("1", "Tổng quan đề tài", PRIMARY),
    ("2", "Khảo sát & Phân tích yêu cầu", BLUE),
    ("3", "Phân tích – Thiết kế hệ thống", PURPLE),
    ("4", "Công nghệ & Kiến trúc", GREEN),
    ("5", "Demo các chức năng chính", PRIMARY_DARK),
    ("6", "Kiểm thử & Đánh giá", RED),
    ("7", "Phân công công việc", BLUE),
    ("8", "Kết luận & Hướng phát triển", GREEN),
]
col_w = Cm(15); row_h = Cm(1.05)
for i, (num, name, col) in enumerate(agenda):
    top = Cm(3.2 + i * 1.25)
    circle = s.shapes.add_shape(MSO_SHAPE.OVAL, Cm(2.5), top, Cm(1.0), Cm(1.0))
    circle.fill.solid(); circle.fill.fore_color.rgb = col
    circle.line.fill.background()
    tf = circle.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = num
    r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Calibri"
    add_text(s, name, Cm(4.0), top + Cm(0.05), col_w, Cm(1),
             size=20, bold=True, color=TEXT_DARK, anchor=MSO_ANCHOR.MIDDLE)
add_footer(s)

# ---------- 3. WHY (problem) ------------------------------------------------
s = add_blank(prs); add_header(s, "1 • TỔNG QUAN", "Vì sao chọn đề tài?", 3, TOTAL)
add_text(s, "“Thị trường thú cưng tăng nóng – nhưng giao dịch còn rời rạc trên MXH.”",
         Cm(1.5), Cm(2.8), Cm(20), Cm(1.2),
         size=18, bold=True, color=TEXT_DARK)
stats = [
    ("40%", "hộ gia đình thành thị nuôi thú cưng", PRIMARY),
    ("Top 5", "thị trường thú cưng tăng trưởng nhanh ĐNÁ", GREEN),
    ("80%", "giao dịch qua MXH, thiếu bảo đảm", RED),
    ("0", "app Việt chuyên Pet kết hợp AI tư vấn", BLUE),
]
W = Cm(7); H = Cm(4.7); GAP = Cm(0.6)
for i, (big, small, col) in enumerate(stats):
    left = Cm(1) + (W + GAP) * (i % 2) + (Cm(8) if i // 2 else Cm(0))
    top  = Cm(4.5) + (H + GAP) * (i // 2)
    # alt: 4 cards in 2x2
    left = Cm(1) + (W + GAP) * (i % 2)
    top  = Cm(4.4) + (H + GAP) * (i // 2)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, W, H)
    box.adjustments[0] = 0.05
    box.fill.solid(); box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = col; box.line.width = Pt(1)
    add_text(s, big, left, top + Cm(0.4), W, Cm(2.2),
             size=46, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, small, left + Cm(0.5), top + Cm(2.6), W - Cm(1), Cm(2),
             size=14, color=TEXT_DARK, align=PP_ALIGN.CENTER)
# right side big takeaway
add_card(s, "Cần một giải pháp",
         ["Nền tảng tập trung, chuyên cho lĩnh vực thú cưng",
          "Có tích hợp thanh toán điện tử & AI tư vấn",
          "Hỗ trợ cả KHÁCH HÀNG và QUẢN TRỊ VIÊN trong 1 app"],
         Cm(16.5), Cm(4.4), Cm(13.3), Cm(10),
         accent=PRIMARY, title_size=22, body_size=16)
add_footer(s)

# ---------- 4. GOALS --------------------------------------------------------
s = add_blank(prs); add_header(s, "1 • TỔNG QUAN", "Mục tiêu & Phạm vi", 4, TOTAL)
goals = [
    ("Người dùng", "Khách hàng + Quản trị viên", PRIMARY),
    ("Sản phẩm", "Thú cưng (Pet) + Thức ăn (Food)", BLUE),
    ("E-commerce", "Cart → Checkout → COD/VNPay → Giao hàng → Hoàn trả", GREEN),
    ("Backend", "Firebase Auth + Firestore + Storage", PURPLE),
    ("AI", "Chatbot OpenAI gpt-4o-mini tư vấn 24/7", RED),
    ("Kiến trúc", "MVVM + Repository Pattern", PRIMARY_DARK),
]
W = Cm(9.6); H = Cm(3.4); GAP = Cm(0.4)
for i, (t, b, col) in enumerate(goals):
    col_idx = i % 3; row_idx = i // 3
    left = Cm(1) + (W + GAP) * col_idx
    top  = Cm(3.2) + (H + GAP) * row_idx
    add_card(s, t, b, left, top, W, H, accent=col, title_size=18, body_size=15)
add_footer(s)

# ---------- 5. USE CASE -----------------------------------------------------
s = add_blank(prs); add_header(s, "2 • PHÂN TÍCH YÊU CẦU", "Use Case Diagram", 5, TOTAL)
add_image_fit(s, "diagram_usecase.png",
              Cm(0.7), Cm(2.7), max_w=Cm(31.5), max_h=Cm(8.5))
add_card(s, "Khách hàng",
         ["10 chức năng chính", "Đặt hàng + Thanh toán", "Hoàn trả + Đánh giá", "Chat AI 24/7"],
         Cm(0.7), Cm(11.5), Cm(15), Cm(2.6),
         accent=PRIMARY, body_size=14, title_size=16)
add_card(s, "Quản trị viên",
         ["Dashboard real-time", "CRUD Pet/Food/Voucher", "Duyệt đơn & Hoàn trả", "Gửi notification hàng loạt"],
         Cm(16.5), Cm(11.5), Cm(15), Cm(2.6),
         accent=BLUE, body_size=14, title_size=16)
add_footer(s)

# ---------- 6. ARCH ---------------------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Kiến trúc tổng thể (MVVM + Repository + Firebase)", 6, TOTAL)
add_image_fit(s, "diagram_architecture.png",
              Cm(0.7), Cm(2.8), max_w=Cm(31.5), max_h=Cm(7.5))
items = [
    ("View",       "Activity / Fragment / Adapter", PRIMARY),
    ("ViewModel",  "LiveData – tách logic UI", BLUE),
    ("Repository", "I/O Firestore + API ngoài", GREEN),
    ("Backend",    "Firebase + VNPay + OpenAI + SMTP", PURPLE),
]
W = Cm(7.5); GAP = Cm(0.4)
for i, (t, b, c) in enumerate(items):
    left = Cm(0.7) + (W + GAP) * i
    add_card(s, t, b, left, Cm(11.0), W, Cm(3.0),
             accent=c, body_size=14, title_size=16)
add_footer(s)

# ---------- 7. ERD ----------------------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Mô hình dữ liệu (Firestore – ER logic)", 7, TOTAL)
add_image_fit(s, "diagram_erd.png",
              Cm(0.7), Cm(2.8), max_w=Cm(31.5), max_h=Cm(7.5))
add_card(s, "15 collection chính",
         ["users, addresses, notifications",
          "pets, foods, categories",
          "orders, order_items, return_requests",
          "vouchers, voucher_usage, promotions",
          "chat_sessions, chat_messages, banners"],
         Cm(0.7), Cm(11.0), Cm(15.5), Cm(3.0),
         accent=PURPLE, body_size=14, title_size=16)
add_card(s, "Điểm thiết kế nổi bật",
         ["Snapshot listener real-time",
          "Atomic update bằng Firestore Transaction",
          "Sub-collection cho voucher_usage / chat_messages"],
         Cm(16.7), Cm(11.0), Cm(15.5), Cm(3.0),
         accent=GREEN, body_size=14, title_size=16)
add_footer(s)

# ---------- 8. AUTH FLOW ----------------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Luồng Đăng ký – Đăng nhập (Auth Flow)", 8, TOTAL)
add_image_fit(s, "diagram_auth-flow.png",
              Cm(0.5), Cm(2.7), max_w=Cm(21.5), max_h=Cm(11.5))
add_pill(s, "Email + Password",   Cm(22.5), Cm(3.0),  Cm(9), Cm(1.0), fill=PRIMARY)
add_pill(s, "Google Sign-In",     Cm(22.5), Cm(4.3),  Cm(9), Cm(1.0), fill=BLUE)
add_pill(s, "OTP qua Gmail SMTP", Cm(22.5), Cm(5.6),  Cm(9), Cm(1.0), fill=GREEN)
add_pill(s, "Quên mật khẩu",      Cm(22.5), Cm(6.9),  Cm(9), Cm(1.0), fill=PURPLE)
add_card(s, "Bảo mật",
         ["Firebase Auth quản lý phiên",
          "OTP 6 số sinh ngẫu nhiên (5 phút)",
          "parseAuthError → dịch tiếng Việt"],
         Cm(22.5), Cm(8.3), Cm(9), Cm(5.5),
         accent=RED, body_size=14, title_size=16)
add_footer(s)

# ---------- 9. CHECKOUT FLOW -----------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Luồng Đặt hàng & Thanh toán", 9, TOTAL)
add_image_fit(s, "diagram_checkout-flow.png",
              Cm(0.5), Cm(2.7), max_w=Cm(15), max_h=Cm(11.5))
add_card(s, "2 phương thức",
         ["COD – Pending ngay", "VNPay – chờ thanh toán"],
         Cm(16), Cm(3.0), Cm(15.5), Cm(3.2),
         accent=PRIMARY, body_size=15, title_size=18)
add_card(s, "Phí ship theo vùng",
         ["TP. HCM: 30k", "Miền Nam: 45k", "Miền Trung: 60k",
          "Miền Bắc: 75k", "Free ship ≥ 500.000đ"],
         Cm(16), Cm(6.4), Cm(15.5), Cm(5.0),
         accent=GREEN, body_size=15, title_size=18)
add_card(s, "Voucher",
         ["PERCENT • FIXED • FREESHIP"],
         Cm(16), Cm(11.6), Cm(15.5), Cm(2.4),
         accent=BLUE, body_size=15, title_size=18)
add_footer(s)

# ---------- 10. STATE -------------------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Sơ đồ trạng thái Đơn hàng", 10, TOTAL)
add_image_fit(s, "diagram_order-state.png",
              Cm(0.7), Cm(2.7), max_w=Cm(14), max_h=Cm(11.5))
add_card(s, "11 trạng thái",
         ["WAITING_PAYMENT  •  PENDING",
          "CONFIRMED  •  PREPARING  •  SHIPPING",
          "DELIVERED  •  COMPLETED",
          "CANCELLED",
          "RETURN_REQUESTED  •  RETURN_APPROVED  •  REFUNDED"],
         Cm(15.5), Cm(3.0), Cm(16), Cm(6.0),
         accent=PURPLE, body_size=15, title_size=18)
add_card(s, "Bảo toàn dữ liệu",
         ["Mọi chuyển trạng thái dùng Firestore Transaction",
          "Tự động hoàn stock & lượt voucher khi CANCELLED",
          "Cập nhật totalOrders / totalSpent best-effort"],
         Cm(15.5), Cm(9.2), Cm(16), Cm(4.8),
         accent=GREEN, body_size=15, title_size=18)
add_footer(s)

# ---------- 11. SEQUENCE VNPay ---------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Sequence Diagram – Thanh toán VNPay", 11, TOTAL)
add_image_fit(s, "diagram_sequence-vnpay.png",
              Cm(0.5), Cm(2.7), max_w=Cm(31.5), max_h=Cm(7.5))
add_card(s, "VNPayHelper",
         ["URL-encode UTF-8",
          "Sort tham số TreeMap",
          "HMAC-SHA512 chữ ký",
          "vnp_ExpireDate = 15 phút"],
         Cm(0.7), Cm(11.0), Cm(15.5), Cm(3.2),
         accent=RED, body_size=14, title_size=16)
add_card(s, "completeVNPayOrder",
         ["Atomic transaction:",
          "status = PENDING  •  paymentStatus = PAID",
          "Trừ stock + Pet = RESERVED + Notification"],
         Cm(16.7), Cm(11.0), Cm(15.5), Cm(3.2),
         accent=GREEN, body_size=14, title_size=16)
add_footer(s)

# ---------- 12. CHAT RAG ----------------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Chat AI – RAG nhẹ với dữ liệu sản phẩm", 12, TOTAL)
add_image_fit(s, "diagram_chat-rag.png",
              Cm(0.5), Cm(2.7), max_w=Cm(31.5), max_h=Cm(7.5))
add_card(s, "Khách chưa login",
         ["Lưu local SharedPreferences", "Giới hạn 50 tin"],
         Cm(0.7), Cm(11.0), Cm(10), Cm(3.2),
         accent=PRIMARY, body_size=14, title_size=16)
add_card(s, "Khách đã login",
         ["Sync lên Firestore (chat_sessions)", "Đa phiên hội thoại"],
         Cm(11.0), Cm(11.0), Cm(10), Cm(3.2),
         accent=GREEN, body_size=14, title_size=16)
add_card(s, "Tính năng nâng cao",
         ["Voice → Text", "Gửi ảnh (Base64)", "Markdown render"],
         Cm(21.3), Cm(11.0), Cm(10.5), Cm(3.2),
         accent=PURPLE, body_size=14, title_size=16)
add_footer(s)

# ---------- 13. RETURN FLOW -------------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Luồng Hoàn trả & Hoàn tiền", 13, TOTAL)
add_image_fit(s, "diagram_return-flow.png",
              Cm(0.5), Cm(2.7), max_w=Cm(13), max_h=Cm(11.5))
add_card(s, "Hoàn trả COD",
         ["Khách nhập Số tài khoản + Tên ngân hàng",
          "Admin chuyển khoản thủ công",
          "Status: REQUESTED → APPROVED → REFUNDED"],
         Cm(14), Cm(3.0), Cm(17.5), Cm(4.0),
         accent=PRIMARY, body_size=15, title_size=18)
add_card(s, "Hoàn trả VNPay",
         ["Hoàn về thẻ/tài khoản thanh toán gốc",
          "Cần tích hợp Cloud Function (TODO)"],
         Cm(14), Cm(7.2), Cm(17.5), Cm(3.5),
         accent=BLUE, body_size=15, title_size=18)
add_card(s, "Tác động Dashboard",
         ["Tự động trừ doanh thu (refundedMoney)",
          "Cập nhật tile Tiền hoàn"],
         Cm(14), Cm(10.9), Cm(17.5), Cm(3.0),
         accent=RED, body_size=15, title_size=18)
add_footer(s)

# ---------- 14. ADMIN DASHBOARD --------------------------------------------
s = add_blank(prs); add_header(s, "3 • THIẾT KẾ", "Admin Dashboard – Real-time với SnapshotListener", 14, TOTAL)
add_image_fit(s, "diagram_admin-dashboard.png",
              Cm(0.5), Cm(2.7), max_w=Cm(17), max_h=Cm(11.5))
add_card(s, "9 chỉ số real-time",
         ["Tổng doanh thu", "Tổng đơn (đã chốt)",
          "Người dùng", "Đơn pending",
          "Preparing • Shipping • Delivered",
          "Đơn huỷ", "Tiền hoàn"],
         Cm(18), Cm(3.0), Cm(13.5), Cm(6.0),
         accent=PRIMARY, body_size=14, title_size=18)
add_card(s, "Quy tắc tính",
         ["Chỉ tính khách hàng ACTIVE",
          "COD → đếm khi DELIVERED/COMPLETED",
          "VNPAY → đếm khi PAID",
          "Doanh thu thực = revenue – refund"],
         Cm(18), Cm(9.2), Cm(13.5), Cm(4.8),
         accent=GREEN, body_size=14, title_size=18)
add_footer(s)

# ---------- 15. TECH STACK --------------------------------------------------
s = add_blank(prs); add_header(s, "4 • CÔNG NGHỆ", "Stack đầy đủ", 15, TOTAL)
tech = [
    ("Java 11", "Ngôn ngữ chính", PRIMARY),
    ("Android SDK 36", "min API 24, target 36", BLUE),
    ("Material Design", "Component + Color theme", GREEN),
    ("Firebase Auth", "Email + Google", PURPLE),
    ("Firestore", "NoSQL real-time", RED),
    ("Firebase Storage", "Upload ảnh / video", PRIMARY_DARK),
    ("VNPay Sandbox", "HMAC-SHA512", BLUE),
    ("OpenAI GPT-4o-mini", "Chatbot + Vision", GREEN),
    ("OkHttp + Gson", "HTTP & JSON", PURPLE),
    ("Glide", "Tải & cache ảnh", PRIMARY),
    ("JavaMail", "OTP qua Gmail SMTP", RED),
    ("Gradle KTS", "Version Catalog", PRIMARY_DARK),
]
W = Cm(7.2); H = Cm(2.5); GAP_X = Cm(0.4); GAP_Y = Cm(0.35)
for i, (t, b, col) in enumerate(tech):
    col_idx = i % 4; row_idx = i // 4
    left = Cm(1) + (W + GAP_X) * col_idx
    top  = Cm(3.2) + (H + GAP_Y) * row_idx
    add_card(s, t, b, left, top, W, H, accent=col, body_size=12, title_size=15)
add_footer(s)

# ---------- 16. CODE STATS --------------------------------------------------
s = add_blank(prs); add_header(s, "4 • CÔNG NGHỆ", "Quy mô mã nguồn", 16, TOTAL)
nums = [
    ("30+",  "Activity",            PRIMARY),
    ("6",    "Fragment",            BLUE),
    ("19",   "Adapter",             GREEN),
    ("14",   "ViewModel",           PURPLE),
    ("13",   "Repository",          RED),
    ("17",   "Entity (model)",      PRIMARY_DARK),
    ("62",   "Layout XML",          BLUE),
    ("~20K", "LOC Java + XML",      GREEN),
]
W = Cm(7.2); H = Cm(4.7); GAP = Cm(0.4)
for i, (big, small, col) in enumerate(nums):
    col_idx = i % 4; row_idx = i // 4
    left = Cm(1) + (W + GAP) * col_idx
    top  = Cm(3.4) + (H + GAP) * row_idx
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, W, H)
    box.adjustments[0] = 0.05
    box.fill.solid(); box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = col; box.line.width = Pt(1.2)
    add_text(s, big, left, top + Cm(0.5), W, Cm(2.4),
             size=44, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, small, left, top + Cm(3.0), W, Cm(1.4),
             size=15, color=TEXT_DARK, align=PP_ALIGN.CENTER, bold=True)
add_footer(s)

# ---------- 17. DEMO CUSTOMER 1 (Auth + Home) -------------------------------
s = add_blank(prs); add_header(s, "5 • DEMO", "Khách hàng – Đăng ký & Trang chủ", 17, TOTAL)
ph_w = Cm(7); ph_h = Cm(11)
captions = [
    ("Splash + Onboarding", "activity_splash"),
    ("Đăng ký + OTP email", "activity_register"),
    ("Đăng nhập Google",    "activity_login"),
    ("Trang chủ + Search",  "fragment_home"),
]
for i, (cap, lay) in enumerate(captions):
    left = Cm(1.2 + i * 7.6); top = Cm(3.0)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, ph_w, ph_h)
    box.adjustments[0] = 0.04
    box.fill.solid(); box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = PRIMARY_LITE; box.line.width = Pt(1)
    add_text(s, "[ Screenshot ]", left, top + Cm(4.5), ph_w, Cm(1),
             size=14, color=TEXT_GREY, align=PP_ALIGN.CENTER, bold=True)
    add_text(s, lay + ".xml", left, top + Cm(5.3), ph_w, Cm(0.7),
             size=11, color=TEXT_GREY, align=PP_ALIGN.CENTER)
    add_text(s, cap, left, top + ph_h + Cm(0.2), ph_w, Cm(0.8),
             size=14, bold=True, color=TEXT_DARK, align=PP_ALIGN.CENTER)
add_text(s, "Chèn ảnh thật vào 4 khung trên (chụp từ emulator)",
         Cm(1), SLIDE_H - Cm(1.5), Cm(30), Cm(0.6),
         size=11, color=TEXT_GREY, align=PP_ALIGN.CENTER)
add_footer(s)

# ---------- 18. DEMO CUSTOMER 2 (Cart + Checkout + VNPay) -------------------
s = add_blank(prs); add_header(s, "5 • DEMO", "Khách hàng – Giỏ hàng & Thanh toán", 18, TOTAL)
captions = [
    ("Pet/Food Detail",    "activity_pet_detail"),
    ("Giỏ hàng",            "activity_cart"),
    ("Checkout + Voucher",  "activity_checkout"),
    ("VNPay Sandbox",       "activity_vnpay_webview"),
]
for i, (cap, lay) in enumerate(captions):
    left = Cm(1.2 + i * 7.6); top = Cm(3.0)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, ph_w, ph_h)
    box.adjustments[0] = 0.04
    box.fill.solid(); box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = PRIMARY_LITE; box.line.width = Pt(1)
    add_text(s, "[ Screenshot ]", left, top + Cm(4.5), ph_w, Cm(1),
             size=14, color=TEXT_GREY, align=PP_ALIGN.CENTER, bold=True)
    add_text(s, lay + ".xml", left, top + Cm(5.3), ph_w, Cm(0.7),
             size=11, color=TEXT_GREY, align=PP_ALIGN.CENTER)
    add_text(s, cap, left, top + ph_h + Cm(0.2), ph_w, Cm(0.8),
             size=14, bold=True, color=TEXT_DARK, align=PP_ALIGN.CENTER)
add_footer(s)

# ---------- 19. DEMO CUSTOMER 3 (Order, Return, Notif, Chat) ----------------
s = add_blank(prs); add_header(s, "5 • DEMO", "Khách hàng – Đơn hàng • Hoàn trả • Thông báo • Chat AI", 19, TOTAL)
captions = [
    ("Lịch sử đơn",         "activity_order_history"),
    ("Yêu cầu hoàn trả",    "activity_return_request"),
    ("Thông báo + badge",   "activity_notification"),
    ("Chat AI hỗ trợ",      "activity_chat"),
]
for i, (cap, lay) in enumerate(captions):
    left = Cm(1.2 + i * 7.6); top = Cm(3.0)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, ph_w, ph_h)
    box.adjustments[0] = 0.04
    box.fill.solid(); box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = PRIMARY_LITE; box.line.width = Pt(1)
    add_text(s, "[ Screenshot ]", left, top + Cm(4.5), ph_w, Cm(1),
             size=14, color=TEXT_GREY, align=PP_ALIGN.CENTER, bold=True)
    add_text(s, lay + ".xml", left, top + Cm(5.3), ph_w, Cm(0.7),
             size=11, color=TEXT_GREY, align=PP_ALIGN.CENTER)
    add_text(s, cap, left, top + ph_h + Cm(0.2), ph_w, Cm(0.8),
             size=14, bold=True, color=TEXT_DARK, align=PP_ALIGN.CENTER)
add_footer(s)

# ---------- 20. DEMO ADMIN 1 (Dashboard + Order) ----------------------------
s = add_blank(prs); add_header(s, "5 • DEMO", "Admin – Dashboard & Quản lý đơn", 20, TOTAL)
captions = [
    ("Admin Dashboard",         "activity_admin"),
    ("Quản lý đơn hàng",         "activity_admin_order_list"),
    ("Chi tiết đơn (Admin)",    "activity_order_detail"),
    ("Duyệt hoàn trả",           "activity_admin_return_list"),
]
for i, (cap, lay) in enumerate(captions):
    left = Cm(1.2 + i * 7.6); top = Cm(3.0)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, ph_w, ph_h)
    box.adjustments[0] = 0.04
    box.fill.solid(); box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = BLUE; box.line.width = Pt(1)
    add_text(s, "[ Screenshot ]", left, top + Cm(4.5), ph_w, Cm(1),
             size=14, color=TEXT_GREY, align=PP_ALIGN.CENTER, bold=True)
    add_text(s, lay + ".xml", left, top + Cm(5.3), ph_w, Cm(0.7),
             size=11, color=TEXT_GREY, align=PP_ALIGN.CENTER)
    add_text(s, cap, left, top + ph_h + Cm(0.2), ph_w, Cm(0.8),
             size=14, bold=True, color=TEXT_DARK, align=PP_ALIGN.CENTER)
add_footer(s)

# ---------- 21. DEMO ADMIN 2 (CRUD) -----------------------------------------
s = add_blank(prs); add_header(s, "5 • DEMO", "Admin – Quản lý sản phẩm & marketing", 21, TOTAL)
captions = [
    ("Quản lý Pet",     "activity_manage_pets"),
    ("Quản lý Food",    "activity_manage_foods"),
    ("Quản lý Voucher", "activity_manage_vouchers"),
    ("Quản lý Khuyến mãi","activity_manage_promotions"),
]
for i, (cap, lay) in enumerate(captions):
    left = Cm(1.2 + i * 7.6); top = Cm(3.0)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, ph_w, ph_h)
    box.adjustments[0] = 0.04
    box.fill.solid(); box.fill.fore_color.rgb = BG_CARD
    box.line.color.rgb = GREEN; box.line.width = Pt(1)
    add_text(s, "[ Screenshot ]", left, top + Cm(4.5), ph_w, Cm(1),
             size=14, color=TEXT_GREY, align=PP_ALIGN.CENTER, bold=True)
    add_text(s, lay + ".xml", left, top + Cm(5.3), ph_w, Cm(0.7),
             size=11, color=TEXT_GREY, align=PP_ALIGN.CENTER)
    add_text(s, cap, left, top + ph_h + Cm(0.2), ph_w, Cm(0.8),
             size=14, bold=True, color=TEXT_DARK, align=PP_ALIGN.CENTER)
add_footer(s)

# ---------- 22. TEST RESULTS ------------------------------------------------
s = add_blank(prs); add_header(s, "6 • KIỂM THỬ", "Kết quả Test Case (14 ca tiêu biểu)", 22, TOTAL)
items_l = [
    ("TC-01", "Đăng ký email trùng → báo lỗi", GREEN),
    ("TC-02", "OTP sai → cảnh báo, không tạo TK", GREEN),
    ("TC-03", "Đặt COD → status PENDING, trừ stock", GREEN),
    ("TC-04", "VNPay PAID → status PENDING + paid", GREEN),
    ("TC-05", "VNPay huỷ → đơn vẫn WAIT_PAY", GREEN),
    ("TC-06", "Voucher FREESHIP → ship = 0", GREEN),
    ("TC-07", "Voucher quá hạn → từ chối", GREEN),
]
items_r = [
    ("TC-08", "Huỷ đơn → hoàn stock + voucher", GREEN),
    ("TC-09", "Hoàn trả COD → bắt buộc STK", GREEN),
    ("TC-10", "Admin REFUND → doanh thu giảm", GREEN),
    ("TC-11", "Notification real-time (badge)", GREEN),
    ("TC-12", "Chat AI gửi ảnh < 10s", GREEN),
    ("TC-13", "Login admin → AdminActivity", GREEN),
    ("TC-14", "Logout → xoá session", GREEN),
]

def add_tc_row(slide, code, desc, color, left, top, w, h):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Cm(2.0), h)
    pill.adjustments[0] = 0.4
    pill.fill.solid(); pill.fill.fore_color.rgb = color
    pill.line.fill.background()
    tf = pill.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = code
    r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Calibri"
    add_text(slide, desc, left + Cm(2.3), top, w - Cm(2.4), h,
             size=13, color=TEXT_DARK, anchor=MSO_ANCHOR.MIDDLE)

for i, (c, d, col) in enumerate(items_l):
    add_tc_row(s, c, d, col, Cm(1), Cm(3.0 + i * 1.4), Cm(14.5), Cm(1.1))
for i, (c, d, col) in enumerate(items_r):
    add_tc_row(s, c, d, col, Cm(16.5), Cm(3.0 + i * 1.4), Cm(14.5), Cm(1.1))

add_pill(s, "PASS 14/14", Cm(12), Cm(13.0), Cm(8), Cm(1.1), fill=GREEN, size=20)
add_footer(s)

# ---------- 23. PROS / CONS -------------------------------------------------
s = add_blank(prs); add_header(s, "6 • ĐÁNH GIÁ", "Ưu điểm & Hạn chế", 23, TOTAL)
add_card(s, "✓  Ưu điểm",
         ["Phủ trọn nghiệp vụ E-commerce thú cưng",
          "Real-time mạnh nhờ Firestore SnapshotListener",
          "Tích hợp 3 dịch vụ: Google • VNPay • OpenAI",
          "Kiến trúc MVVM rõ ràng, dễ mở rộng",
          "UI Material Design, Tiếng Việt đầy đủ",
          "Có cả vai trò Customer & Admin trong 1 app"],
         Cm(0.7), Cm(3.0), Cm(15), Cm(11),
         accent=GREEN, body_size=16, title_size=22)
add_card(s, "✗  Hạn chế",
         ["Chưa có CI/CD",
          "Chưa đủ unit test tự động",
          "Chưa dùng FCM (mới in-app)",
          "ShippingHelper hardcode, chưa gọi GHN/GHTK",
          "Refund VNPay vẫn thủ công (cần Cloud Function)",
          "Chưa có analytics chi tiết theo ngày"],
         Cm(16.5), Cm(3.0), Cm(15), Cm(11),
         accent=RED, body_size=16, title_size=22)
add_footer(s)

# ---------- 24. WORK ALLOCATION TABLE ---------------------------------------
s = add_blank(prs); add_header(s, "7 • PHÂN CÔNG", "Khối lượng công việc – chia đều 3 thành viên", 24, TOTAL)
members = [
    ("Nguyễn Văn Trường", "Trưởng nhóm – Customer flow & UI",
     ["Splash, Home, Detail, Cart, Checkout",
      "VNPay (URL builder + HMAC-SHA512)",
      "Order History/Detail",
      "Admin: Pet/Food/Category/Voucher/Promotion CRUD",
      "Báo cáo: Chương 1, 3, 5, 6 (Customer)"],
     "34 %", PRIMARY),

    ("Đào Trúc Mai", "Notification • Hoàn trả • Media",
     ["UI Notification, Promotion screen, Banner slider",
      "Module Hoàn trả (Customer + Admin Approve)",
      "Upload media: ảnh / video Pet & Food",
      "Hỗ trợ Admin Dashboard UI",
      "Báo cáo: Chương 2, 6 (Admin), 7"],
     "33 %", BLUE),

    ("Nguyễn Hữu Đức Thọ", "Auth • Chat AI • Profile",
     ["Login / Register / Google / OTP (JavaMail)",
      "Profile + Edit Profile + Manage Address",
      "Chat AI (OkHttp ↔ OpenAI) + Lịch sử phiên",
      "Logic dashboard thống kê + bug-fix role",
      "Báo cáo: Chương 4, 8 + Slide PowerPoint"],
     "33 %", GREEN),
]
W = Cm(10); H = Cm(10.5); GAP = Cm(0.4)
for i, (name, sub, tasks, pct, col) in enumerate(members):
    left = Cm(1) + (W + GAP) * i; top = Cm(3.0)
    card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, W, H)
    card.adjustments[0] = 0.05
    card.fill.solid(); card.fill.fore_color.rgb = BG_CARD
    card.line.color.rgb = col; card.line.width = Pt(1.5)
    # head
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, W, Cm(2))
    head.fill.solid(); head.fill.fore_color.rgb = col
    head.line.fill.background()
    add_text(s, name, left, top + Cm(0.15), W, Cm(0.9),
             size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, sub, left, top + Cm(1.05), W, Cm(0.8),
             size=12, color=WHITE, align=PP_ALIGN.CENTER)
    # tasks
    add_bullets(s, tasks, left + Cm(0.4), top + Cm(2.3),
                W - Cm(0.6), H - Cm(3.5), size=13)
    # pct
    pct_pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  left + W/2 - Cm(2), top + H - Cm(1.2),
                                  Cm(4), Cm(0.9))
    pct_pill.adjustments[0] = 0.5
    pct_pill.fill.solid(); pct_pill.fill.fore_color.rgb = col
    pct_pill.line.fill.background()
    tf = pct_pill.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = pct
    r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Calibri"

add_text(s, "Tổng: 100 %  •  Mức độ chia đều dựa trên khối lượng module thực tế",
         Cm(1), SLIDE_H - Cm(1.5), SLIDE_W - Cm(2), Cm(0.7),
         size=12, color=TEXT_GREY, align=PP_ALIGN.CENTER, bold=True)
add_footer(s)

# ---------- 25. ROADMAP -----------------------------------------------------
s = add_blank(prs); add_header(s, "8 • TƯƠNG LAI", "Hướng phát triển", 25, TOTAL)
roadmap = [
    ("Push Notification", "Firebase Cloud Messaging", PRIMARY),
    ("Cloud Functions",   "Refund VNPay tự động + Email auto", BLUE),
    ("Shipping API",      "Tích hợp GHN / GHTK / J&T", GREEN),
    ("Google Maps",       "Pick địa chỉ trên bản đồ", PURPLE),
    ("Review media",      "Đánh giá có ảnh/video", RED),
    ("Multi-platform",    "Bản iOS (Flutter / KMP)", PRIMARY_DARK),
    ("Analytics",         "Biểu đồ doanh thu chi tiết", BLUE),
    ("AI Voice Agent",    "Trợ lý mua hàng bằng giọng nói", GREEN),
]
W = Cm(7.4); H = Cm(4.6); GAP = Cm(0.4)
for i, (t, b, col) in enumerate(roadmap):
    col_idx = i % 4; row_idx = i // 4
    left = Cm(0.7) + (W + GAP) * col_idx
    top  = Cm(3.4) + (H + GAP) * row_idx
    add_card(s, t, b, left, top, W, H, accent=col, body_size=14, title_size=16)
add_footer(s)

# ---------- 26. CONCLUSION --------------------------------------------------
s = add_blank(prs); add_header(s, "8 • KẾT LUẬN", "Kết quả đạt được", 26, TOTAL)
add_card(s, "Hoàn thành",
         ["100 % chức năng bắt buộc",
          "80 % chức năng nâng cao",
          "Chạy ổn định Android 8.0+",
          "Test pass 14/14 ca tiêu biểu"],
         Cm(0.7), Cm(3.0), Cm(15), Cm(5.5),
         accent=GREEN, body_size=18, title_size=22)
add_card(s, "Học được",
         ["Áp dụng MVVM thực chiến",
          "Real-time Firestore SnapshotListener",
          "Bảo mật API key qua local.properties",
          "Tích hợp service bên thứ 3 (VNPay, OpenAI)"],
         Cm(16.5), Cm(3.0), Cm(15), Cm(5.5),
         accent=BLUE, body_size=18, title_size=22)
add_card(s, "Sản phẩm",
         ["1 ứng dụng Android hoàn chỉnh • 30+ Activity • 14 ViewModel • 13 Repository • 17 Entity • ~20.000 LOC"],
         Cm(0.7), Cm(8.8), Cm(30.8), Cm(5.0),
         accent=PRIMARY, body_size=18, title_size=22)
add_footer(s)

# ---------- 27. THANKS ------------------------------------------------------
s = add_blank(prs)
hero = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
hero.fill.solid(); hero.fill.fore_color.rgb = PRIMARY
hero.line.fill.background()
deco = s.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE,
                          0, SLIDE_H - Cm(8), Cm(10), Cm(8))
deco.fill.solid(); deco.fill.fore_color.rgb = PRIMARY_DARK
deco.line.fill.background()
add_text(s, "CẢM ƠN THẦY/CÔ ĐÃ LẮNG NGHE",
         0, Cm(5), SLIDE_W, Cm(2),
         size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "🐾  Q & A  🐾",
         0, Cm(8), SLIDE_W, Cm(1.5),
         size=28, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Nhóm PetShop  •  KunT  •  Đào Trúc Mai  •  Nguyễn Hữu Đức Thọ",
         0, Cm(11.5), SLIDE_W, Cm(1),
         size=16, color=WHITE, align=PP_ALIGN.CENTER)

# ---------- 28. APPENDIX ----------------------------------------------------
s = add_blank(prs); add_header(s, "PHỤ LỤC", "Hướng dẫn nhóm chèn ảnh thật", 27, TOTAL)
steps = [
    "1. Mở app trên emulator (API ≥ 30) hoặc thiết bị thật.",
    "2. Vào từng màn hình theo thứ tự gợi ý ở Slide 17 → 21.",
    "3. Chụp bằng phím Power+Volume Down (real device) hoặc nút Camera trong Android Studio.",
    "4. Lưu ảnh vào docs/screenshots/ và đặt tên đúng quy ước (vd: 06_login.png).",
    "5. Mở file BAO_CAO_SLIDES.pptx → click khung [Screenshot] → Insert → Picture → thay thế.",
    "6. Đối với báo cáo Word: chèn ảnh tại các vị trí [CHỤP ẢNH …] trong BAO_CAO.md.",
    "7. Render lại các sơ đồ Mermaid (.mmd) trên https://mermaid.live nếu muốn chỉnh sửa.",
]
add_bullets(s, steps, Cm(1.5), Cm(3.0), Cm(28), Cm(10), size=18, line_spacing=1.4)
add_footer(s)


# Save -----------------------------------------------------------------------
prs.save(OUT)
print(f"Saved {OUT}  – {len(prs.slides)} slides")
