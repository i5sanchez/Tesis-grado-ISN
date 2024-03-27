# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:37:12 2024

@author: Usuario

Info general de los parámetros
Time = Hora
ID = Identificador (identifica el datalogger) (adimensional) (se elimina dado que es irrelevante durante el proceso)
V1 = Tensión batería (mv)
V2 = Tensión USB (mv)
V3 = Tesión panel FV (mV)
I1 = Corriente del Jack (mA)
I2 = Corriente del USB (mA)
I3 = Corriente del sistema de monitoreo (mA)
I4 = Corriente del panel FV (mA)
O1 = Tensión de circuito abierto (Voc) (mV)
O2 = Corriente de cortocircuito (Isc) (mA)
Pgen = Potencia generada (W)
Demanda = Demanda eléctrica (W)
Bat2 = Batería según el nivel de tensión en bornes (Wh)
Bat = Batería según flujos de potencia sin considerar pérdidas (Wh)
Surplus = Energía que se desperdiciaría de no haber conexión con otras cargas (Wh)
Flujo_bateriaWh = Flujo de energía con la batería (positivo = cargando // negativo = descargando) (Wh)
"""
import pandas as pd
import os
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

CapBat = 89 #Wh
# Directorio donde se encuentran los archivos de texto
directorio = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\ID-21"

# Patrón para buscar archivos txt en el directorio
patron = "*.txt"

# Lista para almacenar todos los DataFrames
dataframes = []

# Iterar sobre todos los archivos que coincidan con el patrón
for archivo in sorted(glob(os.path.join(directorio, patron))):
    # Lee el archivo de texto y conviértelo en un DataFrame
    df = pd.read_csv(archivo, delimiter=' ')  # Ajusta el delimitador según corresponda
    # Asegurarse de que la columna 'Time' esté en el formato de fecha de pandas
    #df['Time'] = pd.to_datetime(df['Time'])
    
    # Resetear el índice para convertir la columna de fecha en una columna regular
    df.reset_index(drop=False, inplace=True)
    
    # Agrega el DataFrame a la lista
    dataframes.append(df)

# Concatena todos los DataFrames en uno solo
dataframe_final = pd.concat(dataframes, ignore_index=True)

# Eliminar las filas donde todas las columnas especificadas son 0
dataframe_final = dataframe_final.loc[~(dataframe_final[['V1', 'V2', 'V3', 'I1', 'I2', 'I3', 'I4', 'O1', 'O2']] == 0).all(axis=1)]
dataframe_final.reset_index(drop=True, inplace=True)

# Reiniciar los índices del DataFrame resultante
#dataframe_final.reset_index(drop=True, inplace=True)

# Suponiendo que ya tienes tu DataFrame llamado 'dataframe_final'

# Eliminar la columna 'ID'
dataframe_final.drop(columns=['ID'], inplace=True)
 
# Establecer los valores negativos de la corriente del jack a cero
dataframe_final['I1'] = dataframe_final['I1'].clip(lower=0)
# Establecer los valores negativos de la corriente del USB a cero
dataframe_final['I2'] = dataframe_final['I2'].clip(lower=0)

# Crear la nueva columna 'Potencia Generada'
dataframe_final['Pgen'] = (dataframe_final['V3'] / 1000) * (dataframe_final['I4'] / 1000)
# Crear la nueva columna 'DemUSB'
dataframe_final['DemUSB'] = (dataframe_final['V2'] / 1000) * (dataframe_final['I2'] / 1000)
# Crear la nueva columna 'DemJack'
dataframe_final['DemJack']=(dataframe_final['I1']/1000)*12

# Agregar una columna 'Consumo_Registrador' con el valor constante de 0.3
dataframe_final['DemReg'] = 0.3
dataframe_final['Demanda']=dataframe_final['DemReg']+dataframe_final['DemJack']+dataframe_final['DemUSB']
dataframe_final.drop(columns=['DemReg','DemJack','DemUSB'], inplace=True)

#if dataframe_final['Pgen']>dataframe_final['Demanda']:
 #   dataframe_final['FluxBat'] = (dataframe_final['V1'] / 1000) * (dataframe_final['I4'] / 1000)
#else:
 #   dataframe_final['FluxBat']=dataframe_final['Pgen']-dataframe_final['Demanda']
# Condición de comparación
condicion = dataframe_final['Pgen'] > dataframe_final['Demanda']

# Calcular 'FluxBat' basado en la condición
dataframe_final['FluxBat'] = np.where(condicion, 
                                      (dataframe_final['V1'] / 1000) * (dataframe_final['I4'] / 1000),
                                      dataframe_final['Pgen'] - dataframe_final['Demanda'])

dataframe_final['FluxBatWh']=dataframe_final['FluxBat']*(1/6)
# Normalizar los valores de V1
scaler = MinMaxScaler()
dataframe_final['V1_normalized'] = scaler.fit_transform(dataframe_final[['V1']])

# Definir la relación lineal entre V1 y Bat2
# Aquí se asume una relación lineal simple entre V1 y Bat2
# Puedes ajustar los coeficientes de acuerdo a tu relación esperada
a = 89 / dataframe_final['V1_normalized'].max()  # Escalar V1_normalized al rango [0, 89]
b = 0  # Intercepción

# Calcular los valores de Bat2
dataframe_final['Bat2'] = a * dataframe_final['V1_normalized'] + b

# Eliminar la columna temporal V1_normalized
dataframe_final.drop(columns=['V1_normalized'], inplace=True)

# Inicializar la columna de la batería
dataframe_final['Bat'] = 0

# Iterar sobre cada fila del DataFrame
for i in range(len(dataframe_final)):
    # Si es la primera fila, no hay fila anterior, por lo que cargamos la batería inicial
    if i == 0:
        carga_bat_actual = dataframe_final.at[i, 'Bat2']
    else:
        # Calcular la diferencia entre generación y demanda en el período actual
        flujos_bat = dataframe_final.at[i, 'FluxBatWh']
    
        # Calcular la carga de la batería en el período actual
        carga_bat_actual = dataframe_final.at[i - 1, 'Bat'] + flujos_bat
    
    # Limitar la carga de la batería entre 0 y 89 (cap_bat)
    carga_bat_actual = max(0, min(carga_bat_actual, CapBat))
    
    # Actualizar la carga de la batería en el DataFrame
    dataframe_final.at[i, 'Bat'] = carga_bat_actual
# Calcular la energía excedente que no puede entrar en la batería
exceso_energia = dataframe_final['FluxBatWh'].where(dataframe_final['Bat'] + dataframe_final['FluxBatWh'] > CapBat, 0)
exceso_energia = exceso_energia - (CapBat - dataframe_final['Bat'])

# Asegurarse de que el exceso de energía sea no negativo
exceso_energia = exceso_energia.clip(lower=0)

# Almacenar el exceso de energía en la columna "Surplus"
dataframe_final['Surplus'] = exceso_energia

dataframe_final['Flujo_bateriaWh'] = dataframe_final['FluxBatWh'] - exceso_energia

# Crear la nueva columna 'Flujo_bateriaWh' que resta la energía excedente
if dataframe_final['Bat'].any()<CapBat: 
    dataframe_final['Flujo_bateriaWh'] = dataframe_final['FluxBatWh'] - exceso_energia
else:
    dataframe_final['Flujo_bateriaWh']=0
# Eliminar las columnas 'FluxBat' y 'FluxBatWh'
dataframe_final.drop(columns=['FluxBat', 'FluxBatWh'], inplace=True)

# Graficar Bat2 y Bat
plt.plot(dataframe_final.index, dataframe_final['Bat2'], label='Bat2 Predicted')
plt.plot(dataframe_final.index, dataframe_final['Bat'], label='Bat')
plt.xlabel('Índice')
plt.ylabel('Valor de la Batería')
plt.title('Comparación entre Bat2 y Bat')
plt.legend()
plt.show()
# Especifica la ruta y el nombre de archivo donde deseas guardar el CSV
ruta_archivo_csv = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\balance_real_ID21.csv"

# Exporta el DataFrame a un archivo CSV
dataframe_final.to_csv(ruta_archivo_csv, index=False)

print("DataFrame exportado correctamente a CSV.")