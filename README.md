# Giải Phương Trình Bậc 1

Ứng dụng GUI giải phương trình bậc 1 dạng **ax + b = 0**, được xây dựng bằng **PyQt6** & **Qt Designer** với giao diện Modern Flat Design.

## Tính năng

- **Giải phương trình** dạng `ax + b = 0` với độ chính xác tuyệt đối (sử dụng `Fraction`)
- **Lời giải chi tiết** từng bước được hiển thị rõ ràng
- **Thông tin bổ sung**: góc nghiêng đường thẳng `y = ax + b`, giao điểm với trục Ox và Oy
- **Lịch sử** tự động lưu vào `history.json`, giữ tối đa 50 mục
- **Xuất lịch sử** ra file `.txt` hoặc `.csv`
- **Chế độ Sáng / Tối** (Light / Dark Mode)
- **Phím tắt**: Enter → Giải, Esc → Xóa, Ctrl+S → Xuất, Ctrl+Q → Thoát
- **Highlight đỏ** ô nhập khi dữ liệu không hợp lệ
- **Hỗ trợ** nhập số nguyên, thập phân (dấu chấm / dấu phẩy), và phân số

## Cấu trúc file

```
my-function/
├── main.py              # Entry point — khởi chạy ứng dụng
├── gui.py               # Module giao diện PyQt6 chính
├── solver.py            # Logic giải phương trình (Fraction chính xác tuyệt đối)
├── validators.py        # Đọc và định dạng số từ đầu vào người dùng
├── steps.py             # Sinh lời giải chi tiết từng bước
├── history.py           # Quản lý lịch sử (lưu JSON, xuất TXT / CSV)
├── ui_mainwindow.ui     # File Qt Designer — bố cục giao diện chính
├── style.qss            # Stylesheet light mode — Modern Flat Design
├── history.json         # File lưu lịch sử tự động
├── icons/               # Thư mục icon SVG
│   ├── app.svg          # Icon ứng dụng
│   ├── solve.svg        # Icon giải
│   ├── clear.svg        # Icon xóa
│   ├── export.svg       # Icon xuất
│   ├── history.svg      # Icon lịch sử
│   ├── theme.svg        # Icon chuyển theme
│   └── trash.svg        # Icon xóa lịch sử
└── README.md            # Tài liệu này
```

## Cách khởi chạy

### Yêu cầu

- Python 3.9+
- PyQt6

```bash
pip install PyQt6
```

### Chạy ứng dụng

```bash
python main.py
```

### Trong PyCharm

Mở `main.py` và nhấn nút **Run** (▶), hoặc tạo Run Configuration với script path trỏ đến `main.py`.

## Phím tắt

| Phím | Chức năng |
|------|-----------|
| `Enter` | Giải phương trình |
| `Esc` | Xóa dữ liệu nập |
| `Ctrl+S` | Xuất lịch sử |
| `Ctrl+Q` | Thoát ứng dụng |

## Thiết kế

- **Bảng màu**: Royal Blue (`#2563eb`), Emerald Green (`#10b981`), Amber (`#f59e0b`), Red (`#ef4444`)
- **Phong cách**: Modern Flat Design — bo góc 10px, hiệu ứng `:hover` / `:pressed` / `:disabled`
- **Font**: Segoe UI / Roboto
- **Dark Mode**: stylesheet inline, chuyển đổi tức thì không cần file riêng

## Công thức

Phương trình bậc 1: **ax + b = 0**

| Trường hợp | Kết quả |
|------------|---------|
| `a ≠ 0` | **x = −b / a** (một nghiệm) |
| `a = 0`, `b ≠ 0` | **Vô nghiệm** |
| `a = 0`, `b = 0` | **Vô số nghiệm** (x ∈ ℝ) |

### Thông tin bổ sung

Khi phương trình có một nghiệm (`a ≠ 0`), ứng dụng tính thêm:

- **Góc nghiêng** của đường thẳng `y = ax + b` so với trục Ox: `α = arctan(a)` (độ)
- **Giao điểm với trục Ox**: `(−b/a, 0)`
- **Giao điểm với trục Oy**: `(0, b)`

## Đóng góp

| Thành viên | Phần trăm đóng góp | Nhiệm vụ |
|------------|-------------------|----------|
| Tình | 14.28% | `main.py` — Entry point, khởi chạy ứng dụng |
| Vy | 14.28% | `gui.py` — Module giao diện PyQt6 chính |
| Tiên | 14.28% | `solver.py` — Logic giải phương trình bậc 1 |
| Hùng | 14.29% | `validators.py` — Đọc và định dạng số từ đầu vào |
| Vân Anh | 14.29% | `steps.py` — Sinh lời giải chi tiết từng bước |
| Trúc Giang | 14.29% | `history.py` — Quản lý lịch sử (lưu JSON, xuất TXT/CSV) |
| Ngọc Trâm | 14.29% | `style.qss`, `ui_mainwindow.ui`, `icons/` — Giao diện và stylesheet |
