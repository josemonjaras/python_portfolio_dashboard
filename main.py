# main.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Dashboard de Ventas", layout="wide")

st.title("📊 Dashboard Interactivo de Ventas")
st.markdown("Visualización de ventas por producto, categoría, ciudad y fecha.")

# Cargar datos


@st.cache_data
def load_data():
    df = pd.read_excel("venta.xlsx")
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'])
    return df


df = load_data()

# Filtros
st.sidebar.header("Filtros")
city = st.sidebar.multiselect(
    "Ciudad", options=df['city'].unique(), default=df['city'].unique())
category = st.sidebar.multiselect("Categoría", options=df['product_category'].unique(
), default=df['product_category'].unique())
date_range = st.sidebar.date_input(
    "Rango de fechas", [df['date_of_sale'].min(), df['date_of_sale'].max()])

# Filtrado dinámico
df_filtered = df[
    (df['city'].isin(city)) &
    (df['product_category'].isin(category)) &
    (df['date_of_sale'] >= pd.to_datetime(date_range[0])) &
    (df['date_of_sale'] <= pd.to_datetime(date_range[1]))
]

# Métricas clave
total_sales = df_filtered['sales_amount'].sum()
total_orders = df_filtered['order_id'].nunique()
total_products = df_filtered['product_id'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventas totales", f"${total_sales:,.2f}")
col2.metric("🧾 Total de órdenes", total_orders)
col3.metric("📦 Productos vendidos", total_products)

# Gráficos
tab1, tab2 = st.tabs(["📅 Ventas por Fecha", "🏙️ Ventas por Ciudad"])

with tab1:
    sales_time = df_filtered.groupby('date_of_sale')[
        'sales_amount'].sum().reset_index()
    fig1 = px.line(sales_time, x='date_of_sale', y='sales_amount',
                   title="Tendencia de Ventas por Fecha")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    city_sales = df_filtered.groupby('city')['sales_amount'].sum(
    ).sort_values(ascending=False).reset_index()
    fig2 = px.bar(city_sales, x='city', y='sales_amount',
                  title="Ventas por Ciudad", color='sales_amount')
    st.plotly_chart(fig2, use_container_width=True)

# Tabla dinámica
st.subheader("📋 Detalle de Ventas")
st.dataframe(df_filtered.sort_values(by="date_of_sale",
             ascending=False), use_container_width=True)
