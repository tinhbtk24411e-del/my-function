"""Module giao dien PyQt6 — Giai phuong trinh bac 1.

Tai UI tu file Qt Designer (ui_mainwindow.ui), ap dung stylesheet (style.qss),
quan ly signal-slot, highlight loi nhap lieu, phim tat, Light/Dark mode,
va xuat lich su ra file .txt / .csv.
"""

import os
import sys
from fractions import Fraction

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
)
from PyQt6.uic import loadUi

from solver import (
    giai_pt_bac_1,
    MOT_NGHIEM,
    VO_NGHIEM,
    VO_SO_NGHIEM,
    tinh_goc_nghieng,
    giao_diem_truc,
)
from steps import tao_loi_giai
from validators import doc_so, dinh_dang_so, dinh_dang_pt
from history import doc_lich_su, luu_lich_su, them_muc, xuat_txt, xuat_csv


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_UI_FILE = os.path.join(_BASE_DIR, "ui_mainwindow.ui")
_QSS_LIGHT = os.path.join(_BASE_DIR, "style.qss")
_ICONS_DIR = os.path.join(_BASE_DIR, "icons")


class MainWindow(QMainWindow):
    """Cua so chinh cua ung dung Giai phuong trinh bac 1."""

    def __init__(self) -> None:
        super().__init__()
        self._dark_mode: bool = False
        self.lich_su: list[str] = doc_lich_su()

        # Tai UI tu file Qt Designer
        loadUi(_UI_FILE, self)

        # Ap dung stylesheet
        self._apply_style(False)

        # Ket noi signal-slot cho nut bam
        self.btnSolve.clicked.connect(self.on_giai)
        self.btnClear.clicked.connect(self.on_xoa)
        self.btnClearHistory.clicked.connect(self.on_xoa_lich_su)
        self.btnExport.clicked.connect(self.on_xuat_lich_su)
        self.btnTheme.clicked.connect(self.on_toggle_theme)

        # Ket noi signal-slot cho menu
        self.actionExport.triggered.connect(self.on_xuat_lich_su)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.on_about)

        # Phim tat: Enter -> Giai, Esc -> Xoa
        solve_shortcut = QShortcut(QKeySequence("Return"), self)
        solve_shortcut.activated.connect(self.on_giai)
        clear_shortcut = QShortcut(QKeySequence("Escape"), self)
        clear_shortcut.activated.connect(self.on_xoa)

        # Hien thi lich su da luu
        self._hien_lich_su()

        # Status bar
        self.statusBar().showMessage("San sang — Nhap he so va nhan Giai")

    # ------------------------------------------------------------------
    #  Stylesheet & Theme
    # ------------------------------------------------------------------

    def _apply_style(self, dark: bool) -> None:
        """Ap dung stylesheet sang hoac toi.

        Args:
            dark: True de ap dung dark mode.
        """
        if dark:
            self._ap_dung_qss_inline_dark()
        else:
            self._ap_dung_qss_file()

    def _ap_dung_qss_file(self) -> None:
        """Tai va ap dung file QSS (light mode)."""
        if os.path.exists(_QSS_LIGHT):
            with open(_QSS_LIGHT, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def _ap_dung_qss_inline_dark(self) -> None:
        """Ap dung dark mode inline (khong can file rieng)."""
        dark_qss = """
        QMainWindow { background-color: #0f172a; }
        QWidget { font-family: "Segoe UI", "Roboto", sans-serif; font-size: 13px; color: #e2e8f0; }
        QLabel { background: transparent; color: #e2e8f0; }
        QLineEdit {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 10px;
            padding: 10px 14px;
            color: #f1f5f9;
            font-size: 14px;
            selection-background-color: #3b82f6;
            selection-color: #ffffff;
        }
        QLineEdit:hover { border-color: #3b82f6; background-color: #1e3a5f; }
        QLineEdit:focus { border-color: #3b82f6; border-width: 2px; }
        QLineEdit#error { border: 2px solid #ef4444; background-color: #451a1a; }
        QLineEdit#error:hover { border-color: #dc2626; }
        QPushButton {
            background-color: #3b82f6;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
        }
        QPushButton:hover { background-color: #2563eb; }
        QPushButton:pressed { background-color: #1d4ed8; }
        QPushButton:disabled { background-color: #475569; color: #64748b; }
        QPushButton#btnSolve { background-color: #10b981; font-size: 14px; }
        QPushButton#btnSolve:hover { background-color: #059669; }
        QPushButton#btnSolve:pressed { background-color: #047857; }
        QPushButton#btnClear { background-color: #f59e0b; }
        QPushButton#btnClear:hover { background-color: #d97706; }
        QPushButton#btnClear:pressed { background-color: #b45309; }
        QPushButton#btnExport { background-color: #3b82f6; }
        QPushButton#btnExport:hover { background-color: #2563eb; }
        QPushButton#btnClearHistory { background-color: #ef4444; font-size: 12px; padding: 6px 14px; }
        QPushButton#btnClearHistory:hover { background-color: #dc2626; }
        QPushButton#btnTheme {
            background-color: #334155;
            color: #e2e8f0;
            border-radius: 20px;
            font-size: 18px;
            padding: 6px;
            border: 2px solid #475569;
        }
        QPushButton#btnTheme:hover { background-color: #475569; }
        QFrame#frameResult {
            background-color: #1e3a5f;
            border: 2px solid #3b82f6;
            border-radius: 12px;
        }
        QLabel#lblResult {
            font-size: 20px;
            font-weight: 700;
            color: #60a5fa;
        }
        QLabel#lblResultTitle { color: #60a5fa; }
        QLabel#lblSubtitle { color: #94a3b8; }
        QLabel#lblEquation { color: #60a5fa; background-color: #1e3a5f; }
        QTextBrowser {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 10px;
            padding: 10px;
            color: #cbd5e1;
        }
        QListWidget {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 10px;
            padding: 6px;
            color: #cbd5e1;
        }
        QListWidget::item { padding: 8px 10px; border-radius: 6px; border-bottom: 1px solid #334155; }
        QListWidget::item:hover { background-color: #1e3a5f; }
        QListWidget::item:selected { background-color: #3b82f6; color: #ffffff; }
        QScrollBar:vertical {
            background-color: #1e293b;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #475569;
            border-radius: 5px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover { background-color: #64748b; }
        QFrame#frameInput {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 12px;
        }
        QMenuBar {
            background-color: #1e293b;
            color: #e2e8f0;
            border-bottom: 1px solid #334155;
        }
        QMenuBar::item:selected { background-color: #334155; }
        QMenu {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
        }
        QMenu::item:selected { background-color: #3b82f6; color: #ffffff; }
        QMenu::separator { background-color: #334155; }
        QStatusBar {
            background-color: #1e293b;
            color: #94a3b8;
            border-top: 1px solid #334155;
        }
        QMessageBox { background-color: #1e293b; }
        QMessageBox QLabel { color: #e2e8f0; }
        """
        self.setStyleSheet(dark_qss)

    def on_toggle_theme(self) -> None:
        """Chuyen doi giua Light va Dark mode."""
        self._dark_mode = not self._dark_mode
        self._apply_style(self._dark_mode)
        self.btnTheme.setText("☀️" if self._dark_mode else "🌙")

    # ------------------------------------------------------------------
    #  Highlight loi nhap lieu
    # ------------------------------------------------------------------

    def _highlight_error(self, line_edit, enable: bool) -> None:
        """Dat hoac bo highlight do cho QLineEdit.

        Args:
            line_edit: Widget QLineEdit can highlight.
            enable: True de bat highlight do, False de tat.
        """
        if enable:
            line_edit.setObjectName("error")
        else:
            line_edit.setObjectName("")
        line_edit.style().unpolish(line_edit)
        line_edit.style().polish(line_edit)

    def _xoa_highlight(self) -> None:
        """Xoa highlight loi khoi tat ca o nhap."""
        for widget in (self.txtA, self.txtB):
            self._highlight_error(widget, False)

    # ------------------------------------------------------------------
    #  Giai phuong trinh
    # ------------------------------------------------------------------

    def on_giai(self) -> None:
        """Xu ly su kien nhan nut Giai."""
        self._xoa_highlight()

        # Doc va validate dau vao
        try:
            a = doc_so(self.txtA.text(), "a")
        except ValueError as exc:
            self._highlight_error(self.txtA, True)
            self._show_warning("Lỗi Nhập Liệu", str(exc))
            return

        try:
            b = doc_so(self.txtB.text(), "b")
        except ValueError as exc:
            self._highlight_error(self.txtB, True)
            self._show_warning("Lỗi Nhập Liệu", str(exc))
            return

        # Giai phuong trinh ax + b = 0
        loai, x = giai_pt_bac_1(a, b)

        if loai == VO_NGHIEM:
            kq = "Phương trình vô nghiệm"
            self.lblResult.setStyleSheet("color: #ef4444; font-size: 20px; font-weight: 700;")
        elif loai == VO_SO_NGHIEM:
            kq = "Phương trình có vô số nghiệm (x ∈ ℝ)"
            self.lblResult.setStyleSheet("color: #f59e0b; font-size: 20px; font-weight: 700;")
        else:
            kq = f"x = {dinh_dang_so(x)}"
            self.lblResult.setStyleSheet("color: #10b981; font-size: 20px; font-weight: 700;")

        self.lblResult.setText(kq)

        # Hien thi loi giai chi tiet
        buoc = tao_loi_giai(a, b)
        self.txtSteps.setPlainText("\n".join(buoc))

        # Hien thi thong tin bo sung
        self._hien_thong_tin_bsung(a, b, loai, x)

        # Them vao lich su
        pt_str = dinh_dang_pt(a, b)
        muc = f"{pt_str}  →  {kq}"
        self.lich_su = them_muc(self.lich_su, muc)
        self._hien_lich_su()
        luu_lich_su(self.lich_su)

        self.statusBar().showMessage(f"Da giai: {pt_str}")

    def _hien_thong_tin_bsung(
        self,
        a: Fraction,
        b: Fraction,
        loai: str,
        x: Fraction,
    ) -> None:
        """Hien thi thong tin bo sung: goc nghieng, giao diem truc.

        Args:
            a: He so cua x.
            b: He so tu do.
            loai: Loai nghiem.
            x: Gia tri nghiem (neu co).
        """
        lines: list[str] = []

        if loai == MOT_NGHIEM and a != 0:
            # Duong thang y = ax + b
            goc = tinh_goc_nghieng(a)
            lines.append(
                f"Goc nghieng cua y = {dinh_dang_so(a)}x + ({dinh_dang_so(b)}) "
                f"so voi truc Ox: {goc}°"
            )

            giao_ox, giao_oy = giao_diem_truc(a, b)
            if giao_ox is not None:
                lines.append(f"Giao diem voi truc Ox: ({dinh_dang_so(giao_ox)}, 0)")
            else:
                lines.append("Duong thang song song voi truc Ox")
            lines.append(f"Giao diem voi truc Oy: (0, {dinh_dang_so(giao_oy)})")
        elif loai == VO_NGHIEM:
            lines.append("Phuong trinh vo nghiem → khong co nghiem de xac dinh duong thang.")
        elif loai == VO_SO_NGHIEM:
            lines.append("Phuong trinh co vo so nghiem → 0 = 0 (luon dung).")

        self.txtInfo.setPlainText("\n".join(lines))

    # ------------------------------------------------------------------
    #  Xoa & Lich su
    # ------------------------------------------------------------------

    def on_xoa(self) -> None:
        """Xoa tat ca o nhap va ket qua."""
        for widget in (self.txtA, self.txtB):
            widget.clear()
        self._xoa_highlight()
        self.lblResult.setText("Kết quả sẽ hiển thị ở đây")
        self.lblResult.setStyleSheet("")
        self.txtSteps.setPlainText("")
        self.txtInfo.setPlainText("")
        self.txtA.setFocus()
        self.statusBar().showMessage("Da xoa du lieu nhap")

    def on_xoa_lich_su(self) -> None:
        """Xoa toan bo lich su."""
        reply = self._show_question(
            "Xác nhận",
            "Bạn có chắc muốn xóa toàn bộ lịch sử?",
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.lich_su = []
            self._hien_lich_su()
            luu_lich_su(self.lich_su)
            self.statusBar().showMessage("Da xoa lich su")

    def _hien_lich_su(self) -> None:
        """Hien thi danh sach lich su vao QListWidget."""
        self.listHistory.clear()
        for muc in self.lich_su:
            self.listHistory.addItem(muc)

    def on_xuat_lich_su(self) -> None:
        """Mo hop thoai chon file de xuat lich su."""
        if not self.lich_su:
            self._show_info("Thông báo", "Chưa có lịch sử để xuất.")
            return

        duong_dan, loai_file = QFileDialog.getSaveFileName(
            self,
            "Xuat Lich Su",
            os.path.join(_BASE_DIR, "lich_su.txt"),
            "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)",
        )

        if duong_dan:
            if duong_dan.endswith(".csv"):
                xuat_csv(self.lich_su, duong_dan)
            else:
                xuat_txt(self.lich_su, duong_dan)
            self._show_info("Thành công", f"Đã xuất lịch sử vào:\n{duong_dan}")
            self.statusBar().showMessage(f"Da xuat: {os.path.basename(duong_dan)}")

    # ------------------------------------------------------------------
    #  Helper: MessageBox
    # ------------------------------------------------------------------

    @staticmethod
    def _show_warning(title: str, message: str) -> None:
        """Hien thi popup warning."""
        QMessageBox.warning(None, title, message)

    @staticmethod
    def _show_question(title: str, message: str):
        """Hien thi popup hoi xac nhan."""
        return QMessageBox.question(
            None,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

    @staticmethod
    def _show_info(title: str, message: str) -> None:
        """Hien thi popup thong bao."""
        QMessageBox.information(None, title, message)

    # ------------------------------------------------------------------
    #  About
    # ------------------------------------------------------------------

    def on_about(self) -> None:
        """Hien thi thong tin ve ung dung."""
        QMessageBox.about(
            self,
            "Giới thiệu",
            "Giải Phương Trình Bậc 1\n"
            "Phiên bản: 3.0\n\n"
            "Ứng dụng giải phương trình dạng ax + b = 0\n"
            "Được xây dựng bằng PyQt6 & Qt Designer.\n\n"
            "Phím tắt:\n"
            "  Enter  — Giải phương trình\n"
            "  Esc    — Xóa dữ liệu nhập\n"
            "  Ctrl+S — Xuất lịch sử\n"
            "  Ctrl+Q — Thoát ứng dụng",
        )

    # ------------------------------------------------------------------
    #  Dong ung dung
    # ------------------------------------------------------------------

    def closeEvent(self, event) -> None:
        """Lu lich su khi dong ung dung.

        Args:
            event: Su kien dong cua so.
        """
        luu_lich_su(self.lich_su)
        event.accept()


def run_app() -> None:
    """Khoi chay ung dung PyQt6."""
    app = QApplication(sys.argv)
    app.setApplicationName("Giai Phuong Trinh Bac 1")
    app.setOrganizationName("MyFunction")

    # Set application icon neu co
    icon_path = os.path.join(_ICONS_DIR, "app.svg")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
