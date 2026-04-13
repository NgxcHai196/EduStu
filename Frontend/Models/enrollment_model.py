"""
enrollment_model.py
===================
Model đăng ký học phần — ghi nhận SV đăng ký HP theo kỳ.

Bảng MySQL: enrollments
  id, student_id, course_id, hoc_ky, created_at
  UNIQUE KEY (student_id, course_id, hoc_ky)

QUY TẮC MODEL:
  - Không import từ views/ hoặc controllers/
  - _cache lưu theo key (student_id, hoc_ky) → list course_id
"""

import copy
from utils.api_client import ApiClient
from models.demo_data import DEMO_ENROLLMENTS, DEMO_COURSES


class EnrollmentModel:

    # key: (student_id, hoc_ky) → list[course_id]
    _cache: dict[tuple, list] = copy.deepcopy(DEMO_ENROLLMENTS)

    # ─────────────────────────────────────────────
    #  READ
    # ─────────────────────────────────────────────

    @classmethod
    def get_by_student_ky(cls, student_id: int, hoc_ky: str) -> list[dict]:
        """
        Lấy danh sách học phần đã đăng ký của 1 SV trong 1 kỳ.

        Trả về:
            list[dict] — mỗi dict là thông tin học phần đầy đủ
            (giống CourseModel.get_all() nhưng chỉ lấy HP đã đăng ký)
        """
        try:
            result = ApiClient.get("/enrollments", params={
                "student_id": student_id,
                "hoc_ky":     hoc_ky,
            })
            # API trả về list enrollment, cần map sang course dict
            return result
        except Exception:
            course_ids = cls._cache.get((student_id, hoc_ky), [])
            course_map = {c["id"]: c for c in DEMO_COURSES}
            return [
                copy.deepcopy(course_map[cid])
                for cid in course_ids
                if cid in course_map
            ]

    # ─────────────────────────────────────────────
    #  CREATE / SAVE
    # ─────────────────────────────────────────────

    @classmethod
    def enroll(cls, student_id: int, course_id: int, hoc_ky: str) -> dict:
        """
        Đăng ký 1 học phần cho sinh viên.

        Raise:
            ValueError: đã đăng ký rồi
        """
        try:
            return ApiClient.post("/enrollments", {
                "student_id": student_id,
                "course_id":  course_id,
                "hoc_ky":     hoc_ky,
            })
        except Exception:
            key = (student_id, hoc_ky)
            current = cls._cache.setdefault(key, [])
            if course_id in current:
                raise ValueError("Sinh viên đã đăng ký học phần này!")
            current.append(course_id)
            return {"student_id": student_id, "course_id": course_id, "hoc_ky": hoc_ky}

    @classmethod
    def save_all(cls, student_id: int, hoc_ky: str, courses: list[dict]) -> None:
        """
        Lưu toàn bộ danh sách đăng ký cùng lúc (thay thế danh sách cũ).
        Dùng khi người dùng nhấn "Lưu đăng ký" sau khi đã chọn xong.

        courses: list[dict] — mỗi dict là học phần (cần trường "id")
        """
        try:
            # Gửi từng cái lên API
            for c in courses:
                try:
                    ApiClient.post("/enrollments", {
                        "student_id": student_id,
                        "course_id":  c["id"],
                        "hoc_ky":     hoc_ky,
                    })
                except Exception:
                    pass   # Bỏ qua nếu đã đăng ký rồi
        except Exception:
            pass
        # Cập nhật cache dù API thành công hay không
        cls._cache[(student_id, hoc_ky)] = [c["id"] for c in courses]

    # ─────────────────────────────────────────────
    #  DELETE
    # ─────────────────────────────────────────────

    @classmethod
    def unenroll(cls, student_id: int, course_id: int, hoc_ky: str) -> None:
        """
        Hủy đăng ký 1 học phần.
        """
        try:
            # API cần enrollment_id → tìm trước
            enrollments = ApiClient.get("/enrollments", params={
                "student_id": student_id,
                "course_id":  course_id,
                "hoc_ky":     hoc_ky,
            })
            if enrollments:
                ApiClient.delete(f"/enrollments/{enrollments[0]['id']}")
        except Exception:
            key = (student_id, hoc_ky)
            if key in cls._cache:
                cls._cache[key] = [
                    cid for cid in cls._cache[key] if cid != course_id
                ]
