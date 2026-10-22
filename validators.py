"""Module kiem tra & dinh dang du lieu nhap.

Cung cap cac ham:
    - doc_so: doc chuoi nguoi dung thanh Fraction (ho tro phan so, thap phan).
    - dinh_dang_so: dinh dang Fraction thanh chuoi hien thi dep.
    - dinh_dang_pt: dinh dang phuong trinh ax + b = 0 thanh chuoi.
"""

from fractions import Fraction
from typing import Optional


def doc_so(
    raw: str,
    ten: str = "he so",
    mac_dinh: Optional[Fraction] = None,
) -> Fraction:
    """Doc chuoi dau vao cua nguoi dung va chuyen thanh Fraction.

    Ho tro cac dinh dang:
        - So nguyen: "3", "-7"
        - Thap phan dau cham: "3.14"
        - Thap phan dau phay: "1,5"  ->  Fraction(3, 2)
        - Phan so: "3/4"

    Args:
        raw: Chuoi nhap tu nguoi dung.
        ten: Ten he so de hien thi trong thong bao loi.
        mac_dinh: Gia tri mac dinh neu chuoi rong. Neu None thi bao loi.

    Returns:
        Fraction tuong ung.

    Raises:
        ValueError: Neu chuoi khong hop le va khong co gia tri mac dinh.
    """
    text = raw.strip()
    if text == "":
        if mac_dinh is not None:
            return mac_dinh
        raise ValueError(f"He so '{ten}' khong duoc de trong.")

    # Xu ly phan so "3/4"
    if "/" in text:
        parts = text.split("/", 1)
        try:
            tu = float(parts[0].strip().replace(",", "."))
            mau = float(parts[1].strip().replace(",", "."))
            if mau == 0:
                raise ValueError(f"Mau so khong duoc bang 0 trong '{raw}'.")
            return Fraction(tu) / Fraction(mau)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"He so '{ten}' khong hop le: '{raw}'.") from exc

    # Xu ly dau phay thap phan "1,5" -> "1.5"
    text = text.replace(",", ".")
    try:
        return Fraction(text)
    except ValueError as exc:
        raise ValueError(f"He so '{ten}' khong hop le: '{raw}'.") from exc


def dinh_dang_so(val: Fraction) -> str:
    """Dinh dang Fraction thanh chuoi hien thi.

    - Neu la so nguyen: tra ve dang nguyen "3".
    - Neu la phan so uu han ngan: tra ve dang thap phan "0.25".
    - Neu la phan so vo han: tra ve dang "1/3 ≈ 0.3333".

    Args:
        val: Fraction can dinh dang.

    Returns:
        Chuoi da dinh dang.
    """
    if val.denominator == 1:
        return str(val.numerator)

    # Kiem tra xem phan so co bieu dien duoc duoi dang thap phan uu han ngan
    decimal = float(val)
    rounded = round(decimal, 10)
    if Fraction(rounded) == val:
        return str(rounded)

    return f"{val.numerator}/{val.denominator} ≈ {round(float(val), 4)}"


def dinh_dang_pt(a: Fraction, b: Fraction) -> str:
    """Dinh dang phuong trinh ax + b = 0 thanh chuoi dep.

    Args:
        a: He so cua x.
        b: He so tu do.

    Returns:
        Chuoi phuong trinh, vi du: "3x + 2 = 0".
    """
    parts: list[str] = []

    # He so a (x)
    if a != 0:
        abs_a = abs(a)
        coeff = dinh_dang_so(abs_a) if abs_a != 1 else ""
        if a < 0:
            parts.append(f"-{coeff}x")
        else:
            parts.append(f"{coeff}x")

    # He so b
    if b != 0:
        abs_b = abs(b)
        val_b = dinh_dang_so(abs_b)
        if b < 0:
            if parts:
                parts.append(f"- {val_b}")
            else:
                parts.append(f"-{val_b}")
        else:
            if parts:
                parts.append(f"+ {val_b}")
            else:
                parts.append(val_b)

    left = " ".join(parts) if parts else "0"
    return f"{left} = 0"
