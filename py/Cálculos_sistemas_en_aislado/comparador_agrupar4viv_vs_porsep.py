# -*- coding: utf-8 -*-
"""
Created on Sat May 11 23:46:50 2024

@author: Usuario
"""

import pandas as pd
import matplotlib.pyplot as plt



df_combi = pd.read_csv('C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\datos_escalones_energ_insatisf_viviendas_combinadas.csv')
df_aislado = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\datos_escalones_energ_insatisf_en_aislado_t23.csv")

df_combi['Proporción de energía insatisfecha (%)']*=100
df_aislado['Proporción de energía insatisfecha (%)']*=100

# Para la primera gráfica
plt.plot(df_combi['Proporción de energía insatisfecha (%)'], df_combi['Precio por casa (USD)'], label='Dataframe viviendas combinadas')
plt.plot(df_aislado['Proporción de energía insatisfecha (%)'], df_aislado['Precio casa (USD)'], label='DataFrame viviendas aisladas')
plt.xlabel('Proporción de energía insatisfecha (%)')
plt.ylabel('Precio de la instalación por vivienda (USD)')
plt.title('Gráfico de precios frente a proporción de energía insatisfecha')
plt.legend()
plt.grid(True)  # Agregar malla
plt.show()

# Para la segunda gráfica
plt.plot(df_combi['Proporción de energía insatisfecha (%)'], df_combi['Surplus energy (kWh/año)'], label='Surplus energy total de viviendas combinadas')
plt.plot(df_aislado['Proporción de energía insatisfecha (%)'], df_aislado['Surplus energy generada por las 4 viviendas (kWh/año)'], label='Surplus energy total de viviendas aisladas')
plt.xlabel('Proporción de energía insatisfecha (%)')
plt.ylabel('Surplus energy entre las 4 viviendas (kWh)')
plt.title('Gráfico de surplus energy frente a proporción de energía insatisfecha')
plt.legend()
plt.grid(True)  # Agregar malla
plt.show()


# Para la tercera gráfica
plt.plot(df_combi['Proporción de energía insatisfecha (%)'], df_combi['LCOE (USD/kWh)'], label='LCOE de las viviendas combinadas')
plt.plot(df_aislado['Proporción de energía insatisfecha (%)'], df_aislado['LCOE (USD/kWh)'], label='LCOE de las viviendas aisladas')
plt.xlabel('Proporción de energía insatisfecha (%)')
plt.ylabel('LCOE entre las 4 viviendas (USD/kWh)')
plt.title('Gráfico de LCOE en USD/kWh frente a proporción de energía insatisfecha')
plt.legend()
plt.grid(True)  # Agregar malla
plt.show()
