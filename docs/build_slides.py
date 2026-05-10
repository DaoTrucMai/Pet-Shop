"""Generate BAO_CAO_SLIDES.pptx for PetShop project.

A polished 16:9 deck (~36 slides) with:
- Gradient backgrounds
- 18 Mermaid diagram images embedded
- Per-chapter slides matching the Word report structure
- 4-member work allocation slide

Run:
    pip install python-pptx Pillow
    python3 build_slides.py
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Cm, Inches, Pt
from lxml import etree

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "images"
OUT = ROOT / "BAO_CAO_SLIDES.pptx"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# ---- Brand palette (warm orange, modern) -----------------------------------
P1 = RGBColor(0xF5, 0xA6, 0x23)   # primary cam
P2 = RGBColor(0xE0, 0x90, 0x10)   # cam dam
P3 = RGBColor(0xFF, 0xD5, 0x80)   # cam nhat
BG = RGBColor(0xFF, 0xF8, 0xF2)   # nen kem
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
TEXT = RGBColor(0x33, 0x33, 0x33)
GREY = RGBColor(0x66, 0x66, 0x66)
LIGHT = RGBColor(0xEE, 0xEE, 0xEE)
GREEN = RGBColor(0x34, 0xC7, 0x59)
RED = RGBColor(0xFF, 0x3B, 0x30)
BLUE = RGBColor(0x00, 0x7A, 0xFF)
PURPLE = RGBColor(0x7B, 0x42, 0xF6)
TEAL = RGBColor(0x00, 0xB8, 0xA9)
PINK = RGBColor(0xFF, 0x6B, 0x9E)


# ===========================================================================
# Helpers
# ===========================================================================

def setup_prs() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    bg.line.fill.background()
    return s


def add_gradient_rect(slide, left, top, width, height, color1, color2,
                      angle=0):
    """Add a rectangle filled with a 2-stop gradient."""
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    s.line.fill.background()
    sp = s.fill._xPr
    # Replace solidFill with gradFill via XML
    # Build gradient fill XML
    fill = s.fill
    fill_xml = (
        f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        f'rotWithShape="1">'
        f'<a:gsLst>'
        f'<a:gs pos="0"><a:srgbClr val="{format(color1, "06X") if isinstance(color1, int) else "%02X%02X%02X" % (color1[0], color1[1], color1[2])}"/></a:gs>'
        f'<a:gs pos="100000"><a:srgbClr val="%02X%02X%02X"/></a:gs>'
        f'</a:gsLst>'
        f'<a:lin ang="{angle * 60000}" scaled="1"/>'
        f'</a:gradFill>'
    )
    # Easier: use solid color but pre-shaded gradient effect
    return s


def _color_hex(rgb: RGBColor) -> str:
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def gradient_rect(slide, left, top, width, height, c1, c2, angle=0):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    s.line.fill.background()
    spPr = s.fill._xPr  # spPr element
    # remove existing fill child
    for child in list(spPr):
        if child.tag.endswith('}solidFill') or child.tag.endswith('}noFill') \
                or child.tag.endswith('}gradFill') or child.tag.endswith('}pattFill') \
                or child.tag.endswith('}blipFill'):
            spPr.remove(child)

    nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    grad = etree.SubElement(spPr, '{%s}gradFill' % nsmap['a'],
                            attrib={'rotWithShape': '1'})
    gsLst = etree.SubElement(grad, '{%s}gsLst' % nsmap['a'])

    gs1 = etree.SubElement(gsLst, '{%s}gs' % nsmap['a'], attrib={'pos': '0'})
    etree.SubElement(gs1, '{%s}srgbClr' % nsmap['a'],
                     attrib={'val': _color_hex(c1)})

    gs2 = etree.SubElement(gsLst, '{%s}gs' % nsmap['a'], attrib={'pos': '100000'})
    etree.SubElement(gs2, '{%s}srgbClr' % nsmap['a'],
                     attrib={'val': _color_hex(c2)})

    etree.SubElement(grad, '{%s}lin' % nsmap['a'],
                     attrib={'ang': str(int(angle * 60000)), 'scaled': '1'})
    return s


def add_text(slide, text, left, top, width, height,
             size=18, bold=False, italic=False, color=DARK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Cm(0.1); tf.margin_right = Cm(0.1)
    tf.margin_top = Cm(0.05); tf.margin_bottom = Cm(0.05)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font
    return tb


def add_bullets(slide, items, left, top, width, height,
                size=16, color=DARK, line_spacing=1.2,
                bullet="•", font="Calibri"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(4)
        r = p.add_run(); r.text = f"{bullet}  {item}"
        r.font.size = Pt(size); r.font.color.rgb = color
        r.font.name = font
    return tb


def add_pill(slide, text, left, top, width, height, fill, fg=WHITE,
             size=14, bold=True):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                               left, top, width, height)
    s.adjustments[0] = 0.5
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.fill.background()
    tf = s.text_frame
    tf.margin_left = Cm(0.2); tf.margin_right = Cm(0.2)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = fg; r.font.name = "Calibri"
    return s


def add_card(slide, title, body, left, top, width, height,
             accent=P1, body_size=14, title_size=18, body_color=DARK):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  left, top, width, height)
    card.adjustments[0] = 0.04
    card.fill.solid(); card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = P3
    card.line.width = Pt(1)

    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 left, top, Cm(0.25), height)
    bar.adjustments[0] = 0.5
    bar.fill.solid(); bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    add_text(slide, title,
             left + Cm(0.55), top + Cm(0.2),
             width - Cm(0.75), Cm(0.95),
             size=title_size, bold=True, color=accent)
    add_bullets(slide, body if isinstance(body, list) else [body],
                left + Cm(0.55), top + Cm(1.0),
                width - Cm(0.75), height - Cm(1.1),
                size=body_size, color=body_color)


def add_header(slide, eyebrow, title, page_no=None, total=None,
               accent=P1):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Cm(0.4))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    add_text(slide, eyebrow, Cm(1), Cm(0.55), Cm(20), Cm(0.7),
             size=12, bold=True, color=P2, font="Calibri")
    add_text(slide, title, Cm(1), Cm(1.1), SLIDE_W - Cm(2), Cm(1.5),
             size=28, bold=True, color=DARK, font="Calibri")
    ul = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                Cm(1), Cm(2.45), Cm(2.5), Cm(0.12))
    ul.fill.solid(); ul.fill.fore_color.rgb = accent
    ul.line.fill.background()

    if page_no and total:
        add_text(slide, f"{page_no} / {total}",
                 SLIDE_W - Cm(3.5), Cm(0.55), Cm(2.5), Cm(0.7),
                 size=11, color=GREY, align=PP_ALIGN.RIGHT)


def add_footer(slide, text="PetShop  •  Đồ án Phát triển Ứng dụng Di động  •  Nhóm 4 thành viên"):
    add_text(slide, text, Cm(1), SLIDE_H - Cm(0.95),
             SLIDE_W - Cm(2), Cm(0.6),
             size=10, color=GREY, align=PP_ALIGN.LEFT)
    # decoration
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                 SLIDE_W - Cm(1.2), SLIDE_H - Cm(0.95),
                                 Cm(0.5), Cm(0.5))
    dot.fill.solid(); dot.fill.fore_color.rgb = P1
    dot.line.fill.background()


def add_image_fit(slide, path, left, top, max_w, max_h, center=True):
    p = IMG / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return None
    from PIL import Image as PILImage
    with PILImage.open(p) as im:
        iw, ih = im.size
    ratio = iw / ih
    box_ratio = max_w / max_h
    if ratio > box_ratio:
        w = max_w; h = int(max_w / ratio)
    else:
        h = max_h; w = int(max_h * ratio)
    cx = left + (max_w - w) // 2 if center else left
    cy = top + (max_h - h) // 2 if center else top
    return slide.shapes.add_picture(str(p), cx, cy, width=w, height=h)


# ===========================================================================
# Slides
# ===========================================================================
prs = setup_prs()
TOTAL = 36

# ----- Slide 1: COVER -------------------------------------------------------
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P1, P2, angle=135)
# decorative shapes
deco1 = s.shapes.add_shape(MSO_SHAPE.OVAL,
                           SLIDE_W - Cm(8), -Cm(4), Cm(14), Cm(14))
deco1.fill.solid(); deco1.fill.fore_color.rgb = P3
deco1.line.fill.background()
deco1.fill.transparency = 0.4

deco2 = s.shapes.add_shape(MSO_SHAPE.OVAL,
                           -Cm(4), SLIDE_H - Cm(6), Cm(10), Cm(10))
deco2.fill.solid(); deco2.fill.fore_color.rgb = P2
deco2.line.fill.background()

add_text(s, "ĐỒ ÁN PHÁT TRIỂN ỨNG DỤNG DI ĐỘNG",
         Cm(2), Cm(2.0), Cm(20), Cm(1),
         size=20, bold=True, color=WHITE)
add_text(s, "PETSHOP",
         Cm(2), Cm(3.0), Cm(20), Cm(3),
         size=80, bold=True, color=WHITE)
add_text(s, "Ứng dụng cửa hàng thú cưng & thức ăn cho thú cưng",
         Cm(2), Cm(7.0), Cm(28), Cm(1),
         size=22, color=WHITE)
add_text(s, "trên nền tảng Android",
         Cm(2), Cm(7.8), Cm(28), Cm(1),
         size=22, color=WHITE)

add_pill(s, "Java",     Cm(2.0),  Cm(9.5), Cm(2.6), Cm(1.0), fill=WHITE, fg=P2, size=14)
add_pill(s, "Firebase", Cm(4.8),  Cm(9.5), Cm(3.0), Cm(1.0), fill=WHITE, fg=P2, size=14)
add_pill(s, "VNPay",    Cm(8.0),  Cm(9.5), Cm(2.6), Cm(1.0), fill=WHITE, fg=P2, size=14)
add_pill(s, "OpenAI",   Cm(10.8), Cm(9.5), Cm(2.8), Cm(1.0), fill=WHITE, fg=P2, size=14)
add_pill(s, "MVVM",     Cm(13.8), Cm(9.5), Cm(2.6), Cm(1.0), fill=WHITE, fg=P2, size=14)

# Footer with team
add_text(s, "Nhóm thực hiện",
         Cm(2), Cm(13.0), Cm(20), Cm(0.7),
         size=14, bold=True, color=WHITE)
add_text(s, "Nguyễn Hữu Đức Thọ  •  Đào Trúc Mai  •  Nguyễn Văn Trường  •  …………………",
         Cm(2), Cm(13.7), Cm(28), Cm(0.7),
         size=14, color=WHITE)
add_text(s, "GVHD: …………………………………  •  Năm học 2025-2026",
         Cm(2), Cm(14.4), Cm(28), Cm(0.7),
         size=12, color=WHITE)

# ----- Slide 2: AGENDA ------------------------------------------------------
s = add_blank(prs); add_header(s, "MỞ ĐẦU", "Nội dung trình bày", 2, TOTAL)
agenda = [
    ("01", "Tổng quan đề tài & Công nghệ", P1),
    ("02", "Phân tích & Thiết kế hệ thống", BLUE),
    ("03", "Module Tài khoản (TV1)", PURPLE),
    ("04", "Module Trang chủ – Sản phẩm (TV2)", TEAL),
    ("05", "Module Giỏ hàng – Thanh toán (TV3)", GREEN),
    ("06", "Module Quản trị & Chatbot (TV4)", PINK),
    ("07", "Kiểm thử – Triển khai – Đánh giá", RED),
    ("08", "Kết luận & Hướng phát triển", P2),
]
for i, (num, name, col) in enumerate(agenda):
    col_idx = i % 2; row_idx = i // 2
    left = Cm(1.2) + Cm(15.5) * col_idx
    top = Cm(3.2) + Cm(2.6) * row_idx

    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                             left, top, Cm(15), Cm(2.2))
    box.adjustments[0] = 0.15
    box.fill.solid(); box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = col
    box.line.width = Pt(1.5)

    circle = s.shapes.add_shape(MSO_SHAPE.OVAL,
                                left + Cm(0.4), top + Cm(0.35),
                                Cm(1.5), Cm(1.5))
    circle.fill.solid(); circle.fill.fore_color.rgb = col
    circle.line.fill.background()
    tf = circle.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = num
    r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = WHITE

    add_text(s, name, left + Cm(2.3), top + Cm(0.4), Cm(12), Cm(1.4),
             size=18, bold=True, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
add_footer(s)

# ===========================================================================
# CHUONG 1
# ===========================================================================

# ----- Slide 3: CHƯƠNG 1 DIVIDER --------------------------------------------
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P3, P1, angle=135)
add_text(s, "CHƯƠNG 1", Cm(2), Cm(5), Cm(28), Cm(2),
         size=64, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Tổng quan đề tài & Công nghệ sử dụng",
         Cm(2), Cm(8.5), Cm(28), Cm(1.5),
         size=28, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "1.1 Khảo sát hiện trạng  •  1.2 Yêu cầu chức năng  •  1.3 Công nghệ  •  1.4 Công cụ phát triển",
         Cm(2), Cm(11.0), Cm(28), Cm(1),
         size=14, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# ----- Slide 4: WHY ---------------------------------------------------------
s = add_blank(prs); add_header(s, "1.1 KHẢO SÁT", "Vì sao chọn đề tài?", 4, TOTAL)
add_text(s, "“Thị trường thú cưng tăng trưởng nhanh – nhưng giao dịch còn rời rạc”",
         Cm(1.5), Cm(2.9), Cm(30), Cm(1.1),
         size=18, bold=True, italic=True, color=GREY)
stats = [
    ("40%",  "hộ gia đình thành thị nuôi thú cưng", P1),
    ("Top 5","thị trường thú cưng tăng nhanh ĐNÁ",  GREEN),
    ("80%",  "giao dịch trên MXH thiếu bảo đảm",   RED),
    ("0",    "app Việt chuyên Pet kèm AI tư vấn",   BLUE),
]
W = Cm(7.0); H = Cm(4.5); GAP = Cm(0.3)
for i, (big, small, col) in enumerate(stats):
    col_idx = i % 2; row_idx = i // 2
    left = Cm(1) + (W + GAP) * (i % 2)
    top  = Cm(4.2) + (H + GAP) * (i // 2)
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                             left, top, W, H)
    box.adjustments[0] = 0.05
    box.fill.solid(); box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = col; box.line.width = Pt(1.5)
    add_text(s, big, left, top + Cm(0.4), W, Cm(2.2),
             size=42, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, small, left + Cm(0.4), top + Cm(2.6), W - Cm(0.8), Cm(1.7),
             size=13, color=DARK, align=PP_ALIGN.CENTER)

add_card(s, "Cần một giải pháp chuyên biệt",
         ["Nền tảng tập trung cho lĩnh vực thú cưng",
          "Quản lý từng cá thể pet (AVAILABLE/RESERVED/SOLD)",
          "Tích hợp thanh toán điện tử & AI tư vấn",
          "Hỗ trợ cả Khách hàng và Quản trị viên trong 1 app"],
         Cm(16), Cm(4.2), Cm(15.5), Cm(9.5),
         accent=P1, body_size=15, title_size=22)
add_footer(s)

# ----- Slide 5: GOALS -------------------------------------------------------
s = add_blank(prs); add_header(s, "1.2 MỤC TIÊU", "Mục tiêu & phạm vi đề tài", 5, TOTAL)
goals = [
    ("Người dùng", "Khách hàng + Quản trị viên",                 P1),
    ("Sản phẩm",   "Pet (cá thể) + Food (tồn kho)",              BLUE),
    ("E-commerce", "Cart → Checkout → COD/VNPay → Giao → Hoàn", GREEN),
    ("Backend",    "Firebase Auth + Firestore + Storage",        PURPLE),
    ("AI",         "Chatbot OpenAI gpt-4o-mini RAG nhẹ",         RED),
    ("Kiến trúc",  "MVVM + Repository, ViewBinding, LiveData",   TEAL),
]
W = Cm(9.8); H = Cm(3.4); GAP = Cm(0.4)
for i, (t, b, col) in enumerate(goals):
    col_idx = i % 3; row_idx = i // 3
    left = Cm(1) + (W + GAP) * col_idx
    top  = Cm(3.2) + (H + GAP) * row_idx
    add_card(s, t, b, left, top, W, H,
             accent=col, body_size=14, title_size=18)
add_footer(s)

# ----- Slide 6: TECH STACK --------------------------------------------------
s = add_blank(prs); add_header(s, "1.3 CÔNG NGHỆ", "Stack đầy đủ", 6, TOTAL)
tech = [
    ("Java 11",        "Ngôn ngữ chính",        P1),
    ("Android SDK 36", "min API 24",            BLUE),
    ("Material 3",     "UI components",         GREEN),
    ("Firebase Auth",  "Email + Google",        PURPLE),
    ("Firestore",      "NoSQL real-time",       RED),
    ("Storage",        "Upload ảnh / video",    TEAL),
    ("VNPay Sandbox",  "HMAC-SHA512",           BLUE),
    ("OpenAI gpt-4o",  "Chatbot + Vision",      GREEN),
    ("OkHttp + Gson",  "HTTP & JSON",           PURPLE),
    ("Glide",          "Tải & cache ảnh",       P1),
    ("JavaMail",       "OTP qua Gmail SMTP",    RED),
    ("Gradle KTS",     "Version Catalog",       PINK),
]
W = Cm(7.4); H = Cm(2.6); GAP_X = Cm(0.4); GAP_Y = Cm(0.35)
for i, (t, b, col) in enumerate(tech):
    col_idx = i % 4; row_idx = i // 4
    left = Cm(1) + (W + GAP_X) * col_idx
    top  = Cm(3.3) + (H + GAP_Y) * row_idx
    add_card(s, t, b, left, top, W, H,
             accent=col, body_size=12, title_size=15)
add_footer(s)

# ----- Slide 7: PROJECT TOOLS -----------------------------------------------
s = add_blank(prs); add_header(s, "1.4 CÔNG CỤ", "Công cụ phát triển & Quản lý dự án", 7, TOTAL)
tools = [
    ("Android Studio Hedgehog 2024",
     ["IDE chính, debug, profiling",
      "Layout Editor, Logcat, Emulator API 30/33/34"]),
    ("Gradle 8 (Kotlin DSL)",
     ["build.gradle.kts với version catalog libs.versions.toml",
      "Inject biến từ local.properties qua BuildConfig"]),
    ("Git + GitHub",
     ["Mỗi feature 1 nhánh; Pull Request review",
      "Commit theo prefix: feat: / fix: / docs:"]),
    ("Figma",
     ["Wireframe & mockup các màn hình chính",
      "Design system (màu, font, icon) thống nhất"]),
]
W = Cm(15); H = Cm(5); GAP = Cm(0.5)
for i, (t, items) in enumerate(tools):
    col = [P1, BLUE, GREEN, PURPLE][i]
    col_idx = i % 2; row_idx = i // 2
    left = Cm(1) + (W + GAP) * col_idx
    top  = Cm(3.2) + (H + GAP) * row_idx
    add_card(s, t, items, left, top, W, H,
             accent=col, body_size=14, title_size=18)
add_footer(s)

# ===========================================================================
# CHUONG 2
# ===========================================================================
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P3, BLUE, angle=135)
add_text(s, "CHƯƠNG 2", Cm(2), Cm(5), Cm(28), Cm(2),
         size=64, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Phân tích & Thiết kế hệ thống",
         Cm(2), Cm(8.5), Cm(28), Cm(1.5),
         size=28, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Use Case  •  Activity Diagram  •  Firestore  •  Kiến trúc  •  UI/UX",
         Cm(2), Cm(11.0), Cm(28), Cm(1),
         size=14, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# ----- Slide 9: USE CASE ----------------------------------------------------
s = add_blank(prs); add_header(s, "2.1 USE CASE", "Sơ đồ Use Case tổng quát", 9, TOTAL)
add_image_fit(s, "diagram_usecase.png",
              Cm(0.7), Cm(2.7), Cm(31.5), Cm(8.5))
add_card(s, "Tác nhân Khách hàng",
         ["12 use case", "Đặt hàng + Thanh toán + Hoàn trả",
          "Chat AI 24/7"],
         Cm(0.7), Cm(11.5), Cm(15), Cm(2.6),
         accent=P1, body_size=14, title_size=16)
add_card(s, "Tác nhân Quản trị viên",
         ["9 use case", "CRUD Pet/Food/Voucher",
          "Dashboard real-time + Duyệt return"],
         Cm(16.5), Cm(11.5), Cm(15), Cm(2.6),
         accent=BLUE, body_size=14, title_size=16)
add_footer(s)

# ----- Slide 10: ARCHITECTURE -----------------------------------------------
s = add_blank(prs); add_header(s, "2.5 KIẾN TRÚC",
                               "Kiến trúc tổng thể MVVM + Repository + Firebase",
                               10, TOTAL)
add_image_fit(s, "diagram_architecture.png",
              Cm(0.7), Cm(2.8), Cm(31.5), Cm(7.5))
items = [
    ("View",       "Activity / Fragment / Adapter",    P1),
    ("ViewModel",  "LiveData – tách logic UI",         BLUE),
    ("Repository", "I/O Firestore + REST",             GREEN),
    ("Backend",    "Firebase + VNPay + OpenAI + SMTP", PURPLE),
]
W = Cm(7.5); GAP = Cm(0.4)
for i, (t, b, c) in enumerate(items):
    add_card(s, t, b, Cm(0.7) + (W + GAP) * i, Cm(11.0), W, Cm(3.0),
             accent=c, body_size=14, title_size=16)
add_footer(s)

# ----- Slide 11: PACKAGE LAYOUT ---------------------------------------------
s = add_blank(prs); add_header(s, "2.5.3 ĐÓNG GÓI",
                               "Tổ chức package mã nguồn", 11, TOTAL)
add_image_fit(s, "diagram_package-layout.png",
              Cm(0.7), Cm(2.8), Cm(20), Cm(11.5))
add_card(s, "Quy ước đặt tên",
         ["Activity / Fragment / Adapter / ViewModel / Repository",
          "Layout: activity_/fragment_/item_/dialog_*.xml",
          "Resource id: tvName, etEmail, btnLogin,…",
          "Hằng số: HOA_GẠCH_DƯỚI"],
         Cm(21), Cm(3.0), Cm(10.5), Cm(5.5),
         accent=P1, body_size=14, title_size=16)
add_card(s, "Số liệu mã nguồn",
         ["30+ Activity  •  6 Fragment  •  19 Adapter",
          "14 ViewModel  •  13 Repository  •  17 Entity",
          "62 layout XML  •  ~20 000 LOC"],
         Cm(21), Cm(8.7), Cm(10.5), Cm(5.0),
         accent=GREEN, body_size=14, title_size=16)
add_footer(s)

# ----- Slide 12: ERD --------------------------------------------------------
s = add_blank(prs); add_header(s, "2.4 CSDL",
                               "Mô hình dữ liệu Firestore (ERD logic)", 12, TOTAL)
add_image_fit(s, "diagram_erd.png",
              Cm(0.7), Cm(2.8), Cm(31.5), Cm(7.5))
add_card(s, "15 collection chính",
         ["users, addresses, notifications",
          "pets, foods, categories",
          "orders, return_requests, vouchers, promotions",
          "chat_sessions, chat_messages, banners"],
         Cm(0.7), Cm(11.0), Cm(15.5), Cm(3.0),
         accent=PURPLE, body_size=14, title_size=18)
add_card(s, "Điểm thiết kế nổi bật",
         ["Real-time SnapshotListener",
          "Atomic Firestore Transaction (đặt hàng, refund)",
          "Sub-collection (voucher_usage, chat_messages)"],
         Cm(16.7), Cm(11.0), Cm(15.5), Cm(3.0),
         accent=GREEN, body_size=14, title_size=18)
add_footer(s)

# ----- Slide 13: FIRESTORE COLLECTIONS --------------------------------------
s = add_blank(prs); add_header(s, "2.4.2 COLLECTION",
                               "Sơ đồ collection trên Cloud Firestore", 13, TOTAL)
add_image_fit(s, "diagram_firestore-collections.png",
              Cm(0.7), Cm(2.8), Cm(20), Cm(11.5))
add_card(s, "Cấu trúc",
         ["Top-level: 13 collection",
          "Sub-collection: 3 (sessions, messages, voucher_usage)",
          "Mọi document đều có createdAt/updatedAt"],
         Cm(21), Cm(3.0), Cm(10.5), Cm(5.0),
         accent=P1, body_size=14, title_size=16)
add_card(s, "Ưu điểm Firestore",
         ["Real-time mặc định (SnapshotListener)",
          "Offline cache",
          "Scale tốt, không cần dựng server"],
         Cm(21), Cm(8.2), Cm(10.5), Cm(5.5),
         accent=BLUE, body_size=14, title_size=16)
add_footer(s)

# ----- Slide 14: SECURITY RULES ---------------------------------------------
s = add_blank(prs); add_header(s, "2.4.3 BẢO MẬT",
                               "Logic Firestore Security Rules", 14, TOTAL)
add_image_fit(s, "diagram_security-rules.png",
              Cm(0.7), Cm(2.8), Cm(20), Cm(11.5))
add_card(s, "Nguyên tắc",
         ["Mặc định DENY",
          "isOwner(uid) hoặc isAdmin()",
          "Customer chỉ READ catalog, WRITE cua minh",
          "Admin toàn quyền (sau khi xác thực role)"],
         Cm(21), Cm(3.0), Cm(10.5), Cm(5.5),
         accent=RED, body_size=14, title_size=16)
add_card(s, "Lợi ích",
         ["Bảo vệ dữ liệu khi client truy cập trực tiếp",
          "Không cần backend trung gian",
          "Dễ test bằng Firebase Emulator"],
         Cm(21), Cm(8.7), Cm(10.5), Cm(5.0),
         accent=GREEN, body_size=14, title_size=16)
add_footer(s)

# ----- Slide 15: MVVM Data flow ---------------------------------------------
s = add_blank(prs); add_header(s, "2.5.2 LUỒNG DỮ LIỆU",
                               "Sequence dữ liệu giữa các tầng MVVM", 15, TOTAL)
add_image_fit(s, "diagram_mvvm-dataflow.png",
              Cm(0.7), Cm(2.8), Cm(31.5), Cm(7.5))
add_card(s, "View",
         ["Observe LiveData → cập nhật UI tự động",
          "Không chứa business logic"],
         Cm(0.7), Cm(11.0), Cm(10.0), Cm(3.0),
         accent=P1, body_size=14, title_size=16)
add_card(s, "ViewModel",
         ["Giữ trạng thái màn hình",
          "Sống theo lifecycle Activity/Fragment"],
         Cm(11.2), Cm(11.0), Cm(10.0), Cm(3.0),
         accent=BLUE, body_size=14, title_size=16)
add_card(s, "Repository",
         ["I/O với Firestore + REST",
          "Trả callback (data hoặc error)"],
         Cm(21.7), Cm(11.0), Cm(10.0), Cm(3.0),
         accent=GREEN, body_size=14, title_size=16)
add_footer(s)

# ----- Slide 16: ORDER STATE ------------------------------------------------
s = add_blank(prs); add_header(s, "2.3.2 TRẠNG THÁI",
                               "State Diagram – Đơn hàng (11 trạng thái)", 16, TOTAL)
add_image_fit(s, "diagram_order-state.png",
              Cm(0.7), Cm(2.7), Cm(14), Cm(11.5))
add_card(s, "11 trạng thái",
         ["WAITING_PAYMENT  •  PENDING",
          "CONFIRMED  •  PREPARING  •  SHIPPING",
          "DELIVERED  •  COMPLETED",
          "CANCELLED",
          "RETURN_REQUESTED  •  RETURN_APPROVED  •  REFUNDED"],
         Cm(15.5), Cm(3.0), Cm(16), Cm(6.0),
         accent=PURPLE, body_size=15, title_size=18)
add_card(s, "Bảo toàn dữ liệu",
         ["Mọi chuyển trạng thái đều dùng Firestore Transaction",
          "Tự hoàn stock & lượt voucher khi CANCELLED",
          "Cập nhật totalOrders/totalSpent best-effort"],
         Cm(15.5), Cm(9.2), Cm(16), Cm(4.8),
         accent=GREEN, body_size=15, title_size=18)
add_footer(s)

# ===========================================================================
# CHUONG 3 - TV1
# ===========================================================================
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P3, PURPLE, angle=135)
add_text(s, "CHƯƠNG 3", Cm(2), Cm(4), Cm(28), Cm(2),
         size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Module Tài khoản & Hồ sơ người dùng",
         Cm(2), Cm(7.0), Cm(28), Cm(1.5),
         size=26, color=WHITE, align=PP_ALIGN.CENTER)
add_pill(s, "TV1 – Nguyễn Hữu Đức Thọ (Trưởng nhóm)",
         Cm(7), Cm(9.5), Cm(20), Cm(1.4),
         fill=WHITE, fg=PURPLE, size=18)
add_text(s, "3.1 Phân tích  •  3.2-3.3 Model & Auth  •  3.5-3.7 Login (Email/Google/Facebook)  •  3.8-3.10 Profile, Address, Notification, Session",
         Cm(2), Cm(11.5), Cm(28), Cm(1.5),
         size=13, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# ----- Slide 18: AUTH FLOW --------------------------------------------------
s = add_blank(prs); add_header(s, "3.5-3.7 ĐĂNG NHẬP",
                               "Luồng Đăng ký – Đăng nhập",
                               18, TOTAL, accent=PURPLE)
add_image_fit(s, "diagram_auth-flow.png",
              Cm(0.5), Cm(2.7), Cm(20), Cm(11.5))
add_pill(s, "Email + Password",   Cm(21.5), Cm(3.0), Cm(10), Cm(1.0), fill=P1)
add_pill(s, "Google Sign-In",     Cm(21.5), Cm(4.3), Cm(10), Cm(1.0), fill=BLUE)
add_pill(s, "OTP qua Gmail SMTP", Cm(21.5), Cm(5.6), Cm(10), Cm(1.0), fill=GREEN)
add_pill(s, "Facebook Login (mở rộng)", Cm(21.5), Cm(6.9), Cm(10), Cm(1.0), fill=PURPLE)
add_pill(s, "Quên mật khẩu",      Cm(21.5), Cm(8.2), Cm(10), Cm(1.0), fill=RED)
add_card(s, "Bảo mật",
         ["Firebase Auth quản lý phiên",
          "OTP 6 số ngẫu nhiên",
          "parseAuthError → tiếng Việt",
          "Không lưu mật khẩu local"],
         Cm(21.5), Cm(9.5), Cm(10), Cm(4.5),
         accent=PURPLE, body_size=13, title_size=16)
add_footer(s)

# ----- Slide 19: CUSTOMER JOURNEY -------------------------------------------
s = add_blank(prs); add_header(s, "3.4 ĐIỀU HƯỚNG",
                               "Hành trình người dùng (Customer Journey)",
                               19, TOTAL, accent=PURPLE)
add_image_fit(s, "diagram_customer-journey.png",
              Cm(0.5), Cm(2.8), Cm(31.5), Cm(8.5))
add_card(s, "5 đường vào ứng dụng",
         ["Splash → Home Guest / Home Customer",
          "Login Email / Login Google / Register OTP",
          "Sau login: Home → Cart → Checkout → Order"],
         Cm(0.7), Cm(11.5), Cm(15), Cm(2.6),
         accent=P1, body_size=14, title_size=16)
add_card(s, "Chức năng phụ",
         ["Notification real-time",
          "Chat AI 24/7",
          "Profile + Address"],
         Cm(16.5), Cm(11.5), Cm(15), Cm(2.6),
         accent=GREEN, body_size=14, title_size=16)
add_footer(s)

# ===========================================================================
# CHUONG 4 - TV2
# ===========================================================================
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P3, TEAL, angle=135)
add_text(s, "CHƯƠNG 4", Cm(2), Cm(4), Cm(28), Cm(2),
         size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Module Danh mục sản phẩm & Trang chủ",
         Cm(2), Cm(7.0), Cm(28), Cm(1.5),
         size=26, color=WHITE, align=PP_ALIGN.CENTER)
add_pill(s, "TV2 – Đào Trúc Mai",
         Cm(7), Cm(9.5), Cm(20), Cm(1.4),
         fill=WHITE, fg=TEAL, size=18)
add_text(s, "4.1 Phân tích KH  •  4.2 Model Pet/Food  •  4.4 HomeFragment  •  4.6-4.7 Pet/Food Detail  •  4.8 Glide  •  4.9 Search/Filter",
         Cm(2), Cm(11.5), Cm(28), Cm(1.5),
         size=13, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# ----- Slide 21: TV2 Modules ------------------------------------------------
s = add_blank(prs); add_header(s, "4.4 - 4.7 GIAO DIỆN KHÁCH HÀNG",
                               "Các màn hình Module Danh mục & Trang chủ",
                               21, TOTAL, accent=TEAL)
modules = [
    ("HomeFragment",   "Banner • Lời chào theo giờ • Search • Danh mục • Sản phẩm nổi bật • Badge Cart/Notif", P1),
    ("CategoryFragment\n+ ProductListActivity", "Lưới 2 cột • Sort/Filter (giá, loài, KM) • Cuộn vô hạn", BLUE),
    ("PetDetailActivity", "Slider ảnh + video • Giống/Tuổi/Cân nặng • Tiêm phòng • Status RESERVED", PURPLE),
    ("FoodDetailActivity","Brand • Loại • Trọng lượng • Số lượng theo stock • Tab mô tả/đánh giá", GREEN),
    ("PromotionActivity",  "Voucher hệ thống • Apply 1 chạm", RED),
    ("Glide + Storage",  "Cache đĩa • Placeholder • Transformations", TEAL),
]
W = Cm(9.8); H = Cm(3.4); GAP = Cm(0.4)
for i, (t, b, col) in enumerate(modules):
    col_idx = i % 3; row_idx = i // 3
    left = Cm(1) + (W + GAP) * col_idx
    top  = Cm(3.2) + (H + GAP) * row_idx
    add_card(s, t, b, left, top, W, H,
             accent=col, body_size=13, title_size=16)
add_footer(s)

# ----- Slide 22: HomeFragment Layout (visual mockup) ------------------------
s = add_blank(prs); add_header(s, "4.4 HOMEFRAGMENT",
                               "Bố cục màn hình Trang chủ",
                               22, TOTAL, accent=TEAL)
# Phone mockup
phone = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                           Cm(11), Cm(2.8), Cm(10), Cm(11.4))
phone.adjustments[0] = 0.06
phone.fill.solid(); phone.fill.fore_color.rgb = WHITE
phone.line.color.rgb = DARK; phone.line.width = Pt(1.5)
# top bar
tb = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(11.3), Cm(3.2), Cm(9.4), Cm(1.0))
tb.fill.solid(); tb.fill.fore_color.rgb = P1; tb.line.fill.background()
add_text(s, "Hi, Mai 🐾", Cm(11.5), Cm(3.3), Cm(5), Cm(0.8),
         size=12, bold=True, color=WHITE)
add_text(s, "🛒  🔔", Cm(17), Cm(3.3), Cm(3.5), Cm(0.8),
         size=12, color=WHITE, align=PP_ALIGN.RIGHT)
# search
sb = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                        Cm(11.4), Cm(4.4), Cm(9.2), Cm(0.9))
sb.adjustments[0] = 0.4
sb.fill.solid(); sb.fill.fore_color.rgb = LIGHT; sb.line.fill.background()
add_text(s, "🔍  Tìm theo giống, kích thước, tên...", Cm(11.6), Cm(4.5), Cm(9), Cm(0.8),
         size=10, color=GREY)
# banner
bn = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                        Cm(11.4), Cm(5.5), Cm(9.2), Cm(2.0))
bn.adjustments[0] = 0.05
bn.fill.solid(); bn.fill.fore_color.rgb = P3; bn.line.fill.background()
add_text(s, "Banner ViewPager2", Cm(11.4), Cm(6.0), Cm(9.2), Cm(1),
         size=12, bold=True, color=P2, align=PP_ALIGN.CENTER)
# categories
add_text(s, "Danh mục", Cm(11.5), Cm(7.7), Cm(9), Cm(0.5),
         size=11, bold=True, color=DARK)
for i in range(4):
    c = s.shapes.add_shape(MSO_SHAPE.OVAL,
                           Cm(11.5 + i * 2.2), Cm(8.3),
                           Cm(1.7), Cm(1.7))
    c.fill.solid(); c.fill.fore_color.rgb = [P3, BLUE, GREEN, PURPLE][i]
    c.line.fill.background()
# product
add_text(s, "Thú cưng nổi bật", Cm(11.5), Cm(10.4), Cm(9), Cm(0.5),
         size=11, bold=True, color=DARK)
for i in range(2):
    pr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                            Cm(11.5 + i * 4.5), Cm(11.0),
                            Cm(4.0), Cm(2.0))
    pr.adjustments[0] = 0.06
    pr.fill.solid(); pr.fill.fore_color.rgb = LIGHT
    pr.line.fill.background()

# Side notes
add_card(s, "Top Bar",
         ["Lời chào theo giờ (sáng/chiều/tối)",
          "Badge số trên giỏ + thông báo"],
         Cm(0.7), Cm(3.0), Cm(10), Cm(2.5),
         accent=P1, body_size=12, title_size=15)
add_card(s, "Search realtime",
         ["TextWatcher → vm.search()",
          "Filter tức thì, không call Firestore"],
         Cm(0.7), Cm(5.7), Cm(10), Cm(2.5),
         accent=BLUE, body_size=12, title_size=15)
add_card(s, "Banner ViewPager2",
         ["Auto-scroll 4s/lần",
          "Click → mở Promotion"],
         Cm(0.7), Cm(8.4), Cm(10), Cm(2.5),
         accent=GREEN, body_size=12, title_size=15)
add_card(s, "Sản phẩm nổi bật",
         ["Pet (cá thể) + Food (tồn kho)",
          "Hiển thị giá KM nếu có"],
         Cm(0.7), Cm(11.1), Cm(10), Cm(2.6),
         accent=PURPLE, body_size=12, title_size=15)

add_card(s, "Repository",
         ["FoodRepository / PetRepository / CategoryRepository",
          "Pattern Callback chuẩn cho mọi ViewModel"],
         Cm(22), Cm(3.0), Cm(9.5), Cm(5),
         accent=TEAL, body_size=13, title_size=16)
add_card(s, "Hiển thị ảnh",
         ["Glide + Firebase Storage",
          "Placeholder + Error",
          "Cache đĩa cho danh sách dài"],
         Cm(22), Cm(8.3), Cm(9.5), Cm(5.5),
         accent=PINK, body_size=13, title_size=16)
add_footer(s)

# ===========================================================================
# CHUONG 5 - TV3
# ===========================================================================
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P3, GREEN, angle=135)
add_text(s, "CHƯƠNG 5", Cm(2), Cm(4), Cm(28), Cm(2),
         size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Module Giỏ hàng – Thanh toán – Đơn hàng",
         Cm(2), Cm(7.0), Cm(28), Cm(1.5),
         size=26, color=WHITE, align=PP_ALIGN.CENTER)
add_pill(s, "TV3 – Nguyễn Văn Trường",
         Cm(7), Cm(9.5), Cm(20), Cm(1.4),
         fill=WHITE, fg=GREEN, size=18)
add_text(s, "5.3 Cart  •  5.4 Checkout  •  5.5 VNPay  •  5.6 OrderHistory  •  5.7 ReturnRequest",
         Cm(2), Cm(11.5), Cm(28), Cm(1.5),
         size=13, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# ----- Slide 24: CHECKOUT FLOW ----------------------------------------------
s = add_blank(prs); add_header(s, "5.4 CHECKOUT",
                               "Activity Diagram – Đặt hàng & Thanh toán",
                               24, TOTAL, accent=GREEN)
add_image_fit(s, "diagram_checkout-flow.png",
              Cm(0.5), Cm(2.7), Cm(15), Cm(11.5))
add_card(s, "2 phương thức",
         ["COD – Pending ngay", "VNPay – chờ thanh toán"],
         Cm(16), Cm(3.0), Cm(15.5), Cm(3.2),
         accent=P1, body_size=15, title_size=18)
add_card(s, "Phí ship theo vùng",
         ["TP. HCM: 30 000đ",
          "Miền Nam: 45 000đ",
          "Miền Trung: 60 000đ",
          "Miền Bắc: 75 000đ",
          "Free ship ≥ 500 000đ"],
         Cm(16), Cm(6.4), Cm(15.5), Cm(5.0),
         accent=GREEN, body_size=15, title_size=18)
add_card(s, "Voucher",
         ["PERCENT • FIXED • FREESHIP",
          "Validate: hạn / lượt / minOrder"],
         Cm(16), Cm(11.6), Cm(15.5), Cm(2.4),
         accent=BLUE, body_size=13, title_size=18)
add_footer(s)

# ----- Slide 25: VNPay Sequence ---------------------------------------------
s = add_blank(prs); add_header(s, "5.5 VNPAY",
                               "Sequence Diagram – Thanh toán VNPay",
                               25, TOTAL, accent=GREEN)
add_image_fit(s, "diagram_sequence-vnpay.png",
              Cm(0.5), Cm(2.7), Cm(31.5), Cm(7.5))
add_card(s, "VNPayHelper.buildPaymentUrl",
         ["URL-encode UTF-8",
          "Sort tham số TreeMap",
          "Chữ ký HMAC-SHA512",
          "vnp_ExpireDate = 15 phút"],
         Cm(0.7), Cm(11.0), Cm(15.5), Cm(3.2),
         accent=RED, body_size=14, title_size=18)
add_card(s, "completeVNPayOrder",
         ["Atomic Firestore Transaction:",
          "→ status = PENDING; paymentStatus = PAID",
          "→ Trừ stock + Pet RESERVED + Notification"],
         Cm(16.7), Cm(11.0), Cm(15.5), Cm(3.2),
         accent=GREEN, body_size=14, title_size=18)
add_footer(s)

# ----- Slide 26: VNPay Data flow + Order status -----------------------------
s = add_blank(prs); add_header(s, "5.5 - 5.6 LUỒNG TIỀN & TRẠNG THÁI",
                               "Tóm tắt thanh toán & vòng đời đơn",
                               26, TOTAL, accent=GREEN)
add_image_fit(s, "diagram_payment-data-flow.png",
              Cm(0.7), Cm(2.7), Cm(31.5), Cm(4.5))
add_image_fit(s, "diagram_order-status-bar.png",
              Cm(0.7), Cm(8.0), Cm(31.5), Cm(3.5))
add_card(s, "Bảo toàn dữ liệu",
         ["Mọi cập nhật trạng thái dùng Firestore Transaction",
          "Hoàn stock + Voucher khi CANCELLED",
          "Refund REFUNDED → trừ doanh thu Dashboard"],
         Cm(0.7), Cm(11.8), Cm(31.5), Cm(2.0),
         accent=PURPLE, body_size=14, title_size=18)
add_footer(s)

# ----- Slide 27: Return Flow ------------------------------------------------
s = add_blank(prs); add_header(s, "5.7 HOÀN TRẢ",
                               "Activity Diagram – Yêu cầu hoàn trả & hoàn tiền",
                               27, TOTAL, accent=GREEN)
add_image_fit(s, "diagram_return-flow.png",
              Cm(0.5), Cm(2.7), Cm(13), Cm(11.5))
add_card(s, "COD",
         ["Khách nhập số tài khoản + tên ngân hàng",
          "Admin chuyển khoản thủ công"],
         Cm(14), Cm(3.0), Cm(17.5), Cm(3.5),
         accent=P1, body_size=15, title_size=18)
add_card(s, "VNPay",
         ["Hoàn về thẻ thanh toán gốc",
          "Cần Cloud Function (TODO)"],
         Cm(14), Cm(6.7), Cm(17.5), Cm(3.5),
         accent=BLUE, body_size=15, title_size=18)
add_card(s, "Tác động Dashboard",
         ["Tự động trừ doanh thu (refundedMoney)",
          "Cập nhật tile Tiền hoàn"],
         Cm(14), Cm(10.4), Cm(17.5), Cm(3.5),
         accent=RED, body_size=15, title_size=18)
add_footer(s)

# ===========================================================================
# CHUONG 6 - TV4
# ===========================================================================
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P3, PINK, angle=135)
add_text(s, "CHƯƠNG 6", Cm(2), Cm(4), Cm(28), Cm(2),
         size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Module Quản trị & Chatbot tư vấn",
         Cm(2), Cm(7.0), Cm(28), Cm(1.5),
         size=26, color=WHITE, align=PP_ALIGN.CENTER)
add_pill(s, "TV4 – ……………………………………",
         Cm(7), Cm(9.5), Cm(20), Cm(1.4),
         fill=WHITE, fg=PINK, size=18)
add_text(s, "6.3 AdminActivity  •  6.4-6.10 9 màn hình quản lý  •  6.11 Storage  •  6.12 Chatbot OpenAI",
         Cm(2), Cm(11.5), Cm(28), Cm(1.5),
         size=13, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# ----- Slide 29: Admin Journey ----------------------------------------------
s = add_blank(prs); add_header(s, "6.3 ADMIN JOURNEY",
                               "Hành trình quản trị viên",
                               29, TOTAL, accent=PINK)
add_image_fit(s, "diagram_admin-journey.png",
              Cm(0.7), Cm(2.7), Cm(31.5), Cm(8.5))
add_card(s, "9 màn hình quản trị",
         ["Dashboard • Users • Categories",
          "Pets • Foods • Promotions • Vouchers",
          "Orders • Returns"],
         Cm(0.7), Cm(11.5), Cm(15), Cm(2.6),
         accent=PINK, body_size=14, title_size=16)
add_card(s, "Real-time",
         ["SnapshotListener cho mọi tile",
          "Auto-update khi khách đặt đơn / refund"],
         Cm(16.5), Cm(11.5), Cm(15), Cm(2.6),
         accent=GREEN, body_size=14, title_size=16)
add_footer(s)

# ----- Slide 30: Admin Dashboard real-time ----------------------------------
s = add_blank(prs); add_header(s, "6.3 DASHBOARD",
                               "Sequence Diagram – Admin Dashboard real-time",
                               30, TOTAL, accent=PINK)
add_image_fit(s, "diagram_admin-dashboard.png",
              Cm(0.5), Cm(2.7), Cm(17), Cm(11.5))
add_card(s, "9 chỉ số real-time",
         ["Tổng doanh thu • Tổng đơn",
          "Người dùng • Đơn pending",
          "Preparing • Shipping • Delivered",
          "Đơn huỷ • Tiền hoàn"],
         Cm(18), Cm(3.0), Cm(13.5), Cm(6.0),
         accent=P1, body_size=14, title_size=18)
add_card(s, "Quy tắc tính",
         ["Chỉ tính khách hàng ACTIVE",
          "COD → đếm khi DELIVERED/COMPLETED",
          "VNPAY → đếm khi PAID",
          "Doanh thu thực = revenue – refund"],
         Cm(18), Cm(9.2), Cm(13.5), Cm(4.8),
         accent=GREEN, body_size=14, title_size=18)
add_footer(s)

# ----- Slide 31: Chat RAG ---------------------------------------------------
s = add_blank(prs); add_header(s, "6.12 CHATBOT",
                               "Kiến trúc Chatbot RAG nhẹ với OpenAI",
                               31, TOTAL, accent=PINK)
add_image_fit(s, "diagram_chat-rag.png",
              Cm(0.5), Cm(2.7), Cm(31.5), Cm(7.5))
add_card(s, "Khách chưa login",
         ["Lưu local SharedPreferences",
          "Giới hạn 50 tin"],
         Cm(0.7), Cm(11.0), Cm(10), Cm(3.0),
         accent=P1, body_size=14, title_size=16)
add_card(s, "Khách đã login",
         ["Sync lên Firestore",
          "users/{uid}/sessions/{id}/messages"],
         Cm(11.0), Cm(11.0), Cm(10), Cm(3.0),
         accent=GREEN, body_size=14, title_size=16)
add_card(s, "Tính năng nâng cao",
         ["Voice → Text",
          "Gửi ảnh (Vision)",
          "Markdown render"],
         Cm(21.3), Cm(11.0), Cm(10.5), Cm(3.0),
         accent=PURPLE, body_size=14, title_size=16)
add_footer(s)

# ===========================================================================
# CHUONG 7 - TEST
# ===========================================================================
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P3, RED, angle=135)
add_text(s, "CHƯƠNG 7", Cm(2), Cm(4), Cm(28), Cm(2),
         size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Kiểm thử – Triển khai – Đánh giá",
         Cm(2), Cm(7.0), Cm(28), Cm(1.5),
         size=26, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "7.1 Kế hoạch  •  7.2 Test case 5 module  •  7.4 Hiệu năng  •  7.5 Hướng dẫn build",
         Cm(2), Cm(10.5), Cm(28), Cm(1.5),
         size=14, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

# ----- Slide 33: Test Result Summary ----------------------------------------
s = add_blank(prs); add_header(s, "7.2 KIỂM THỬ",
                               "Tổng kết 49 test case (5 module) – PASS 100%",
                               33, TOTAL, accent=RED)
modules = [
    ("Auth (TV1)",    "10 / 10 PASS", PURPLE),
    ("Catalog (TV2)", "10 / 10 PASS", TEAL),
    ("Order (TV3)",   "12 / 12 PASS", GREEN),
    ("Admin (TV4)",   "9 / 9 PASS",  PINK),
    ("Chat (TV4)",    "8 / 8 PASS",  P1),
]
W = Cm(6.0); H = Cm(5.0); GAP = Cm(0.4)
total_w = (W + GAP) * len(modules) - GAP
left_start = (Cm(33.0) - total_w) // 2 if Cm(33.0) >= total_w else Cm(0.5)
for i, (m, r, col) in enumerate(modules):
    left = left_start + (W + GAP) * i
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                             left, Cm(3.5), W, H)
    box.adjustments[0] = 0.05
    box.fill.solid(); box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = col; box.line.width = Pt(1.5)
    add_text(s, m, left, Cm(3.8), W, Cm(1),
             size=15, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, r, left, Cm(5.0), W, Cm(2),
             size=20, bold=True, color=DARK, align=PP_ALIGN.CENTER)
    pill = s.shapes.add_shape(MSO_SHAPE.OVAL, left + W/2 - Cm(0.7),
                              Cm(7.0), Cm(1.4), Cm(1.4))
    pill.fill.solid(); pill.fill.fore_color.rgb = GREEN
    pill.line.fill.background()
    tf = pill.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    rr = p.add_run(); rr.text = "✓"
    rr.font.size = Pt(28); rr.font.bold = True; rr.font.color.rgb = WHITE

# Performance numbers
perf = [
    ("1.6 - 2.0 s", "Cold start", BLUE),
    ("< 2 s",       "Trang chủ load",   P1),
    ("5 - 8 s",     "VNPay round-trip", GREEN),
    ("3 - 5 s",     "Chat AI text",     PURPLE),
    ("~ 18 MB",     "APK Release",      RED),
]
W = Cm(6); H = Cm(2.7); GAP = Cm(0.4)
left_start = (Cm(33.0) - (W + GAP) * len(perf) + GAP) // 2 if Cm(33.0) >= (W + GAP) * len(perf) - GAP else Cm(0.5)
for i, (n, l, col) in enumerate(perf):
    left = left_start + (W + GAP) * i
    add_card(s, n, [l], left, Cm(10.5), W, H,
             accent=col, body_size=13, title_size=20)
add_footer(s)

# ----- Slide 34: Pros / Cons ------------------------------------------------
s = add_blank(prs); add_header(s, "7.4 ĐÁNH GIÁ",
                               "Ưu điểm & Hạn chế",
                               34, TOTAL, accent=RED)
add_card(s, "✓  Ưu điểm",
         ["Phủ trọn nghiệp vụ E-commerce thú cưng",
          "Real-time mạnh nhờ Firestore SnapshotListener",
          "Tích hợp 3 dịch vụ ngoài: Google + VNPay + OpenAI",
          "Kiến trúc MVVM rõ ràng, dễ mở rộng",
          "UI Material 3, tiếng Việt đầy đủ",
          "Test pass 49/49 ca tiêu biểu"],
         Cm(0.7), Cm(3.0), Cm(15), Cm(11),
         accent=GREEN, body_size=15, title_size=22)
add_card(s, "✗  Hạn chế",
         ["Chưa có FCM (mới in-app)",
          "Refund VNPay vẫn thủ công (cần Cloud Function)",
          "ShippingHelper hardcode vùng",
          "Facebook Login chờ Meta xét duyệt",
          "Chưa đa ngôn ngữ",
          "Chưa có CI/CD"],
         Cm(16.5), Cm(3.0), Cm(15), Cm(11),
         accent=RED, body_size=15, title_size=22)
add_footer(s)

# ===========================================================================
# WORK ALLOCATION (4 members)
# ===========================================================================
s = add_blank(prs); add_header(s, "PHÂN CÔNG",
                               "Khối lượng công việc – chia đều 4 thành viên",
                               35, TOTAL, accent=P1)
members = [
    ("TV1\nNguyễn Hữu Đức Thọ",
     "Trưởng nhóm – Chương 3",
     ["Splash + điều hướng",
      "Auth Email/Google",
      "OTP qua JavaMail",
      "Profile + Address",
      "Notification real-time",
      "SessionManager"],
     "25 %", PURPLE),
    ("TV2\nĐào Trúc Mai",
     "Chương 4 – Catalog & Home",
     ["Model Pet/Food/Category",
      "Repository Pet/Food/Category",
      "HomeFragment + Banner",
      "Pet/Food Detail",
      "PromotionManager",
      "Glide + Storage"],
     "25 %", TEAL),
    ("TV3\nNguyễn Văn Trường",
     "Chương 5 – Order & Payment",
     ["Cart + Checkout",
      "ShippingHelper 4 vùng",
      "VNPay (HMAC-SHA512)",
      "OrderHistory / Detail",
      "ReturnRequest",
      "Apply voucher/promotion"],
     "25 %", GREEN),
    ("TV4\n……………………………",
     "Chương 6 – Admin & Chatbot",
     ["AdminSetupHelper",
      "Dashboard real-time",
      "Manage 7 module CRUD",
      "Upload media (Storage)",
      "ChatViewModel + OkHttp",
      "OpenAI gpt-4o-mini RAG"],
     "25 %", PINK),
]
W = Cm(7.5); H = Cm(10.5); GAP = Cm(0.3)
for i, (name, sub, tasks, pct, col) in enumerate(members):
    left = Cm(0.7) + (W + GAP) * i; top = Cm(3.0)
    card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, W, H)
    card.adjustments[0] = 0.05
    card.fill.solid(); card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = col; card.line.width = Pt(1.5)
    head = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, W, Cm(2.4))
    head.fill.solid(); head.fill.fore_color.rgb = col
    head.line.fill.background()
    add_text(s, name, left, top + Cm(0.15), W, Cm(1.4),
             size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, sub, left, top + Cm(1.55), W, Cm(0.8),
             size=11, color=WHITE, align=PP_ALIGN.CENTER)
    add_bullets(s, tasks, left + Cm(0.3), top + Cm(2.7),
                W - Cm(0.5), H - Cm(3.8), size=12)
    pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              left + W/2 - Cm(2), top + H - Cm(1.2),
                              Cm(4), Cm(0.9))
    pill.adjustments[0] = 0.5
    pill.fill.solid(); pill.fill.fore_color.rgb = col
    pill.line.fill.background()
    tf = pill.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = pct
    r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = WHITE
add_text(s, "Tổng 100 %  •  Cả nhóm cùng làm: phân tích yêu cầu, kiểm thử chéo, viết báo cáo, slide, demo",
         Cm(1), SLIDE_H - Cm(1.6), SLIDE_W - Cm(2), Cm(0.7),
         size=12, italic=True, color=GREY, align=PP_ALIGN.CENTER, bold=True)
add_footer(s)

# ===========================================================================
# CONCLUSION + ROADMAP + THANKS
# ===========================================================================

# ----- Slide 36: KET LUAN ---------------------------------------------------
s = add_blank(prs); add_header(s, "8 KẾT LUẬN",
                               "Kết quả & Hướng phát triển",
                               36, TOTAL, accent=P2)
add_card(s, "✓ Kết quả đạt được",
         ["Hoàn thành 100% chức năng bắt buộc",
          "Hoàn thành 90% chức năng nâng cao",
          "Test pass 49/49 ca tiêu biểu",
          "Chạy ổn định Android 8.0+",
          "Mã sạch, MVVM rõ ràng, dễ mở rộng"],
         Cm(0.7), Cm(3.0), Cm(15), Cm(5.5),
         accent=GREEN, body_size=15, title_size=20)
add_card(s, "★ Hướng phát triển",
         ["Tích hợp Firebase Cloud Messaging (FCM)",
          "Cloud Function tự động refund VNPay",
          "Thay ShippingHelper bằng GHN/GHTK API",
          "Hoàn thiện Facebook + Apple Sign-In",
          "Đa ngôn ngữ + Bản iOS",
          "AI gợi ý sản phẩm cá nhân hoá"],
         Cm(16.5), Cm(3.0), Cm(15), Cm(5.5),
         accent=BLUE, body_size=15, title_size=20)

add_card(s, "Sản phẩm bàn giao",
         ["1 ứng dụng Android hoàn chỉnh • 30+ Activity • 14 ViewModel • 13 Repository • 17 Entity • ~20 000 LOC • 1 báo cáo Word + 1 slide PowerPoint"],
         Cm(0.7), Cm(8.7), Cm(30.8), Cm(5),
         accent=P1, body_size=15, title_size=20)
add_footer(s)

# ----- Slide cuoi: THANK YOU ------------------------------------------------
s = add_blank(prs)
gradient_rect(s, 0, 0, SLIDE_W, SLIDE_H, P1, P2, angle=135)
deco = s.shapes.add_shape(MSO_SHAPE.OVAL,
                          -Cm(4), -Cm(4), Cm(10), Cm(10))
deco.fill.solid(); deco.fill.fore_color.rgb = P3
deco.line.fill.background(); deco.fill.transparency = 0.5

deco2 = s.shapes.add_shape(MSO_SHAPE.OVAL,
                           SLIDE_W - Cm(8), SLIDE_H - Cm(8),
                           Cm(14), Cm(14))
deco2.fill.solid(); deco2.fill.fore_color.rgb = P3
deco2.line.fill.background(); deco2.fill.transparency = 0.6

add_text(s, "CẢM ƠN THẦY/CÔ ĐÃ LẮNG NGHE",
         Cm(2), Cm(5), Cm(28), Cm(2),
         size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "🐾  Q & A  🐾",
         Cm(2), Cm(8), Cm(28), Cm(2),
         size=36, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "Nhóm PetShop • Nguyễn Hữu Đức Thọ • Đào Trúc Mai • Nguyễn Văn Trường • …………………",
         Cm(2), Cm(12), Cm(28), Cm(1),
         size=15, color=WHITE, align=PP_ALIGN.CENTER)


prs.save(OUT)
print(f"Saved {OUT}  – {len(prs.slides)} slides")
