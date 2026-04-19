# utils/config.py

API_BASE_URL = "http://localhost:8000"
BASE_URL = API_BASE_URL

APP_NAME = "EduStu"
APP_VERSION = "1.0.0"

DB_HOST = "localhost"
DB_NAME = "edustu" # Ten database de theo tren may
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "110252702Nhat" # Mat khau de theo tren may

# Mau sac dung trong QSS — Light theme
PRIMARY   = "#F0F4F8"   # background chinh
SECONDARY = "#FFFFFF"   # sidebar / card
ACCENT    = "#2563EB"   # blue chinh (action)
HIGHLIGHT = "#2563EB"   # brand / active
TEXT_LIGHT = "#1E293B"  # chu tren nen sang (dark text)
TEXT_MUTED = "#64748B"  # chu phu
BORDER    = "#CBD5E1"   # vien ngoai
WHITE     = "#FFFFFF"
SUCCESS   = "#10B981"
WARNING   = "#F59E0B"
DANGER    = "#EF4444"
INFO      = "#3B82F6"

# Cau hinh nghiep vu
TRONG_SO_GK = 0.4
TRONG_SO_CK = 0.6

# Du lieu co dinh
TRANG_THAI_SV = ["Dang hoc", "Thoi hoc", "Tot nghiep", "Bao luu"]
TRANG_THAI_HP = ["Da dong", "Dong thieu", "Chua dong"]
HOC_KY_LIST = ["HK1-2024-2025", "HK2-2024-2025", "HK1-2023-2024"]
KHOA_LIST = ["Cong nghe thong tin", "Kinh te", "Ngoai ngu", "Dien - Dien tu"]
GIOI_TINH = ["Nam", "Nu", "Khac"]
