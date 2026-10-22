"""Module quan ly lich su giai phuong trinh.

Lu / doc / xoa lich su duoi dang file JSON, dong thoi ho tro
xuat lich su ra file .txt hoac .csv.
"""

import csv
import json
import os
from datetime import datetime
from typing import Optional

FILE_MAC_DINH = "history.json"


def doc_lich_su(duong_dan: str = FILE_MAC_DINH) -> list[str]:
    """Doc lich su tu file JSON.

    Args:
        duong_dan: Duong dan den file JSON.

    Returns:
        Danh sach cac muc lich su. Neu file khong ton tai hoac loi, tra ve [].
    """
    if not os.path.exists(duong_dan):
        return []
    try:
        with open(duong_dan, "r", encoding="utf-8") as f:
            du_lieu = json.load(f)
        return du_lieu if isinstance(du_lieu, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def luu_lich_su(ds: list[str], duong_dan: str = FILE_MAC_DINH) -> None:
    """Lu danh sach lich su vao file JSON.

    Args:
        ds: Danh sach cac muc lich su.
        duong_dan: Duong dan den file JSON.
    """
    with open(duong_dan, "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=2)


def them_muc(ds: list[str], muc: str, toi_da: int = 50) -> list[str]:
    """Them muc moi len dau danh sach, giu toi da `toi_da` muc.

    Args:
        ds: Danh sach lich su hien tai.
        muc: Muc moi can them.
        toi_da: So muc toi da.

    Returns:
        Danh sach da cap nhat.
    """
    # Them timestamp vao muc
    timestamp = datetime.now().strftime("%H:%M:%S")
    muc_voi_thoi_gian = f"[{timestamp}] {muc}"
    return ([muc_voi_thoi_gian] + ds)[:toi_da]


def xuat_txt(ds: list[str], duong_dan: str) -> None:
    """Xuat lich su ra file .txt, moi mot dong.

    Args:
        ds: Danh sach cac muc lich su.
        duong_dan: Duong dan file .txt dich.
    """
    with open(duong_dan, "w", encoding="utf-8") as f:
        f.write("Lich su giai phuong trinh bac 1\n")
        f.write("=" * 40 + "\n\n")
        for i, muc in enumerate(ds, 1):
            f.write(f"{i}. {muc}\n")


def xuat_csv(ds: list[str], duong_dan: str) -> None:
    """Xuat lich su ra file .csv voi hai cot: STT va Chi tiet.

    Args:
        ds: Danh sach cac muc lich su.
        duong_dan: Duong dan file .csv dich.
    """
    with open(duong_dan, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["STT", "Chi tiet"])
        for i, muc in enumerate(ds, 1):
            writer.writerow([i, muc])
