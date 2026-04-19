"""
preview.py — Xem toan bo UI ma khong can backend
Chay tu thu muc Frontend/:
    python preview.py
"""
import sys
from unittest.mock import MagicMock

# ─────────────────────────────────────────────────────────────────────────────
# 1. Session gia lap (user da dang nhap)
# ─────────────────────────────────────────────────────────────────────────────
from models.user import User
from utils.session import Session

_fake_user = User(
    id=1,
    username="admin",
    ho_ten="Nguyen Van Admin",
    role="admin",
    email="admin@edustu.vn",
)
Session.set(token="fake-token", user=_fake_user)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Du lieu mau
# ─────────────────────────────────────────────────────────────────────────────
FAKE_STUDENTS = [
    {"mssv": "SV001", "ho_ten": "Nguyen Van An",   "lop": "CNTT-K67",
     "khoa": "Cong nghe thong tin", "ngay_sinh": "2003-05-10",
     "trang_thai": "Dang hoc",  "gioi_tinh": "Nam",
     "email": "an@sv.edu", "so_dien_thoai": "0901111111",
     "dia_chi": "123 Pho Hue, Hai Ba Trung, Ha Noi",
     "que_quan": "Nam Dinh", "cccd": "012345678901"},
    {"mssv": "SV002", "ho_ten": "Tran Thi Bich",   "lop": "KT-K67",
     "khoa": "Kinh te",           "ngay_sinh": "2003-08-22",
     "trang_thai": "Dang hoc",  "gioi_tinh": "Nu",
     "email": "bich@sv.edu", "so_dien_thoai": "0902222222",
     "dia_chi": "45 Le Hong Phong, Ngo Quyen, Hai Phong",
     "que_quan": "Hai Phong", "cccd": "032198765432"},
    {"mssv": "SV003", "ho_ten": "Le Van Cuong",    "lop": "CNTT-K66",
     "khoa": "Cong nghe thong tin", "ngay_sinh": "2002-11-15",
     "trang_thai": "Thoi hoc",  "gioi_tinh": "Nam",
     "email": "cuong@sv.edu", "so_dien_thoai": "0903333333",
     "dia_chi": "78 Nguyen Chi Thanh, Hai Chau, Da Nang",
     "que_quan": "Quang Nam", "cccd": "049112233445"},
    {"mssv": "SV004", "ho_ten": "Pham Thi Dung",   "lop": "NN-K67",
     "khoa": "Ngoai ngu",         "ngay_sinh": "2003-03-01",
     "trang_thai": "Bao luu",   "gioi_tinh": "Nu",
     "email": "dung@sv.edu", "so_dien_thoai": "0904444444",
     "dia_chi": "200 Nguyen Trai, Q.1, TP HCM",
     "que_quan": "Tien Giang", "cccd": "079304455667"},
    {"mssv": "SV005", "ho_ten": "Hoang Van Em",    "lop": "DDT-K67",
     "khoa": "Dien - Dien tu",    "ngay_sinh": "2003-07-19",
     "trang_thai": "Dang hoc",  "gioi_tinh": "Nam",
     "email": "em@sv.edu", "so_dien_thoai": "0905555555",
     "dia_chi": "15 Ly Thai To, Bac Ninh",
     "que_quan": "Bac Ninh", "cccd": "023567891234"},
]

from models.course import Course
FAKE_COURSES = [
    Course(ma_hp="CS101", ten_hp="Lap trinh Python",    so_tin_chi=3,
           giao_vien="GS. Nguyen Van A",  hoc_ky="HK1-2024-2025"),
    Course(ma_hp="CS102", ten_hp="Co so du lieu",       so_tin_chi=3,
           giao_vien="TS. Tran Thi B",   hoc_ky="HK1-2024-2025"),
    Course(ma_hp="MA101", ten_hp="Giai tich 1",         so_tin_chi=4,
           giao_vien="PGS. Le Van C",    hoc_ky="HK2-2024-2025"),
    Course(ma_hp="EN101", ten_hp="Tieng Anh co ban",    so_tin_chi=2,
           giao_vien="ThS. Pham Thi D",  hoc_ky="HK1-2024-2025"),
    Course(ma_hp="CS201", ten_hp="Ky thuat phan mem",   so_tin_chi=3,
           giao_vien="TS. Nguyen Van E", hoc_ky="HK2-2024-2025"),
]

from models.grade import Grade
FAKE_GRADES = [
    Grade(id=1, mssv="SV001", ma_hp="CS101", ten_hp="Lap trinh Python",
          so_tin_chi=3, diem_gk=7.5, diem_ck=8.0, hoc_ky="HK1-2024-2025"),
    Grade(id=2, mssv="SV001", ma_hp="CS102", ten_hp="Co so du lieu",
          so_tin_chi=3, diem_gk=6.0, diem_ck=7.0, hoc_ky="HK1-2024-2025"),
    Grade(id=3, mssv="SV001", ma_hp="MA101", ten_hp="Giai tich 1",
          so_tin_chi=4, diem_gk=4.0, diem_ck=3.5, hoc_ky="HK2-2024-2025"),
    Grade(id=4, mssv="SV001", ma_hp="EN101", ten_hp="Tieng Anh co ban",
          so_tin_chi=2, diem_gk=8.5, diem_ck=9.0, hoc_ky="HK1-2024-2025"),
]
FAKE_GRADE_DATA = {
    "diem_list": [g.to_dict() | {"ten_hp": g.ten_hp, "so_tin_chi": g.so_tin_chi, "id": g.id} for g in FAKE_GRADES],
    "gpa_tich_luy": 2.85,
    "gpa_ky": 2.63,
    "tin_chi_dat": 8,
    "tin_chi_dang_ky": 12,
    "xep_loai": "Kha",
    "canh_bao": "",
}

from models.tuition import Tuition
FAKE_TUITIONS = [
    Tuition(mssv="SV001", ho_ten="Nguyen Van An",
            phai_nop=8_500_000, da_nop=8_500_000, trang_thai="Da dong"),
    Tuition(mssv="SV002", ho_ten="Tran Thi Bich",
            phai_nop=8_500_000, da_nop=5_000_000, trang_thai="Dong thieu"),
    Tuition(mssv="SV003", ho_ten="Le Van Cuong",
            phai_nop=8_500_000, da_nop=0,          trang_thai="Chua dong"),
    Tuition(mssv="SV004", ho_ten="Pham Thi Dung",
            phai_nop=8_500_000, da_nop=8_500_000, trang_thai="Da dong"),
    Tuition(mssv="SV005", ho_ten="Hoang Van Em",
            phai_nop=8_500_000, da_nop=2_000_000, trang_thai="Dong thieu"),
]

FAKE_DASHBOARD = {
    "tong_sv": 342,
    "dang_hoc": 301,
    "canh_bao_hv": 18,
    "no_hoc_phi": 47,
    "alerts": [
        {"ho_ten": "Le Van Cuong",   "mo_ta": "GPA 1.45 - canh bao hoc vu lan 2"},
        {"ho_ten": "Pham Thi Dung",  "mo_ta": "Chua nop hoc phi HK1-2024-2025"},
        {"ho_ten": "Nguyen Van Em",  "mo_ta": "Vang qua 30% tiet hoc"},
        {"ho_ten": "Tran Quoc Hung", "mo_ta": "GPA 1.72 - canh bao hoc vu lan 1"},
    ],
}

FAKE_STATS = [
    {"khoa": "Cong nghe thong tin", "tong_sv": 120, "dang_hoc": 110,
     "gpa_tb": 2.91, "ti_le_dat": 87.5, "canh_bao_hv": 8},
    {"khoa": "Kinh te",             "tong_sv": 95,  "dang_hoc": 88,
     "gpa_tb": 2.74, "ti_le_dat": 82.1, "canh_bao_hv": 5},
    {"khoa": "Ngoai ngu",           "tong_sv": 73,  "dang_hoc": 68,
     "gpa_tb": 3.10, "ti_le_dat": 91.0, "canh_bao_hv": 3},
    {"khoa": "Dien - Dien tu",      "tong_sv": 54,  "dang_hoc": 35,
     "gpa_tb": 2.55, "ti_le_dat": 78.0, "canh_bao_hv": 2},
]

# ─────────────────────────────────────────────────────────────────────────────
# 3. Tao mock controllers (khong goi HTTP)
# ─────────────────────────────────────────────────────────────────────────────

def _student_ctrl():
    ctrl = MagicMock()
    svc  = MagicMock()
    svc.get_list.return_value       = {"items": FAKE_STUDENTS, "total": len(FAKE_STUDENTS)}
    svc.get_by_mssv.return_value    = FAKE_STUDENTS[0]
    ctrl._svc = svc

    def load_list(search="", *args, on_success=None, on_error=None, **kw):
        if on_success:
            on_success(svc.get_list.return_value)
    ctrl.load_list.side_effect = load_list

    def load_one(mssv, on_success=None, on_error=None):
        from models.student import Student
        raw = next((s for s in FAKE_STUDENTS if s["mssv"] == mssv), FAKE_STUDENTS[0])
        sv  = Student(mssv=raw["mssv"], ho_ten=raw["ho_ten"], lop=raw["lop"],
                      khoa=raw["khoa"], trang_thai=raw["trang_thai"])
        if on_success:
            on_success(sv)
    ctrl.load_one.side_effect = load_one
    return ctrl


def _course_ctrl():
    ctrl = MagicMock()
    svc  = MagicMock()
    svc.get_list.return_value = FAKE_COURSES
    ctrl._svc = svc

    def load_list(search="", *args, on_success=None, on_error=None, **kw):
        if on_success:
            on_success(FAKE_COURSES)
    ctrl.load_list.side_effect = load_list
    return ctrl


def _grade_ctrl():
    ctrl = MagicMock()
    svc  = MagicMock()
    svc.get_transcript.return_value = FAKE_GRADE_DATA
    ctrl._svc = svc
    return ctrl


def _tuition_ctrl():
    ctrl = MagicMock()
    svc  = MagicMock()
    svc.get_list.return_value      = FAKE_TUITIONS
    svc.get_debt_list.return_value = FAKE_TUITIONS
    ctrl._svc = svc

    def load_list(search="", *args, on_success=None, on_error=None, **kw):
        if on_success:
            on_success(FAKE_TUITIONS)
    ctrl.load_list.side_effect = load_list

    def load_debt_list(on_success=None, on_error=None):
        if on_success:
            on_success(FAKE_TUITIONS)
    ctrl.load_debt_list.side_effect = load_debt_list
    return ctrl


def _report_ctrl():
    ctrl = MagicMock()
    svc  = MagicMock()
    svc.get_dashboard.return_value  = FAKE_DASHBOARD
    svc.get_statistics.return_value = FAKE_STATS
    ctrl._svc = svc

    def load_statistics(on_success=None, on_error=None):
        if on_success:
            on_success(FAKE_STATS)
    ctrl.load_statistics.side_effect = load_statistics
    return ctrl


# ─────────────────────────────────────────────────────────────────────────────
# 4. Monkey-patch controllers truoc khi import views
# ─────────────────────────────────────────────────────────────────────────────
import controllers.student as _cs
import controllers.course  as _cc
import controllers.grade   as _cg
import controllers.tuition as _ct
import controllers.report  as _cr

_cs.StudentController = lambda: _student_ctrl()
_cc.CourseController  = lambda: _course_ctrl()
_cg.GradeController   = lambda: _grade_ctrl()
_ct.TuitionController = lambda: _tuition_ctrl()
_cr.ReportController  = lambda: _report_ctrl()

# Mock GPA chi tiết trong GradeController
_FAKE_GPA = {
    "gpa_tich_luy": 2.85,
    "tin_chi_dat":  8,
    "tin_chi_dang_ky": 12,
    "xep_loai":     "Kha",
    "canh_bao":     "",
    "by_ky": [
        {"hoc_ky": "HK1-2023-2024", "gpa": 2.70, "tin_chi_dat": 10, "xep_loai": "Trung binh"},
        {"hoc_ky": "HK2-2023-2024", "gpa": 3.10, "tin_chi_dat": 12, "xep_loai": "Kha"},
        {"hoc_ky": "HK1-2024-2025", "gpa": 2.85, "tin_chi_dat":  8, "xep_loai": "Kha"},
    ],
}

def _grade_ctrl():
    ctrl = MagicMock()
    svc  = MagicMock()
    svc.get_transcript.return_value = FAKE_GRADE_DATA
    svc.get_gpa.return_value = _FAKE_GPA
    ctrl._svc = svc
    def load_gpa(mssv, on_success=None, on_error=None):
        if on_success:
            on_success(_FAKE_GPA)
    ctrl.load_gpa.side_effect = load_gpa
    return ctrl

# AuthController mock don gian (de LoginView khong crash)
import controllers.auth as _ca
_auth_mock = MagicMock()
_ca.AuthController = lambda: _auth_mock

# ─────────────────────────────────────────────────────────────────────────────
# 5. Import views (sau khi da patch)
# ─────────────────────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from utils.config import PRIMARY, SECONDARY, HIGHLIGHT, TEXT_LIGHT, TEXT_MUTED, BORDER

NAV_SCREENS = [
    ("login",     "  Login (man hinh dang nhap)"),
    ("dashboard", "  Dashboard"),
    ("sinhvien",  "  Sinh vien"),
    ("hocphan",   "  Hoc phan"),
    ("diem",      "  Diem so"),
    ("hocphi",    "  Hoc phi"),
    ("baocao",    "  Bao cao"),
]


class PreviewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduStu — Preview UI (khong can backend)")
        self.setMinimumSize(1280, 750)
        self.setStyleSheet(f"background: {PRIMARY}; color: {TEXT_LIGHT};")
        self._build()
        self._load_screens()
        self._switch("dashboard")

    # ── Build layout ──────────────────────────────────────────────────────────
    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._make_sidebar())

        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background: {PRIMARY};")
        root.addWidget(self.stack)

    def _make_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"""
            QFrame {{ background: {SECONDARY}; border-right: 1px solid {BORDER}; }}
        """)
        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Brand header
        brand = QFrame()
        brand.setFixedHeight(64)
        brand.setStyleSheet(f"border-bottom: 1px solid {BORDER};")
        bl = QVBoxLayout(brand)
        bl.setContentsMargins(16, 8, 16, 8)
        bl.setSpacing(2)
        lbl1 = QLabel("EduStu — Preview")
        lbl1.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl1.setStyleSheet(f"color: {HIGHLIGHT}; border: none;")
        lbl2 = QLabel("Chon man hinh de xem")
        lbl2.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px; border: none;")
        bl.addWidget(lbl1)
        bl.addWidget(lbl2)
        lay.addWidget(brand)
        lay.addSpacing(6)

        # Nav buttons
        self._nav_btns: dict[str, QPushButton] = {}
        for key, label in NAV_SCREENS:
            btn = QPushButton(label)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding-left: 14px;
                    border: none;
                    border-left: 3px solid transparent;
                    background: transparent;
                    font-size: 12px;
                    color: {TEXT_MUTED};
                }}
                QPushButton:hover {{
                    background: rgba(255,255,255,0.05);
                    color: {TEXT_LIGHT};
                }}
                QPushButton:checked {{
                    background: rgba(233,69,96,0.12);
                    color: {HIGHLIGHT};
                    border-left: 3px solid {HIGHLIGHT};
                    font-weight: 600;
                }}
            """)
            btn.clicked.connect(lambda _, k=key: self._switch(k))
            self._nav_btns[key] = btn
            lay.addWidget(btn)

        lay.addStretch()

        # Footer hint
        hint = QLabel("Khong can backend / API")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 10px; padding: 8px;")
        lay.addWidget(hint)
        return sidebar

    # ── Load tat ca man hinh ─────────────────────────────────────────────────
    def _load_screens(self):
        from views.login_view     import LoginView
        from views.dashboard_view import DashboardView
        from views.student_view   import StudentView
        from views.course_view    import CourseView
        from views.grade_view     import GradeView
        from views.tuition_view   import TuitionView
        from views.report_view    import ReportView

        self._screens: dict[str, QWidget] = {
            "login":     LoginView(on_success=lambda user: None),
            "dashboard": DashboardView(),
            "sinhvien":  StudentView(),
            "hocphan":   CourseView(),
            "diem":      GradeView(),
            "hocphi":    TuitionView(),
            "baocao":    ReportView(),
        }
        for w in self._screens.values():
            self.stack.addWidget(w)

        self._preload_grade_view()

    def _preload_grade_view(self):
        """Hien thi bang diem mau ngay khi mo man hinh Diem so."""
        from views.grade_view import GradeView
        from models.student import Student
        gv: GradeView = self._screens["diem"]
        fake_sv = Student(mssv="SV001", ho_ten="Nguyen Van An",
                          lop="CNTT-K67", khoa="Cong nghe thong tin",
                          trang_thai="Dang hoc")
        gv._student = fake_sv
        gv.inp_mssv.setText("SV001")
        gv.av.setText(fake_sv.avatar_text)
        gv.p_name.setText(fake_sv.ho_ten)
        gv.p_lop.setText(f"{fake_sv.lop} · {fake_sv.khoa}")

    # ── Chuyen man hinh ──────────────────────────────────────────────────────
    def _switch(self, key: str):
        for k, btn in self._nav_btns.items():
            btn.setChecked(k == key)
        if key not in self._screens:
            return
        self.stack.setCurrentWidget(self._screens[key])
        view = self._screens[key]
        if hasattr(view, "refresh"):
            try:
                view.refresh()
            except Exception as e:
                print(f"[preview] refresh '{key}' error: {e}")
        elif key == "diem":
            try:
                view._reload()
            except Exception as e:
                print(f"[preview] reload 'diem' error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Chay
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    win = PreviewWindow()
    win.show()
    sys.exit(app.exec())
