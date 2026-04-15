from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import io
from typing import Literal

from database import get_db
from dependencies import admin_or_phongdt, all_roles
from models.student import Student
from models.grade import Grade
from models.course import Course
from models.tuition import Tuition
from utils.grade_calc import calc_tong_ket, compute_transcript_stats
from utils.excel import export_students, export_grades, export_debts

router = APIRouter(prefix="/baocao", tags=["Reports"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(all_roles)):
    tong_sv = db.query(func.count(Student.mssv)).scalar()
    dang_hoc = db.query(func.count(Student.mssv)).filter(Student.trang_thai == "Đang học").scalar()
    canh_bao_hv = db.query(func.count(Student.mssv)).filter(Student.trang_thai == "Cảnh báo").scalar()

    # Outstanding tuition: tổng (phai_nop - da_nop) where da_nop < phai_nop
    tuitions = db.query(Tuition).all()
    no_hoc_phi = sum(
        max(t.phai_nop - t.da_nop, 0)
        for t in tuitions
        if t.phai_nop > t.da_nop
    )

    # Recent alerts: students with warning status
    warned = (
        db.query(Student)
        .filter(Student.trang_thai == "Cảnh báo")
        .limit(6)
        .all()
    )
    alerts = [{"ho_ten": sv.ho_ten, "mo_ta": "Cảnh báo học vụ"} for sv in warned]

    return {
        "tong_sv": tong_sv,
        "dang_hoc": dang_hoc,
        "canh_bao_hv": canh_bao_hv,
        "no_hoc_phi": no_hoc_phi,
        "alerts": alerts,
    }


@router.get("/thongke")
def statistics(db: Session = Depends(get_db), _=Depends(admin_or_phongdt)):
    khoa_list = db.query(Student.khoa).distinct().all()
    result = []
    for (khoa,) in khoa_list:
        if not khoa:
            continue
        students = db.query(Student).filter(Student.khoa == khoa).all()
        tong_sv = len(students)
        dang_hoc = sum(1 for sv in students if sv.trang_thai == "Đang học")
        canh_bao_hv = sum(1 for sv in students if sv.trang_thai == "Cảnh báo")

        # GPA trung bình của sinh viên trong khoa
        gpas = []
        for sv in students:
            grades = db.query(Grade, Course.so_tin_chi).join(
                Course, Grade.ma_hp == Course.ma_hp
            ).filter(Grade.mssv == sv.mssv).all()
            raw = [{"so_tin_chi": tc, "diem_gk": g.diem_gk, "diem_ck": g.diem_ck} for g, tc in grades]
            stats = compute_transcript_stats(raw)
            if stats["tin_chi_dang_ky"] > 0:
                gpas.append(stats["gpa_tich_luy"])

        gpa_tb = round(sum(gpas) / len(gpas), 2) if gpas else 0.0

        # Ti le dat: tỷ lệ môn đạt / tổng môn
        all_grades = db.query(Grade, Course.so_tin_chi).join(
            Course, Grade.ma_hp == Course.ma_hp
        ).filter(Grade.mssv.in_([sv.mssv for sv in students])).all()
        total_subjects = len(all_grades)
        passed = sum(
            1 for g, tc in all_grades
            if calc_tong_ket(g.diem_gk, g.diem_ck) is not None
            and calc_tong_ket(g.diem_gk, g.diem_ck) >= 5.0
        )
        ti_le_dat = round(passed / total_subjects * 100, 1) if total_subjects > 0 else 0.0

        result.append({
            "khoa": khoa,
            "tong_sv": tong_sv,
            "dang_hoc": dang_hoc,
            "gpa_tb": gpa_tb,
            "ti_le_dat": ti_le_dat,
            "canh_bao_hv": canh_bao_hv,
        })
    return result


@router.get("/export/excel")
def export_excel(
    loai: Literal["sinhvien", "bangdiem", "conno"] = Query(...),
    db: Session = Depends(get_db),
    _=Depends(admin_or_phongdt),
):
    if loai == "sinhvien":
        students = db.query(Student).all()
        data = [
            {c.name: getattr(sv, c.name) for c in sv.__table__.columns}
            for sv in students
        ]
        for d in data:
            d["ngay_sinh"] = str(d["ngay_sinh"]) if d.get("ngay_sinh") else None
            d["gpa"] = None
        file_bytes = export_students(data)
        filename = "danh_sach_sinh_vien.xlsx"

    elif loai == "bangdiem":
        rows = db.query(Grade, Course, Student).join(
            Course, Grade.ma_hp == Course.ma_hp
        ).join(Student, Grade.mssv == Student.mssv).all()
        data = []
        for g, c, sv in rows:
            tong = calc_tong_ket(g.diem_gk, g.diem_ck)
            data.append({
                "mssv": g.mssv, "ho_ten": sv.ho_ten,
                "ma_hp": g.ma_hp, "ten_hp": c.ten_hp,
                "so_tin_chi": c.so_tin_chi, "hoc_ky": g.hoc_ky,
                "diem_gk": g.diem_gk, "diem_ck": g.diem_ck,
                "tong_ket": tong,
                "ket_qua": ("Đạt" if tong >= 5.0 else "Rớt") if tong is not None else None,
            })
        file_bytes = export_grades(data)
        filename = "bang_diem.xlsx"

    else:  # conno
        rows = db.query(Tuition, Student).join(Student, Tuition.mssv == Student.mssv).filter(
            Tuition.da_nop < Tuition.phai_nop
        ).all()
        data = [{
            "mssv": t.mssv, "ho_ten": sv.ho_ten,
            "phai_nop": t.phai_nop, "da_nop": t.da_nop,
            "han_nop": str(t.han_nop) if t.han_nop else None,
            "trang_thai": "Quá hạn" if t.han_nop and t.han_nop < date.today() else "Chưa nộp",
        } for t, sv in rows]
        file_bytes = export_debts(data)
        filename = "con_no_hoc_phi.xlsx"

    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
