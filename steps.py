"""Module sinh loi giai tung buoc.

Tao danh sach cac dong mo ta qua trinh giai phuong trinh ax + b = 0,
bao gom ca cac buoc bien doi trung gian va ket luan cuoi cung.
"""

from fractions import Fraction

from solver import giai_pt_bac_1, VO_NGHIEM, VO_SO_NGHIEM
from validators import dinh_dang_so, dinh_dang_pt


def tao_loi_giai(a: Fraction, b: Fraction) -> list[str]:
    """Tra ve danh sach cac dong loi giai cho phuong trinh ax + b = 0.

    Args:
        a: He so cua x.
        b: He so tu do.

    Returns:
        Danh sach chuoi, moi chuoi la mot buoc giai.
    """
    pt_str = dinh_dang_pt(a, b)

    buoc: list[str] = [
        f"Phuong trinh: {pt_str}",
    ]

    loai, x = giai_pt_bac_1(a, b)

    if loai == VO_NGHIEM:
        buoc.append(
            f"Buoc 1: He so a = {dinh_dang_so(a)} = 0, he so b = {dinh_dang_so(b)} ≠ 0"
        )
        buoc.append(
            f"Buoc 2: Phuong trinh co dang 0.x + ({dinh_dang_so(b)}) = 0 → {dinh_dang_so(b)} = 0 (ma tran)"
        )
        buoc.append("Ket luan: Phuong trinh VO NGHIEM")
    elif loai == VO_SO_NGHIEM:
        buoc.append(
            f"Buoc 1: He so a = {dinh_dang_so(a)} = 0, he so b = {dinh_dang_so(b)} = 0"
        )
        buoc.append(
            f"Buoc 2: Phuong trinh co dang 0.x + 0 = 0 → 0 = 0 (dung moi luon)"
        )
        buoc.append("Ket luan: Phuong trinh co VO SO NGHIEM (x ∈ R)")
    else:
        buoc.append(f"Buoc 1: Chuyen vế → ax = -b")
        buoc.append(
            f"       {dinh_dang_so(a)}.x = -({dinh_dang_so(b)})"
        )
        buoc.append(
            f"Buoc 2: Chia hai ve cho a → x = -b / a"
        )
        buoc.append(
            f"       x = -({dinh_dang_so(b)}) / {dinh_dang_so(a)}"
        )
        buoc.append(f"       x = {dinh_dang_so(x)}")
        buoc.append(f"Ket luan: x = {dinh_dang_so(x)}")

    return buoc
