from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("mssv", "ma_hp", "hoc_ky", name="uq_enrollment"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    mssv = Column(String(20), ForeignKey("students.mssv", ondelete="CASCADE"), nullable=False)
    ma_hp = Column(String(20), ForeignKey("courses.ma_hp", ondelete="CASCADE"), nullable=False)
    hoc_ky = Column(String(20), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
