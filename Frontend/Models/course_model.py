"""
course_model.py
===============
Model học phần — thêm, sửa, xóa, lấy danh sách.

Mỗi dict khớp cột bảng MySQL: courses
  id, ma_hp, ten_hp, tin_chi, hoc_ky, giang_vien, is_active

QUY TẮC MODEL:
  - Không import từ views/ hoặc controllers/
  - Không hiển thị UI
  - _cache hoạt động như bảng MySQL tạm khi offline
"""

import copy
from utils.api_client import ApiClient
from models.demo_data import DEMO_COURSES


class CourseModel:

    _cache: list[dict] = copy.deepcopy(DEMO_COURSES)

    # ─────────────────────────────────────────────
    #  READ
    # ─────────────────────────────────────────────

    @classmethod
    def get_all(cls, hoc_ky: str = "") -> list[dict]:
        """
        Lấy tất cả học phần.
        Nếu truyền hoc_ky → lọc theo học kỳ đó.
        """
        try:
            params = {"hoc_ky": hoc_ky} if hoc_ky else {}
            return ApiClient.get("/courses", params=params)
        except Exception:
            result = cls._cache
            if hoc_ky:
                result = [c for c in result if c["hoc_ky"] == hoc_ky]
            return copy.deepcopy(result)

    @classmethod
    def get_by_id(cls, course_id: int) -> dict:
        """
        Lấy 1 học phần theo id.

        Raise:
            ValueError: không tìm thấy
        """
        try:
            return ApiClient.get(f"/courses/{course_id}")
        except Exception:
            c = next((x for x in cls._cache if x["id"] == course_id), None)
            if c is None:
                raise ValueError(f"Không tìm thấy học phần id = {course_id}")
            return copy.deepcopy(c)

    # ─────────────────────────────────────────────
    #  CREATE
    # ─────────────────────────────────────────────

    @classmethod
    def create(cls, data: dict) -> dict:
        """
        Thêm học phần mới.
        data cần có: ma_hp, ten_hp, tin_chi

        Raise:
            ValueError: mã HP đã tồn tại
        """
        try:
            return ApiClient.post("/courses", data)
        except Exception:
            if any(c["ma_hp"] == data["ma_hp"] for c in cls._cache):
                raise ValueError(f"Mã học phần '{data['ma_hp']}' đã tồn tại!")

            new_id = max((c["id"] for c in cls._cache), default=0) + 1
            new_record = {
                "id":          new_id,
                "ma_hp":       data.get("ma_hp", ""),
                "ten_hp":      data.get("ten_hp", ""),
                "tin_chi":     data.get("tin_chi", 3),
                "hoc_ky":      data.get("hoc_ky", ""),
                "giang_vien":  data.get("giang_vien", ""),
                "is_active":   1,
            }
            cls._cache.append(new_record)
            return copy.deepcopy(new_record)

    # ─────────────────────────────────────────────
    #  UPDATE
    # ─────────────────────────────────────────────

    @classmethod
    def update(cls, course_id: int, data: dict) -> dict:
        """
        Cập nhật học phần (partial update).

        Raise:
            ValueError: không tìm thấy
        """
        try:
            return ApiClient.put(f"/courses/{course_id}", data)
        except Exception:
            c = next((x for x in cls._cache if x["id"] == course_id), None)
            if c is None:
                raise ValueError(f"Không tìm thấy học phần id = {course_id}")
            c.update(data)
            return copy.deepcopy(c)

    # ─────────────────────────────────────────────
    #  DELETE
    # ─────────────────────────────────────────────

    @classmethod
    def delete(cls, course_id: int) -> None:
        """
        Xóa học phần khỏi database.
        (Khác với sinh viên — học phần xóa vật lý, không xóa mềm)

        Raise:
            ValueError: không tìm thấy
        """
        try:
            ApiClient.delete(f"/courses/{course_id}")
        except Exception:
            before = len(cls._cache)
            cls._cache = [c for c in cls._cache if c["id"] != course_id]
            if len(cls._cache) == before:
                raise ValueError(f"Không tìm thấy học phần id = {course_id}")
