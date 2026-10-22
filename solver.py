"""Module giai phuong trinh bac 1.

Giai phuong trinh dang: ax + b = 0

Su dung Fraction de dam bao do chinh xac tuyet doi, khong bi loi lam tron
so thuc phy dong.
"""

from fractions import Fraction
from math import atan, degrees
from typing import Literal, Optional, Tuple


# --- Hang so bieu thi loai nghiem ---
MOT_NGHIEM: Literal["mot_nghiem"] = "mot_nghiem"
VO_NGHIEM: Literal["vo_nghiem"] = "vo_nghiem"
VO_SO_NGHIEM: Literal["vo_so_nghiem"] = "vo_so_nghiem"

NguyenLoai = Literal["mot_nghiem", "vo_nghiem", "vo_so_nghiem"]


def giai_pt_bac_1(a: Fraction, b: Fraction) -> Tuple[NguyenLoai, Fraction]:
    """Giai phuong trinh ax + b = 0.

    Args:
        a: He so cua x.
        b: He so tu do.

    Returns:
        Bo doi (loai_nghiem, gia_tri_x).
        - Khi co 1 nghiem: gia_tri_x = -b / a.
        - Khi vo nghiem hoac vo so nghiem: gia_tri_x = Fraction(0).
    """
    if a == 0:
        if b == 0:
            return VO_SO_NGHIEM, Fraction(0)
        else:
            return VO_NGHIEM, Fraction(0)
    else:
        x = -b / a
        return MOT_NGHIEM, x


def tinh_goc_nghieng(a: Fraction) -> float:
    """Tinh goc nghieng duong thang y = ax + b so voi truc hoanh (do).

    Args:
        a: He so goc (slope) cua duong thang.

    Returns:
        Goc nghieng tinh bang do, lam tron 2 chu so thap phan.
    """
    radian = atan(float(a))
    return round(degrees(radian), 2)


def giao_diem_truc(
    a: Fraction, b: Fraction
) -> Tuple[Optional[Fraction], Fraction]:
    """Xac dinh giao diem duong thang y = ax + b voi cac toa do.

    Args:
        a: He so goc.
        b: Tung do goc.

    Returns:
        (giao_diem_Ox, giao_diem_Oy)
        - giao_diem_Ox: hoanh do giao diem voi truc Ox (y=0),
          hoac None neu song song.
        - giao_diem_Oy: tung do giao diem voi truc Oy (x=0), luon bang b.
    """
    if a == 0:
        giao_ox: Optional[Fraction] = None  # song song voi Ox
    else:
        giao_ox = -b / a
    giao_oy: Fraction = b
    return giao_ox, giao_oy
