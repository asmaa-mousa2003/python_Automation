
import pandas as pd
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class ReportExporter:
    """مسؤول عن تصدير النتائج بصيغ متعددة"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def to_excel(self, dataframes: Dict[str, pd.DataFrame], filename: str = 'Full_Analysis.xlsx') -> str:
        """حفظ عدة جداول في ملف إكسل واحد (شيتات متعددة)"""
        path = self.output_dir / filename

        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            for sheet_name, df in dataframes.items():
                clean_name = sheet_name[:31].replace('/', '-')
                df.to_excel(writer, sheet_name=clean_name, index=True)

        logger.info(f"✅ تم حفظ إكسل: {filename}")
        return str(path)

    def to_pdf_simple(self, kpis: dict, top_regions: pd.DataFrame,
                      filename: str = 'Sales_Report.pdf') -> Optional[str]:
        """إنشاء تقرير PDF بسيط (يتطلب reportlab)"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet

            path = self.output_dir / filename
            doc = SimpleDocTemplate(str(path), pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # العنوان
            elements.append(Paragraph("📊 Sales Analysis Report", styles['Heading1']))
            elements.append(Spacer(1, 15))

            # مؤشرات الأداء
            summary = f"""
            <b>📈 Key Metrics:</b><br/>
            • Total Revenue: ${kpis.get('total_revenue', 0):,.2f}<br/>
            • Avg Order Value: ${kpis.get('avg_order_value', 0):,.2f}<br/>
            • Total Orders: {kpis.get('total_orders', 0)}<br/>
            • Top Region: {kpis.get('top_region', 'N/A')}<br/>
            • Top Product: {kpis.get('top_product', 'N/A')}
            """
            elements.append(Paragraph(summary, styles['Normal']))
            elements.append(Spacer(1, 20))

            # جدول المناطق ✅ التصحيح: استخدام أسماء الأعمدة المسطحة
            if not top_regions.empty:
                elements.append(Paragraph("🌍 Top Regions", styles['Heading2']))
                table_data = [['Region', 'Total Sales', 'Avg Sale', 'Orders']]
                for idx, row in top_regions.head(5).iterrows():
                    table_data.append([
                        idx,
                        f"${row['Total_Sales']:,.2f}",      # ✅ مش ('Total', 'sum')
                        f"${row['Avg_Sale']:,.2f}",         # ✅ مش ('Total', 'mean')
                        int(row['Orders_Count'])            # ✅ مش ('Total', 'count')
                    ])

                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ]))
                elements.append(table)

            doc.build(elements)
            logger.info(f"✅ تم حفظ PDF: {filename}")
            return str(path)

        except ImportError:
            logger.warning("⚠️ reportlab غير مثبت. تخطي إنشاء PDF.")
            return None