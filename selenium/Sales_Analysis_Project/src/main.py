import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_dir, 'data', 'input.xlsx')
# إعدادات الرسم (عشان يدعم العربية)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


class SalesAnalyzer:
    """كلاس تحليل المبيعات المتكامل"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.reports_path = 'data/reports'

        # إنشاء فولدر التقارير لو مش موجود
        os.makedirs(self.reports_path, exist_ok=True)

    def load_and_clean(self):
        """قراءة وتنظيف البيانات"""
        print("📂 جاري قراءة الملف...")
        self.df = pd.read_excel(self.filepath)

        print(f"📊 قبل التنظيف: {len(self.df)} صف")

        # تنظيف
        self.df = self.df.dropna(subset=['Product', 'Sales', 'Total'])
        self.df['Sales'] = pd.to_numeric(self.df['Sales'], errors='coerce')
        self.df['Total'] = pd.to_numeric(self.df['Total'], errors='coerce')
        self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
        self.df['Quantity'] = pd.to_numeric(self.df['Quantity'], errors='coerce')

        print(f"✅ بعد التنظيف: {len(self.df)} صف")
        return self.df

    def filter_by_date(self, start_date, end_date):
        """فلترة البيانات حسب التاريخ"""
        mask = (self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)
        return self.df.loc[mask].copy()

    def analyze_by_region(self):
        """تحليل حسب المنطقة"""
        return self.df.groupby('Region').agg({
            'Total': 'sum',
            'Sales': 'mean',
            'Order_ID': 'count',
            'Customer_Rating': 'mean'
        }).round(2).rename(columns={
            'Total': 'Total_Sales',
            'Sales': 'Avg_Sale',
            'Order_ID': 'Orders_Count',
            'Customer_Rating': 'Avg_Rating'
        }).sort_values('Total_Sales', ascending=False)

    def analyze_by_product(self):
        """تحليل حسب المنتج"""
        return self.df.groupby('Product').agg({
            'Total': 'sum',
            'Quantity': 'sum',
            'Order_ID': 'count'
        }).round(2).rename(columns={
            'Total': 'Total_Sales',
            'Quantity': 'Total_Quantity',
            'Order_ID': 'Orders_Count'
        }).sort_values('Total_Sales', ascending=False)

    def create_charts(self):
        """إنشاء الرسوم البيانية"""
        print("\n📈 جاري إنشاء الرسوم البيانية...")

        # 1. رسم المبيعات حسب المنطقة
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        region_data = self.analyze_by_region()
        ax1.bar(region_data.index, region_data['Total_Sales'], color='#3498db')
        ax1.set_title('Total Sales by Region', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Region')
        ax1.set_ylabel('Total Sales')
        ax1.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.reports_path}/sales_by_region.png', dpi=300)
        plt.close()

        # 2. رسم المبيعات حسب المنتج
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        product_data = self.analyze_by_product()
        ax2.barh(product_data.index, product_data['Total_Sales'], color='#2ecc71')
        ax2.set_title('Total Sales by Product', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Total Sales')
        ax2.set_ylabel('Product')
        plt.tight_layout()
        plt.savefig(f'{self.reports_path}/sales_by_product.png', dpi=300)
        plt.close()

        # 3. رسم المبيعات خلال الوقت (Time Series)
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        daily_sales = self.df.groupby(self.df['Date'].dt.date)['Total'].sum()
        ax3.plot(daily_sales.index, daily_sales.values, color='#e74c3c', linewidth=2)
        ax3.set_title('Daily Sales Trend', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Total Sales')
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax3.xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.reports_path}/sales_trend.png', dpi=300)
        plt.close()

        print("✅ تم حفظ 3 رسوم بيانية")

    def export_to_pdf(self):
        """تصدير تقرير PDF"""
        print("\n📄 جاري إنشاء تقرير PDF...")

        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
            from reportlab.lib.styles import getSampleStyleSheet

            pdf_path = f'{self.reports_path}/Sales_Report.pdf'
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # العنوان
            title = Paragraph("Sales Analysis Report", styles['Heading1'])
            elements.append(title)
            elements.append(Spacer(1, 20))

            # ملخص
            summary = f"""
            <b>Total Records:</b> {len(self.df)}<br/>
            <b>Total Revenue:</b> ${self.df['Total'].sum():,.2f}<br/>
            <b>Average Sale:</b> ${self.df['Sales'].mean():,.2f}<br/>
            <b>Date Range:</b> {self.df['Date'].min().date()} to {self.df['Date'].max().date()}
            """
            elements.append(Paragraph(summary, styles['Normal']))
            elements.append(Spacer(1, 20))

            # جدول المناطق
            elements.append(Paragraph("Top Regions by Sales", styles['Heading2']))
            region_data = self.analyze_by_region().head(5).reset_index()
            region_table = Table([['Region', 'Total Sales', 'Orders']] +
                                 region_data.values.tolist())
            region_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ]))
            elements.append(region_table)
            elements.append(Spacer(1, 20))

            # جدول المنتجات
            elements.append(Paragraph("Top Products by Sales", styles['Heading2']))
            product_data = self.analyze_by_product().head(5).reset_index()
            product_table = Table([['Product', 'Total Sales', 'Quantity']] +
                                  product_data.values.tolist())
            product_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ]))
            elements.append(product_table)

            # بناء الـ PDF
            doc.build(elements)
            print(f"✅ تم حفظ تقرير PDF: {pdf_path}")

        except ImportError:
            print("⚠️ مكتبة reportlab غير مثبتة. تخطي إنشاء PDF.")

    def save_all_reports(self):
        """حفظ جميع التقارير في إكسل"""
        print("\n💾 جاري حفظ تقارير الإكسل...")

        with pd.ExcelWriter(f'{self.reports_path}/Full_Analysis.xlsx') as writer:
            self.df.to_excel(writer, sheet_name='Clean_Data', index=False)
            self.analyze_by_region().to_excel(writer, sheet_name='By_Region')
            self.analyze_by_product().to_excel(writer, sheet_name='By_Product')

            # تحليل إضافي: حسب مندوب المبيعات
            rep_analysis = self.df.groupby('Sales_Rep').agg({
                'Total': 'sum', 'Order_ID': 'count'
            }).sort_values('Total', ascending=False)
            rep_analysis.to_excel(writer, sheet_name='By_SalesRep')

            # تحليل إضافي: حسب حالة الطلب
            status_analysis = self.df.groupby('Status').agg({
                'Total': 'sum', 'Order_ID': 'count'
            })
            status_analysis.to_excel(writer, sheet_name='By_Status')

        print("✅ تم حفظ تقارير الإكسل")


# ==================== التشغيل الرئيسي ====================
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Sales Analysis Project - Starting...")
    print("=" * 50)

    try:
        # 1. تهيئة المحلل
        analyzer = SalesAnalyzer('data/input.xlsx')

        # 2. تحميل وتنظيف
        analyzer.load_and_clean()

        # 3. مثال على الفلترة بالتاريخ
        print("\n📅 مثال على الفلترة بالتاريخ:")
        filtered = analyzer.filter_by_date(
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 6, 30)
        )
        print(f"الطلبات من يناير إلى يونيو: {len(filtered)} طلب")

        # 4. التحليلات
        print("\n📊 التحليل حسب المنطقة:")
        print(analyzer.analyze_by_region())

        print("\n📊 التحليل حسب المنتج:")
        print(analyzer.analyze_by_product())

        # 5. الرسوم البيانية
        analyzer.create_charts()

        # 6. حفظ التقارير
        analyzer.save_all_reports()

        # 7. تقرير PDF
        analyzer.export_to_pdf()

        print("\n" + "=" * 50)
        print("🎉 جميع التقارير تم إنشاؤها بنجاح!")
        print("=" * 50)

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")