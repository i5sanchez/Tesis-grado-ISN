import os
import pandas as pd

# Carpeta donde se encuentran los archivos CSV
carpeta_generacion = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar"

# Lista para almacenar los DataFrames de generación y potencia pico del sistema
archivos_generacion = []

# Leer los archivos de generación
for nombre_archivo in os.listdir(carpeta_generacion):
    if nombre_archivo.startswith("generacion_") and nombre_archivo.endswith(".csv"):
        ruta_archivo = os.path.join(carpeta_generacion, nombre_archivo)
        df_generacion = pd.read_csv(ruta_archivo)
        archivos_generacion.append((ruta_archivo, df_generacion))

# Archivos de consumo
consumo_1 = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\output_file_t1.csv", header=0)
consumo_2 = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\output_file_t2.csv", header=0)
consumo_3 = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\output_file_t3.csv", header=0)
consumo_4 = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\output_file_t4.csv", header=0)

archivos_consumo = [consumo_1, consumo_2, consumo_3, consumo_4]

# Define listas de valores de capacidad de la batería, nombres de archivos de generación y nombres de archivos de consumo
capacidades_bateria = [89,500, 1000, 1500, 2000, 2500,3000,4000,5000,10e3,25e3,50e3]  # Valores de capacidad de la batería en Wh

def calcular_surplus(generacion_file, consumo_file, cap_bat, potencia_pico_sistema):
    # Leer los archivos de generación y consumo
    generacion = generacion_file
    consumo = consumo_file

    # Seleccionar cada minuto de consumo y ajustar el índice
    consumo_f = consumo[consumo.index % 60 == 0]
    consumo_f.index = range(1, len(consumo_f) + 1)

    # Concatenar los DataFrames de generación y consumo
    df_junto = pd.concat([generacion, consumo_f], axis=1)

    # Multiplicar por 1000 los valores de la columna 'electricity' para pasar de kW a W
    df_junto['electricity'] *= 1000
    df_junto.rename(columns={'0': 'demanda'}, inplace=True)
    df_junto.rename(columns={'electricity': 'generacion'}, inplace=True)

    # Inicializar la columna 'carga_bat' con ceros
    df_junto['carga_bat'] = 0

    # Iterar sobre cada fila del DataFrame
    for i in range(1, len(df_junto)):
        # Calcular la diferencia entre generación y demanda en el período actual
        flujos_bat = df_junto.at[i, 'generacion'] - df_junto.at[i, 'demanda']

        # Calcular la carga de la batería en el período actual
        carga_bat_actual = df_junto.at[i - 1, 'carga_bat'] + flujos_bat

        # Limitar la carga de la batería entre 0 y la capacidad de la batería
        carga_bat_actual = max(0, min(carga_bat_actual, cap_bat))

        # Actualizar la carga de la batería en el DataFrame
        df_junto.at[i, 'carga_bat'] = carga_bat_actual

        # Calcular el excedente de energía (si la carga supera el límite)
        if carga_bat_actual == cap_bat:
            df_junto.at[i, 'surplus'] = -(cap_bat - flujos_bat - df_junto.at[i - 1, 'carga_bat'])
        else:
            df_junto.at[i, 'surplus'] = 0

    # Calcular la suma total de la columna 'surplus' o energía desperdiciada en Wh
    suma_surplus = round(df_junto['surplus'].sum()/1000)

    # Calcular la capacidad de la batería en kWh
    cap_bat_kwh = cap_bat / 1000

    # Calcular la potencia pico del sistema en kW
    potencia_pico_sistema_kw = potencia_pico_sistema

    return suma_surplus, cap_bat_kwh, potencia_pico_sistema_kw

resultados_consumo_1 = []
resultados_consumo_2 = []
resultados_consumo_3 = []
resultados_consumo_4 = []

# Carpeta donde se encuentran los archivos CSV de consumo
carpeta_consumo = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar"

# Itera sobre los valores de capacidad de la batería, archivos de generación y nombres de archivos de consumo
for cap_bat in capacidades_bateria:
    for ruta_generacion, generacion_file in archivos_generacion:
        for index, consumo_file in enumerate(archivos_consumo):
            # Obtener el nombre del archivo de generación
            nombre_archivo_generacion = os.path.basename(ruta_generacion)
            # Obtener la potencia pico del sistema del nombre del archivo de generación
            potencia_pico_sistema = float(os.path.splitext(nombre_archivo_generacion)[0].split("_")[-1].replace("kwp", ""))
            # Obtener el nombre del archivo de consumo
            nombre_consumo = "output_file_t{}.csv".format(index + 1)
            
            surplus_energy, cap_bat_kwh, potencia_pico_sistema_kw = calcular_surplus(generacion_file, consumo_file, cap_bat, potencia_pico_sistema)
            if index == 0:
                resultados_consumo_1.append((cap_bat_kwh, potencia_pico_sistema_kw, surplus_energy))
            elif index == 1:
                resultados_consumo_2.append((cap_bat_kwh, potencia_pico_sistema_kw, surplus_energy))
            elif index == 2:
                resultados_consumo_3.append((cap_bat_kwh, potencia_pico_sistema_kw, surplus_energy))
            elif index == 3:
                resultados_consumo_4.append((cap_bat_kwh, potencia_pico_sistema_kw, surplus_energy))

# Convertir los resultados en DataFrames
df_consumo_1 = pd.DataFrame(resultados_consumo_1, columns=["Capacidad (kWh)", "Potencia pico (kW)", "Surplus energy (kWh)"])
df_consumo_2 = pd.DataFrame(resultados_consumo_2, columns=["Capacidad (kWh)", "Potencia pico (kW)", "Surplus energy (kWh)"])
df_consumo_3 = pd.DataFrame(resultados_consumo_3, columns=["Capacidad (kWh)", "Potencia pico (kW)", "Surplus energy (kWh)"])
df_consumo_4 = pd.DataFrame(resultados_consumo_4, columns=["Capacidad (kWh)", "Potencia pico (kW)", "Surplus energy (kWh)"])

# Imprimir los DataFrames
print("Resultados para consumo_1:")
print(df_consumo_1)
print("\nResultados para consumo_2:")
print(df_consumo_2)
print("\nResultados para consumo_3:")
print(df_consumo_3)
print("\nResultados para consumo_4:")
print(df_consumo_4)


# Exportar los DataFrames de consumo como archivos CSV
df_consumo_1.to_csv(os.path.join(carpeta_consumo, "df_consumo_1.csv"), index=False)
df_consumo_2.to_csv(os.path.join(carpeta_consumo, "df_consumo_2.csv"), index=False)
df_consumo_3.to_csv(os.path.join(carpeta_consumo, "df_consumo_3.csv"), index=False)
df_consumo_4.to_csv(os.path.join(carpeta_consumo, "df_consumo_4.csv"), index=False)
