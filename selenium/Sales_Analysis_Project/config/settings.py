
from pathlib import Path

# 🎯 الحل الصحيح: احسبي المسار بناءً على موقع ملف الإعدادات نفسه
# ملف settings.py ده موجود في: .../Sales_Analysis_Project/config/settings.py
# عشان نروح للـ root (Sales_Analysis_Project) نطلع خطوة واحدة لفوق
BASE_DIR = Path(__file__).resolve().parent.parent

print(f"🔍 BASE_DIR = {BASE_DIR}")  # 👈 سطر للتجربة، امسحيه بعدين

# مسارات البيانات
DATA_DIR = BASE_DIR / 'data'
INPUT_FILE = DATA_DIR / 'input.xlsx'

# مسارات المخرجات
REPORTS_DIR = DATA_DIR / 'reports'
IMAGES_DIR = REPORTS_DIR / 'images'

# إنشاء المجلدات تلقائياً
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# إعدادات الرسوم البيانية
CHART_CONFIG = {
    'dpi': 300,
    'figsize_region': (10, 6),
    'figsize_product': (10, 6),
    'figsize_trend': (12, 6),
    'colors': {
        'region': '#3498db',
        'product': '#2ecc71',
        'trend': '#e74c3c'
    }
}

# أعمدة البيانات الأساسية
REQUIRED_COLUMNS = ['Product', 'Sales', 'Total', 'Date', 'Region']

# 👇 أضيفي ده في آخر الملف للتجربة 👇
# if __name__ == "__main__":
#     print("\n" + "="*60)
#     print("🔍 مسار المشروع (BASE_DIR):")
#     print(f"   {BASE_DIR}")
#     print("\n📄 ملف الإدخال (INPUT_FILE):")
#     print(f"   {INPUT_FILE}")
#     print("\n📁 فولدر التقارير (REPORTS_DIR):")
#     print(f"   {REPORTS_DIR}")
#     print("\n✅ هل ملف input.xlsx موجود؟")
#     print(f"   {INPUT_FILE.exists()}")
#     print("="*60 + "\n")