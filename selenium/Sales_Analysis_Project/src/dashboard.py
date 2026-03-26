#!/usr/bin/env python3
"""
Dashboard تفاعلي لعرض تحليل المبيعات
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# إعدادات الصفحة
st.set_page_config(
    page_title="Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# العنوان
st.title("📊 Sales Analysis Dashboard")
st.markdown("---")


# تحميل البيانات
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / 'data' / 'input.xlsx'
    try:
        df = pd.read_excel(data_path)
        # تنظيف بسيط
        df = df.dropna(subset=['Product', 'Sales', 'Total'])
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"❌ خطأ في تحميل البيانات: {e}")
        return None


df = load_data()

if df is not None:
    # 📊 المؤشرات الرئيسية (KPIs)
    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("إجمالي الإيرادات", f"${df['Total'].sum():,.2f}")

    with col2:
        st.metric("متوسط البيع", f"${df['Sales'].mean():,.2f}")

    with col3:
        st.metric("عدد الطلبات", len(df))

    with col4:
        st.metric("المنتجات", df['Product'].nunique())

    st.markdown("---")

    # 📊 الرسوم التفاعلية
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 المبيعات حسب المنطقة")
        region_sales = df.groupby('Region')['Total'].sum().reset_index()
        fig_region = px.bar(region_sales, x='Region', y='Total',
                            color='Total', color_continuous_scale='Blues')
        st.plotly_chart(fig_region, use_container_width=True)

    with col2:
        st.subheader("📦 المبيعات حسب المنتج")
        product_sales = df.groupby('Product')['Total'].sum().reset_index()
        fig_product = px.bar(product_sales, x='Total', y='Product',
                             orientation='h', color='Total',
                             color_continuous_scale='Greens')
        st.plotly_chart(fig_product, use_container_width=True)

    st.markdown("---")

    # 📈 الاتجاه الزمني
    st.subheader("📈 الاتجاه الزمني للمبيعات")
    df_sorted = df.sort_values('Date')
    daily_sales = df_sorted.groupby(df_sorted['Date'].dt.date)['Total'].sum().reset_index()
    daily_sales.columns = ['Date', 'Total']
    fig_trend = px.line(daily_sales, x='Date', y='Total',
                        markers=True, color_discrete_sequence=['#e74c3c'])
    st.plotly_chart(fig_trend, use_container_width=True)

    # 📋 عرض البيانات الخام
    with st.expander("📋 عرض البيانات الخام"):
        st.dataframe(df, use_container_width=True)

        # زر تحميل
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 تحميل البيانات (CSV)",
            data=csv,
            file_name='sales_data.csv',
            mime='text/csv'
        )

# التذييل
st.markdown("---")
st.caption("Built with ❤️ by Asmaa Mousa | Streamlit + Plotly")