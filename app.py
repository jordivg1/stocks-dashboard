import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Stocks Dashboard", layout="wide")
st.title("Stocks Dashboard - Export Prices and Futures")

# Simulación de datos
export_data = {
    "Name": [
        "Wheat, Canada 1 CWAD, St. Lawrence",
        "Wheat, EU (France) Grade 1, Rouen",
        "Wheat, US HRW (11.5%), Gulf",
        "Wheat, US SRW, Gulf",
        "Durum wheat, EU (France), Port la Nouvelle",
        "Barley, Black Sea Feed",
        "Barley, EU (France) Feed, Rouen",
        "Maize, EU (France), Bordeaux",
        "Maize, US 3YC, Gulf",
        "Soyabeans, US 2Y (Gulf)"
    ],
    "€/t": [310, 235, 253, 235, 299, 222, 222, np.nan, 216, 404],
    "$ /t": [328, 243, 261, 243, 308, 229, 229, np.nan, 223, 418],
    "€/t (m/m var.)": ["-1%", "-1%", "+4%", "+3%", "-", "+6%", "+1%", "-", "+4%", "+4%"],
    "$/t (m/m var.)": ["+2%", "-1%", "+4%", "+4%", "-", "+6%", "+1%", "-", "+4%", "+4%"],
    "€/t (y/y var.)": ["-19%", "+8%", "-5%", "-1%", "-", "+22%", "+16%", "-", "+17%", "-7%"],
    "$/t (y/y var.)": ["-22%", "-9%", "-9%", "-5%", "-", "+17%", "+11%", "-", "+13%", "-11%"]
}

data_df = pd.DataFrame(export_data)

# Mostrar tabla interactiva
st.subheader("Export Prices FOB on 04-02-2025")
st.dataframe(data_df, use_container_width=True)

# Gráficos simulados
st.subheader("Monthly Average Export Prices (FOB)")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Primer gráfico - Trigo
x_months = ["24-03", "24-06", "24-09", "24-12", "25-02"]
wheat_prices = {
    "Russia Milling (12.5%)": [220, 210, 200, 230, 237],
    "France Grade 1, Rouen": [210, 215, 205, 220, 237],
    "US SRW, Gulf": [200, 190, 210, 220, 236]
}

for label, values in wheat_prices.items():
    ax[0].plot(x_months, values, label=label)
ax[0].set_title("Wheat - Monthly Avg. Export Prices")
ax[0].set_xlabel("Months")
ax[0].set_ylabel("$/t")
ax[0].legend()
ax[0].grid(True)

# Segundo gráfico - Maíz
maize_prices = {
    "Black Sea Feed": [180, 190, 200, 215, 223],
    "Mais fob Atlantique": [170, 180, 190, 210, 223],
    "US 3YC, Gulf": [160, 170, 185, 200, 217]
}

for label, values in maize_prices.items():
    ax[1].plot(x_months, values, label=label)
ax[1].set_title("Maize - Monthly Avg. Export Prices")
ax[1].set_xlabel("Months")
ax[1].set_ylabel("$/t")
ax[1].legend()
ax[1].grid(True)

# Mostrar gráficos
st.pyplot(fig)

# Futuros de precios
st.subheader("EU (Milling) Wheat Futures Terms - 60 Days")
fig2, ax2 = plt.subplots()
futures_terms = [231, 237, 233]
labels = ["Mar2025", "May2025", "Sep2025"]
ax2.bar(labels, futures_terms, color=["blue", "purple", "yellow"])
ax2.set_title("EU Wheat Futures Prices")
ax2.set_ylabel("€/t")

st.pyplot(fig2)

# Footer
st.write("Data simulated for demonstration purposes. Actual data may vary.")
