"""
dashboard_model.py
==================
Model Dashboard — tổng hợp thống kê từ nhiều bảng.

Không có bảng riêng trong MySQL.
Dữ liệu được tính từ: students, courses, grades, tuitions.

QUY TẮC MODEL:
  - Không import từ views/ hoặc controllers/
  - Được phép import các Model khác để tổng hợp số liệu
"""

from utils.api_client import ApiClient
from models.demo_data import DEMO_STUDENTS, DEMO_COURSES, DEMO_GRADES


class DashboardModel:

    @staticmethod
    def get_stats() -> dict:
        """
        Lấy 4 chỉ số thống kê cho stat cards trên Dashboard.

        Trả về:
            {
                "total_students": int,   — SV đang học
                "active_courses": int,   — HP đang mở
                "avg_gpa":        float, — GPA trung bình toàn trường
                "debtors":        int,   — SV nợ học phí
            }
        """
        try:
            return ApiClient.get("/dashboard/stats")
        except Exception:
            from models.grade_model import quy_doi_sang_gpa4
            from models.tuition_model import TuitionModel

            # Đếm SV đang học
            total_sv = sum(
                1 for s in DEMO_STUDENTS
                if s["trang_thai"] == "Đang học"
            )

            # Đếm HP đang mở
            active_hp = sum(1 for c in DEMO_COURSES if c["is_active"])

            # Tính GPA trung bình
            all_tonget = [g["tong_ket"] for g in DEMO_GRADES.values()]
            avg_gpa = 0.0
            if all_tonget:
                avg_gpa = round(
                    sum(quy_doi_sang_gpa4(d) for d in all_tonget) / len(all_tonget),
                    2
                )

            # Đếm SV nợ học phí
            debtors = len(TuitionModel.get_debtors())

            return {
                "total_students": total_sv,
                "active_courses": active_hp,
                "avg_gpa":        avg_gpa,
                "debtors":        debtors,
            }

    @staticmethod
    def get_warnings() -> list[dict]:
        """
        Lấy danh sách SV bị cảnh báo học vụ (GPA < 1.0).

        Trả về:
            list[dict], mỗi dict gồm:
                mssv, ho_ten, lop, gpa, ly_do, muc_do
        """
        try:
            return ApiClient.get("/dashboard/warnings")
        except Exception:
            from models.grade_model import GradeModel
            results = []
            for sv in DEMO_STUDENTS:
                if sv["trang_thai"] != "Đang học":
                    continue
                gpa = GradeModel.tinh_gpa(sv["id"])
                if gpa < 1.0:
                    results.append({
                        "mssv":    sv["mssv"],
                        "ho_ten":  sv["ho_ten"],
                        "lop":     sv["lop"],
                        "hoc_ky":  "HK1-2024-2025",
                        "gpa":     gpa,
                        "ly_do":   "GPA < 1.0",
                        "muc_do":  "Nghiêm trọng",
                    })
            return results

    @staticmethod
    def get_recent_students(limit: int = 5) -> list[dict]:
        """
        Lấy danh sách SV mới nhập học gần đây nhất.
        Dùng cho widget "Sinh viên gần đây" trên Dashboard.
        """
        try:
            return ApiClient.get("/students", params={
                "sort":  "created_at",
                "order": "desc",
                "limit": limit,
            })
        except Exception:
            # Lấy n sinh viên cuối trong cache (id lớn nhất = mới nhất)
            sorted_sv = sorted(DEMO_STUDENTS, key=lambda s: s["id"], reverse=True)
            return sorted_sv[:limit]
