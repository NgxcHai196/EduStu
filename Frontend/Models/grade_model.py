"""
grade_model.py
==============
Model điểm số — nhập điểm, tính tổng kết, xếp loại, tính GPA.

Bảng MySQL: grades
  id, student_id, course_id, hoc_ky,
  diem_gk, diem_ck, tong_ket, xep_loai, updated_at
  UNIQUE KEY (student_id, course_id, hoc_ky)

Công thức:
  tong_ket = diem_gk * 0.4 + diem_ck * 0.6
  GPA (thang 4) quy đổi từ thang 10

QUY TẮC MODEL:
  - Không import từ views/ hoặc controllers/
  - Hàm tinh_tong_ket() và xep_loai() là logic nghiệp vụ
    → nằm ở Model, không nằm ở View hay Controller
"""

import copy
from utils.api_client import ApiClient
from models.demo_data import DEMO_GRADES, DEMO_STUDENTS


# ─────────────────────────────────────────────────────────────
#  HÀM NGHIỆP VỤ (business logic thuần Python)
# ─────────────────────────────────────────────────────────────

def tinh_tong_ket(diem_gk: float, diem_ck: float) -> float:
    """
    Công thức chuẩn: GK 40% + CK 60%.
    Làm tròn 2 chữ số thập phân.
    """
    return round(diem_gk * 0.4 + diem_ck * 0.6, 2)


def xep_loai_diem(tong_ket: float) -> str:
    """
    Xếp loại theo thang điểm 10.
    Khớp với quy chế đào tạo đại học phổ biến tại Việt Nam.
    """
    if tong_ket >= 8.5: return "Xuất sắc"
    if tong_ket >= 7.0: return "Giỏi"
    if tong_ket >= 5.5: return "Khá"
    if tong_ket >= 4.0: return "Trung bình"
    if tong_ket >= 2.0: return "Yếu"
    return "Kém"


def quy_doi_sang_gpa4(diem10: float) -> float:
    """
    Quy đổi điểm thang 10 → thang 4 (GPA kiểu Mỹ).
    Bảng quy đổi theo quy chế Bộ GD&ĐT.
    """
    if diem10 >= 8.5: return 4.0
    if diem10 >= 8.0: return 3.7
    if diem10 >= 7.5: return 3.5
    if diem10 >= 7.0: return 3.0
    if diem10 >= 6.5: return 2.5
    if diem10 >= 6.0: return 2.0
    if diem10 >= 5.5: return 1.5
    if diem10 >= 5.0: return 1.0
    if diem10 >= 4.0: return 0.5
    return 0.0


def xep_loai_hoc_luc(gpa: float) -> str:
    """
    Xếp loại học lực theo GPA thang 4.
    Dùng để hiển thị trong bảng điểm cá nhân.
    """
    if gpa >= 3.6: return "Xuất sắc"
    if gpa >= 3.2: return "Giỏi"
    if gpa >= 2.5: return "Khá"
    if gpa >= 2.0: return "Trung bình"
    if gpa >= 1.0: return "Yếu"
    return "Kém — Cảnh báo học vụ"


# ─────────────────────────────────────────────────────────────
#  CLASS MODEL
# ─────────────────────────────────────────────────────────────

class GradeModel:

    # key: (student_id, course_id, hoc_ky)
    # value: {diem_gk, diem_ck, tong_ket, xep_loai}
    _cache: dict[tuple, dict] = copy.deepcopy(DEMO_GRADES)

    # ─────────────────────────────────────────────
    #  READ
    # ─────────────────────────────────────────────

    @classmethod
    def get_by_course_ky(cls, course_id: int, hoc_ky: str) -> list[dict]:
        """
        Lấy danh sách điểm của TẤT CẢ sinh viên trong 1 học phần + kỳ.
        Dùng cho màn hình Nhập điểm.

        Trả về:
            list[dict], mỗi dict gồm:
              id, mssv, ho_ten, lop   ← thông tin SV
              diem_gk, diem_ck, tong_ket, xep_loai  ← điểm (0.0 nếu chưa có)
        """
        try:
            return ApiClient.get("/grades", params={
                "course_id": course_id,
                "hoc_ky":    hoc_ky,
            })
        except Exception:
            # Lấy tất cả SV đang học và ghép điểm vào
            students = [s for s in DEMO_STUDENTS if s["trang_thai"] == "Đang học"]
            result = []
            for sv in students:
                key = (sv["id"], course_id, hoc_ky)
                grade = cls._cache.get(key, {
                    "diem_gk":  0.0,
                    "diem_ck":  0.0,
                    "tong_ket": 0.0,
                    "xep_loai": "",
                })
                result.append({
                    "id":      sv["id"],
                    "mssv":    sv["mssv"],
                    "ho_ten":  sv["ho_ten"],
                    "lop":     sv["lop"],
                    **grade,
                })
            return result

    @classmethod
    def tinh_gpa(cls, student_id: int) -> float:
        """
        Tính GPA tích lũy (thang 4) của 1 sinh viên.
        Lấy tất cả điểm → quy đổi sang 4 → tính trung bình có trọng số (tín chỉ).

        Trả về:
            float — GPA tích lũy, làm tròn 2 chữ số
        """
        try:
            result = ApiClient.get(f"/students/{student_id}/gpa")
            return result.get("gpa", 0.0)
        except Exception:
            from models.demo_data import DEMO_COURSES
            course_map = {c["id"]: c for c in DEMO_COURSES}

            total_weighted = 0.0
            total_credits  = 0

            for (sv_id, course_id, hoc_ky), grade in cls._cache.items():
                if sv_id != student_id:
                    continue
                course = course_map.get(course_id)
                if course is None:
                    continue
                tin_chi     = course["tin_chi"]
                gpa_mon     = quy_doi_sang_gpa4(grade["tong_ket"])
                total_weighted += gpa_mon * tin_chi
                total_credits  += tin_chi

            if total_credits == 0:
                return 0.0
            return round(total_weighted / total_credits, 2)

    # ─────────────────────────────────────────────
    #  CREATE / UPDATE (upsert)
    # ─────────────────────────────────────────────

    @classmethod
    def bulk_save(cls, course_id: int, hoc_ky: str, rows: list[dict]) -> None:
        """
        Lưu điểm hàng loạt cho 1 học phần trong 1 kỳ.
        Dùng UPSERT: nếu đã có thì UPDATE, chưa có thì INSERT.

        rows: list[dict], mỗi dict cần:
            sv_id     : int
            mssv      : str  (để debug)
            diem_gk   : float
            diem_ck   : float
            tong_ket  : float  (đã tính sẵn ở View)
            xep_loai  : str   (đã tính sẵn ở View)
        """
        try:
            ApiClient.post("/grades/bulk", {
                "course_id": course_id,
                "hoc_ky":    hoc_ky,
                "grades":    rows,
            })
        except Exception:
            # Lưu vào cache offline
            for row in rows:
                sv_id = row.get("sv_id")
                if sv_id is None:
                    continue
                key = (sv_id, course_id, hoc_ky)
                cls._cache[key] = {
                    "diem_gk":  row.get("diem_gk",  0.0),
                    "diem_ck":  row.get("diem_ck",  0.0),
                    "tong_ket": row.get("tong_ket", 0.0),
                    "xep_loai": row.get("xep_loai", ""),
                }

    @classmethod
    def upsert_one(cls, student_id: int, course_id: int,
                   hoc_ky: str, diem_gk: float, diem_ck: float) -> dict:
        """
        Lưu điểm 1 sinh viên.
        Tính tong_ket và xep_loai tự động.

        Trả về dict điểm đã lưu.
        """
        tong_ket = tinh_tong_ket(diem_gk, diem_ck)
        xep_loai = xep_loai_diem(tong_ket)

        data = {
            "student_id": student_id,
            "course_id":  course_id,
            "hoc_ky":     hoc_ky,
            "diem_gk":    diem_gk,
            "diem_ck":    diem_ck,
            "tong_ket":   tong_ket,
            "xep_loai":   xep_loai,
        }

        try:
            return ApiClient.post("/grades/upsert", data)
        except Exception:
            key = (student_id, course_id, hoc_ky)
            cls._cache[key] = {
                "diem_gk":  diem_gk,
                "diem_ck":  diem_ck,
                "tong_ket": tong_ket,
                "xep_loai": xep_loai,
            }
            return data
