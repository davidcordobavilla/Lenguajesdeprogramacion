# S23 Taller 6 — Observatorio financiero

**Curso:** Lenguajes de Programación  
**Estudiante:** David Córdoba  
**Proyecto:** Observatorio financiero interactivo

## Objetivo

Desarrollar una aplicación que permita consultar, analizar y comparar el comportamiento histórico de diferentes activos financieros mediante indicadores y gráficos.

## Funcionalidades

- Selección de tres o más activos financieros.
- Consulta de precios históricos.
- Selección del período de análisis.
- Gráficos de precios normalizados con base 100.
- Cálculo de rendimientos diarios y acumulados.
- Cálculo de volatilidad anualizada.
- Visualización de medias móviles.
- Matriz de correlación entre rendimientos.
- Descarga de datos históricos en formato CSV.

## Tecnologías utilizadas

- **Streamlit:** construcción de la interfaz interactiva.
- **yfinance:** consulta de datos históricos de Yahoo Finance.
- **Pandas:** organización y análisis de los datos.
- **NumPy:** cálculos numéricos.
- **Matplotlib:** visualización de correlaciones.

## Instalación y ejecución

Se recomienda utilizar Python 3.10 o superior.

1. Descarga o clona el repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Instala las dependencias:

   `pip install -r requirements.txt`

4. Ejecuta la aplicación:

   `streamlit run app.py`

## Indicadores financieros

- **Precios normalizados:** permiten comparar la variación relativa de los activos usando una base común de 100.
- **Rendimiento diario:** mide el cambio porcentual entre dos precios consecutivos.
- **Rendimiento acumulado:** mide la variación porcentual entre el primer y el último precio del período.
- **Volatilidad anualizada:** estima la variabilidad de los rendimientos históricos, usando la desviación estándar diaria y la raíz cuadrada de 252.
- **Media móvil:** suaviza las fluctuaciones de los precios para facilitar la observación de tendencias.
- **Correlación:** mide la relación lineal entre los rendimientos de dos activos, con valores entre -1 y +1.

## Fuente de datos y limitaciones

La aplicación utiliza datos históricos de Yahoo Finance mediante la biblioteca yfinance. La disponibilidad y calidad de los datos pueden variar. Los indicadores históricos no garantizan resultados futuros y el proyecto tiene fines académicos, no constituye asesoría financiera.

## Evidencias y resultados

En el informe PDF se incluirán capturas reales de la aplicación, junto con la comparación e interpretación de al menos tres activos financieros.

**Repositorio de GitHub:** completar con el enlace del repositorio.  
**Aplicación desplegada:** completar si se publica una versión en línea.
