"""
tuition_model.py
================
Model học phí — ghi nhận thanh toán, theo dõi công nợ.

Bảng MySQL: tuitions
  id, student_id, hoc_ky, so_tien, da_nop,
  ngay_nop, trang_thai, ghi_chu, created_at

Trạng thái:
  "Đã đóng"    — da_nop >= so_tien
  "Đóng thiếu" — 0 < da_nop < so_tien
  "Chưa đóng"  — da_nop == 0

QUY TẮC MODEL:
  - Không import từ views/ hoặc controllers/
  - Logic tính trạng thái nằm ở Model, không nằm ở View
"""

import copy
from utils.api_client import ApiClient
from models.demo_data import DEMO_TUITION


class TuitionModel:

    _cache: list[dict] = copy.deepcopy(DEMO_TUITION)

    # ─────────────────────────────────────────────
    #  HELPER TÍNH TRẠNG THÁI
    # ─────────────────────────────────────────────

    @staticmethod
    def _calc_trang_thai(so_tien: float, da_nop: float) -> str:
        """Tính trạng thái từ số tiền — logic nghiệp vụ."""
        if da_nop >= so_tien:  return "Đã đóng"
        if da_nop > 0:         return "Đóng thiếu"
        return "Chưa đóng"

    # ─────────────────────────────────────────────
    #  READ
    # ─────────────────────────────────────────────

    @classmethod
    def get_all(cls, trang_thai: str = "") -> list[dict]:
        """
        Lấy tất cả bản ghi học phí.
        Nếu truyền trang_thai → lọc theo trạng thái đó.

        Trả về list[dict] — mỗi dict gồm:
            id, student_id, mssv, ho_ten,
            hoc_ky, so_tien, da_nop, ngay_nop, trang_thai, ghi_chu
        """
        try:
            params = {}
            if trang_thai:
                params["trang_thai"] = trang_thai
            return ApiClient.get("/tuition", params=params)
        except Exception:
            result = cls._cache
            if trang_thai:
                result = [t for t in result if t["trang_thai"] == trang_thai]
            return copy.deepcopy(result)

    @classmethod
    def get_by_student(cls, student_id: int) -> list[dict]:
        """
        Lấy lịch sử học phí của 1 sinh viên (tất cả kỳ).
        """
        try:
            return ApiClient.get("/tuition", params={"student_id": student_id})
        except Exception:
            return copy.deepcopy([
                t for t in cls._cache if t["student_id"] == student_id
            ])

    @classmethod
    def get_debtors(cls) -> list[dict]:
        """
        Lấy danh sách SV chưa đóng đủ học phí (công nợ).
        Bao gồm cả "Đóng thiếu" lẫn "Chưa đóng".
        """
        try:
            return ApiClient.get("/tuition/debtors")
        except Exception:
            return copy.deepcopy([
                t for t in cls._cache if t["trang_thai"] != "Đã đóng"
            ])

    # ─────────────────────────────────────────────
    #  WRITE
    # ─────────────────────────────────────────────

    @classmethod
    def pay(cls,
            student_id: int,
            mssv:       str,
            ho_ten:     str,
            hoc_ky:     str,
            so_tien_nop: float,
            ngay_nop:   str,
            ghi_chu:    str = "") -> dict:
        """
        Ghi nhận thanh toán học phí.

        - Nếu đã có bản ghi → cộng thêm vào da_nop
        - Nếu chưa có bản ghi → tạo mới với so_tien mặc định
        - Tự động cập nhật trang_thai theo số tiền

        Trả về dict bản ghi sau khi cập nhật.
        """
        try:
            return ApiClient.post("/tuition/pay", {
                "student_id":  student_id,
                "hoc_ky":      hoc_ky,
                "so_tien":     so_tien_nop,
                "ngay_nop":    ngay_nop,
                "ghi_chu":     ghi_chu,
            })
        except Exception:
            # Tìm bản ghi hiện có
            record = next(
                (t for t in cls._cache
                 if t["student_id"] == student_id and t["hoc_ky"] == hoc_ky),
                None
            )

            if record:
                # Cộng thêm
                record["da_nop"] = min(
                    record["da_nop"] + so_tien_nop,
                    record["so_tien"]
                )
                record["ngay_nop"] = ngay_nop
                record["ghi_chu"]  = ghi_chu
                record["trang_thai"] = cls._calc_trang_thai(
                    record["so_tien"], record["da_nop"]
                )
                return copy.deepcopy(record)
            else:
                # Tạo bản ghi mới
                so_tien_ky = 8_500_000   # mức học phí mặc định
                new_record = {
                    "id":         len(cls._cache) + 1,
                    "student_id": student_id,
                    "mssv":       mssv,
                    "ho_ten":     ho_ten,
                    "hoc_ky":     hoc_ky,
                    "so_tien":    so_tien_ky,
                    "da_nop":     min(so_tien_nop, so_tien_ky),
                    "ngay_nop":   ngay_nop,
                    "trang_thai": cls._calc_trang_thai(so_tien_ky, so_tien_nop),
                    "ghi_chu":    ghi_chu,
                }
                cls._cache.append(new_record)
                return copy.deepcopy(new_record)

    # ─────────────────────────────────────────────
    #  THỐNG KÊ
    # ─────────────────────────────────────────────

    @classmethod
    def tinh_tong_thu(cls, hoc_ky: str = "") -> dict:
        """
        Thống kê tổng thu học phí theo kỳ.

        Trả về:
            {
                "tong_phai_thu": float,
                "tong_da_thu":   float,
                "tong_con_lai":  float,
                "so_sv_no":      int,
            }
        """
        data = cls.get_all()
        if hoc_ky:
            data = [t for t in data if t["hoc_ky"] == hoc_ky]

        tong_phai_thu = sum(t["so_tien"] for t in data)
        tong_da_thu   = sum(t["da_nop"]  for t in data)
        so_sv_no      = sum(1 for t in data if t["trang_thai"] != "Đã đóng")

        return {
            "tong_phai_thu": tong_phai_thu,
            "tong_da_thu":   tong_da_thu,
            "tong_con_lai":  tong_phai_thu - tong_da_thu,
            "so_sv_no":      so_sv_no,
        }
