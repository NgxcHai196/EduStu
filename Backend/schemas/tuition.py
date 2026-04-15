from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum


class PhuongThucEnum(str, Enum):
    tien_mat = "Tiền mặt"
    chuyen_khoan = "Chuyển khoản"
    the = "Thẻ"
    momo = "MoMo"


class TuitionOut(BaseModel):
    mssv: str
    ho_ten: str
    phai_nop: float
    da_nop: float
    han_nop: Optional[str] = None
    trang_thai: str
    ghi_chu: Optional[str] = None

    model_config = {"from_attributes": True}


class PaymentRequest(BaseModel):
    mssv: str
    so_tien: float
    phuong_thuc: PhuongThucEnum
    ghi_chu: Optional[str] = None

    @field_validator("so_tien")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        if v > 100_000_000:
            raise ValueError("Số tiền không được vượt quá 100,000,000")
        return v


class PaymentResponse(BaseModel):
    message: str
    trang_thai_moi: str
