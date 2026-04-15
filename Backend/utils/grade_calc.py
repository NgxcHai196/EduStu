"""Business logic for GPA and grade calculations."""

TRONG_SO_GK = 0.3
TRONG_SO_CK = 0.7


def calc_tong_ket(diem_gk: float | None, diem_ck: float | None) -> float | None:
    if diem_gk is None or diem_ck is None:
        return None
    return round(diem_gk * TRONG_SO_GK + diem_ck * TRONG_SO_CK, 2)


def is_passed(tong_ket: float | None) -> bool | None:
    if tong_ket is None:
        return None
    return tong_ket >= 5.0


def xep_loai(gpa: float) -> str:
    if gpa >= 8.5:
        return "Xuất sắc"
    elif gpa >= 7.0:
        return "Giỏi"
    elif gpa >= 5.5:
        return "Khá"
    elif gpa >= 4.0:
        return "Trung bình"
    else:
        return "Yếu"


def canh_bao(gpa: float) -> str:
    if gpa < 0.8:
        return "Lần 2"
    elif gpa < 1.0:
        return "Lần 1"
    return ""


def compute_transcript_stats(grades: list[dict]) -> dict:
    """
    grades: list of dicts with keys: so_tin_chi, diem_gk, diem_ck
    Returns dict with: gpa_ky, gpa_tich_luy, tin_chi_dat, tin_chi_dang_ky, xep_loai, canh_bao
    """
    tin_chi_dang_ky = 0
    tin_chi_dat = 0
    weighted_sum = 0.0

    for g in grades:
        tc = g.get("so_tin_chi", 0) or 0
        tong_ket = calc_tong_ket(g.get("diem_gk"), g.get("diem_ck"))
        tin_chi_dang_ky += tc
        if tong_ket is not None:
            weighted_sum += tong_ket * tc
            if tong_ket >= 5.0:
                tin_chi_dat += tc

    gpa = round(weighted_sum / tin_chi_dang_ky, 2) if tin_chi_dang_ky > 0 else 0.0

    return {
        "gpa_ky": gpa,
        "gpa_tich_luy": gpa,
        "tin_chi_dat": tin_chi_dat,
        "tin_chi_dang_ky": tin_chi_dang_ky,
        "xep_loai": xep_loai(gpa),
        "canh_bao": canh_bao(gpa),
    }
