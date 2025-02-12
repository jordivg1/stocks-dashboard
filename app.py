import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import yfinance as yf

# Configuración de la página
st.set_page_config(page_title="Stocks Dashboard", layout="wide")
st.title("Stocks Dashboard - Export Prices and Futures")

# Función para obtener datos de avena y aluminio
@st.cache_data
def get_commodity_data(ticker):
    asset = yf.Ticker(ticker)
    asset_history = asset.history(period='2y')
    asset_df = asset_history.reset_index()[['Date', 'Close']]
    asset_df['Date'] = pd.to_datetime(asset_df['Date'])
    return asset_df

# Obtener datos de avena y aluminio
oats_data = get_commodity_data('ZO=F')
aluminum_data = get_commodity_data('ALI=F')

st.subheader("Historical Data (from Yahoo Finance)")

# Mostrar datos de avena y aluminio en columnas
col1, col2 = st.columns(2)

with col1:
    st.write("### Oats Data")
    if not oats_data.empty:
        st.write(oats_data.head(10))
        fig_oats = go.Figure()
        fig_oats.add_trace(go.Scatter(x=oats_data['Date'], y=oats_data['Close'], mode='lines', name='Oats Prices'))
        fig_oats.update_layout(
            title="Oats Prices Over Time",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig_oats)
    else:
        st.write("No data available for oats.")

with col2:
    st.write("### Aluminum Data")
    if not aluminum_data.empty:
        st.write(aluminum_data.head(10))
        fig_aluminum = go.Figure()
        fig_aluminum.add_trace(go.Scatter(x=aluminum_data['Date'], y=aluminum_data['Close'], mode='lines', name='Aluminum Prices'))
        fig_aluminum.update_layout(
            title="Aluminum Prices Over Time",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig_aluminum)
    else:
        st.write("No data available for aluminum.")

file_path_ordi = "Dades_Ordi_Cat_vs_Esp__Corregido.csv"
file_path_cereals = "Dades_Cereals_Esp_2022-24__Corregido.csv"

df_ordi = pd.read_csv(file_path_ordi)
df_cereals = pd.read_csv(file_path_cereals)

# Mostrar los datos en Streamlit
st.subheader("Loaded Data from CSV Files")

st.write("### Ordi Data (Catalonia vs Spain)")
st.dataframe(df_ordi, use_container_width=True)

st.write("### Cereals Data (Spain 2022-2024)")
st.dataframe(df_cereals, use_container_width=True)

# Graficar datos de ambos CSVs en la misma gráfica
st.subheader("Comparison of Ordi and Cereals Data")
fig_ordi = go.Figure()
fig_cereals = go.Figure()

for column in df_ordi.columns[1:]:  # Excluir las primeras dos columnas si son identificadores
    fig_ordi.add_trace(go.Scatter(x=df_ordi['Date'], y=df_ordi[column], mode='lines', name=f'Ordi - {column}'))

for column in df_cereals.columns[1:]:  # Excluir las primeras dos columnas si son identificadores
    fig_cereals.add_trace(go.Scatter(x=df_cereals['Date'], y=df_cereals[column], mode='lines', name=f'Cereals - {column}'))

fig_ordi.update_layout(
    title="Ordi vs Cereals Prices Over Time",
    xaxis_title="Week",
    yaxis_title="Price (EUR/t)",
    template="plotly_white"
)

fig_cereals.update_layout(
    title="Ordi vs Cereals Prices Over Time",
    xaxis_title="Week",
    yaxis_title="Price (EUR/t)",
    template="plotly_white"
)

st.plotly_chart(fig_ordi)
st.plotly_chart(fig_cereals)



# Footer
# st.write("Data sourced from Yahoo Finance and uploaded CSV files.")



