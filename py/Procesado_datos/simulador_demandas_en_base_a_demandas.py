# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:15:04 2024

@author: Usuario
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.stats import gaussian_kde
from scipy.stats import norm
from scipy.stats import lognorm

import random

# Ruta del archivo CSV de demanda real
csv_path = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\balance_real_ID21_pruebas.csv"

# Cargar datos del archivo CSV en un DataFrame
datos_demand = pd.read_csv(csv_path)
datos_demand = datos_demand.rename(columns={'index': 'Fecha'})
time_sequence = pd.date_range('15:00', periods=len(datos_demand), freq='10T').strftime('%H:%M:%S')
datos_demand['Time']=time_sequence


def generar_modelo_demand(df, days, num_samples=1000):
    # Convertir la columna de tiempo a tipo timedelta
    df['Time'] = pd.to_datetime(df['Time']).dt.time
        
    # Ajustar una distribución de probabilidad diferente para cada registro horario
    distribuciones_por_hora = {}
    for hora in range(24):
        for minuto in range(0, 60, 10):  # Incremento de 10 minutos
            # Filtrar los datos para la hora y minuto actuales
            time_actual = pd.to_timedelta(f'{hora:02}:{minuto:02}:00')
            demanda_real_hora = df[df['Time'] == time_actual]['Demanda'].values
            # Tu lógica para ajustar las distribuciones de probabilidad y generar datos sintéticos
            # Verificar si hay suficientes datos para ajustar una distribución
            if len(demanda_real_hora) >= 2:  # Se necesitan al menos dos puntos para ajustar una distribución
                # Ajustar una distribución lognormal
                mu, sigma = np.log(demanda_real_hora.mean()), demanda_real_hora.std()
                kde = lognorm(s=sigma, scale=np.exp(mu))
            else:
                # Si no hay suficientes datos, utiliza una estrategia alternativa (por ejemplo, distribución uniforme)
                kde = None
        
            distribuciones_por_hora[(hora, minuto)] = kde
    
    # Generar datos de demanda sintética para cada registro horario
    demanda_sintetica = []
    for _, row in df.iterrows():
        hora_actual = row['Time'].hour * 6 + row['Time'].minute // 10
        kde_hora = distribuciones_por_hora[(row['Time'].hour, row['Time'].minute)]

        if kde_hora is not None:
            # Generar valores sintéticos para cada registro horario basados en la distribución de la hora actual
            samples = kde_hora.rvs(size=num_samples)
            samples = samples.clip(min=0)  # Truncar valores negativos a cero
            random_sample = np.random.choice(samples)
            demanda_sintetica.append(float(random_sample))  # Convertirlo a float si es necesario
        else:
            # Si no se ajustó una distribución, utilizar un valor aleatorio cercano al promedio de esa hora
            demanda_media_hora = df[(df['Time'] == row['Time'])]['Demanda'].mean()
            demanda_sintetica.append(max(float(np.random.normal(loc=demanda_media_hora, scale=demanda_media_hora*0.59)), 0))  # Asegurar que no sea negativo

    # Concatenar los datos sintéticos en un DataFrame
    datos_sinteticos = pd.DataFrame({'Demanda': demanda_sintetica})

    return datos_sinteticos





# Generar el modelo de demanda sintético para 30 días
modelo_demand = generar_modelo_demand(datos_demand, days=197)
time_sequence = pd.date_range('15:00', periods=len(modelo_demand), freq='10T').strftime('%H:%M:%S')
modelo_demand['Time']=time_sequence

# Visualizar los primeros datos generados
print(modelo_demand.head())

# Visualizar la demanda sintética
plt.figure(figsize=(10, 6))
datos_demand['Demanda'].plot()
plt.title('Modelo original')
plt.xlabel('Tiempo')
plt.ylabel('Demanda')
plt.grid(True)
plt.show()

# Visualizar la demanda sintética
plt.figure(figsize=(10, 6))
modelo_demand['Demanda'].plot()
plt.title('Modelo de Demanda Sintético')
plt.xlabel('Tiempo')
plt.ylabel('Demanda')
plt.grid(True)
plt.show()

def plot_demand_boxplot(df, column_name, dataframe_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(df[column_name].groupby(df['Time']).apply(list), showfliers=False)
    ax.set_xlabel('Hora del día')
    ax.set_ylabel(column_name.capitalize())
    ax.set_title(f'Boxplot de {column_name.capitalize()} por hora del día - DataFrame: {dataframe_name.capitalize()}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Ejemplo de uso:
plot_demand_boxplot(datos_demand, 'Demanda', 'datos_demand')
plot_demand_boxplot(modelo_demand, 'Demanda','modelo_demand')
print(modelo_demand.head())
