# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:14:20 2024

@author: Usuario
"""

import pandas as pd


# Ruta base de los archivos CSV
base_path = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\"
#    VARIABLES
cat_Pgen3=1
num_bat = 1
cap_bat = 89*num_bat #capacidad de la batería en Wh
dist_nodo=2 #m
long_cables=2*(dist_nodo+0.5)

cable_1_5mm=[13.7*(1+1.7e-5*70),30*0.9,1.5,0.2] #[0] es la R en ohm/km a 90º, [1] es la Iz con los cables al sol, [2] sección del cable, [3] USD/metro de cable,  
cable_2_5mm=[8.21*(1+1.7e-5*70),41*0.9,2.5,0.31]
cable_4mm=[5.09*(1+1.7e-5*70),55*0.9,4,0.58]
cable_6mm=[3.39*(1+1.7e-5*70),70*0.9,6,0.9]
cable_10mm=[1.95*(1+1.7e-5*70),98*0.9,10,1.89]
cable_16mm=[1.24*(1+1.7e-5*70),132*0.9,16,2.45]
cable_25mm=[0.795*(1+1.7e-5*70),176*0.9,25,4.18]
cable_35mm=[0.565*(1+1.7e-5*70),218*0.9,35,8.96]
cable_50mm=[0.393*(1+1.7e-5*70),276*0.9,50,11.49]
cable_70mm=[0.277*(1+1.7e-5*70),347*0.9,70,12.86]
cable_95mm=[0.210*(1+1.7e-5*70),416*0.9,95,16.93] 
cable_120mm=[0.164*(1+1.7e-5*70),488*0.9,120,20.99]
cable_150mm=[0.132*(1+1.7e-5*70),566*0.9,150,45.99]
cable_185mm=[0.108*(1+1.7e-5*70),644*0.9,185,51.58]
cable_240mm=[0.0817*(1+1.7e-5*70),644*0.9,240,53.73]

cabl = cable_1_5mm
def paralelo(cable1,cable2):
    R=(cable1[0]*cable2[0])/(cable1[0]+cable2[0])
    Iz=cable1[1]+cable2[1]
    prec_met=cable1[2]+cable2[2]
    cable_final = [R,Iz,prec_met]
    return cable_final

# Importar los archivos CSV
modelo_demand1_upg = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand1_upg.csv")
modelo_demand2_upg = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand2_upg.csv")
modelo_demand3_upg = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand3_upg.csv")
modelo_demand4_upg = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\modelo_demand4_upg.csv")

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
num_50= cat_Pgen3//3
num_20= cat_Pgen3%3
Ppan = num_50*50 + num_20*20
Imax= Ppan/tension_dc


def caidas_tensión(I, cable, long_cables):
    Rohm_m = cable[0] / 1000
    R = Rohm_m * long_cables
    perd_pot = I * I * R
    caida = I * R
    caida_porc = ((caida) / 12) * 100
    precio = cable[2] * long_cables
    cabl = cable
    validez_term = (I + 2 < cable[1])  # Comprobación para todos los elementos de la serie

    return caida, caida_porc, precio, validez_term, perd_pot,cabl

cable_par=paralelo(cable_6mm, cable_6mm)
caida,caida_porc,precio_cables,validez_term,perd_pot,cabl = caidas_tensión(Imax,cabl, dist_nodo*2)


# Crear un DataFrame 'suma_demandas' con una columna llamada 'Demanda'
suma_demandas = pd.DataFrame()# Sumar las columnas de demanda
suma_demandas['Time']=modelo_demand1_upg['Time']

#Procedo a sumar las demandas
suma_demandas['Demanda'] = modelo_demand1_upg['Demanda']+modelo_demand2_upg['Demanda']+modelo_demand3_upg['Demanda']+modelo_demand4_upg['Demanda']


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

def crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, suma_demandas_f, cat_Pgen,tipo_cable,long_cables):
    dfs = []
    # Definir los multiplicadores para cada tipo de panel solar (20 y 50 Wp)
    multiplicadores_20 = [0, 1, 2]
    multiplicadores_50 = [i for i in range(200)]  # 20 multiplicadores para cubrir un amplio rango

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
            # Calcular la caída de tensión en los conductores
            caida, caida_porc, precio, validez_term, perd_pot,cabl = caidas_tensión(df['Demanda']/12, tipo_cable, long_cables)

            # Agregar las columnas de caída de tensión, porcentaje de caída, precio y validez térmica al DataFrame
            df['caida_tension'] = caida
            df['caida_porc'] = caida_porc
            df['precio_cables'] = precio
            df['validez_termica'] = validez_term
            df['perdida_potencia'] = perd_pot
            df['Demanda']+=df['perdida_potencia']
            df['Iz']=tipo_cable[1]
            df['Pz']=tipo_cable[1]*12
            
            # Agregar el DataFrame a la lista
            dfs.append(df)

    # Eliminar las columnas 'gen20', 'gen50' y 'local_time' de todos los DataFrames en la lista
    for df in dfs:
        df.drop(columns=['gen50', 'local_time'], inplace=True)

    # Devolver el DataFrame específico de acuerdo con cat_Pgen
    return dfs
dfs = crear_dfs(generacion_0_05kwp_df, generacion_0_02kwp_df, suma_demandas,cat_Pgen3,cabl,long_cables)

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

def calcular_y_mostrar_resultados_(cap_bat, cat_Pgen, num_bat, dfs, nombre_df,precio_cables):
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
    precio_u_regulador120W=precio_u_regulador120W_bs/6.92
    precio_u_regulador240W=precio_u_regulador240W_bs/6.92

    precio_u_bat = (precio_u_bat_bs/6.92)
    precio_u_panel_20 = (precio_u_panel_20_bs/6.92)
    precio_u_panel_50 = (precio_u_panel_50_bs/6.92)
    precioUSDw_regulador = 1.2

    if potinst <= 120:
        potreg = 120
        precioreg=precio_u_regulador120W

    elif 240 >= potinst > 120:
        potreg = 240
        precioreg=precio_u_regulador240W
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


    precio_total = precio_u_bat * num_bat + precio_u_panel_20 * num_20 + precio_u_panel_50 * num_50 + precioreg + precio_cables
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
    
    energia_consumida = energia_demandada-energia_insatisfecha
    interest_rate=0.08
    energy = (energia_consumida)/1000
    # Calcular Ai, NPC y LCOE
    Ai = calculate_annual_investment(num_bat, precio_u_bat, num_20, precio_u_panel_20, num_50, precio_u_panel_50, precioreg)
    npc = calculate_npc(precio_total,Ai, interest_rate)
    lcoe = round(calculate_lcoe(npc, energy, interest_rate),2)


    print("Con {} paneles de 20 Wp, {} paneles de 50 Wp y {} baterías de 89 Wh.".format(num_20, num_50, num_bat))
    print("El precio del conjunto de baterías, paneles y reguladores para el DataFrame {} sería de {} $ USD o {} Bs.".format(nombre_df, precio_total_redondeado, preciobs))
    print("El conductor tiene una corriente admisible Iz = {} y una Pz={}".format(max(dfs[cat_Pgen3]['Iz']),round(max(dfs[cat_Pgen3]['Pz']))))
    return precio_total_redondeado,lcoe

calcular_y_mostrar_resultados_(cap_bat, cat_Pgen3, num_bat, dfs, "del sistema unificado para las 4 viviendas",precio_cables)

prec1,lcoe = calcular_y_mostrar_resultados_(cap_bat, cat_Pgen3, num_bat, dfs, '', precio_cables)
prec1_4=round(prec1*4,2)
if caida_porc < 5 and validez_term == True:
    print('El cable de {} es válido'.format(cabl[2]))
else:
    print ('El cable no es válido')
print('El LCOE es de {} USD/kWh'.format(lcoe))




df_final = dfs[cat_Pgen3]
energia_insatisfecha = calcular_energia_insatisfecha(cap_bat, df_final)

# Calcular la energía insatisfecha como un porcentaje de la demanda total
energia_insatisfecha_porcentaje = (energia_insatisfecha / suma_demandas['Demanda'].sum()) * 100

# Redondear el resultado a dos decimales
energia_insatisfecha_porcentaje_redondeado = round(energia_insatisfecha_porcentaje, 2)

# Mostrar el resultado
print("La energía insatisfecha como porcentaje de la demanda total es del {}%".format(energia_insatisfecha_porcentaje_redondeado))

# Crear el nombre del archivo CSV con el porcentaje de energía insatisfecha
nombre_archivo = "caso_{}_porc_insatisfecha.csv".format(energia_insatisfecha_porcentaje_redondeado)
"""
# Ruta de guardado del archivo CSV en el directorio dataproysolar
ruta_guardado = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\df_4viviendas_{}.csv".format(energia_insatisfecha_porcentaje_redondeado)

# Exportar el DataFrame a un archivo CSV
df_final.to_csv(ruta_guardado, index=False)
"""