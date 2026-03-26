"""
وحدة تحميل البيانات: قراءة، تنظيف، وتحقق
"""
import pandas as pd
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """مسؤول عن تحميل وتنظيف بيانات المبيعات"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df: Optional[pd.DataFrame] = None

    def load(self) -> 'DataLoader':  # 👈 التعديل 1: نرجع self مش df
        """قراءة ملف الإكسل"""
        logger.info(f"📂 جاري القراءة من: {self.filepath}")
        self.df = pd.read_excel(self.filepath)
        logger.info(f"✅ تم قراءة {len(self.df)} صف")
        return self  # 👈 نرجع الكائن نفسه عشان نكمل السلسلة

    def clean(self, required_cols: List[str]) -> pd.DataFrame:  # 👈 التعديل 2: نرجع الـ df في النهاية
        """تنظيف البيانات: حذف الفارغ، تحويل الأنواع"""
        if self.df is None:
            raise ValueError("يجب تحميل البيانات أولاً باستخدام load()")

        original_count = len(self.df)
        logger.info(f"📊 قبل التنظيف: {original_count} صف")

        # حذف الصفوف ذات القيم المفقودة في الأعمدة الحرجة
        self.df = self.df.dropna(subset=required_cols)

        # تحويل الأنواع مع معالجة الأخطاء
        numeric_cols = ['Sales', 'Total']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')

        # حذف أي صفوف أصبحت فارغة بعد التحويل
        self.df = self.df.dropna(subset=numeric_cols)

        cleaned_count = len(self.df)
        logger.info(f"✅ بعد التنظيف: {cleaned_count} صف (تم حذف {original_count - cleaned_count})")

        return self.df  # 👈 نرجع الـ DataFrame النظيف في النهاية

    def get_summary(self) -> dict:
        """ملخص سريع عن البيانات"""
        if self.df is None:
            return {}

        return {
            'rows': len(self.df),
            'columns': list(self.df.columns),
            'date_range': (
                self.df['Date'].min().date() if 'Date' in self.df.columns else None,
                self.df['Date'].max().date() if 'Date' in self.df.columns else None
            ),
            'total_revenue': self.df['Total'].sum() if 'Total' in self.df.columns else 0
        }