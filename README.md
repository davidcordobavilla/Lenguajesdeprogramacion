# S23 Taller 6 — Observatorio financiero

**Curso:** Lenguajes de Programación  
**Estudiante:** David Córdoba  
**Proyecto:** aplicación interactiva para explorar y comparar activos financieros usando datos históricos.

## ¿Qué hace la aplicación?

- Permite seleccionar tres o más activos financieros.
- Consulta precios históricos a través de Yahoo Finance usando `yfinance`.
- Permite escoger el período de análisis.
- Compara precios normalizados con base 100.
- Calcula rendimientos diarios, rendimiento acumulado y volatilidad anualizada.
- Muestra una media móvil configurable.
- Presenta una matriz de correlación entre rendimientos.
- Permite descargar los precios consultados en CSV.

## Tecnologías

- **Streamlit:** interfaz web interactiva.
- **yfinance:** consulta de datos históricos de Yahoo Finance.
- **Pandas:** organización y análisis de series temporales.
- **NumPy:** operaciones numéricas y cálculos estadísticos.
- **Matplotlib:** visualización de la matriz de correlación.

## Instalación y ejecución local

Se recomienda usar Python 3.10 o superior.

1. Descarga o clona este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

5. Abre en el navegador la dirección local que muestra Streamlit, normalmente `http://localhost:8501`.

## Significado de los indicadores

- **Precio normalizado:** transforma la primera observación de cada activo a una base de 100 para comparar cambios relativos.
- **Rendimiento diario:** variación porcentual entre dos cierres consecutivos.
- **Rendimiento acumulado:** variación porcentual entre el primer y el último precio del período.
- **Volatilidad anualizada:** desviación estándar de los rendimientos diarios multiplicada por la raíz cuadrada de 252 y expresada en porcentaje. Es una estimación basada en datos históricos.
- **Media móvil:** promedio de los precios de una ventana de días bursátiles; ayuda a observar tendencias, pero no predice el futuro.
- **Correlación:** mide la relación lineal entre los rendimientos de dos activos, entre -1 y +1.

## Limitaciones

Los datos dependen de la disponibilidad y calidad de Yahoo Finance. Los mercados tienen calendarios diferentes; los activos pueden tener datos faltantes y los resultados dependen del período elegido. Los indicadores históricos no garantizan rendimientos futuros y esta aplicación es educativa, no asesoría financiera.

## Evidencias y entrega

Añade al informe PDF capturas reales de la aplicación en ejecución, con títulos y explicaciones. Incluye al menos cuatro capturas: selección de activos y período, precios normalizados, tabla de indicadores y correlaciones. Compara al menos tres activos y explica los resultados observados.

**Enlace del repositorio:** pega aquí la URL de tu repositorio de GitHub después de publicar los archivos.  
**Aplicación desplegada (opcional):** pega aquí la URL pública si la despliegas.
