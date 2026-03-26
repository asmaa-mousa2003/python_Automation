"""
وحدة التصور: إنشاء وحفظ الرسوم البيانية
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from typing import Optional
import pandas as pd
from pip._internal.utils import logging

# إعدادات الخطوط للعربية
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

logger = logging.getLogger(__name__)


class ChartGenerator:
    """مسؤول عن إنشاء وحفظ الرسوم البيانية"""

    def __init__(self, output_dir: Path, config: dict):
        self.output_dir = output_dir
        self.config = config

    def bar_by_region(self, data: pd.DataFrame, filename: str = 'sales_by_region.png') -> str:
        """رسم بار للمبيعات حسب المنطقة"""
        plt.figure(figsize=self.config['figsize_region'])
        plt.bar(data.index, data['Total_Sales'], color=self.config['colors']['region'])
        plt.title('Total Sales by Region', fontsize=14, fontweight='bold')
        plt.xlabel('Region')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()

        path = self.output_dir / filename
        plt.savefig(path, dpi=self.config['dpi'], bbox_inches='tight')
        plt.close()
        logger.info(f"✅ تم حفظ: {filename}")
        return str(path)

    def barh_by_product(self, data: pd.DataFrame, filename: str = 'sales_by_product.png') -> str:
        """رسم بار أفقي للمبيعات حسب المنتج"""
        plt.figure(figsize=self.config['figsize_product'])
        plt.barh(data.index, data['Total_Sales'], color=self.config['colors']['product'])
        plt.title('Total Sales by Product', fontsize=14, fontweight='bold')
        plt.xlabel('Total Sales ($)')
        plt.ylabel('Product')
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()

        path = self.output_dir / filename
        plt.savefig(path, dpi=self.config['dpi'], bbox_inches='tight')
        plt.close()
        logger.info(f"✅ تم حفظ: {filename}")
        return str(path)

    def line_trend(self, data: pd.DataFrame, filename: str = 'sales_trend.png') -> str:
        """رسم خطي لاتجاه المبيعات"""
        plt.figure(figsize=self.config['figsize_trend'])
        plt.plot(data['Date'], data['Total_Sales'], color=self.config['colors']['trend'],
                 linewidth=2, marker='o', markersize=4)
        plt.title('Daily Sales Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Total Sales ($)')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        plt.tight_layout()

        path = self.output_dir / filename
        plt.savefig(path, dpi=self.config['dpi'], bbox_inches='tight')
        plt.close()
        logger.info(f"✅ تم حفظ: {filename}")
        return str(path)