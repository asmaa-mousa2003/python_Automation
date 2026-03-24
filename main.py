import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import os
import os

base_dir = os.path.join(os.path.dirname(__file__), 'selenium', 'Sales_Analysis_Project')
file_path = os.path.join(base_dir, 'data', 'input.xlsx')

# إعدادات لدعم اللغة العربية في الرسوم
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

print("🚀 بدء تحليل المبيعات...")

# 1️⃣ قراءة وتنظيف البيانات
filepath = r"E:\python_Automation\selenium\Sales_Analysis_Project\data\input.xlsx"
df = pd.read_excel(file_path)

print(f"📊 قبل التنظيف: {len(df)} صف")
df = df.dropna(subset=['Product', 'Sales', 'Total'])
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
print(f"✅ بعد التنظيف: {len(df)} صف")

# 2️⃣ إنشاء فولدر للصور والتقارير
output_folder = r"E:\python_Automation\selenium\tastcase\reports"
os.makedirs(output_folder, exist_ok=True)

# 3️⃣ 📈 إنشاء الرسوم البيانية
print("\n📈 جاري إنشاء الرسوم البيانية...")

# رسم 1: المبيعات حسب المنطقة
region_sales = df.groupby('Region')['Total'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(region_sales.index, region_sales.values, color='#3498db')
plt.title('Total Sales by Region', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_folder}/sales_by_region.png', dpi=300)
plt.close()
print("✅ تم حفظ: sales_by_region.png")

# رسم 2: المبيعات حسب المنتج
product_sales = df.groupby('Product')['Total'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
plt.barh(product_sales.index, product_sales.values, color='#2ecc71')
plt.title('Total Sales by Product', fontsize=14, fontweight='bold')
plt.xlabel('Total Sales')
plt.ylabel('Product')
plt.tight_layout()
plt.savefig(f'{output_folder}/sales_by_product.png', dpi=300)
plt.close()
print("✅ تم حفظ: sales_by_product.png")

# رسم 3: اتجاه المبيعات خلال الوقت
df_sorted = df.sort_values('Date')
daily_sales = df_sorted.groupby(df_sorted['Date'].dt.date)['Total'].sum()
plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales.values, color='#e74c3c', linewidth=2, marker='o')
plt.title('Daily Sales Trend', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_folder}/sales_trend.png', dpi=300)
plt.close()
print("✅ تم حفظ: sales_trend.png")

# 4️⃣ 📄 إنشاء تقرير PDF بسيط
print("\n📄 جاري إنشاء تقرير PDF...")
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    pdf_path = f'{output_folder}/Sales_Report.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # عنوان التقرير
    elements.append(Paragraph("Sales Analysis Report", styles['Heading1']))
    elements.append(Spacer(1, 20))

    # ملخص الأرقام
    summary = f"""
    <b>Total Records:</b> {len(df)}<br/>
    <b>Total Revenue:</b> ${df['Total'].sum():,.2f}<br/>
    <b>Average Sale:</b> ${df['Sales'].mean():,.2f}<br/>
    <b>Top Region:</b> {region_sales.idxmax()} (${region_sales.max():,.2f})<br/>
    <b>Top Product:</b> {product_sales.idxmax()} (${product_sales.max():,.2f})
    """
    elements.append(Paragraph(summary, styles['Normal']))
    elements.append(Spacer(1, 20))

    # جدول أفضل 5 مناطق
    elements.append(Paragraph("Top 5 Regions", styles['Heading2']))
    table_data = [['Region', 'Total Sales']] + region_sales.head(5).reset_index().values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(table)

    doc.build(elements)
    print(f"✅ تم حفظ: Sales_Report.pdf")

except ImportError:
    print("⚠️ مكتبة reportlab غير مثبتة. تخطي إنشاء PDF.")

# 5️⃣ 💾 حفظ تحليلات الإكسل
print("\n💾 جاري حفظ تقارير الإكسل...")
with pd.ExcelWriter(f'{output_folder}/Full_Analysis.xlsx') as writer:
    df.to_excel(writer, sheet_name='Clean_Data', index=False)
    region_sales.to_excel(writer, sheet_name='By_Region')
    product_sales.to_excel(writer, sheet_name='By_Product')
print(f"✅ تم حفظ: Full_Analysis.xlsx")

print("\n" + "=" * 50)
print("🎉 انتهى التحليل! الملفات في:")
print(output_folder)
print("=" * 50)