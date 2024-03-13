# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 12:40:29 2024

@author: Sir Sánchez
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# Rutas de los archivos CSV exportados
ruta_consumo_1 = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\df_consumo_1.csv"
ruta_consumo_2 = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\df_consumo_2.csv"
ruta_consumo_3 = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\df_consumo_3.csv"
ruta_consumo_4 = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\df_consumo_4.csv"

# Lista de rutas de archivos CSV
rutas_consumo = [ruta_consumo_1, ruta_consumo_2, ruta_consumo_3, ruta_consumo_4]

# Crear una figura y ejes para cada DataFrame de consumo
for idx, ruta_consumo in enumerate(rutas_consumo):
    # Importar el archivo CSV como DataFrame
    df_consumo = pd.read_csv(ruta_consumo)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extraer los datos de los DataFrames
    potencia_pico = df_consumo['Potencia pico (kW)']
    capacidad_bateria = df_consumo['Capacidad (kWh)']
    surplus_energy = df_consumo['Surplus energy (kWh)']

    # Interpolación
    x = capacidad_bateria
    y = potencia_pico
    z = surplus_energy

    x_range = np.linspace(min(x), max(x), 100)
    y_range = np.linspace(min(y), max(y), 100)
    x_grid, y_grid = np.meshgrid(x_range, y_range)

    z_interp = griddata((x, y), z, (x_grid, y_grid), method='cubic')

    # Gráfico 3D
    ax.plot_surface(x_grid, y_grid, z_interp, cmap='Oranges', edgecolor='none')

    ax.set_xlabel('Capacidad de la batería (kWh)')
    ax.set_ylabel('Potencia pico (kWp)')
    ax.set_zlabel('Surplus energy (kWh)')

    plt.title(f'Gráfico 3D para df_consumo_{idx+1}')
    plt.show()
