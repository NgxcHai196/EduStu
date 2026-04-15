from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from dependencies import admin_or_phongdt, all_roles
from models.course import Course
from models.enrollment import Enrollment
from schemas.course import CourseCreate, CourseUpdate, CourseOut, EnrollmentCreate, EnrollmentOut

router = APIRouter(tags=["Courses"])


# ── Courses ──────────────────────────────────────────────────────────────────

@router.get("/hocphan", response_model=list[CourseOut])
def list_courses(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(all_roles),
):
    q = db.query(Course)
    if search:
        q = q.filter(
            Course.ma_hp.ilike(f"%{search}%") | Course.ten_hp.ilike(f"%{search}%")
        )
    return q.all()


@router.post("/hocphan", response_model=CourseOut, status_code=201)
def create_course(body: CourseCreate, db: Session = Depends(get_db), _=Depends(admin_or_phongdt)):
    if db.query(Course).filter(Course.ma_hp == body.ma_hp).first():
        raise HTTPException(status_code=400, detail="Mã học phần đã tồn tại")
    course = Course(**body.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.put("/hocphan/{ma_hp}", response_model=CourseOut)
def update_course(
    ma_hp: str, body: CourseUpdate, db: Session = Depends(get_db), _=Depends(admin_or_phongdt)
):
    course = db.query(Course).filter(Course.ma_hp == ma_hp).first()
    if not course:
        raise HTTPException(status_code=404, detail="Không tìm thấy học phần")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@router.delete("/hocphan/{ma_hp}")
def delete_course(ma_hp: str, db: Session = Depends(get_db), _=Depends(admin_or_phongdt)):
    course = db.query(Course).filter(Course.ma_hp == ma_hp).first()
    if not course:
        raise HTTPException(status_code=404, detail="Không tìm thấy học phần")
    db.delete(course)
    db.commit()
    return {"message": f"Đã xóa học phần {ma_hp}"}


# ── Enrollments ───────────────────────────────────────────────────────────────

@router.get("/dangky/{mssv}", response_model=list[EnrollmentOut])
def get_enrollments(
    mssv: str,
    hoc_ky: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(all_roles),
):
    q = db.query(Enrollment, Course.ten_hp).join(Course, Enrollment.ma_hp == Course.ma_hp).filter(
        Enrollment.mssv == mssv
    )
    if hoc_ky:
        q = q.filter(Enrollment.hoc_ky == hoc_ky)
    results = []
    for enrollment, ten_hp in q.all():
        results.append({
            "id": enrollment.id,
            "mssv": enrollment.mssv,
            "ma_hp": enrollment.ma_hp,
            "ten_hp": ten_hp,
            "hoc_ky": enrollment.hoc_ky,
        })
    return results


@router.post("/dangky", response_model=EnrollmentOut, status_code=201)
def create_enrollment(body: EnrollmentCreate, db: Session = Depends(get_db), _=Depends(admin_or_phongdt)):
    existing = db.query(Enrollment).filter(
        Enrollment.mssv == body.mssv,
        Enrollment.ma_hp == body.ma_hp,
        Enrollment.hoc_ky == body.hoc_ky,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Sinh viên đã đăng ký học phần này")
    course = db.query(Course).filter(Course.ma_hp == body.ma_hp).first()
    if not course:
        raise HTTPException(status_code=404, detail="Không tìm thấy học phần")
    enrollment = Enrollment(**body.model_dump())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return {
        "id": enrollment.id,
        "mssv": enrollment.mssv,
        "ma_hp": enrollment.ma_hp,
        "ten_hp": course.ten_hp,
        "hoc_ky": enrollment.hoc_ky,
    }


@router.delete("/dangky/{enrollment_id}")
def cancel_enrollment(enrollment_id: int, db: Session = Depends(get_db), _=Depends(admin_or_phongdt)):
    e = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Không tìm thấy đăng ký")
    db.delete(e)
    db.commit()
    return {"message": "Đã hủy đăng ký"}
