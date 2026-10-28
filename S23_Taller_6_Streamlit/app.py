import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.set_page_config(page_title="Observatorio financiero", page_icon="📈", layout="wide")

st.title("📈 Observatorio financiero")
st.write(
    "Explora precios históricos, rendimientos, volatilidad, medias móviles y correlaciones "
    "de activos financieros. Los resultados se basan en datos históricos y no son una recomendación de inversión."
)

ACTIVOS = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "Alphabet / Google (GOOGL)": "GOOGL",
    "NVIDIA (NVDA)": "NVDA",
    "Tesla (TSLA)": "TSLA",
    "Coca-Cola (KO)": "KO",
    "JPMorgan Chase (JPM)": "JPM",
    "S&P 500 ( ^GSPC)": "^GSPC",
    "Bitcoin (BTC-USD)": "BTC-USD",
}

with st.sidebar:
    st.header("Configuración")
    seleccion = st.multiselect(
        "Selecciona al menos 3 activos",
        options=list(ACTIVOS.keys()),
        default=["Apple (AAPL)", "Microsoft (MSFT)", "Amazon (AMZN)"],
        help="Puedes seleccionar tres o más activos para compararlos."
    )
    fecha_fin = st.date_input("Fecha final", value=date.today())
    fecha_inicio = st.date_input("Fecha inicial", value=fecha_fin - timedelta(days=365))
    ventana = st.slider("Ventana de media móvil (días bursátiles)", min_value=5, max_value=100, value=20, step=5)
    consultar = st.button("Consultar datos", type="primary", use_container_width=True)

if fecha_inicio >= fecha_fin:
    st.error("La fecha inicial debe ser anterior a la fecha final.")
    st.stop()

if len(seleccion) < 3:
    st.info("Selecciona al menos tres activos en el panel izquierdo para comenzar.")
    st.stop()

tickers = [ACTIVOS[nombre] for nombre in seleccion]

@st.cache_data(ttl=900, show_spinner=False)
def descargar_datos(tickers, inicio, fin):
    # yfinance trata la fecha final como límite exclusivo; sumamos un día para incluirla.
    datos = yf.download(
        tickers=tickers,
        start=inicio,
        end=(pd.Timestamp(fin) + pd.Timedelta(days=1)).date(),
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )
    if datos.empty:
        return pd.DataFrame()
    if isinstance(datos.columns, pd.MultiIndex):
        if "Close" in datos.columns.get_level_values(0):
            precios = datos["Close"].copy()
        else:
            precios = datos.xs(datos.columns.levels[0][0], axis=1, level=0)
    else:
        # Protección por si la descarga devuelve columnas sencillas.
        if "Close" in datos.columns:
            precios = datos[["Close"]].copy()
            precios.columns = tickers[:1]
        else:
            precios = datos.copy()
    if isinstance(precios, pd.Series):
        precios = precios.to_frame(name=tickers[0])
    return precios

if consultar or "precios" not in st.session_state:
    with st.spinner("Consultando datos históricos..."):
        try:
            precios = descargar_datos(tuple(tickers), str(fecha_inicio), str(fecha_fin))
            st.session_state["precios"] = precios
            st.session_state["tickers_consultados"] = tickers
            st.session_state["nombres_consultados"] = seleccion
        except Exception as exc:
            st.error(f"No fue posible consultar los datos. Detalle: {exc}")
            st.stop()
else:
    precios = st.session_state["precios"]

if precios.empty:
    st.error("No se recibieron datos para la selección. Cambia las fechas o los activos e inténtalo de nuevo.")
    st.stop()

# Mantener solamente columnas con datos y limpiar huecos.
precios = precios.dropna(axis=1, how="all").ffill().dropna(how="all")
if precios.empty or precios.shape[1] == 0:
    st.error("No hay precios suficientes para calcular los indicadores.")
    st.stop()

# Recuperar nombres/tickers correspondientes a las columnas efectivamente descargadas.
nombres_map = {ACTIVOS[nombre]: nombre for nombre in st.session_state.get("nombres_consultados", seleccion)}
precios = precios.rename(columns={col: nombres_map.get(col, col) for col in precios.columns})
precios = precios.loc[:, ~precios.columns.duplicated()]

if precios.shape[1] < 3:
    st.warning(f"Solo se encontraron datos para {precios.shape[1]} activo(s). Selecciona otros activos o cambia el período.")

rendimientos = precios.pct_change().dropna(how="all")
precios_normalizados = precios.div(precios.iloc[0]).mul(100)
volatilidad = rendimientos.std() * np.sqrt(252) * 100
rendimiento_acumulado = (precios.iloc[-1] / precios.iloc[0] - 1) * 100
medias = precios.rolling(window=ventana, min_periods=ventana).mean()
correlaciones = rendimientos.corr()

st.caption(
    f"Período consultado: {precios.index.min().date()} a {precios.index.max().date()} · "
    f"Activos con datos: {precios.shape[1]}"
)

c1, c2, c3 = st.columns(3)
c1.metric("Activos analizados", int(precios.shape[1]))
c2.metric("Días con datos", int(len(precios)))
c3.metric("Ventana de media móvil", f"{ventana} días")

st.subheader("1. Precios normalizados")
st.write("Cada serie comienza en una base de 100, lo que facilita comparar la variación porcentual aunque los precios originales sean diferentes.")
st.line_chart(precios_normalizados, use_container_width=True)

st.subheader("2. Rendimientos diarios")
st.write("El rendimiento diario expresa el cambio porcentual entre un cierre y el cierre anterior.")
st.line_chart(rendimientos * 100, use_container_width=True)

st.subheader("3. Indicadores por activo")
indicadores = pd.DataFrame({
    "Precio inicial": precios.iloc[0],
    "Precio final": precios.iloc[-1],
    "Rendimiento acumulado (%)": rendimiento_acumulado,
    "Volatilidad anualizada (%)": volatilidad,
})
st.dataframe(indicadores.style.format({
    "Precio inicial": "{:.2f}",
    "Precio final": "{:.2f}",
    "Rendimiento acumulado (%)": "{:.2f}",
    "Volatilidad anualizada (%)": "{:.2f}",
}), use_container_width=True)

st.subheader(f"4. Precios y media móvil ({ventana} días)")
activo_grafico = st.selectbox("Elige un activo para ver su media móvil", list(precios.columns))
serie = pd.DataFrame({
    "Precio de cierre ajustado": precios[activo_grafico],
    f"Media móvil ({ventana} días)": medias[activo_grafico],
})
st.line_chart(serie, use_container_width=True)
st.caption("Una media móvil suaviza variaciones de corto plazo; no predice ni garantiza el precio futuro.")

st.subheader("5. Correlación entre rendimientos")
st.write("La correlación se encuentra entre -1 y +1: positiva significa que los rendimientos suelen moverse en la misma dirección; negativa, en direcciones opuestas.")
fig, ax = plt.subplots(figsize=(max(6, len(correlaciones.columns) * 0.8), max(4, len(correlaciones.columns) * 0.6)))
imagen = ax.imshow(correlaciones, vmin=-1, vmax=1, cmap="coolwarm")
ax.set_xticks(range(len(correlaciones.columns)))
ax.set_yticks(range(len(correlaciones.index)))
ax.set_xticklabels(correlaciones.columns, rotation=45, ha="right")
ax.set_yticklabels(correlaciones.index)
for i in range(len(correlaciones.index)):
    for j in range(len(correlaciones.columns)):
        valor = correlaciones.iloc[i, j]
        if pd.notna(valor):
            ax.text(j, i, f"{valor:.2f}", ha="center", va="center", fontsize=8)
fig.colorbar(imagen, ax=ax, label="Correlación")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

with st.expander("Ver datos históricos"):
    st.dataframe(precios, use_container_width=True)

csv = precios.to_csv().encode("utf-8")
st.download_button(
    "Descargar precios históricos en CSV",
    data=csv,
    file_name="precios_historicos.csv",
    mime="text/csv",
)

st.divider()
st.caption("Fuente de datos: Yahoo Finance mediante yfinance. Los datos pueden tener retrasos, faltar o cambiar. Uso educativo.")
