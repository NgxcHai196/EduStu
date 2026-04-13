"""
student_model.py
================
Model sinh viên — thêm, sửa, xóa mềm, tìm kiếm, lấy bảng điểm.

Chiến lược demo:
  - _cache là danh sách hoạt động như bảng MySQL tạm thời
  - Khi backend bật → gọi API thật, bỏ qua _cache
  - Khi backend chưa bật → đọc/ghi vào _cache
  - GPA tính từ bảng grades → trường "gpa" được inject
    bởi GradeModel.tinh_gpa() trước khi trả về View

QUY TẮC MODEL:
  - Không import từ views/ hoặc controllers/
  - Không raise chuỗi tiếng Anh raw — luôn wrap thành ValueError tiếng Việt
  - _cache là list of dict, mỗi dict khớp cột bảng MySQL students
"""

import copy
from utils.api_client import ApiClient
from models.demo_data import DEMO_STUDENTS


class StudentModel:

    # Bản sao độc lập để tránh sửa demo gốc
    _cache: list[dict] = copy.deepcopy(DEMO_STUDENTS)

    # ─────────────────────────────────────────────
    #  READ
    # ─────────────────────────────────────────────

    @classmethod
    def get_all(cls,
                keyword:    str = "",
                lop:        str = "",
                trang_thai: str = "") -> list[dict]:
        """
        Lấy danh sách sinh viên, có thể lọc theo:
          - keyword  : tìm trong MSSV hoặc Họ tên (không phân biệt hoa thường)
          - lop      : tên lớp chính xác
          - trang_thai: "Đang học" | "Thôi học" | "Tốt nghiệp" | "Bảo lưu"

        Trả về list[dict] — mỗi dict là 1 hàng bảng students.
        GPA được GradeModel tính thêm vào sau (xem GradeModel.inject_gpa).
        """
        try:
            # Gọi API thật
            params = {}
            if keyword:    params["keyword"]    = keyword
            if lop:        params["lop"]        = lop
            if trang_thai: params["trang_thai"] = trang_thai
            return ApiClient.get("/students", params=params)

        except Exception:
            # Lọc trong cache (offline)
            result = cls._cache
            if keyword:
                kw = keyword.lower()
                result = [
                    s for s in result
                    if kw in s["mssv"].lower()
                    or kw in s["ho_ten"].lower()
                ]
            if lop:
                result = [s for s in result if s["lop"] == lop]
            if trang_thai:
                result = [s for s in result if s["trang_thai"] == trang_thai]
            return copy.deepcopy(result)

    @classmethod
    def get_by_id(cls, student_id: int) -> dict:
        """
        Lấy 1 sinh viên theo id.

        Raise:
            ValueError: không tìm thấy
        """
        try:
            return ApiClient.get(f"/students/{student_id}")
        except Exception:
            sv = next((s for s in cls._cache if s["id"] == student_id), None)
            if sv is None:
                raise ValueError(f"Không tìm thấy sinh viên có id = {student_id}")
            return copy.deepcopy(sv)

    @classmethod
    def get_by_mssv(cls, mssv: str) -> dict:
        """
        Lấy 1 sinh viên theo MSSV.

        Raise:
            ValueError: không tìm thấy
        """
        try:
            result = ApiClient.get("/students", params={"keyword": mssv})
            match = next((s for s in result if s["mssv"] == mssv), None)
            if match is None:
                raise ValueError(f"Không tìm thấy MSSV {mssv}")
            return match
        except ValueError:
            raise
        except Exception:
            sv = next((s for s in cls._cache if s["mssv"] == mssv), None)
            if sv is None:
                raise ValueError(f"Không tìm thấy MSSV {mssv}")
            return copy.deepcopy(sv)

    # ─────────────────────────────────────────────
    #  CREATE
    # ─────────────────────────────────────────────

    @classmethod
    def create(cls, data: dict) -> dict:
        """
        Thêm sinh viên mới.

        data cần có tối thiểu: mssv, ho_ten, trang_thai
        Các trường còn lại là tùy chọn.

        Raise:
            ValueError: MSSV đã tồn tại
        """
        try:
            return ApiClient.post("/students", data)
        except Exception:
            # Kiểm tra MSSV trùng trong cache
            if any(s["mssv"] == data["mssv"] for s in cls._cache):
                raise ValueError(f"MSSV '{data['mssv']}' đã tồn tại trong hệ thống!")

            new_id = max((s["id"] for s in cls._cache), default=0) + 1
            new_record = {
                "id":           new_id,
                "mssv":         data.get("mssv", ""),
                "ho_ten":       data.get("ho_ten", ""),
                "ngay_sinh":    data.get("ngay_sinh", ""),
                "gioi_tinh":    data.get("gioi_tinh", ""),
                "email":        data.get("email", ""),
                "sdt":          data.get("sdt", ""),
                "dia_chi":      data.get("dia_chi", ""),
                "lop":          data.get("lop", ""),
                "khoa":         data.get("khoa", ""),
                "nam_nhap_hoc": data.get("nam_nhap_hoc", None),
                "trang_thai":   data.get("trang_thai", "Đang học"),
            }
            cls._cache.append(new_record)
            return copy.deepcopy(new_record)

    # ─────────────────────────────────────────────
    #  UPDATE
    # ─────────────────────────────────────────────

    @classmethod
    def update(cls, student_id: int, data: dict) -> dict:
        """
        Cập nhật thông tin sinh viên.
        Chỉ cần truyền các trường cần thay đổi (partial update).

        Raise:
            ValueError: không tìm thấy sinh viên
        """
        try:
            return ApiClient.put(f"/students/{student_id}", data)
        except Exception:
            sv = next((s for s in cls._cache if s["id"] == student_id), None)
            if sv is None:
                raise ValueError(f"Không tìm thấy sinh viên có id = {student_id}")
            sv.update(data)
            return copy.deepcopy(sv)

    @classmethod
    def soft_delete(cls, student_id: int) -> dict:
        """
        Xóa mềm — không xóa khỏi database.
        Chỉ cập nhật trang_thai = 'Thôi học'.
        Đây là 1 dòng SQL: UPDATE students SET trang_thai='Thôi học' WHERE id=?
        """
        return cls.update(student_id, {"trang_thai": "Thôi học"})

    # ─────────────────────────────────────────────
    #  TRANSCRIPT (bảng điểm)
    # ─────────────────────────────────────────────

    @classmethod
    def get_transcript(cls, student_id: int) -> dict[str, list]:
        """
        Lấy bảng điểm toàn bộ các kỳ của 1 sinh viên.

        Trả về:
            {
                "HK1-2024-2025": [
                    {
                        "ma_hp": "CS101",
                        "ten_hp": "Nhập môn Lập trình",
                        "tin_chi": 3,
                        "diem_gk": 7.5,
                        "diem_ck": 8.0,
                        "tong_ket": 7.8,
                        "xep_loai": "Giỏi"
                    },
                    ...
                ],
                "HK2-2024-2025": [...]
            }
        """
        try:
            return ApiClient.get(f"/students/{student_id}/transcript")
        except Exception:
            # Ghép từ DEMO_GRADES + DEMO_COURSES
            from models.demo_data import DEMO_GRADES, DEMO_COURSES
            course_map = {c["id"]: c for c in DEMO_COURSES}
            result: dict[str, list] = {}

            for (sv_id, course_id, hoc_ky), grade in DEMO_GRADES.items():
                if sv_id != student_id:
                    continue
                course = course_map.get(course_id)
                if course is None:
                    continue
                row = {
                    "ma_hp":    course["ma_hp"],
                    "ten_hp":   course["ten_hp"],
                    "tin_chi":  course["tin_chi"],
                    **grade,   # diem_gk, diem_ck, tong_ket, xep_loai
                }
                result.setdefault(hoc_ky, []).append(row)

            return result
