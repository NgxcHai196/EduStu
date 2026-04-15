from sqlalchemy import Column, Integer, String, Enum
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    ho_ten = Column(String(100), nullable=False)
    role = Column(Enum("admin", "phongdt", "giaovien"), nullable=False)
    email = Column(String(100), nullable=True)
