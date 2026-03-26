# test_imports.py
try:
    from config.settings import INPUT_FILE
    from core.loader import DataLoader
    print("✅ جميع الـ Imports شغالة بنجاح!")
    print(f"📂 مسار البيانات المتوقع: {INPUT_FILE}")
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")