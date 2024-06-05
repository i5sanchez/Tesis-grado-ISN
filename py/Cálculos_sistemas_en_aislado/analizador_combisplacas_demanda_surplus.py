# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:34:46 2024

@author: Usuario
"""

import pandas as pd

# Lista para almacenar los DataFrames importados
dataframes = []

# Ruta base de los archivos CSV
base_path = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\"


# Nombres de los archivos CSV
csv_files = ["modelo_demand1.csv", "modelo_demand2.csv", "modelo_demand3.csv", "modelo_demand4.csv"]

modelo_demand1 = pd.read_csv(base_path + csv_files[0])
modelo_demand2 = pd.read_csv(base_path + csv_files[1])
modelo_demand3 = pd.read_csv(base_path + csv_files[2])
modelo_demand4 = pd.read_csv(base_path + csv_files[3])

# Bucle para importar los archivos CSV
for csv_file in csv_files:
    # Importar el DataFrame desde el archivo CSV
    df = pd.read_csv(base_path + csv_file)
    # Agregar el DataFrame a la lista
    dataframes.append(df)

# Ahora puedes acceder a los DataFrames importados a través de la lista 'dataframes'
# Sumar los valores de la columna 'Demanda' de cada DataFrame
suma_demandas = dataframes[0].copy()  # Creamos una copia del primer DataFrame
for df in dataframes[1:]:
    suma_demandas['Demanda'] += df['Demanda']  # Sumamos los valores de la columna 'Demanda'

# Importar el DataFrame desde el archivo CSV generacion_0.05kwp.csv
generacion_0_05kwp_df = pd.read_csv(base_path + "generacion_0.05kwp.csv")

# Importar el DataFrame desde el archivo CSV generacion_0.02kwp.csv
generacion_0_02kwp_df = pd.read_csv(base_path + "generacion_0.02kwp.csv")

# Cambiar el nombre de la columna 'electricity' en generacion_0_05kwp_df a 'gen50'
generacion_0_05kwp_df = generacion_0_05kwp_df.rename(columns={'electricity': 'gen50'})

# Cambiar el nombre de la columna 'electricity' en generacion_0_02kwp_df a 'gen20'
generacion_0_02kwp_df = generacion_0_02kwp_df.rename(columns={'electricity': 'gen20'})

# Eliminar la columna 'time' de generacion_0_05kwp_df
generacion_0_05kwp_df.drop(columns=['time'], inplace=True)

# Eliminar la columna 'time' de generacion_0_02kwp_df
generacion_0_02kwp_df.drop(columns=['time'], inplace=True)


generacion_0_02kwp_df['gen20']*=1000
generacion_0_05kwp_df['gen50']*=1000

def preparar_datos(df):
    # Seleccionar filas cuyos índices sean múltiplos de 60
    df_filtrado = df[df.index % 6 == 0]

    # Reindexar el DataFrame para tener índices numéricos comenzando desde 1
    df_filtrado.index = range(1, len(df_filtrado) + 1)

    # Obtener la longitud del DataFrame filtrado
    longitud_df_filtrado = len(df_filtrado)

    # Truncar o expandir los datos para que tengan la misma longitud que el DataFrame filtrado
    df_truncado = df.iloc[:longitud_df_filtrado]

    # Resetear el índice del DataFrame filtrado para que comience en 0
    df_filtrado.reset_index(drop=True, inplace=True)

    return df_filtrado

suma_demandas_f=preparar_datos(suma_demandas)
"""
# Seleccionar filas cuyos índices sean múltiplos de 60
suma_demandas_f = suma_demandas[suma_demandas.index % 6 == 0]

# Reindexar el DataFrame para tener índices numéricos comenzando desde 1
suma_demandas_f.index = range(1, len(suma_demandas_f) + 1)

# Obtener la longitud de suma_demandas_f
longitud_suma_demandas_f = len(suma_demandas_f)

# Truncar o expandir los datos de generación para que tengan la misma longitud que suma_demandas_f
generacion_005kwp_truncado = generacion_0_05kwp_df.iloc[:longitud_suma_demandas_f]
generacion_002kwp_truncado = generacion_0_02kwp_df.iloc[:longitud_suma_demandas_f]

# Resetear el índice de suma_demandas_f para que comience en 0
suma_demandas_f.reset_index(drop=True, inplace=True)
"""
dfs = []
"""
# Definir los multiplicadores para cada tipo de panel solar (20 y 50 Wp)
multiplicadores_20 = [0, 1, 2]
multiplicadores_50 = [i for i in range(80)]  # 20 multiplicadores para cubrir un amplio rango

# Iterar sobre los multiplicadores para los paneles de 50 Wp
for mult_50 in multiplicadores_50:

    # Iterar sobre los multiplicadores para los paneles de 20 Wp
    for mult_20 in multiplicadores_20:
        # Concatenar los DataFrames suma_demandas_f y generacion_005kwp_df
        df = pd.concat([suma_demandas_f, generacion_0_05kwp_df], axis=1)

        # Crear una nueva columna para los multiplicadores
        df['num_pan20'] = mult_20
        
        # Aplicar el multiplicador a la columna 'gen50'
        df['gen'] = df['gen50'] * mult_50
        #df['num_pan50'] = mult_50

        # Si el multiplicador de gen20 es mayor que 0, agregar generación de 20 Wp
        if mult_20 > 0:
            # Concatenar el DataFrame generacion_002kwp_truncado
            
            # Aplicar el multiplicador a la columna 'gen20'
            df['gen'] += generacion_0_02kwp_df['gen20'] * mult_20

        
       
        # Agregar el DataFrame a la lista
        dfs.append(df)
    df['num_pan50'] = mult_50

# Eliminar las columnas 'gen20', 'gen50' y 'local_time' de todos los DataFrames en la lista
for df in dfs:
    df.drop(columns=['gen50', 'local_time'], inplace=True)
"""

def crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, suma_demandas_f, cat_Pgen):
    dfs = []
    # Definir los multiplicadores para cada tipo de panel solar (20 y 50 Wp)
    multiplicadores_20 = [0, 1, 2]
    multiplicadores_50 = [i for i in range(80)]  # 20 multiplicadores para cubrir un amplio rango

    # Iterar sobre los multiplicadores para los paneles de 50 Wp
    for mult_50 in multiplicadores_50:
        # Iterar sobre los multiplicadores para los paneles de 20 Wp
        for mult_20 in multiplicadores_20:
            # Concatenar los DataFrames suma_demandas_f y generacion_005kwp_df
            df = pd.concat([suma_demandas_f, generacion_0_05kwp_df], axis=1)

            # Crear una nueva columna para los multiplicadores
            df['num_pan20'] = mult_20
            
            # Aplicar el multiplicador a la columna 'gen50'
            df['gen'] = df['gen50'] * mult_50

            # Si el multiplicador de gen20 es mayor que 0, agregar generación de 20 Wp
            if mult_20 > 0:
                # Concatenar el DataFrame generacion_0_02kwp_df
                df['gen'] += generacion_0_02kwp_df['gen20'] * mult_20

            # Agregar el DataFrame a la lista
            dfs.append(df)

    # Eliminar las columnas 'gen20', 'gen50' y 'local_time' de todos los DataFrames en la lista
    for df in dfs:
        df.drop(columns=['gen50', 'local_time'], inplace=True)

    # Devolver el DataFrame específico de acuerdo con cat_Pgen
    return dfs


# Llamada a la función y almacenamiento del resultado en la variable 'dfs'
cat_Pgen1=2
modelo_demand1_f=preparar_datos(modelo_demand1)
modelo_demand2_f=preparar_datos(modelo_demand2)
modelo_demand3_f=preparar_datos(modelo_demand3)
modelo_demand4_f=preparar_datos(modelo_demand4)

dfs = crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, suma_demandas_f,cat_Pgen1)

dfs_t1o2_1 = crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df,modelo_demand1_f,cat_Pgen1)
dfs_t1o2_2=crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, modelo_demand2_f,cat_Pgen1)
dfs_t1o2_3=crear_dfs(generacion_0_05kwp_df,generacion_0_02kwp_df, modelo_demand3_f,cat_Pgen1)
dfs_t1o2_4=crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, modelo_demand4_f,cat_Pgen1)

def calcular_surplus_energy(cap_bat, df):
    # Inicializar la columna 'carga_bat' con ceros
    df['carga_bat'] = 0
    df['surplus'] = 0
    
    # Iterar sobre cada fila del DataFrame
    for i in range(1, len(df)):
        # Calcular la diferencia entre generación y demanda en el período actual
        flujos_bat = df.at[i, 'gen'] - df.at[i, 'Demanda']
        
        # Calcular la carga de la batería en el período actual
        carga_bat_actual = df.at[i - 1, 'carga_bat'] + flujos_bat
        
        # Limitar la carga de la batería entre 0 y la capacidad de la batería
        carga_bat_actual = max(0, min(carga_bat_actual, cap_bat))
        
        # Actualizar la carga de la batería en el DataFrame
        df.at[i, 'carga_bat'] = carga_bat_actual
    
        # Calcular el excedente de energía (si la carga supera el límite)
        if carga_bat_actual == cap_bat:
            df.at[i, 'surplus'] = -(cap_bat - flujos_bat - df.at[i - 1, 'carga_bat']) 
        else:
            df.at[i, 'surplus'] = 0
    
    # Calcular la suma total de la columna 'surplus' o energía desperdiciada en Wh
    suma_surplus = round(df['surplus'].sum())
    
    return suma_surplus


def calcular_energia_insatisfecha(cap_bat, df):
    # Inicializar la columna 'carga_bat' con ceros
    df['carga_bat'] = 0
    df['energia_insatisfecha'] = 0
    
    # Iterar sobre cada fila del DataFrame
    for i in range(1, len(df)):
        # Calcular la diferencia entre generación y demanda en el período actual
        flujos_bat = df.at[i, 'gen'] - df.at[i, 'Demanda']
        
        # Calcular la carga de la batería en el período actual
        carga_bat_actual = df.at[i - 1, 'carga_bat'] + flujos_bat
        
        # Limitar la carga de la batería entre 0 y la capacidad de la batería
        carga_bat_actual = max(0, min(carga_bat_actual, cap_bat))
        
        # Actualizar la carga de la batería en el DataFrame
        df.at[i, 'carga_bat'] = carga_bat_actual
    
        # Calcular la energía insatisfecha (si la carga no cubre toda la demanda)
        if carga_bat_actual + df.at[i, 'gen'] < df.at[i, 'Demanda']:
            df.at[i, 'energia_insatisfecha'] = df.at[i, 'Demanda'] - df.at[i, 'gen'] - carga_bat_actual
        else:
            df.at[i, 'energia_insatisfecha'] = 0
    
    # Calcular la suma total de la columna 'energia_insatisfecha' en Wh
    energia_insatisfecha_total = round(df['energia_insatisfecha'].sum())
    
    return energia_insatisfecha_total

def calcular_generada_y_consumida(cap_bat, df):
    # Calcular la energía total generada sumando todos los valores de la columna 'gen'
    energia_generada = df['gen'].sum()
    
    # Calcular la energía total consumida sumando todos los valores de la columna 'Demanda'
    energia_consumida = df['Demanda'].sum()
    
    return energia_generada, energia_consumida

def calcular_surplus_e_insatisfecha(cap_bat, df):
    # Calcular surplus energy
    surplus_energy = calcular_surplus_energy(cap_bat, df)
    
    # Calcular energía insatisfecha
    energia_insatisfecha = calcular_energia_insatisfecha(cap_bat, df)
    
    return surplus_energy, energia_insatisfecha

num_bat = 2

cap_bat = 89*num_bat #capacidad de la batería en Wh

def calcular_y_mostrar_resultados(cap_bat, df, nombre_df):
    """
    Calcula y muestra los resultados de energía generada, consumida, surplus energy y energía insatisfecha.

    Parameters:
    - cap_bat (float): Capacidad de la batería en Wh.
    - df (DataFrame): DataFrame que contiene las columnas de demanda y generación de energía.
    - nombre_df (str): Nombre del DataFrame.
    """
    # Calcular energía generada y consumida
    energia_generada, energia_consumida = calcular_generada_y_consumida(cap_bat, df)
    
    # Calcular surplus energy y energía insatisfecha
    surplus_energy, energia_insatisfecha = calcular_surplus_e_insatisfecha(cap_bat, df)
    

    # Calcular la proporción de energía insatisfecha respecto a la energía demandada
    proporcion_insatisfecha = (energia_insatisfecha / df['Demanda'].sum()) * 100 if df['Demanda'].sum() != 0 else 0
    
    # Redondear los resultados
    energia_generada = round(energia_generada)
    energia_consumida = round(energia_consumida)
    surplus_energy = round(surplus_energy)
    energia_insatisfecha = round(energia_insatisfecha)
    proporcion_insatisfecha = round(proporcion_insatisfecha, 2)  # Redondear a dos decimales

    # Mostrar los resultados
    print("Resultados para el DataFrame '{}':".format(nombre_df))
    print("Energía total generada: {} Wh".format(energia_generada))
    print("Energía total consumida: {} Wh".format(energia_consumida))
    print("Surplus energy: {} Wh".format(surplus_energy))
    print("Energía demandada no suministrada: {} Wh".format(energia_insatisfecha))
    print("Proporción de energía insatisfecha respecto a la demanda: {}%".format(proporcion_insatisfecha))
    return energia_generada, energia_consumida, surplus_energy, energia_insatisfecha, proporcion_insatisfecha

#energia_generada, energia_consumida, surplus_energy, energia_insatisfecha, proporcion_insatisfecha = calcular_y_mostrar_resultados(cap_bat, dfs[cat_Pgen])

def calcular_y_mostrar_resultados_(cap_bat, cat_Pgen, num_bat, dfs, nombre_df):
    calcular_y_mostrar_resultados(cap_bat, dfs[cat_Pgen],nombre_df)
    if cat_Pgen % 3 == 0 or cat_Pgen == 0:
        num_20 = 0
    elif (cat_Pgen - 1) % 3 == 0 or cat_Pgen == 1:
        num_20 = 1
    else:
        num_20 = 2

    num_50 = cat_Pgen // 3
    potinst = num_20 * 20 + num_50 * 50
    precio_u_bat = 160.61
    precio_u_panel_20 = 29.66
    precio_u_panel_50 = 67.45
    precioUSDw_regulador = 1.2

    if potinst <= 120:
        potreg = 120
    elif 240 >= potinst > 120:
        potreg = 240
    elif 240 < potinst <= 360:
        potreg = 360
    elif 360 < potinst <= 480:
        potreg = 480
    elif 480 < potinst <= 600:
        potreg = 600
    elif 600 < potinst <= 720:
        potreg = 720
    elif 720 < potinst <= 960:
        potreg = 960
    else:
        potreg = potinst

    precioreg = potreg * precioUSDw_regulador

    precio_total = precio_u_bat * num_bat + precio_u_panel_20 * num_20 + precio_u_panel_50 * num_50 + precioreg
    precio_total_redondeado = round(precio_total, 2)
    preciobs = round(precio_total * 6.93, 2)

    print("Con {} paneles de 20 Wp, {} paneles de 50 Wp y {} baterías de 89 Wh.".format(num_20, num_50, num_bat))
    print("El precio del conjunto de baterías, paneles y reguladores para el DataFrame {} sería de {} $ USD o {} Bs.".format(nombre_df, precio_total_redondeado, preciobs))

    # Llamamos a la función que quieres ejecutar
    calcular_y_mostrar_resultados(cap_bat, dfs[cat_Pgen],nombre_df)
num_bat1=1
calcular_y_mostrar_resultados_(cap_bat, cat_Pgen1, num_bat1, dfs_t1o2_1, "de la vivienda 1 aislada en picogrid")
calcular_y_mostrar_resultados_(cap_bat, cat_Pgen1, num_bat1, dfs_t1o2_2, "de la vivienda 2 aislada en picogrid")
calcular_y_mostrar_resultados_(cap_bat, cat_Pgen1, num_bat1, dfs_t1o2_3, "de la vivienda 3 aislada en picogrid")
calcular_y_mostrar_resultados_(cap_bat, cat_Pgen1, num_bat1, dfs_t1o2_4, "de la vivienda 4 aislada en picogrid")


"""
precio_Bs_base_mes=16.6
energ_mensual= energia_consumida//12
if energ_mensual<21000:
    prec_energ_Bs_mes = precio_Bs_base_mes
elif 21000<energ_mensual<71000:
    prec_energ_Bs_mes= 0.649*energ_mensual
elif 71000<energ_mensual<121000:
    prec_energ_Bs_mes= 0.744*energ_mensual
elif 121e3<energ_mensual<501e3:
    prec_energ_Bs_mes= 0.871*energ_mensual
elif 501e3<energ_mensual<1001e3:
    prec_energ_Bs_mes= 1.074*energ_mensual
elif energ_mensual>1001e3:
    prec_energ_Bs_mes= 1.414*energ_mensual
cargo_mensual_pot = potinst/1000 *94.351
subtotal = cargo_mensual_pot+prec_energ_Bs_mes
impuesto = 0.01*subtotal
total_mes = subtotal+impuesto
Payback = round(preciobs/total_mes,2)

print("Esto supondría un payback de {} meses o {} años".format(Payback,round(Payback/12)))
"""
