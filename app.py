import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import yfinance as yf
from prophet import Prophet
import folium
from streamlit_folium import folium_static
from datetime import datetime
import requests



# Configuración de la página
st.set_page_config(page_title="Stocks Dashboard", layout="wide")
st.title("Stocks Dashboard - Export Prices and Futures")

# Sección de noticias en la barra lateral
st.sidebar.subheader("Latest Stock Market News")
news_mock = [
    {"title": "El activo que más vale en los mercados marca máximos históricos: ¿hasta dónde puede llegar?", "link": "https://finance.yahoo.com/news/stock-market-record-highs", "desc": "El Oro vuelve con su brillo especial en los mercados financieros globales, con ese amarillo más intenso que marca la volatilidad del mercado y el pensamiento de los inversores de que vienen curvas en los movimientos de los activos globales...", "img_url": "https://s.yimg.com/uu/api/res/1.2/JIwj.Y6l.xD2P9JW4vqsMQ--~B/Zmk9c3RyaW07aD0yNTI7cT04MDt3PTMzNjthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/es/estrategias_de_inversi_n_556/20089ce4669151c2baaf025217c6cb8c.cf.webp"},
    {"title": "Trump 2.0: ¿hora de moderar el entusiasmo?", "link": "https://finance.yahoo.com/news/tech-stocks-ai-boom", "desc": "Los mercados de riesgo se han mostrado eufóricos tras los resultados de las elecciones en EE. UU.: la renta variable estadounidense ha alcanzado niveles récord...", "img_url": "https://s.yimg.com/uu/api/res/1.2/Rv0qE1hiujb2rFy6cufDTw--~B/Zmk9c3RyaW07aD0yNTI7cT04MDt3PTMzNjthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/es/estrategias_de_inversi_n_556/186ba2a4b52c699a4c2984ac9b8ad918.cf.webp"}
]

for news in news_mock:
    with st.sidebar:
        st.markdown(f"### [{news['title']}]({news['link']})")
        st.write(news['desc']) 
        
                 
# 🔑 API Key de OpenWeatherMap (Gratis)
API_KEY = "c4517e15f41a6204207bcc3b54dd7eb0"

# 📌 Lista de ciudades en España con coordenadas
cities = [
    {"name": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"name": "Barcelona", "lat": 41.3874, "lon": 2.1686},
    {"name": "Valencia", "lat": 39.4699, "lon": -0.3763},
    {"name": "Sevilla", "lat": 37.3886, "lon": -5.9823},
    {"name": "Bilbao", "lat": 43.263, "lon": -2.935},
    {"name": "Zaragoza", "lat": 41.6488, "lon": -0.8891},
    {"name": "Málaga", "lat": 36.7213, "lon": -4.4213},
    {"name": "Granada", "lat": 37.1773, "lon": -3.5986}
]

# 🎯 Función para obtener el pronóstico por horas de OpenWeatherMap
def get_hourly_forecast(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={city['lat']}&lon={city['lon']}&appid={API_KEY}&units=metric&lang=es"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error obteniendo datos de {city['name']}: {e}")
        return None

# 🔥 Crear el mapa de España
m = folium.Map(location=[40.0, -3.7], zoom_start=6)

# 📌 Agregar marcadores para cada ciudad con pronóstico por horas
for city in cities:
    forecast_data = get_hourly_forecast(city)
    if forecast_data:
        forecast_list = forecast_data["list"][:5]  # Pronóstico de las próximas 5 horas
        forecast_text = f"<b>{city['name']}</b><br>"
        
        for forecast in forecast_list:
            dt_txt = forecast["dt_txt"]
            temp = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]
            icon_code = forecast["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}.png"
            
            # Formatear la hora
            time_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
            time_formatted = time_obj.strftime("%d %b %H:%M")
            
            forecast_text += f"🕒 {time_formatted} - {temp}°C, {description.capitalize()}<br>"
            forecast_text += f"<img src='{icon_url}' width='30'><br>"

        folium.Marker(
            [city["lat"], city["lon"]],
            popup=folium.Popup(forecast_text, max_width=300),
            tooltip=f"{city['name']} (Click para ver el clima)"
        ).add_to(m)

# 🌍 Mostrar el mapa en Streamlit
st.subheader("Weather Forecast in Spain")
try:
    folium_static(m)
except Exception as e:
    st.error(f"Error al renderizar el mapa: {e}")   

# Función para obtener datos de avena y aluminio
@st.cache_data
def get_commodity_data(ticker):
    asset = yf.Ticker(ticker)
    asset_history = asset.history(period='2y')
    asset_df = asset_history.reset_index()[['Date', 'Close']]
    asset_df['Date'] = pd.to_datetime(asset_df['Date'])
    return asset_df

# Carga de datos desde CSV
file_path_ordi = "Dades_Ordi_Cat_vs_Esp__Corregido.csv"
file_path_cereals = "Dades_Cereals_Esp_2022-24__Corregido.csv"
file_path_gprd = "gprd.csv"

df_ordi = pd.read_csv(file_path_ordi)
df_cereals = pd.read_csv(file_path_cereals)
oats_data = get_commodity_data('ZO=F')
aluminum_data = get_commodity_data('ALI=F')
gold_data = get_commodity_data('GC=F')
df_gprd = pd.read_csv(file_path_gprd)

st.subheader("Historical Data (from Yahoo Finance)")

# Mostrar datos de avena y aluminio en columnas
col1, col2 = st.columns(2)

with col1:
    st.write("### Gprd index")
    if not oats_data.empty:
        st.write(df_gprd)
        fig_oats = go.Figure()
        fig_oats.add_trace(go.Scatter(x=oats_data['Date'], y=oats_data['Close'], mode='lines', name='Oats Prices'))
        fig_oats.update_layout(
            title="Oats Prices Over Time",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(label="All", step="all")
                    ])
                ),
                rangeslider=dict(visible=True),  # Slider de rango
                type="date"
            ),
            yaxis_title="Price (USD)",
            template="plotly_white"
        )

        st.plotly_chart(fig_oats)
    else:
        st.write("No data available for oats.")

with col2:
    if not aluminum_data.empty:
        fig_aluminum = go.Figure()
        fig_aluminum.add_trace(go.Scatter(x=aluminum_data['Date'], y=aluminum_data['Close'], mode='lines', name='Aluminum Prices'))
        fig_aluminum.update_layout(
            title="Aluminum Prices Over Time",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(label="All", step="all")
                    ])
                ),
                rangeslider=dict(visible=True),  # Slider de rango
                type="date"
            ),
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig_aluminum)
        fig_gold = go.Figure()
        fig_gold.add_trace(go.Scatter(x=gold_data['Date'], y=gold_data['Close'], mode='lines', name='Gold Prices'))
        fig_gold.update_layout(
            title="Gold Prices Over Time",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(label="All", step="all")
                    ])
                ),
                rangeslider=dict(visible=True),  # Slider de rango
                type="date"
            ),
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig_gold)
    else:
        st.write("No data available for aluminum.")


st.subheader("Loaded Data from cereals")

st.write("### Ordi Data (Catalonia vs Spain)")
st.dataframe(df_ordi, use_container_width=True)

st.write("### Cereals Data (Spain 2022-2024)")
st.dataframe(df_cereals, use_container_width=True)

# Graficar datos de ambos CSVs
df_ordi['Date'] = pd.to_datetime(df_ordi['Date'])
df_cereals['Date'] = pd.to_datetime(df_cereals['Date'])

fig_ordi = go.Figure()
fig_cereals = go.Figure()

for column in df_ordi.columns[1:]:
    fig_ordi.add_trace(go.Scatter(x=df_ordi['Date'], y=df_ordi[column], mode='lines', name=f'Ordi - {column}'))

for column in df_cereals.columns[1:]:
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



# Botón para mostrar la predicción
if st.button("Mostrar Predicción "):
    df_ordi['Date'] = pd.to_datetime(df_ordi['Date'])
    df_clean = df_ordi[['Date', 'Ordi_pinso_esp_EURtona']].dropna().sort_values('Date')
    df_clean = df_clean.rename(columns={'Date': 'ds', 'Ordi_pinso_esp_EURtona': 'y'})
    df_clean['ds'] = df_clean['ds'].dt.tz_localize(None)

    model_final = Prophet()
    model_final.fit(df_clean)

    future_final = model_final.make_future_dataframe(periods=45, freq='D')
    forecast_final = model_final.predict(future_final)

    # Filtrar solo los días futuros en la predicción final
    last_date_final = df_clean['ds'].max()
    forecast_future_final = forecast_final[forecast_final['ds'] > last_date_final]

    # Crear DataFrame combinado: datos reales hasta el último punto + predicción futura final
    df_combined_final = pd.concat([df_clean, forecast_future_final[['ds', 'yhat']].rename(columns={'yhat': 'y'})])

    # Guardar el resultado final
    result = {
        'step': "Final",
        'df_segment': df_clean,  # Serie real completa
        'df_combined': df_combined_final,  # Serie real completa + predicción final
        'forecast': forecast_final,
        'mae': np.nan,
        'coincidencias': 0
    }

    fig = go.Figure()

    # Serie original hasta el punto actual
    fig.add_trace(go.Scatter(
        x=result['df_segment']['ds'], y=result['df_segment']['y'], mode='lines',
        name='Actual hasta el corte', line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
            x=result['df_combined']['ds'], y=result['df_combined']['y'], mode='lines',
            name=f'Predicción (Segmento {result["step"]})', line=dict(color='red', dash='dash')
        ))
    
    fig.update_layout(
        title=f"Predicción a 45 dias",
        xaxis_title="Fecha",
        yaxis_title="Precio Ordi_pinso_esp_EURtona",
        legend_title="Serie",
        template="plotly_white"
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)




# Footer
# st.write("Data sourced from Yahoo Finance and uploaded CSV files.")



