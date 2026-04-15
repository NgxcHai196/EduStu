from pydantic import BaseModel, field_validator
from typing import Optional


class GradeCreate(BaseModel):
    mssv: str
    ma_hp: str
    hoc_ky: str
    diem_gk: Optional[float] = None
    diem_ck: Optional[float] = None

    @field_validator("diem_gk", "diem_ck")
    @classmethod
    def validate_score(cls, v):
        if v is not None and not (0.0 <= v <= 10.0):
            raise ValueError("Điểm phải từ 0 đến 10")
        return v


class GradeUpdate(BaseModel):
    diem_gk: Optional[float] = None
    diem_ck: Optional[float] = None

    @field_validator("diem_gk", "diem_ck")
    @classmethod
    def validate_score(cls, v):
        if v is not None and not (0.0 <= v <= 10.0):
            raise ValueError("Điểm phải từ 0 đến 10")
        return v


class GradeOut(BaseModel):
    id: int
    mssv: str
    ma_hp: str
    ten_hp: str
    so_tin_chi: int
    hoc_ky: str
    diem_gk: Optional[float] = None
    diem_ck: Optional[float] = None
    tong_ket: Optional[float] = None
    dat: Optional[bool] = None
    ket_qua: Optional[str] = None

    model_config = {"from_attributes": True}


class TranscriptOut(BaseModel):
    diem_list: list[GradeOut]
    hoc_ky: str
    gpa_tich_luy: float
    gpa_ky: float
    xep_loai: str
    canh_bao: str
    tin_chi_dat: int
    tin_chi_dang_ky: int
