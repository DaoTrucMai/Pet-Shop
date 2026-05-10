"""Generate BAO_CAO.docx for PetShop project.

A long-form Vietnamese university final-year report (~70-90 pages)
that follows the user's required structure.

Run:
    pip install python-docx Pillow
    python3 build_report.py
"""
from __future__ import annotations
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "images"
OUT = ROOT / "BAO_CAO.docx"

# ---- Brand palette ---------------------------------------------------------
PRIMARY = RGBColor(0xE0, 0x90, 0x10)      # cam dam (de in ra)
ACCENT = RGBColor(0x66, 0x33, 0xCC)
GREY = RGBColor(0x55, 0x55, 0x55)
DARK = RGBColor(0x1A, 0x1A, 0x1A)

# ===========================================================================
# Helpers
# ===========================================================================

def _set_run(run, *, font="Times New Roman", size=13, bold=False, italic=False,
             color: RGBColor | None = None):
    run.font.name = font
    rpr = run._element.get_or_add_rPr()
    rfont = rpr.find(qn('w:rFonts'))
    if rfont is None:
        rfont = OxmlElement('w:rFonts')
        rpr.append(rfont)
    rfont.set(qn('w:ascii'), font)
    rfont.set(qn('w:hAnsi'), font)
    rfont.set(qn('w:cs'), font)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def set_para_format(para, *, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                    line_spacing=1.5, space_before=0, space_after=4,
                    first_line_indent_cm: float | None = None,
                    keep_together=False, keep_with_next=False,
                    left_indent_cm: float | None = None):
    pf = para.paragraph_format
    para.alignment = align
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if first_line_indent_cm is not None:
        pf.first_line_indent = Cm(first_line_indent_cm)
    if left_indent_cm is not None:
        pf.left_indent = Cm(left_indent_cm)
    pf.keep_together = keep_together
    pf.keep_with_next = keep_with_next


def add_para(doc, text, *, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=13,
             bold=False, italic=False, color=None, line_spacing=1.5,
             space_before=0, space_after=4, first_line_indent_cm=None,
             left_indent_cm=None, font="Times New Roman", style=None):
    p = doc.add_paragraph(style=style)
    set_para_format(p, align=align, line_spacing=line_spacing,
                    space_before=space_before, space_after=space_after,
                    first_line_indent_cm=first_line_indent_cm,
                    left_indent_cm=left_indent_cm)
    r = p.add_run(text)
    _set_run(r, font=font, size=size, bold=bold, italic=italic, color=color)
    return p


def add_body(doc, text, *, indent=True):
    """Doan van than bai - co thut dau dong."""
    return add_para(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=13,
                    line_spacing=1.5, space_after=6,
                    first_line_indent_cm=1.0 if indent else None)


def add_h1(doc, text, *, page_break_before=True):
    if page_break_before and doc.paragraphs:
        last = doc.paragraphs[-1]
        last.add_run().add_break(WD_BREAK.PAGE)
    p = doc.add_paragraph()
    set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3,
                    space_before=12, space_after=12, keep_with_next=True)
    r = p.add_run(text)
    _set_run(r, font="Times New Roman", size=18, bold=True, color=PRIMARY)
    p.style = doc.styles['Heading 1']
    return p


def add_h2(doc, text):
    p = doc.add_paragraph()
    set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3,
                    space_before=10, space_after=8, keep_with_next=True)
    r = p.add_run(text)
    _set_run(r, font="Times New Roman", size=15, bold=True, color=DARK)
    p.style = doc.styles['Heading 2']
    return p


def add_h3(doc, text):
    p = doc.add_paragraph()
    set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3,
                    space_before=8, space_after=6, keep_with_next=True)
    r = p.add_run(text)
    _set_run(r, font="Times New Roman", size=13, bold=True, italic=True, color=DARK)
    p.style = doc.styles['Heading 3']
    return p


# ---- Image counters --------------------------------------------------------

_FIGURES: list[tuple[str, str]] = []   # (label, caption)
_TABLES: list[tuple[str, str]] = []


def add_image(doc, filename, caption, *, width_cm=15, center=True):
    """Insert image with caption (Hinh X.Y - Caption)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_para_format(p, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.0,
                    space_before=6, space_after=2)
    run = p.add_run()
    img_path = IMG / filename if not Path(filename).is_absolute() else Path(filename)
    if img_path.exists():
        run.add_picture(str(img_path), width=Cm(width_cm))
    else:
        run.add_text(f"[Hinh khong tim thay: {filename}]")
        _set_run(run, italic=True, color=GREY)

    n = len(_FIGURES) + 1
    label = f"Hình {n}"
    _FIGURES.append((label, caption))

    cap = doc.add_paragraph()
    set_para_format(cap, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15,
                    space_before=2, space_after=10)
    r1 = cap.add_run(f"{label}: ")
    _set_run(r1, size=12, italic=True, bold=True, color=DARK)
    r2 = cap.add_run(caption)
    _set_run(r2, size=12, italic=True, color=DARK)
    return n


def add_table_caption(doc, caption):
    n = len(_TABLES) + 1
    label = f"Bảng {n}"
    _TABLES.append((label, caption))
    p = doc.add_paragraph()
    set_para_format(p, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15,
                    space_before=4, space_after=2)
    r1 = p.add_run(f"{label}: ")
    _set_run(r1, size=12, italic=True, bold=True, color=DARK)
    r2 = p.add_run(caption)
    _set_run(r2, size=12, italic=True, color=DARK)


def add_table(doc, header, rows, *, widths_cm=None, header_bg="F5A623"):
    """Add a styled table; header row in PRIMARY, body rows."""
    cols = len(header)
    table = doc.add_table(rows=1, cols=cols)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    if widths_cm:
        for col_idx, w in enumerate(widths_cm):
            for cell in table.columns[col_idx].cells:
                cell.width = Cm(w)

    # Header
    hdr_cells = table.rows[0].cells
    for i, txt in enumerate(header):
        cell = hdr_cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        _set_run(r, size=12, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        # Background color
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), header_bg)
        tcPr.append(shd)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Body
    for row_data in rows:
        cells = table.add_row().cells
        for i, txt in enumerate(row_data):
            c = cells[i]
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT,
                            line_spacing=1.15, space_after=2)
            r = p.add_run(str(txt))
            _set_run(r, size=11)
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Spacing after table
    spacer = doc.add_paragraph()
    set_para_format(spacer, line_spacing=1.0, space_after=4)
    return table


def add_bullets(doc, items, *, indent_cm=0.5, size=13, bold=False):
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        set_para_format(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                        line_spacing=1.5, space_after=2, left_indent_cm=indent_cm)
        r = p.add_run(item)
        _set_run(r, size=size, bold=bold)


def add_numbered(doc, items, *, indent_cm=0.5, size=13):
    for item in items:
        p = doc.add_paragraph(style='List Number')
        set_para_format(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                        line_spacing=1.5, space_after=2, left_indent_cm=indent_cm)
        r = p.add_run(item)
        _set_run(r, size=size)


def add_code(doc, code: str, *, language: str = ""):
    p = doc.add_paragraph()
    set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.15,
                    space_before=4, space_after=8, left_indent_cm=0.5)
    # background shading
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F5F5F5')
    pPr.append(shd)
    r = p.add_run(code)
    _set_run(r, font="Consolas", size=10, color=DARK)


def page_break(doc):
    p = doc.add_paragraph()
    set_para_format(p, line_spacing=1.0, space_after=0)
    p.add_run().add_break(WD_BREAK.PAGE)


def add_centered_text(doc, text, *, size=13, bold=False, italic=False,
                      color=None, space_before=0, space_after=4,
                      line_spacing=1.5):
    p = doc.add_paragraph()
    set_para_format(p, align=WD_ALIGN_PARAGRAPH.CENTER,
                    line_spacing=line_spacing,
                    space_before=space_before, space_after=space_after)
    r = p.add_run(text)
    _set_run(r, size=size, bold=bold, italic=italic, color=color)
    return p


# ===========================================================================
# Build document
# ===========================================================================

doc = Document()

# Page setup A4 with normal margins
for section in doc.sections:
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.0)

# Default style
normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(13)


# ---------------------------------------------------------------------------
# 1. TRANG BIA CHINH
# ---------------------------------------------------------------------------
add_centered_text(doc, "TRƯỜNG ……………………………………………………………………", size=14, bold=True,
                  space_before=12)
add_centered_text(doc, "KHOA CÔNG NGHỆ THÔNG TIN", size=13, bold=True, space_after=4)
add_centered_text(doc, "------ \u2756 ------", size=14, color=PRIMARY, space_after=18)
# Logo placeholder
add_centered_text(doc, "[ LOGO TRƯỜNG ]", size=11, italic=True, color=GREY,
                  space_before=12, space_after=42)

add_centered_text(doc, "ĐỒ ÁN MÔN HỌC", size=20, bold=True, color=PRIMARY,
                  space_before=12, space_after=4)
add_centered_text(doc, "PHÁT TRIỂN ỨNG DỤNG DI ĐỘNG", size=16, bold=True,
                  space_after=24)

add_centered_text(doc, "Đề tài:", size=14, italic=True, space_after=6)
add_centered_text(doc, "XÂY DỰNG ỨNG DỤNG PETSHOP",
                  size=22, bold=True, color=PRIMARY, space_after=4)
add_centered_text(doc, "CỬA HÀNG THÚ CƯNG VÀ THỨC ĂN CHO THÚ CƯNG",
                  size=18, bold=True, color=PRIMARY, space_after=4)
add_centered_text(doc, "TRÊN NỀN TẢNG ANDROID",
                  size=18, bold=True, color=PRIMARY, space_after=42)

add_centered_text(doc, "Giảng viên hướng dẫn :  ……………………………………………", size=13,
                  space_before=24, space_after=4)
add_centered_text(doc, "Nhóm sinh viên thực hiện (Nhóm ………):", size=13, bold=True,
                  space_before=4, space_after=4)
add_centered_text(doc, "1. Nguyễn Hữu Đức Thọ      –  MSSV: ………………", size=13, space_after=2)
add_centered_text(doc, "2. Đào Trúc Mai             –  MSSV: ………………", size=13, space_after=2)
add_centered_text(doc, "3. Nguyễn Văn Trường        –  MSSV: ………………", size=13, space_after=2)
add_centered_text(doc, "4. ……………………………………        –  MSSV: ………………", size=13, space_after=24)

add_centered_text(doc, "Năm học 2025 – 2026",
                  size=14, bold=True, color=PRIMARY,
                  space_before=24, space_after=2)

page_break(doc)

# ---------------------------------------------------------------------------
# 2. TRANG BIA PHU
# ---------------------------------------------------------------------------
add_centered_text(doc, "TRƯỜNG ……………………………………………………………………", size=14, bold=True,
                  space_before=8)
add_centered_text(doc, "KHOA CÔNG NGHỆ THÔNG TIN", size=13, bold=True, space_after=4)
add_centered_text(doc, "------ \u2756 ------", size=14, color=PRIMARY, space_after=24)

add_centered_text(doc, "ĐỒ ÁN MÔN HỌC", size=20, bold=True, color=PRIMARY,
                  space_after=4)
add_centered_text(doc, "PHÁT TRIỂN ỨNG DỤNG DI ĐỘNG",
                  size=16, bold=True, space_after=18)

add_centered_text(doc, "XÂY DỰNG ỨNG DỤNG PETSHOP – CỬA HÀNG THÚ CƯNG",
                  size=18, bold=True, color=PRIMARY, space_after=4)
add_centered_text(doc, "VÀ THỨC ĂN CHO THÚ CƯNG TRÊN NỀN TẢNG ANDROID",
                  size=18, bold=True, color=PRIMARY, space_after=24)

# Bang thong tin
info = doc.add_table(rows=8, cols=2)
info.alignment = WD_TABLE_ALIGNMENT.CENTER
info.autofit = False
labels = [
    ("Tên đề tài", "Ứng dụng PetShop"),
    ("Loại đề tài", "Đồ án môn học – Phát triển ứng dụng di động"),
    ("Nền tảng", "Android (Java, minSdk 24, targetSdk 36)"),
    ("Công nghệ chính", "Firebase, VNPay, OpenAI, MVVM + Repository"),
    ("Giảng viên hướng dẫn", "……………………………………………………………"),
    ("Mã lớp / Học kỳ", "……… / Học kỳ ………… năm học 2025-2026"),
    ("Thời gian thực hiện", "……/……/2026  →  ……/……/2026"),
    ("Nhóm thực hiện", "Nhóm ………… – 04 thành viên"),
]
for i, (k, v) in enumerate(labels):
    rc = info.rows[i].cells
    rc[0].text = ""
    rc[1].text = ""
    p1 = rc[0].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p1.add_run(k)
    _set_run(r1, size=12, bold=True)
    p2 = rc[1].paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r2 = p2.add_run(v)
    _set_run(r2, size=12)
    rc[0].width = Cm(5.5)
    rc[1].width = Cm(10)

add_centered_text(doc, "", space_after=18)

add_centered_text(doc, "DANH SÁCH NHÓM", size=14, bold=True, color=PRIMARY,
                  space_before=12, space_after=8)
team = doc.add_table(rows=5, cols=4)
team.alignment = WD_TABLE_ALIGNMENT.CENTER
team_header = ["STT", "Họ và tên", "MSSV", "Vai trò trong nhóm"]
for i, h in enumerate(team_header):
    c = team.rows[0].cells[i]
    c.text = ""
    p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h); _set_run(r, size=12, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
    tcPr = c._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), 'F5A623')
    tcPr.append(shd)
team_rows = [
    ("1", "Nguyễn Hữu Đức Thọ", "………………", "Trưởng nhóm – TV1"),
    ("2", "Đào Trúc Mai",      "………………", "Thành viên – TV2"),
    ("3", "Nguyễn Văn Trường", "………………", "Thành viên – TV3"),
    ("4", "……………………………………", "………………", "Thành viên – TV4"),
]
for i, row in enumerate(team_rows):
    rc = team.rows[i + 1].cells
    for j, v in enumerate(row):
        rc[j].text = ""
        p = rc[j].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(v); _set_run(r, size=11)

add_centered_text(doc, "", space_after=18)
add_centered_text(doc, "TP. ……………, Tháng …… năm 2026",
                  size=13, italic=True, space_before=18)
page_break(doc)

# ---------------------------------------------------------------------------
# 3. LOI CAM ON
# ---------------------------------------------------------------------------
add_centered_text(doc, "LỜI CẢM ƠN", size=18, bold=True, color=PRIMARY, space_after=18)
add_body(doc, "Lời đầu tiên, nhóm thực hiện đề tài xin gửi lời cảm ơn chân thành và sâu sắc nhất đến quý Thầy, Cô Khoa Công nghệ Thông tin – Trường …………………………… đã tận tình giảng dạy và truyền đạt cho chúng em những kiến thức nền tảng vô cùng quý báu trong suốt thời gian học tập tại trường. Những kiến thức đó là hành trang, là nền tảng vững chắc giúp nhóm có thể tiếp cận và hoàn thành đề tài này.")
add_body(doc, "Đặc biệt, nhóm xin được gửi lời cảm ơn sâu sắc đến giảng viên hướng dẫn – ……………………………………………… – người đã trực tiếp định hướng đề tài, dành nhiều thời gian, công sức để hướng dẫn, đóng góp ý kiến và chỉnh sửa cho từng phần nội dung. Sự tận tâm, nhiệt tình cùng những góp ý quý báu của Thầy/Cô là động lực rất lớn giúp nhóm vượt qua được các khó khăn về kiến thức, công nghệ và tổ chức nhóm trong quá trình thực hiện.")
add_body(doc, "Nhóm cũng xin gửi lời cảm ơn đến các bạn cùng lớp đã nhiệt tình hỗ trợ kiểm thử ứng dụng, đóng góp ý kiến phản hồi từ góc nhìn người dùng để sản phẩm cuối cùng hoàn thiện hơn. Đồng thời, nhóm xin cảm ơn cộng đồng lập trình Android trên các diễn đàn StackOverflow, Android Developers, Firebase Documentation, VNPay Documentation, OpenAI API Reference… đã chia sẻ tri thức một cách cởi mở để chúng em có nguồn tham khảo phong phú trong quá trình triển khai.")
add_body(doc, "Mặc dù đã cố gắng và nỗ lực hết sức, nhưng do thời gian thực hiện có hạn cùng với kinh nghiệm thực tế chưa nhiều, đề tài chắc chắn không tránh khỏi những thiếu sót. Nhóm kính mong nhận được sự góp ý chân thành từ quý Thầy, Cô và các bạn để đề tài được hoàn thiện hơn nữa, đồng thời giúp các thành viên trong nhóm rút kinh nghiệm cho các dự án trong tương lai.")
add_body(doc, "Một lần nữa, nhóm xin trân trọng cảm ơn!")
add_centered_text(doc, "TP. ……………, Tháng …… năm 2026", size=13, italic=True,
                  space_before=18, space_after=4)
add_centered_text(doc, "Nhóm sinh viên thực hiện", size=13, italic=True, space_after=24)
add_centered_text(doc, "(Ký và ghi rõ họ tên)", size=12, italic=True, color=GREY, space_after=4)
page_break(doc)

# ---------------------------------------------------------------------------
# 4. LOI CAM DOAN
# ---------------------------------------------------------------------------
add_centered_text(doc, "LỜI CAM ĐOAN", size=18, bold=True, color=PRIMARY, space_after=18)
add_body(doc, "Nhóm thực hiện đề tài xin cam đoan rằng đề tài “Xây dựng ứng dụng PetShop – Cửa hàng thú cưng và thức ăn cho thú cưng trên nền tảng Android” là công trình nghiên cứu, phân tích, thiết kế và lập trình do chính nhóm thực hiện dưới sự hướng dẫn của giảng viên ………………………………………………")
add_body(doc, "Toàn bộ mã nguồn được nhóm trực tiếp viết bằng ngôn ngữ Java trên Android Studio, có tham khảo tài liệu chính thức của Android Developers, Firebase, VNPay và OpenAI; các đoạn mã tham khảo từ bên thứ ba (nếu có) đều được trích dẫn rõ ràng trong phần Tài liệu tham khảo. Các tài liệu, hình ảnh, sơ đồ, bảng biểu được sử dụng trong báo cáo đều có nguồn gốc minh bạch hoặc do nhóm tự thiết kế.")
add_body(doc, "Nhóm cam kết không sao chép báo cáo từ bất kỳ đề tài, khoá luận hay tài liệu nào khác. Mọi nội dung, kết quả nêu trong báo cáo đều trung thực, phản ánh đúng quá trình làm việc và sản phẩm thực tế. Nếu phát hiện có bất kỳ sự gian lận, sao chép trái phép nào, nhóm xin hoàn toàn chịu trách nhiệm trước Hội đồng đánh giá và Khoa Công nghệ Thông tin.")
add_centered_text(doc, "TP. ……………, Tháng …… năm 2026", size=13, italic=True,
                  space_before=18, space_after=4)
add_centered_text(doc, "Đại diện nhóm thực hiện", size=13, italic=True, space_after=24)
add_centered_text(doc, "(Ký và ghi rõ họ tên)", size=12, italic=True, color=GREY, space_after=4)
add_centered_text(doc, "Nguyễn Hữu Đức Thọ", size=13, bold=True, space_before=18)
page_break(doc)

# ---------------------------------------------------------------------------
# 5. NHAN XET CUA GIANG VIEN
# ---------------------------------------------------------------------------
add_centered_text(doc, "NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN",
                  size=16, bold=True, color=PRIMARY, space_after=18)

add_para(doc, "Họ và tên giảng viên hướng dẫn : …………………………………………………………………………………………………", size=13, space_after=10)
add_para(doc, "Đơn vị công tác                          : …………………………………………………………………………………………………", size=13, space_after=10)
add_para(doc, "Tên đề tài : Xây dựng ứng dụng PetShop – Cửa hàng thú cưng và thức ăn cho thú cưng trên nền tảng Android.", size=13, space_after=10)

add_para(doc, "Nhận xét chung về tinh thần, thái độ làm việc của nhóm:", size=13, bold=True, space_before=8)
for _ in range(5):
    add_para(doc, "……………………………………………………………………………………………………………………………………", size=13, space_after=2)

add_para(doc, "Nhận xét về nội dung và kết quả thực hiện đề tài:", size=13, bold=True, space_before=8)
for _ in range(8):
    add_para(doc, "……………………………………………………………………………………………………………………………………", size=13, space_after=2)

add_para(doc, "Đánh giá chung:", size=13, bold=True, space_before=8)
for _ in range(3):
    add_para(doc, "……………………………………………………………………………………………………………………………………", size=13, space_after=2)

add_para(doc, "Điểm đề xuất (thang 10):  ………/10", size=13, bold=True, space_before=10)
add_centered_text(doc, "TP. ……………, Tháng …… năm 2026", size=13, italic=True,
                  space_before=18, space_after=4)
add_centered_text(doc, "Giảng viên hướng dẫn", size=13, italic=True, space_after=24)
add_centered_text(doc, "(Ký và ghi rõ họ tên)", size=12, italic=True, color=GREY)
page_break(doc)

# ---------------------------------------------------------------------------
# 6. BANG PHAN CONG CONG VIEC NHOM
# ---------------------------------------------------------------------------
add_centered_text(doc, "BẢNG PHÂN CÔNG CÔNG VIỆC NHÓM",
                  size=16, bold=True, color=PRIMARY, space_after=14)

add_body(doc, "Đề tài được thực hiện bởi nhóm 04 sinh viên với sự phân công rõ ràng theo bốn module chức năng chính của ứng dụng. Việc chia module bám sát kiến trúc MVVM của dự án (Model – View – ViewModel) và đảm bảo mỗi thành viên phụ trách một mảng nghiệp vụ trọn vẹn, từ thiết kế CSDL đến giao diện và xử lý nghiệp vụ. Bảng dưới đây mô tả khái quát phần việc của mỗi thành viên; chi tiết tiến độ và sản phẩm bàn giao xem tại Phụ lục A.", indent=False)

add_table_caption(doc, "Phân công công việc tổng quát giữa 04 thành viên")
add_table(doc,
    header=["TV", "Họ và tên", "Module phụ trách", "Phần công việc chính", "Tỉ lệ"],
    rows=[
        ("TV1", "Nguyễn Hữu Đức Thọ\n(Trưởng nhóm)",
         "Tài khoản – Hồ sơ\n(Chương 3)",
         "Phân tích & thiết kế Use Case Auth; Firebase Authentication "
         "(Email/Password, Google Sign-In, thiết kế Facebook Login); OTP "
         "qua JavaMail; Splash; Login/Register; Profile & Edit Profile; "
         "Quản lý địa chỉ; Hệ thống Notification; SessionManager / "
         "SharedPrefManager; tổng hợp báo cáo & họp nhóm.",
         "25 %"),
        ("TV2", "Đào Trúc Mai",
         "Danh mục & Trang chủ\n(Chương 4)",
         "Thiết kế Model Pet/Food/Category/Banner/Review; Repository "
         "Pet/Food/Category; HomeFragment (banner ViewPager2, lời chào, "
         "tìm kiếm, lọc theo danh mục); CategoryFragment; PetDetailActivity "
         "& FoodDetailActivity; tích hợp Glide + Firebase Storage hiển thị "
         "ảnh; chức năng tìm kiếm và lọc sản phẩm.",
         "25 %"),
        ("TV3", "Nguyễn Văn Trường",
         "Giỏ hàng & Thanh toán\n(Chương 5)",
         "Thiết kế Model Cart/CartItem/Order/OrderItem/ReturnRequest/"
         "PaymentTransaction; CartRepository; CartFragment & CartActivity; "
         "CheckoutActivity; tính phí ship theo vùng (ShippingHelper); áp "
         "voucher/promotion; tích hợp VNPay (VNPayHelper – HMAC-SHA512, "
         "VNPayWebViewActivity, VNPayResultActivity Deep Link); OrderHistory "
         "& OrderDetail; ReturnRequestActivity.",
         "25 %"),
        ("TV4", "……………………………………",
         "Quản trị & Chatbot\n(Chương 6)",
         "Phân quyền Admin (AdminSetupHelper); AdminActivity dashboard "
         "real-time (AdminViewModel + SnapshotListener); Quản lý User / "
         "Category / Pet / Food / Promotion / Voucher / Order / Return; "
         "tải ảnh sản phẩm (StorageHelper); thiết kế hội thoại Chatbot; "
         "ChatViewModel gọi OpenAI Chat Completions bằng OkHttp + Gson; "
         "lưu lịch sử chat trên Firestore.",
         "25 %"),
    ],
    widths_cm=[1.0, 3.2, 3.0, 6.5, 1.3])

add_para(doc, "Ngoài phần module riêng, cả 04 thành viên cùng tham gia các nhiệm vụ chung gồm: (1) phân tích yêu cầu, vẽ Use Case tổng quát (Chương 1, 2); (2) thiết kế kiến trúc tổng thể, mô hình dữ liệu Firestore và Security Rules (Chương 2); (3) kiểm thử chéo các module (Chương 7); (4) chuẩn bị slide trình bày, viết báo cáo, demo trực tiếp.", size=12, italic=True, space_before=6)
page_break(doc)

# ---------------------------------------------------------------------------
# 7. DANH MUC TU VIET TAT
# ---------------------------------------------------------------------------
add_centered_text(doc, "DANH MỤC TỪ VIẾT TẮT", size=16, bold=True, color=PRIMARY,
                  space_after=14)
add_table(doc,
    header=["Từ viết tắt", "Nguyên gốc / Tiếng Anh", "Giải thích"],
    rows=[
        ("API", "Application Programming Interface", "Giao diện lập trình ứng dụng"),
        ("APK", "Android Package Kit", "Định dạng cài đặt ứng dụng Android"),
        ("BaaS", "Backend as a Service", "Dịch vụ backend dạng nền tảng (vd: Firebase)"),
        ("CRUD", "Create – Read – Update – Delete", "Bốn tác vụ cơ bản với dữ liệu"),
        ("COD", "Cash On Delivery", "Thanh toán khi nhận hàng"),
        ("FCM", "Firebase Cloud Messaging", "Dịch vụ push notification của Google"),
        ("HMAC", "Hash-based Message Authentication Code", "Mã xác thực thông điệp dựa trên hàm băm"),
        ("JSON", "JavaScript Object Notation", "Định dạng trao đổi dữ liệu phổ biến"),
        ("LiveData", "—", "Lớp dữ liệu nhận thức vòng đời của AndroidX"),
        ("MVC / MVVM", "Model-View-Controller / Model-View-ViewModel", "Các mẫu kiến trúc phần mềm"),
        ("NoSQL", "Not only SQL", "CSDL phi quan hệ (Firestore là một ví dụ)"),
        ("OAuth", "Open Authorization", "Chuẩn xác thực mở (Google/Facebook Sign-In)"),
        ("OTP", "One-Time Password", "Mật khẩu sử dụng một lần (gửi qua email)"),
        ("REST", "Representational State Transfer", "Kiểu kiến trúc dịch vụ web phổ biến"),
        ("SDK", "Software Development Kit", "Bộ công cụ phát triển phần mềm"),
        ("SHA-512", "Secure Hash Algorithm 512-bit", "Hàm băm 512 bit dùng cho HMAC VNPay"),
        ("SMTP", "Simple Mail Transfer Protocol", "Giao thức gửi email"),
        ("UI / UX", "User Interface / User Experience", "Giao diện / Trải nghiệm người dùng"),
        ("URL", "Uniform Resource Locator", "Định danh tài nguyên trên Internet"),
        ("VNPAY", "—", "Cổng thanh toán điện tử Việt Nam"),
        ("XML", "eXtensible Markup Language", "Định dạng đánh dấu mở rộng (Android layout)"),
    ],
    widths_cm=[3.0, 5.5, 7.0])
page_break(doc)

# ---------------------------------------------------------------------------
# 8. DANH MUC HINH ANH (placeholder - will be filled later)
# ---------------------------------------------------------------------------
add_centered_text(doc, "DANH MỤC HÌNH ẢNH", size=16, bold=True, color=PRIMARY,
                  space_after=12)
fig_heading = doc.add_paragraph()
fig_heading.add_run().add_text("(Tự động cập nhật sau khi nhấn F9 trong Word)")
_set_run(fig_heading.runs[0], size=12, italic=True, color=GREY)
fig_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_para(doc, "Mục lục hình ảnh sẽ được sinh tự động bằng cách: trong Word vào References → Insert Table of Figures → chọn Caption label = “Hình”.", size=12, italic=True, color=GREY, space_after=12)
# Pre-list mockup (will list 18 diagrams + screenshots that will be added)
DIAGRAM_FIGURE_LIST = [
    ("Hình 1.1", "Sơ đồ Use Case tổng quát của ứng dụng PetShop"),
    ("Hình 1.2", "Sơ đồ kiến trúc MVVM + Repository + Firebase"),
    ("Hình 1.3", "Mô hình tổ chức package mã nguồn"),
    ("Hình 2.1", "Sơ đồ ERD logic của các collection trên Firestore"),
    ("Hình 2.2", "Sơ đồ collection Firestore của ứng dụng PetShop"),
    ("Hình 2.3", "Tóm tắt logic Firestore Security Rules"),
    ("Hình 2.4", "Sơ đồ luồng dữ liệu giữa các tầng MVVM"),
    ("Hình 2.5", "Sơ đồ trạng thái đơn hàng (State Diagram)"),
    ("Hình 2.6", "Bộ màu chủ đạo và icon của ứng dụng"),
    ("Hình 3.1", "Activity Diagram – luồng đăng ký, đăng nhập"),
    ("Hình 3.2", "Hành trình người dùng (Customer Journey)"),
    ("Hình 4.1", "Giao diện màn hình Trang chủ"),
    ("Hình 5.1", "Activity Diagram – luồng đặt hàng & thanh toán"),
    ("Hình 5.2", "Sequence Diagram – thanh toán qua VNPay"),
    ("Hình 5.3", "Sơ đồ luồng dữ liệu thanh toán VNPay"),
    ("Hình 5.4", "Sơ đồ trạng thái thanh toán hiển thị cho khách"),
    ("Hình 5.5", "Activity Diagram – yêu cầu trả hàng"),
    ("Hình 6.1", "Hành trình quản trị viên (Admin Journey)"),
    ("Hình 6.2", "Sequence Diagram – Admin Dashboard real-time"),
    ("Hình 6.3", "Sơ đồ kiến trúc Chatbot RAG nhẹ"),
]
for code, title in DIAGRAM_FIGURE_LIST:
    p = doc.add_paragraph()
    set_para_format(p, line_spacing=1.15, space_after=2)
    r = p.add_run(f"{code}.   {title}")
    _set_run(r, size=12)
page_break(doc)

# ---------------------------------------------------------------------------
# 9. DANH MUC BANG BIEU
# ---------------------------------------------------------------------------
add_centered_text(doc, "DANH MỤC BẢNG BIỂU", size=16, bold=True, color=PRIMARY,
                  space_after=12)
add_para(doc, "Mục lục bảng biểu sẽ được sinh tự động bằng References → Insert Table of Figures → chọn Caption label = “Bảng”.", size=12, italic=True, color=GREY, space_after=12)
TABLE_LIST = [
    ("Bảng 0", "Phân công công việc tổng quát giữa 04 thành viên"),
    ("Bảng 1.1", "So sánh các giải pháp Pet shop hiện có trên thị trường"),
    ("Bảng 1.2", "Yêu cầu chức năng (FR) cho khách hàng"),
    ("Bảng 1.3", "Yêu cầu chức năng (FR) cho quản trị viên"),
    ("Bảng 1.4", "Yêu cầu phi chức năng (NFR)"),
    ("Bảng 2.1", "Mô tả Use Case 'Đặt hàng và thanh toán'"),
    ("Bảng 2.2", "Mô tả Use Case 'Yêu cầu trả hàng / hoàn tiền'"),
    ("Bảng 2.3", "Cấu trúc các collection chính trên Firestore"),
    ("Bảng 3.1", "Các thuộc tính của Model User"),
    ("Bảng 4.1", "Các thuộc tính của Model Pet"),
    ("Bảng 4.2", "Các thuộc tính của Model Food"),
    ("Bảng 5.1", "Bảng giá phí vận chuyển theo vùng"),
    ("Bảng 5.2", "Tham số chính của VNPay buildPaymentUrl"),
    ("Bảng 6.1", "Các tab quản trị trong AdminActivity"),
    ("Bảng 7.1", "Test case module Tài khoản"),
    ("Bảng 7.2", "Test case module Catalog"),
    ("Bảng 7.3", "Test case module Order & Payment"),
    ("Bảng 7.4", "Test case module Admin"),
    ("Bảng 7.5", "Test case module Chatbot"),
]
for code, title in TABLE_LIST:
    p = doc.add_paragraph()
    set_para_format(p, line_spacing=1.15, space_after=2)
    r = p.add_run(f"{code}.   {title}")
    _set_run(r, size=12)
page_break(doc)

# ---------------------------------------------------------------------------
# 10. MUC LUC
# ---------------------------------------------------------------------------
add_centered_text(doc, "MỤC LỤC", size=16, bold=True, color=PRIMARY,
                  space_after=12)
add_para(doc, "Mục lục được sinh tự động: trong Word vào References → Table of Contents → chọn “Automatic Table 1”. Sau khi nhấn Update Field (F9), Word sẽ liệt kê đầy đủ các chương, mục theo Heading 1/2/3 đã được định nghĩa trong báo cáo này.", size=12, italic=True, color=GREY, space_after=10)

# Manual TOC outline
toc_items = [
    ("MỞ ĐẦU", 0),
    ("1. Lý do chọn đề tài", 1),
    ("2. Mục tiêu của đề tài", 1),
    ("3. Đối tượng và phạm vi nghiên cứu", 1),
    ("4. Phương pháp thực hiện", 1),
    ("5. Bố cục báo cáo", 1),
    ("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ CÔNG NGHỆ SỬ DỤNG", 0),
    ("1.1. Khảo sát hiện trạng các ứng dụng pet shop", 1),
    ("1.2. Mô tả bài toán và yêu cầu chức năng", 1),
    ("1.3. Công nghệ sử dụng", 1),
    ("1.4. Công cụ phát triển và quản lý dự án", 1),
    ("CHƯƠNG 2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", 0),
    ("2.1. Sơ đồ Use Case tổng quát", 1),
    ("2.2. Đặc tả các Use Case chính", 1),
    ("2.3. Sơ đồ hoạt động (Activity Diagram)", 1),
    ("2.4. Thiết kế cơ sở dữ liệu trên Cloud Firestore", 1),
    ("2.5. Kiến trúc tổng thể của ứng dụng", 1),
    ("2.6. Thiết kế giao diện (UI/UX)", 1),
    ("CHƯƠNG 3. XÂY DỰNG MODULE TÀI KHOẢN VÀ HỒ SƠ NGƯỜI DÙNG", 0),
    ("CHƯƠNG 4. XÂY DỰNG MODULE DANH MỤC SẢN PHẨM VÀ TRANG CHỦ", 0),
    ("CHƯƠNG 5. XÂY DỰNG MODULE GIỎ HÀNG, THANH TOÁN VÀ ĐƠN HÀNG", 0),
    ("CHƯƠNG 6. XÂY DỰNG MODULE QUẢN TRỊ VÀ CHATBOT TƯ VẤN", 0),
    ("CHƯƠNG 7. KIỂM THỬ, TRIỂN KHAI VÀ ĐÁNH GIÁ", 0),
    ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 0),
    ("TÀI LIỆU THAM KHẢO", 0),
    ("PHỤ LỤC A. Bảng phân công công việc chi tiết và tiến độ", 0),
    ("PHỤ LỤC B. Cấu trúc thư mục mã nguồn", 0),
    ("PHỤ LỤC C. Sơ đồ Firestore và Security Rules", 0),
    ("PHỤ LỤC D. Ảnh chụp màn hình toàn bộ ứng dụng", 0),
]
for text, level in toc_items:
    p = doc.add_paragraph()
    set_para_format(p, line_spacing=1.3, space_after=3,
                    left_indent_cm=0.6 * level)
    r = p.add_run(text)
    if level == 0:
        _set_run(r, size=12, bold=True)
    else:
        _set_run(r, size=12)

# ---------------------------------------------------------------------------
# Append body chapters
# ---------------------------------------------------------------------------
import sys
sys.path.insert(0, str(ROOT))
from _chapters_body import build_intro, build_chapter1, build_chapter2
from _chapters_body2 import (
    build_chapter3, build_chapter4, build_chapter5, build_chapter6
)
from _chapters_body3 import (
    build_chapter7, build_conclusion, build_references, build_appendix
)

scope = dict(globals())  # share helpers
scope['GREY'] = GREY

build_intro(scope)
build_chapter1(scope)
build_chapter2(scope)
build_chapter3(scope)
build_chapter4(scope)
build_chapter5(scope)
build_chapter6(scope)
build_chapter7(scope)
build_conclusion(scope)
build_references(scope)
build_appendix(scope)

print("Tong so doan:", len(doc.paragraphs))
print("Tong so hinh anh dat caption:", len(_FIGURES))
print("Tong so bang:", len(_TABLES))

doc.save(OUT)
print("Da luu", OUT)
