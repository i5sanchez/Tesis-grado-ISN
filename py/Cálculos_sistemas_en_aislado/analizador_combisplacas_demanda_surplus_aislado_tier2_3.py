# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:15:31 2024

@author: Usuario
"""


import pandas as pd

cat_Pgen2= 3
num_bat = 2
cap_bat = 89*num_bat #capacidad de la batería en Wh

# Lista para almacenar los DataFrames importados
dataframes = []

# Ruta base de los archivos CSV
base_path = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\"


# Nombres de los archivos CSV
csv_files = ["modelo_demand1.csv", "modelo_demand2.csv", "modelo_demand3.csv", "modelo_demand4.csv","packextra_tier2_3_365.csv"]

modelo_demand1 = pd.read_csv(base_path + csv_files[0])
modelo_demand2 = pd.read_csv(base_path + csv_files[1])
modelo_demand3 = pd.read_csv(base_path + csv_files[2])
modelo_demand4 = pd.read_csv(base_path + csv_files[3])
df_extra= pd.read_csv(base_path + csv_files[4])

# Renombrar la columna '0' a 'Demanda'
df_extra = df_extra.rename(columns={'0': 'Demanda'})
# Seleccionar filas cuyos índices sean múltiplos de 6
#df_extra = df_extra[df_extra.index % 60 == 0]

# Reindexar el DataFrame para tener índices numéricos comenzando desde 1
df_extra.reset_index(drop=True, inplace=True)

# Bucle para importar los archivos CSV
for csv_file in csv_files:
    # Importar el DataFrame desde el archivo CSV
    df = pd.read_csv(base_path + csv_file)
    # Agregar el DataFrame a la lista
    dataframes.append(df)
# Sumar la demanda de df_extra a cada modelo de demanda
modelo_demand1['Demanda'] += df_extra['Demanda']
modelo_demand2['Demanda'] += df_extra['Demanda']
modelo_demand3['Demanda'] += df_extra['Demanda']
modelo_demand4['Demanda'] += df_extra['Demanda']

# Redondear los valores de demanda a dos decimales en cada modelo de demanda

modelo_demand1['Demanda'] = modelo_demand1['Demanda'].round(2)
modelo_demand2['Demanda'] = modelo_demand2['Demanda'].round(2)
modelo_demand3['Demanda'] = modelo_demand3['Demanda'].round(2)
modelo_demand4['Demanda'] = modelo_demand4['Demanda'].round(2)

modelo_demand1_sf=modelo_demand1
modelo_demand2_sf=modelo_demand2
modelo_demand3_sf=modelo_demand3
modelo_demand4_sf=modelo_demand4

def preparar_datos(df):
    # Seleccionar filas cuyos índices sean múltiplos de 60
    df_filtrado = df[df.index % 6 == 0]

    # Reindexar el DataFrame para tener índices numéricos comenzando desde 1
    df_filtrado.index = range(1, len(df_filtrado) + 1)

    # Resetear el índice del DataFrame filtrado para que comience en 0
    df_filtrado.reset_index(drop=True, inplace=True)

    return df_filtrado
modelo_demand1f=preparar_datos(modelo_demand1).round(2)
modelo_demand2f=preparar_datos(modelo_demand2).round(2)
modelo_demand3f=preparar_datos(modelo_demand3).round(2)
modelo_demand4f=preparar_datos(modelo_demand4).round(2)

def calcular_corriente_dc_max(df, tension_dc):
    """
    Calcula la corriente de la potencia DC utilizando el máximo valor de potencia.

    Parameters:
    - df (DataFrame): DataFrame que contiene la columna 'Demanda'.
    - tension_dc (float): Tensión en voltios (V).

    Returns:
    - corriente_dc (float): Corriente en amperios (A).
    """
    max_potencia = df['Demanda'].max()  # Obtener el máximo valor de potencia de la columna 'Demanda'
    corriente_dc = max_potencia / tension_dc
    return corriente_dc
tension_dc=12 #V
max_corr_b_1=calcular_corriente_dc_max(modelo_demand1f, tension_dc)
max_corr_b_2=calcular_corriente_dc_max(modelo_demand2f, tension_dc)
max_corr_b_3=calcular_corriente_dc_max(modelo_demand3f, tension_dc)
max_corr_b_4=calcular_corriente_dc_max(modelo_demand4f, tension_dc)

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



dfs_t2o3_1 = crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df,modelo_demand1f,cat_Pgen2)
dfs_t2o3_2=crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, modelo_demand2f,cat_Pgen2)
dfs_t2o3_3=crear_dfs(generacion_0_05kwp_df,generacion_0_02kwp_df, modelo_demand3f,cat_Pgen2)
dfs_t2o3_4=crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, modelo_demand4f,cat_Pgen2)

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

def calcular_generada_y_demandada(cap_bat, df):
    # Calcular la energía total generada sumando todos los valores de la columna 'gen'
    energia_generada = df['gen'].sum()
    
    # Calcular la energía total demandada sumando todos los valores de la columna 'Demanda'
    energia_demandada = df['Demanda'].sum()
    
    return energia_generada, energia_demandada

def calcular_surplus_e_insatisfecha(cap_bat, df):
    
    



    # Calcular surplus energy
    surplus_energy = calcular_surplus_energy(cap_bat, df)
    
    # Calcular energía insatisfecha
    energia_insatisfecha = calcular_energia_insatisfecha(cap_bat, df)
    
    return surplus_energy, energia_insatisfecha


def calcular_y_mostrar_resultados(cap_bat, df, nombre_df):
    """
    Calcula y muestra los resultados de energía generada, demandada, surplus energy y energía insatisfecha.

    Parameters:
    - cap_bat (float): Capacidad de la batería en Wh.
    - df (DataFrame): DataFrame que contiene las columnas de demanda y generación de energía.
    - nombre_df (str): Nombre del DataFrame.
    """
    # Calcular energía generada y demandada
    energia_generada, energia_demandada = calcular_generada_y_demandada(cap_bat, df)
    
    # Calcular surplus energy y energía insatisfecha
    surplus_energy, energia_insatisfecha = calcular_surplus_e_insatisfecha(cap_bat, df)
    

    # Calcular la proporción de energía insatisfecha respecto a la energía demandada
    proporcion_insatisfecha = (energia_insatisfecha / df['Demanda'].sum()) * 100 if df['Demanda'].sum() != 0 else 0
    
    # Redondear los resultados
    energia_generada = round(energia_generada)
    energia_demandada = round(energia_demandada)
    surplus_energy = round(surplus_energy)
    energia_insatisfecha = round(energia_insatisfecha)
    proporcion_insatisfecha = round(proporcion_insatisfecha, 2)  # Redondear a dos decimales

    # Mostrar los resultados
    print("Resultados para el DataFrame '{}':".format(nombre_df))
    print("Energía total generada: {} Wh".format(energia_generada))
    print("Energía total demandada: {} Wh".format(energia_demandada))
    print("Surplus energy: {} Wh".format(surplus_energy))
    print("Energía demandada no suministrada: {} Wh".format(energia_insatisfecha))
    print("Proporción de energía insatisfecha respecto a la demanda: {}%".format(proporcion_insatisfecha))
    return energia_generada, energia_demandada, surplus_energy, energia_insatisfecha, proporcion_insatisfecha

def calcular_y_mostrar_resultados_(cap_bat, cat_Pgen, num_bat, dfs, nombre_df):
    calcular_y_mostrar_resultados(cap_bat, dfs[cat_Pgen],nombre_df)
    energia_generada, energia_demandada, surplus_energy, energia_insatisfecha, proporcion_insatisfecha = calcular_y_mostrar_resultados(cap_bat, dfs[cat_Pgen],nombre_df)
    if cat_Pgen % 3 == 0 or cat_Pgen == 0:
        num_20 = 0
    elif (cat_Pgen - 1) % 3 == 0 or cat_Pgen == 1:
        num_20 = 1
    else:
        num_20 = 2

    num_50 = cat_Pgen // 3
    potinst = num_20 * 20 + num_50 * 50
    precio_u_bat_bs=1595
    precio_u_panel_20_bs=380
    precio_u_panel_50_bs=780
    precio_u_regulador120W_bs=250
    precio_u_regulador240W_bs=320
    
    precio_u_bat = (precio_u_bat_bs/6.92)
    precio_u_panel_20 = (precio_u_panel_20_bs/6.92)
    precio_u_panel_50 = (precio_u_panel_50_bs/6.92)
    precioUSDw_regulador = 1.2
    if potinst <= 120:
        potreg = 120
        precioreg=precio_u_regulador120W_bs/6.92

    elif 240 >= potinst > 120:
        potreg = 240
        precioreg=precio_u_regulador240W_bs/6.92
    elif 240 < potinst <= 360:
        potreg = 360
        precioreg = potreg * precioUSDw_regulador

    elif 360 < potinst <= 480:
        potreg = 480
        precioreg = potreg * precioUSDw_regulador

    elif 480 < potinst <= 600:
        potreg = 600
        precioreg = potreg * precioUSDw_regulador

    elif 600 < potinst <= 720:
        potreg = 720
        precioreg = potreg * precioUSDw_regulador

    elif 720 < potinst <= 960:
        potreg = 960
        precioreg = potreg * precioUSDw_regulador

    else:
        potreg = potinst
        precioreg = potreg * precioUSDw_regulador
        
    precio_total = precio_u_bat * num_bat + precio_u_panel_20 * num_20 + precio_u_panel_50 * num_50 + precioreg
    precio_total_redondeado = round(precio_total, 2)
    preciobs = round(precio_total * 6.93, 2)

    def calculate_annual_investment(num_bat, precio_u_bat, num_20, precio_u_panel_20, num_50, precio_u_panel_50, precio_reg):
    # Calcular la inversión anual (Ai)
        Ai = (num_bat / 10) * precio_u_bat + (num_20 * precio_u_panel_20) / 20 + (num_50 * precio_u_panel_50) / 20 + (precio_reg) / 4
        return Ai
    
    def calculate_npc(Io,Ai, discount_rate, period=20):
        # Calcular el NPC usando la inversión anual y una tasa de descuento
        npc =Io + sum(Ai / (1 + discount_rate)**year for year in range(0, period + 1))
        return npc
    
    def calculate_lcoe(npc, energy, discount_rate, period=20):
        # Calcular el denominador del LCOE, que es la suma de la energía anual generada, descontada a valor presente
        energy_present_value_sum = sum(energy / (1 + discount_rate)**year for year in range(0, period + 1))
        
        # Calcular el LCOE
        lcoe = npc / energy_present_value_sum
        return lcoe
    
    energia_consumida = energia_demandada - energia_insatisfecha
    interest_rate=0.08
    energy = (energia_consumida)/1000
    # Calcular Ai, NPC y LCOE
    Ai = calculate_annual_investment(num_bat, precio_u_bat, num_20, precio_u_panel_20, num_50, precio_u_panel_50, precioreg)
    npc = calculate_npc(precio_total,Ai, interest_rate)
    lcoe = round(calculate_lcoe(npc, energy, interest_rate),2)

    print("Con {} paneles de 20 Wp, {} paneles de 50 Wp y {} baterías de 89 Wh.".format(num_20, num_50, num_bat))
    print("El precio del conjunto de baterías, paneles y reguladores para el DataFrame {} sería de {} $ USD o {} Bs.".format(nombre_df, precio_total_redondeado, preciobs))
    print("El precio del conjunto de baterías, paneles y reguladores para el DataFrame {} sería de {} $ USD o {} Bs.".format(nombre_df, precio_total_redondeado, preciobs))
    return precio_total_redondeado,lcoe

calcular_y_mostrar_resultados_(cap_bat, cat_Pgen2, num_bat, dfs_t2o3_1, "de la vivienda 1 aislada en picogrid")
calcular_y_mostrar_resultados_(cap_bat, cat_Pgen2, num_bat, dfs_t2o3_2, "de la vivienda 2 aislada en picogrid")
calcular_y_mostrar_resultados_(cap_bat, cat_Pgen2, num_bat, dfs_t2o3_3, "de la vivienda 3 aislada en picogrid")
calcular_y_mostrar_resultados_(cap_bat, cat_Pgen2, num_bat, dfs_t2o3_4, "de la vivienda 4 aislada en picogrid")

energia_insatisfecha1 = calcular_energia_insatisfecha(cap_bat, dfs_t2o3_1[cat_Pgen2])
energia_insatisfecha2 = calcular_energia_insatisfecha(cap_bat, dfs_t2o3_2[cat_Pgen2])
energia_insatisfecha3 = calcular_energia_insatisfecha(cap_bat, dfs_t2o3_3[cat_Pgen2])
energia_insatisfecha4 = calcular_energia_insatisfecha(cap_bat, dfs_t2o3_4[cat_Pgen2])

surplus_energy1 = calcular_surplus_energy(cap_bat, dfs_t2o3_1[cat_Pgen2])
surplus_energy2 = calcular_surplus_energy(cap_bat, dfs_t2o3_2[cat_Pgen2])
surplus_energy3 = calcular_surplus_energy(cap_bat, dfs_t2o3_3[cat_Pgen2])
surplus_energy4 = calcular_surplus_energy(cap_bat, dfs_t2o3_4[cat_Pgen2])


energia_generada1, energia_demandada1 = calcular_generada_y_demandada(cap_bat, dfs_t2o3_1[cat_Pgen2])
energia_generada2, energia_demandada2 = calcular_generada_y_demandada(cap_bat, dfs_t2o3_2[cat_Pgen2])
energia_generada3, energia_demandada3 = calcular_generada_y_demandada(cap_bat, dfs_t2o3_3[cat_Pgen2])
energia_generada4, energia_demandada4 = calcular_generada_y_demandada(cap_bat, dfs_t2o3_4[cat_Pgen2])


prec1,lcoe = calcular_y_mostrar_resultados_(cap_bat, cat_Pgen2, num_bat, dfs_t2o3_1, '')
prec1_4=round(prec1*4,2)
prop = 100*(energia_insatisfecha1 + energia_insatisfecha2 + energia_insatisfecha3 + energia_insatisfecha4) / (dfs_t2o3_1[cat_Pgen2]['Demanda'].sum() + dfs_t2o3_2[cat_Pgen2]['Demanda'].sum() + dfs_t2o3_3[cat_Pgen2]['Demanda'].sum() + dfs_t2o3_4[cat_Pgen2]['Demanda'].sum())
surp=round((surplus_energy1+surplus_energy2+surplus_energy3+surplus_energy4)/4)
surp_4=surp*4
print('La media de surplus energy es de {} Wh, en equivalencia para 4 viviendas sería de {} Wh.'.format(surp,surp_4))
print('La proporción total de energía insatisfecha es del {} %.'.format(round(prop,3)))
print('El precio por vivienda es de {} USD, y el equivalente para 4 viviendas de esta forma sería de {} USD.'.format(prec1,prec1_4))
print('El LCOE es de {} USD/kWh'.format(lcoe))


"""
modelo_demand1_sf.to_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand1_upg_sf.csv", index=False)
modelo_demand2_sf.to_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand2_upg_sf.csv", index=False)
modelo_demand3_sf.to_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand3_upg_sf.csv", index=False)
modelo_demand4_sf.to_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand4_upg_sf.csv", index=False)
"""