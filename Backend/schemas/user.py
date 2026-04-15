from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    phongdt = "phongdt"
    giaovien = "giaovien"


class UserOut(BaseModel):
    id: int
    username: str
    ho_ten: str
    role: RoleEnum
    email: Optional[str] = None

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user: UserOut


class ChangePasswordRequest(BaseModel):
    mat_khau_cu: str
    mat_khau_moi: str
