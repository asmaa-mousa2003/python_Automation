import pandas as pd
import random
from datetime import datetime, timedelta
import os

base_dir = os.path.dirname(os.path.dirname(__file__))  # يرجع لـ root
output_path = os.path.join(base_dir, 'data', 'input.xlsx')


def generate_sales_data(num_rows=100, output_path='data/input.xlsx'):
    """توليد بيانات مبيعات وهمية ومعقدة"""

    print(f"🔄 جاري توليد {num_rows} صف من البيانات...")

    # 1. قوائم البيانات العشوائية
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB', 'Headset', 'Webcam', 'Speaker']
    regions = ['Cairo', 'Alex', 'Giza', 'Mansoura', 'Assiut', 'Tanta']
    sales_reps = ['Ahmed', 'Mohamed', 'Sarah', 'Nour', 'Khaled', 'Mona']
    payment_methods = ['Cash', 'Credit Card', 'Instapay', 'Vodafone Cash']
    statuses = ['Completed', 'Pending', 'Cancelled', 'Refunded']

    # 2. توليد البيانات
    data = []
    start_date = datetime(2023, 1, 1)

    for i in range(num_rows):
        # تاريخ عشوائي
        random_days = random.randint(0, 365)
        date = start_date + timedelta(days=random_days)

        # بيانات عشوائية
        product = random.choice(products)
        region = random.choice(regions)
        sales_rep = random.choice(sales_reps)
        payment = random.choice(payment_methods)
        status = random.choice(statuses)

        # سعر عشوائي (بعض المنتجات أغلى)
        base_price = {'Laptop': 5000, 'Monitor': 1500, 'Headset': 800, 'Mouse': 200,
                      'Keyboard': 300, 'USB': 150, 'Webcam': 600, 'Speaker': 450}
        sales = base_price.get(product, 500) + random.randint(-100, 500)

        # كمية عشوائية
        quantity = random.randint(1, 5)
        total = sales * quantity

        # خصم عشوائي (10% من الصفوف فيها خصم)
        discount = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, random.randint(5, 20)])
        final_total = total - (total * discount / 100)

        # ملاحظات (بعضها فاضي عشان نختبر التنظيف)
        notes = random.choice(['', '', '', 'عميل VIP', 'شكوى جودة', 'توصيل سريع'])

        # إضافة بعض البيانات الفارغة عشوائياً (5%)
        if random.random() < 0.05:
            product = ''
        if random.random() < 0.05:
            sales = ''

        data.append({
            'Order_ID': f'ORD-{1000 + i}',
            'Date': date.strftime('%Y-%m-%d'),
            'Product': product,
            'Category': random.choice(['Electronics', 'Accessories', 'Peripherals']),
            'Sales': sales,
            'Quantity': quantity,
            'Total': round(final_total, 2),
            'Discount_%': discount,
            'Region': region,
            'Sales_Rep': sales_rep,
            'Payment_Method': payment,
            'Status': status,
            'Customer_Rating': random.randint(1, 5),
            'Notes': notes
        })

    # 3. إنشاء DataFrame وحفظه
    df = pd.DataFrame(data)

    # حفظ في إكسل
    df.to_excel(output_path, index=False)

    print(f"✅ تم حفظ {num_rows} صف في: {output_path}")
    print(f"📊 عدد الأعمدة: {len(df.columns)}")
    print(f"📝 الأعمدة: {df.columns.tolist()}")

    return df


# تشغيل التوليد
if __name__ == "__main__":
    generate_sales_data(100, output_path)