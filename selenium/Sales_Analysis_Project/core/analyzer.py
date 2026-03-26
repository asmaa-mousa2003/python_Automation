"""
وحدة التحليل: تجميع، إحصائيات، واستخلاص رؤى
"""
import pandas as pd
from typing import Dict, Optional


class SalesAnalyzer:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def by_region(self, ascending: bool = False) -> pd.DataFrame:
        """تحليل المبيعات حسب المنطقة (أعمدة مسطحة)"""
        result = self.df.groupby('Region').agg(
            Total_Sales=('Total', 'sum'),
            Avg_Sale=('Total', 'mean'),
            Orders_Count=('Total', 'count'),
            Avg_Item_Price=('Sales', 'mean')
        ).round(2)

        return result.sort_values('Total_Sales', ascending=ascending)

    def by_product(self, top_n: Optional[int] = None) -> pd.DataFrame:
        """تحليل المبيعات حسب المنتج (أعمدة مسطحة)"""
        # ✅ التصحيح: استخدام named aggregation مباشرة
        if 'Quantity' in self.df.columns:
            result = self.df.groupby('Product').agg(
                Total_Sales=('Total', 'sum'),
                Avg_Sale=('Sales', 'mean'),
                Total_Quantity=('Quantity', 'sum')
            ).round(2)
        else:
            result = self.df.groupby('Product').agg(
                Total_Sales=('Total', 'sum'),
                Avg_Sale=('Sales', 'mean')
            ).round(2)

        result = result.sort_values('Total_Sales', ascending=False)
        return result.head(top_n) if top_n else result

    def by_date(self, freq: str = 'D') -> pd.DataFrame:
        """تحليل الاتجاه الزمني للمبيعات"""
        if 'Date' not in self.df.columns:
            return pd.DataFrame()

        result = self.df.set_index('Date').resample(freq)['Total'].sum().reset_index()
        result.columns = ['Date', 'Total_Sales']
        return result

    def get_kpis(self) -> Dict[str, float]:
        """استخراج مؤشرات الأداء الرئيسية"""
        return {
            'total_revenue': self.df['Total'].sum(),
            'avg_order_value': self.df['Sales'].mean(),
            'total_orders': len(self.df),
            'top_region': self.df.groupby('Region')['Total'].sum().idxmax(),
            'top_product': self.df.groupby('Product')['Total'].sum().idxmax()
        }