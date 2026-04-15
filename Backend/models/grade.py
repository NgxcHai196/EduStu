from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = (
        UniqueConstraint("mssv", "ma_hp", "hoc_ky", name="uq_grade"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    mssv = Column(String(20), ForeignKey("students.mssv", ondelete="CASCADE"), nullable=False)
    ma_hp = Column(String(20), ForeignKey("courses.ma_hp", ondelete="CASCADE"), nullable=False)
    hoc_ky = Column(String(20), nullable=False)
    diem_gk = Column(Float, nullable=True)
    diem_ck = Column(Float, nullable=True)

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
