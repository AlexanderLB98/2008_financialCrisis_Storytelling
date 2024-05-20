import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
import matplotlib.pyplot as plt
from src.common import gen_candle_figs, calc_volatility, calc_volume_rollout
import altair as alt

st.set_page_config(layout="wide")

# Función para crear los gráficos utilizando altair_chart
def create_volatility_chart(df, title):
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('date', axis=alt.Axis(labelAngle=45), title='Fecha'),
        y=alt.Y('volatility', title='Volatilidad'),
        tooltip=['date', 'volatility']
    ).properties(
        title=title,
        width=1180, # Ancho automático
        height=400 # Altura fija
    ).interactive(
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).configure_title(
        anchor="middle",
        fontSize=24
        )
    return chart

# Función para crear los gráficos utilizando altair_chart
def create_volume_rollout_chart(df, title):
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('date', axis=alt.Axis(labelAngle=45), title='Fecha'),
        y=alt.Y('volume_rollout', title='volume_rollout'),
        tooltip=['date', 'volume_rollout']
    ).properties(
        title=title,
        width=1180, # Ancho automático
        height=400 # Altura fija
    ).interactive(
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).configure_title(
        anchor="middle",
        fontSize=24
        )
    return chart




def main():
    st.title('¿Cómo respondieron los principales índices bursátiles del mundo durante la crisis financiera de 2008?') 
    st.subheader('Por Lucas Alexander Bool') 
    st.write(('La crisis financiera de 2008 fue un evento de proporciones globales que sacudió los cimientos de los mercados financieros en todo el mundo. En medio de la incertidumbre y la volatilidad, los principales índices bursátiles se convirtieron en indicadores clave para evaluar el impacto de la crisis en las economías mundiales. Analizar cómo estos índices respondieron durante ese período tumultuoso nos brinda una visión fascinante de la dinámica y la resiliencia de los mercados financieros frente a una de las crisis más significativas de la historia reciente.')) 

    # LOAD DATA
    df_shares = pd.read_csv("data/df_shares.csv")
    df_markets = pd.read_csv("data/df_markets.csv")
    df_companies = pd.read_csv("data/df_companies.csv")

    # Combinamos los df
    df = pd.merge(df_shares, df_companies, on="company_code", how="inner")
    df = pd.merge(df, df_markets, on="market", how="inner")
    tickers = df["company_code"].unique()

    st.header("Primer insight: se da un aumento generalizado en la volatilidad de los diferentes índices del mercado.")

    st.write("La volatilidad es una medida de la variabilidad de los precios en un periodo de tiempo determinado. Un aumento en la volatilidad generalmente indica una mayor incertidumbre y riesgo en el mercado.")
    
    st.write("Observamos un incremento significativo en la volatilidad diaria de los índices AEX, IBEX35, FCHI y GDAXI a partir del verano de 2008. Esto coincide con el deterioro económico global que se intensificó durante ese periodo. Eventos clave como la quiebra de Lehman Brothers en septiembre de 2008 y la subsiguiente crisis de confianza en el sistema financiero global contribuyeron a esta volatilidad.")
    
    st.markdown("- inversores: Los inversores enfrentaron un entorno de mayor riesgo, lo que probablemente les llevó a ajustar sus carteras para mitigar pérdidas.")
    st.markdown("- Mercado: Las oscilaciones diarias de precios aumentaron, reflejando la incertidumbre y la rápida reacción a las noticias económicas y financieras.")
    


    if False:    
        col11, col12 = st.columns(2)

        df_0 = calc_volatility(df, tickers[0])
        col11.line_chart(df_0["volatility"])
        
        df_1 = calc_volatility(df, tickers[1])
        col12.line_chart(df_1["volatility"])


        col21, col22 = st.columns(2)

        
        df_2 = calc_volatility(df, tickers[2])
        col21.line_chart(df_2["volatility"])
        
        df_3 = calc_volatility(df, tickers[3])
        col22.line_chart(df_3["volatility"])
        
        
        
        
        
        
        
        
        
        
    col11, col12 = st.columns(2)



    # Crear los gráficos y mostrarlos en las columnas correspondientes
    df_0 = calc_volatility(df, tickers[0])
    col11.altair_chart(create_volatility_chart(df_0, f'Volatilidad Diaria para {tickers[0]}'))

    df_1 = calc_volatility(df, tickers[1])
    col12.altair_chart(create_volatility_chart(df_1, f'Volatilidad Diaria para {tickers[1]}'))

    col21, col22 = st.columns(2)

    df_2 = calc_volatility(df, tickers[2])
    col21.altair_chart(create_volatility_chart(df_2, f'Volatilidad Diaria para {tickers[2]}'))

    df_3 = calc_volatility(df, tickers[3])
    col22.altair_chart(create_volatility_chart(df_3, f'Volatilidad Diaria para {tickers[3]}'))

    
    
    st.header("Segundo insight: bajada generalizada del volumen.")
    
    st.write("El volumen de transacciones se refiere a la cantidad de acciones o contratos negociados en un periodo de tiempo específico. Una disminución en el volumen puede indicar una menor participación en el mercado y menor liquidez.")
    
    st.write("Desde finales de 2007 hasta 2009, los volúmenes de transacciones en los índices AEX, IBEX35, FCHI y GDAXI mostraron una tendencia a la baja. Este descenso se aceleró notablemente tras el verano de 2008, coincidiendo con la fase aguda de la crisis financiera.")
    
    
    st.markdown("- Liquidez: La disminución del volumen de transacciones redujo la liquidez del mercado, dificultando la compra y venta de activos sin afectar significativamente el precio.")
    st.markdown("- Confianza: La caída en el volumen refleja una pérdida de confianza de los inversores en los mercados bursátiles, llevando a muchos a adoptar una actitud de “esperar y ver”.")
    st.markdown("- Operaciones: Menor actividad en el mercado puede haber exacerbado las fluctuaciones de precios, ya que grandes transacciones individuales podrían tener un mayor impacto en los precios.")
    
    
    col11, col12 = st.columns(2)

    # Crear los gráficos y mostrarlos en las columnas correspondientes
    df_0 = calc_volume_rollout(df, tickers[0])
    col11.altair_chart(create_volume_rollout_chart(df_0, f'Volumen medio de la última semana para {tickers[0]}'))

    df_1 = calc_volume_rollout(df, tickers[1])
    col12.altair_chart(create_volume_rollout_chart(df_1, f'Volumen medio de la última semana para {tickers[1]}'))

    col21, col22 = st.columns(2)

    df_2 = calc_volume_rollout(df, tickers[2])
    col21.altair_chart(create_volume_rollout_chart(df_2, f'Volumen medio de la última semana para {tickers[2]}'))

    df_3 = calc_volume_rollout(df, tickers[3])
    col22.altair_chart(create_volume_rollout_chart(df_3, f'Volumen medio de la última semana para {tickers[3]}'))



    st.header("Momento Eureka: Caída generalizada de los precios")

    st.write("Los precios de los índices bursátiles son un reflejo agregado de las expectativas sobre las ganancias futuras de las empresas que los componen. Una caída sostenida en los precios indica una perspectiva económica negativa.")

    st.write("Durante 2008, los precios de los índices AEX y IBEX35, así como de otros índices importantes, experimentaron caídas significativas. La magnitud de la crisis financiera y la recesión global que se desarrolló durante este periodo llevaron a una reevaluación drástica de las valoraciones de las empresas.")    
    
    
    st.markdown("- Inversores: Aquellos que mantenían posiciones largas (compradas) sufrieron pérdidas significativas, lo que afectó la confianza y el comportamiento de inversión a largo plazo.")
    st.markdown("- Economía: La caída de los precios bursátiles tuvo efectos en cadena sobre la economía real, afectando la riqueza de los hogares, el gasto de los consumidores y las decisiones de inversión de las empresas.")
    



    
    col21, col22 = st.columns(2)

    
    figs = gen_candle_figs(df, tickers)

    
    col21.pyplot(figs[0])
    col22.pyplot(figs[1])

    col21.pyplot(figs[2])
    col22.pyplot(figs[3])









    # Datos de Stock
    #display_stock_data()

    # Gráfica interactiva
    #display_interactive_graph()

@st.cache_data
def display_stock_data():
    df = pd.read_csv("data/stock_data_v0.csv")

    col1, col2, col3 = st.columns(3)

    regions = df["region"].unique()
    col1.write(regions)

    countries = df["country"].unique()
    col2.write(countries)

    st.write(len(df["company_code"].unique()))

    all_companies = df["company_name"].unique()

    col3.write(all_companies)

    # Crear el menú desplegable
    company = st.selectbox(label='Select ticker', options=all_companies, index=0)

    # Mostrar el ticker seleccionado
    st.write('Seleccionaste:', company)

    ticker = df[df["company_name"] == company]["company_code"].values[0]

    st.write(ticker)

    df_AD_AS = df[df["company_code"] == ticker]
    df_AD_AS.set_index("date", inplace=True)

    st.line_chart(df_AD_AS["close"])

@st.cache_data
def display_interactive_graph():
    perc_heads = st.number_input(label='Chance of Coins Landing on Heads', min_value=0.0, max_value=1.0, value=.5)
    graph_title = st.text_input(label='Graph Title')

    distr = perc_heads  # 0.5

    binom_dist = np.random.binomial(100, distr, 10) / 100

    st.write(binom_dist)

    list_of_means = []
    for i in range(0, 1000):
        list_of_means.append(np.mean(np.random.binomial(100, distr, 10) / 100))
    fig1, ax1 = plt.subplots()
    ax1 = plt.hist(list_of_means, range=[0, 1])
    plt.title(graph_title)
    st.pyplot(fig1)
    fig2, ax2 = plt.subplots()
    ax2 = plt.hist([1, 1, 1, 1], range=[0, 1])
    st.pyplot(fig2)

if __name__ == "__main__":
    main()
