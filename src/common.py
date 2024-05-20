import streamlit as st

import pandas as pd
import mplfinance as mpf

import matplotlib.pyplot as plt

# Definir un estilo personalizado
my_style = mpf.make_mpf_style(
    
    rc={
        'font.size': 14,  # Tamaño de la fuente global
        'axes.labelsize': 8,  # Tamaño de la etiqueta de los ejes
        'axes.titlesize': 14,  # Tamaño del título del gráfico
        'xtick.labelsize': 8,  # Tamaño de las etiquetas del eje x
        'ytick.labelsize': 8   # Tamaño de las etiquetas del eje y
    }
)


def gen_candle_figs(df, tickers, style=my_style):
    # Convertir el índice a tipo de fecha si aún no lo está
    df['date'] = pd.to_datetime(df['date'])

    # Agrupar los datos por semana y calcular los precios de apertura, cierre, máximo y mínimo
    df_weekly = df.groupby([pd.Grouper(key='date', freq='W'), 'company_code']).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'company_name': 'first'  # Asegúrate de agregar el nombre de la compañía correctamente
    }).reset_index()

    figs = []  # Lista para almacenar las figuras generadas

    # Iterar sobre los tickers y graficar los datos semanalmente
    for ticker in tickers:
        df_aux = df_weekly[df_weekly["company_code"] == ticker].set_index("date")
        fig, ax = mpf.plot(
            df_aux,
            type = "candle",
            volume = True,
            xrotation = 45,
            axtitle = df_aux["company_name"].unique()[0],
            returnfig = True,
            figsize = (6,4),
            style=style
        )
        figs.append(fig)

    return figs


def calc_volatility(df, ticker):
    df_aux = df[df["company_code"] == ticker]
    
    df_aux["volatility"] = df_aux["close"].pct_change()
    return df_aux


def calc_volume_rollout(df, ticker):
    df_aux = df[df["company_code"] == ticker]
    
    df_aux["volume_rollout"] = df_aux["volume"].rolling(window=28).mean()
    return df_aux



def gen_volatility(df, tickers):
    all_volatilities = []
    for ticker in tickers:
        df_aux = df[df["company_code"] == ticker].set_index("date")
        volatility_daily = df_aux["close"].pct_change() # Calcula el porcentaje de cambio respecto al día anterior
        all_volatilities.append(volatility_daily.tolist())
    return all_volatilities

def gen_volatility_2(df, tickers):
    figs = []
    for ticker in tickers:
        df_aux = df[df["company_code"] == ticker].set_index("date")
        volatility_daily = df_aux["close"].pct_change() # Calcula el porcentaje de cambio respecto al día anterior
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(volatility_daily.index, volatility_daily, label=ticker)
        ax.set_title(f'Volatilidad Diaria para {df_aux["company_name"][0]}')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Volatilidad')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        figs.append(fig)
    return figs



