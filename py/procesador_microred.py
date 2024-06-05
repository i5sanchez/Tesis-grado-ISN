import pandas as pd
import os

# Directorio donde están los archivos CSV
directory = "C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\"
#directory = "C:\\Users\\Intel\\Desktop\\cosas_sanchez\\" #PC CUIE UMSS

# Lista de archivos CSV
files = [
    "df_4viviendas_0.0.csv",
    "df_4viviendas_4.46.csv",
    "df_4viviendas_9.43.csv",
    "df_4viviendas_14.36.csv",
    "df_4viviendas_19.29.csv",
    "df_4viviendas_24.23.csv",
    "df_4viviendas_29.76.csv",
    "df_4viviendas_34.81.csv",
    "df_4viviendas_40.64.csv",
    "df_4viviendas_46.15.csv",
    "df_4viviendas_51.03.csv",
    "df_4viviendas_58.74.csv",
    "df_4viviendas_62.49.csv",
    "df_4viviendas_67.62.csv",
    "df_4viviendas_75.53.csv",
    "df_4viviendas_81.66.csv",
    "df_4viviendas_85.13.csv",
    "df_4viviendas_87.61.csv",
    "df_4viviendas_95.87.csv"
]
files2 = [file.replace(".csv", "_procesado.csv") for file in files]
files3 = [file.replace(".csv", "_procesado2.csv") for file in files]
files4 = [file.replace(".csv", "_procesado3.csv") for file in files]
files5 = [file.replace(".csv", "_procesado4.csv") for file in files]
files6 = [file.replace(".csv", "_procesado5.csv") for file in files]


def protocolo(df):
    horas_diurnas = ['07:00:00', '08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00', 
                     '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00']
    df['Time'] = df['Time'].astype(str)
    protocolos = ['Diurno' if hora in horas_diurnas else 'Nocturno' for hora in df['Time']]
    df['Protocolo'] = protocolos
    return df
def aut(df, i):
    df.at[i, 'cbat_porc']=(df.at[i, 'carga_bat']/df.at[i, 'capbat'])*100
    if df.at[i, 'Protocolo'] == 'Diurno':
        if df.at[i, 'gen'] > df.at[i, 'Demanda'] and df.at[i, 'cbat_porc'] == 100:
            df.at[i, 'Autenv'] = True
            df.at[i, 'Autrecv'] = False
        else:
            df.at[i, 'Autenv'] = False
            df.at[i, 'Autrecv'] = True
    elif df.at[i, 'Protocolo'] == 'Nocturno':
        if df.at[i, 'cbat_porc'] >= 50:
            df.at[i, 'Autenv'] = True
            df.at[i, 'Autrecv'] = False
        elif df.at[i, 'cbat_porc'] <= 20:
            df.at[i, 'Autenv'] = False
            df.at[i, 'Autrecv'] = True
        else:
            df.at[i, 'Autenv'] = False
            df.at[i, 'Autrecv'] = False
    return df

def cont_conex(df1, *connected_dfs):
    df1['nenv'] = 0
    df1['nrecv'] = 0
    
    for index, row in df1.iterrows():
        df1 = aut(df1, index)
        autenv_in = df1.at[index, 'Autenv']
        autrecv_in = df1.at[index, 'Autrecv']
        nenv = 0
        nrecv = 0
        
        for df in connected_dfs:
            df = aut(df, index)
            autenv_ex = df.at[index, 'Autenv']
            autrecv_ex = df.at[index, 'Autrecv']
            
            if autenv_in and autrecv_ex:
                nenv = 1
            if autrecv_in and autenv_ex:
                nrecv = 1
                
        df1.at[index, 'nenv'] = nenv
        df1.at[index, 'nrecv'] = nrecv
        
    return df1


def calc_insatisf(df, n):
    prop_insatis = round(100 - (df['demanda_suplida'].sum() / df['Demanda'].sum()) * 100, 3)
    prop_insatis_or = round((df['energia_insatisfecha'].sum() / df['Demanda'].sum()) * 100, 3)
    print('En la vivienda {} la proporción de energía insatisfecha es del {} %, originalmente era del {} %.'.format(n, prop_insatis, prop_insatis_or))

def calc_carga_surp(df, i):
    if i == 0:
        df.at[i, 'carga_bat'] = df.at[i, 'gen'] - df.at[i, 'Demanda']
        df.at[i, 'surplus'] = max(0, df.at[i, 'carga_bat'])
        df.at[i, 'carga_bat'] = max(0, df.at[i, 'carga_bat'])  # Ensure no negative battery charge
        df.at[i, 'energia_insatisf_conec'] = max(0, df.at[i, 'Demanda'] - df.at[i, 'gen'])
        df.at[i, 'demanda_suplida'] = min(df.at[i, 'Demanda'], df.at[i, 'gen'])
    else:
        prev_carga_bat = df.at[i - 1, 'carga_bat']
        flujos_bat = df.at[i - 1, 'gen'] - df.at[i - 1, 'Demanda']
        
        carga_bat_actual = prev_carga_bat + flujos_bat
        carga_bat_actual = max(0, min(carga_bat_actual, df.at[i, 'capbat']))
        
        energia_disponible = df.at[i, 'gen'] + carga_bat_actual
        if energia_disponible >= df.at[i, 'Demanda']:
            df.at[i, 'demanda_suplida'] = df.at[i, 'Demanda']
            df.at[i, 'carga_bat'] = carga_bat_actual - (df.at[i, 'Demanda'] - df.at[i, 'gen'])
            df.at[i, 'carga_bat'] = max(0, min(df.at[i, 'carga_bat'], df.at[i, 'capbat']))
            df.at[i, 'surplus'] = max(0, energia_disponible - df.at[i, 'Demanda'])
        else:
            df.at[i, 'demanda_suplida'] = energia_disponible
            df.at[i, 'carga_bat'] = 0
            df.at[i, 'surplus'] = 0
        
        df.at[i, 'energia_insatisf_conec'] = max(0, df.at[i, 'Demanda'] - df.at[i, 'demanda_suplida'])
        
    return df


def transmision(df1, df2):
    df1['carga_bat'] = 0
    df2['carga_bat'] = 0
    efs = 0.905 * 0.95 * 0.9
    for i in range(len(df1)):
        if i == 0:
            df1.at[i, 'pext'] = 0
            df2.at[i, 'pext'] = 0
            df1.at[i, 'carga_bat'] = 0
            df2.at[i, 'carga_bat'] = 0
            continue

        df1 = calc_carga_surp(df1, i)
        df2 = calc_carga_surp(df2, i)
        df1 = aut(df1, i)
        df2 = aut(df2, i)
       # df1 = cont_conex(df1, df2)
        #df2 = cont_conex(df2, df1)

        if df1.at[i, 'Autenv'] and df2.at[i, 'Autrecv']:
            if df1.at[i, 'Protocolo'] == 'Diurno':
                potenv = df1.at[i, 'surplus']
                potrec = potenv * efs
                df1.at[i, 'pext'] = -potenv
                df2.at[i, 'pext'] = potrec
                demanda_restante = df2.at[i, 'Demanda'] - df2.at[i, 'demanda_suplida']
                if demanda_restante > 0:
                    df2.at[i, 'demanda_suplida'] += min(potrec, demanda_restante)
                    potrec -= min(potrec, demanda_restante)
                df2.at[i, 'carga_bat'] = min(df2.at[i, 'carga_bat'] + potrec, df2.at[i, 'capbat'])
            else:
                potenv = df2.at[i, 'Demanda'] / efs
                potrec = potenv * efs
                df1.at[i, 'pext'] = -potenv
                df2.at[i, 'pext'] = potrec

                df1.at[i, 'carga_bat'] -= potenv
                demanda_restante = df2.at[i, 'Demanda'] - df2.at[i, 'demanda_suplida']
                if demanda_restante > 0:
                    df2.at[i, 'demanda_suplida'] += min(potrec, demanda_restante)

        elif df1.at[i, 'Autrecv'] and df2.at[i, 'Autenv']:
            if df2.at[i, 'Protocolo'] == 'Diurno':
                potenv = df2.at[i, 'surplus']
                potrec = potenv * efs
                df2.at[i, 'pext'] = -potenv
                df1.at[i, 'pext'] = potrec
                demanda_restante = df1.at[i, 'Demanda'] - df1.at[i, 'demanda_suplida']
                if demanda_restante > 0:
                    df1.at[i, 'demanda_suplida'] += min(potrec, demanda_restante)
                    potrec -= min(potrec, demanda_restante)
                df1.at[i, 'carga_bat'] = min(df1.at[i, 'carga_bat'] + potrec, df1.at[i, 'capbat'])
            else:
                potenv = df1.at[i, 'Demanda']
                potrec = potenv * efs
                df2.at[i, 'carga_bat'] -= potenv
                demanda_restante = df1.at[i, 'Demanda'] - df1.at[i, 'demanda_suplida']
                if demanda_restante > 0:
                    df1.at[i, 'demanda_suplida'] += min(potrec, demanda_restante)

        else:
            df1.at[i, 'pext'] = 0
            df2.at[i, 'pext'] = 0
        print('Registro {} de {} realizado'.format(i,tam))
    print(df1.head())
    print(df2.head())
    return df1, df2


"""

def transmision(nodos, conexiones):
    for nodo in nodos:
        nodo['carga_bat'] = 0
        
    efs = 0.905 * 0.95 * 0.9
    
    for i in range(len(nodos[0])):
        for nodo in nodos:
            nodo.at[i, 'pext'] = 0
            nodo.at[i, 'carga_bat'] = 0
        
        for conexion in conexiones:
            nodo_fuente, nodo_destino = conexion
            
            nodo_fuente = calc_carga_surp(nodo_fuente, i)
            nodo_destino = calc_carga_surp(nodo_destino, i)
            nodo_fuente = aut(nodo_fuente, i)
            nodo_destino = aut(nodo_destino, i)
            
            for nodo in nodos:
                if nodo is nodo_fuente:
                    nodo_fuente = cont_conex(nodo_fuente, nodo_destino)
                else:
                    nodo_destino = cont_conex(nodo_destino, nodo_fuente)
        
        for conexion in conexiones:
            nodo_fuente, nodo_destino = conexion
            
            if nodo_fuente.at[i, 'Autenv'] and nodo_destino.at[i, 'Autrecv']:
                if nodo_fuente.at[i, 'Protocolo'] == 'Diurno':
                    potenv = nodo_fuente.at[i, 'surplus'] / (nodo_fuente.at[i, 'nenv'] * efs)
                    potrec = potenv * efs
                    demanda_restante = nodo_destino.at[i, 'Demanda'] - nodo_destino.at[i, 'demanda_suplida']
                    if demanda_restante > 0:
                        if potrec < demanda_restante:
                            nodo_destino.at[i, 'demanda_suplida'] += potrec 
                            potrec = 0
                        else:
                            nodo_destino.at[i, 'demanda_suplida'] = nodo_destino.at[i, 'Demanda']
                            potrec -= demanda_restante
                    nodo_destino.at[i, 'carga_bat'] = min(nodo_destino.at[i, 'carga_bat'] + potrec, nodo_destino.at[i, 'capbat'])
                else:
                    demanda_restante = nodo_destino.at[i, 'Demanda'] - nodo_destino.at[i, 'demanda_suplida']
                    potenv = nodo_destino.at[i, 'Demanda']/efs
                    potrec = potenv*efs
                    nodo_fuente.at[i,'carga_bat']-=potenv

                    if potenv < demanda_restante:
                        nodo_destino.at[i, 'demanda_suplida'] += potrec
                    else:
                        nodo_destino.at[i, 'demanda_suplida'] = nodo_destino.at[i, 'Demanda']
                        potenv -= demanda_restante / efs
                nodo_fuente.at[i, 'pext'] = -potenv
                nodo_destino.at[i, 'pext'] = potrec
            elif nodo_fuente.at[i, 'Autrecv'] and nodo_destino.at[i, 'Autenv']:
                if nodo_destino.at[i, 'Protocolo'] == 'Diurno':
                    potenv = nodo_destino.at[i, 'surplus'] / (nodo_destino.at[i, 'nenv'] * efs)
                    potrec = potenv * efs
                    demanda_restante = nodo_fuente.at[i, 'Demanda'] - nodo_fuente.at[i, 'demanda_suplida']
                    if demanda_restante > 0:
                        if potrec < demanda_restante:
                            nodo_fuente.at[i, 'demanda_suplida'] += potrec
                            potrec = 0
                        else:
                            nodo_fuente.at[i, 'demanda_suplida'] = nodo_fuente.at[i, 'Demanda']
                            potrec -= demanda_restante
                    nodo_fuente.at[i, 'carga_bat'] = min(nodo_fuente.at[i, 'carga_bat'] + potrec, nodo_fuente.at[i, 'capbat'])
                else:
                    demanda_restante = nodo_fuente.at[i, 'Demanda'] - nodo_fuente.at[i, 'demanda_suplida']
                    potenv = nodo_destino.at[i, 'Demanda']/efs
                    nodo_destino.at[i,'carga_bat']-=potenv
                    potrec = potenv*efs
                    
                    if potenv < demanda_restante:
                        nodo_fuente.at[i, 'demanda_suplida'] += potrec
                    else: 
                        nodo_fuente.at[i, 'demanda_suplida'] = nodo_fuente.at[i, 'Demanda']
                        potenv -= demanda_restante / efs
                nodo_destino.at[i, 'pext'] = -potenv
                nodo_fuente.at[i, 'pext'] = potrec
            # Otras condiciones para nodos sin conexión directa
        print('Registro {} realizado'.format(i))
    return nodos
"""




tam=8760
# Lista para almacenar cada DataFrame
df_list = []

# Leer cada archivo CSV y añadirlo a la lista
for file in files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)

    # Convertir las columnas relevantes a numéricas, manejando errores
    df['gen'] = pd.to_numeric(df['gen'], errors='coerce').fillna(0)
    df['Demanda'] = pd.to_numeric(df['Demanda'], errors='coerce').fillna(0)
    # Truncar el dataframe a 720 registros
    df = df.iloc[:tam]
    if 'carga_bat' in df.columns:
        if max(df['carga_bat']) % 1 == 0:
            df['capbat'] = max(df['carga_bat'])
        else:
            df['capbat'] = 89
        df['cbat_porc'] = (df['carga_bat'] / df['capbat']) * 100
    else:
        df['capbat'] = 89
        df['cbat_porc'] = 0

    df.drop(columns=[
        'num_pan20', 'caida_tension', 'caida_porc', 'precio_cables', 
        'validez_termica', 'perdida_potencia', 'Iz', 'Pz', 
        'surplus', 'carga_bat'
    ], inplace=True, errors='ignore')
    
    df = protocolo(df)
    df_list.append(df)
    """
df_list2 = []

for file in files2:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    
    df['Demanda'] = pd.to_numeric(df['Demanda'], errors='coerce').fillna(0)
    # Truncar el dataframe a 720 registros
    df = df.iloc[:tam]
    # Restablecer el índice para que comience desde 0
    df.reset_index(drop=True, inplace=True)
    if 'carga_bat' in df.columns:
        if max(df['carga_bat']) % 1 == 0:
            df['capbat'] = max(df['carga_bat'])
        else:
            df['capbat'] = 89
        df['cbat_porc'] = (df['carga_bat'] / df['capbat']) * 100
    else:
        df['capbat'] = 89

    df.drop(columns=[
        'num_pan20', 'caida_tension', 'caida_porc', 'precio_cables', 
        'validez_termica', 'perdida_potencia', 'Iz', 'Pz', 
        'surplus', 'carga_bat'
    ], inplace=True, errors='ignore')
    
    df = protocolo(df)
    df_list2.append(df)

# Bucle para procesar files3
df_list3=[]
for file in files3:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    
    df['Demanda'] = pd.to_numeric(df['Demanda'], errors='coerce').fillna(0)
    # Truncar el dataframe a 100 registros
    df = df.iloc[:tam]
    if 'carga_bat' in df.columns:
        if max(df['carga_bat']) % 1 == 0:
            df['capbat'] = max(df['carga_bat'])
        else:
            df['capbat'] = 89
        df['cbat_porc'] = (df['carga_bat'] / df['capbat']) * 100
    else:
        df['capbat'] = 89
        df['cbat_porc'] = 0

    df.drop(columns=[
        'num_pan20', 'caida_tension', 'caida_porc', 'precio_cables', 
        'validez_termica', 'perdida_potencia', 'Iz', 'Pz', 
        'surplus', 'carga_bat'
    ], inplace=True, errors='ignore')
    
    df = protocolo(df)
    df_list3.append(df)

# Bucle para procesar files4
df_list4=[]

for file in files4:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    
    df['Demanda'] = pd.to_numeric(df['Demanda'], errors='coerce').fillna(0)
    # Truncar el dataframe a 100 registros
    df = df.iloc[:tam]
    if 'carga_bat' in df.columns:
        if max(df['carga_bat']) % 1 == 0:
            df['capbat'] = max(df['carga_bat'])
        else:
            df['capbat'] = 89
        df['cbat_porc'] = (df['carga_bat'] / df['capbat']) * 100
    else:
        df['capbat'] = 89
        df['cbat_porc'] = 0

    df.drop(columns=[
        'num_pan20', 'caida_tension', 'caida_porc', 'precio_cables', 
        'validez_termica', 'perdida_potencia', 'Iz', 'Pz', 
        'surplus', 'carga_bat'
    ], inplace=True, errors='ignore')
    
    df = protocolo(df)
    df_list4.append(df)

# Bucle para procesar files5
df_list5=[]

for file in files5:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    
    df['Demanda'] = pd.to_numeric(df['Demanda'], errors='coerce').fillna(0)
    # Truncar el dataframe a 100 registros
    df = df.iloc[:tam]
    if 'carga_bat' in df.columns:
        if max(df['carga_bat']) % 1 == 0:
            df['capbat'] = max(df['carga_bat'])
        else:
            df['capbat'] = 89
        df['cbat_porc'] = (df['carga_bat'] / df['capbat']) * 100
    else:
        df['capbat'] = 89
        df['cbat_porc'] = 0

    df.drop(columns=[
        'num_pan20', 'caida_tension', 'caida_porc', 'precio_cables', 
        'validez_termica', 'perdida_potencia', 'Iz', 'Pz', 
        'surplus', 'carga_bat'
    ], inplace=True, errors='ignore')
    
    df = protocolo(df)
    df_list5.append(df)

# Bucle para procesar files6
df_list6=[]

for file in files6:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    
  
    df['Demanda'] = pd.to_numeric(df['Demanda'], errors='coerce').fillna(0)
    # Truncar el dataframe a 100 registros
    df = df.iloc[:tam]
    if 'carga_bat' in df.columns:
        if max(df['carga_bat']) % 1 == 0:
            df['capbat'] = max(df['carga_bat'])
        else:
            df['capbat'] = 89
        df['cbat_porc'] = (df['carga_bat'] / df['capbat']) * 100
    else:
        df['capbat'] = 89
        df['cbat_porc'] = 0

    df.drop(columns=[
        'num_pan20', 'caida_tension', 'caida_porc', 'precio_cables', 
        'validez_termica', 'perdida_potencia', 'Iz', 'Pz', 
        'surplus', 'carga_bat'
    ], inplace=True, errors='ignore')
    
    df = protocolo(df)
    df_list6.append(df)
# Definir df_list2, df_list3, df_list4, df_list5 y df_list6 como diccionarios
df_list2 = {}
df_list3 = {}
df_list4 = {}
df_list5 = {}
df_list6 = {}

# Procesar cada archivo CSV
for file, df in zip(files, df_list):
    df_list2[file] = df.copy()
    df_list2[file]['gen'] = df['gen'].copy()

    df_list3[file] = df.copy()
    df_list3[file]['gen'] = df['gen'].copy()

    df_list4[file] = df.copy()
    df_list4[file]['gen'] = df['gen'].copy()

    df_list5[file] = df.copy()
    df_list5[file]['gen'] = df['gen'].copy()

    df_list6[file] = df.copy()
    df_list6[file]['gen'] = df['gen'].copy()
    """

# Ahora puedes acceder a cada dataframe procesado a través de df_list2, df_list3, df_list4, df_list5 y df_list6



"""
def init_carga_bat(df):
    df['carga_bat'] = 0
    return df

# Inicializar la columna 'carga_bat' en todos los DataFrames
for i in range(len(df_list)):
    df_list[i] = init_carga_bat(df_list[i])
"""
"""
def macro_transmision(pares_de_conexiones):
    for par in pares_de_conexiones:
        df1, df2 = par
        
        # Aplicar las subfunciones necesarias
        df1 = protocolo(df1)
        df2 = protocolo(df2)
        df1 = cont_conex(df1, df2)
        df2 = cont_conex(df2, df1)
        # Otras subfunciones que necesites aplicar antes de la transmisión
        
        # Llamar a la función de transmisión
        df1, df2 = transmision(df1, df2)
        
        # Otras acciones después de la transmisión
        # Por ejemplo, podrías guardar los resultados en archivos, imprimir resúmenes, etc.

# Ejemplo de uso:
df1=df_list[7]
df2=df_list[11]
df3=df_list[9]
pares_de_conexiones = [(df1, df2), (df1, df3)]  # Lista de pares de DataFrames
macro_transmision(pares_de_conexiones)
"""
"""
df1, df2 = transmision(df_list[7], df_list[11])
df1, df3 = transmision(df1, df_list[9])

calc_insatisf(df1, 1)
calc_insatisf(df2, 2)
calc_insatisf(df3, 3)
"""
num1 = 7
num2 = 8  

# Definir los DataFrames para los nodos
#df0 = df_list[num1]
df1 = df_list[num1]

df2 = df_list[num2]
"""
df3 = df_list4[files[num1]]
df4 = df_list5[files[num1]]
df5 = df_list6[files[num1]]
df6 = df_list[num2]
df7 = df_list2[files[num2]]
df8 = df_list3[files[num2]]
df9 = df_list4[files[num2]]
df10 = df_list5[files[num2]]
df11 = df_list6[files[num2]]

# Organizar los DataFrames en una lista de nodos
nodos = [df0,df1, df2, df3, df4,df5,df6,df7,df8,df9,df10,df11]

# Definir las conexiones entre los nodos
conexiones = [(df0,df1),(df1,df0),(df0,df2),(df2,df0),(df0,df3),(df3,df0),(df1,df10),(df10,df1),(df10,df11),(df11,df10),(df11,df9),(df9,df11),(df9,df1),(df1,df9),(df1,df3),(df3,df1),(df3,df5),(df5,df3),(df5,df6),(df6,df5),(df5,df7),(df7,df5),(df2,df4),(df4,df2),(df3,df4),(df4,df3),(df4,df8),(df8,df4)]

# Llamar a la función macro_transmision
transmision(nodos, conexiones)
# Crear una lista de DataFrames
dataframes = [df0, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11]

# Iterar sobre la lista de DataFrames y llamar a calc_insatisf con el índice como argumento
for i, df in enumerate(dataframes):
    calc_insatisf(df, i)
df0.to_csv('df0.csv', index=False)
df1.to_csv('df1.csv', index=False)
df2.to_csv('df2.csv', index=False)
df3.to_csv('df3.csv', index=False)
df4.to_csv('df4.csv', index=False)
df5.to_csv('df5.csv', index=False)
df6.to_csv('df6.csv', index=False)
df7.to_csv('df7.csv', index=False)
df8.to_csv('df8.csv', index=False)
df9.to_csv('df9.csv', index=False)
df10.to_csv('df10.csv', index=False)
df11.to_csv('df11.csv', index=False)
"""
df1, df2 = transmision(df1, df2)
calc_insatisf(df1, 1)
calc_insatisf(df2, 2)

# Exportar DataFrames a CSV
df1_path = os.path.join(directory, "df1.csv")
df2_path = os.path.join(directory, "df2.csv")

df1.to_csv(df1_path, index=False)
df2.to_csv(df2_path, index=False)

print(f"df1 exportado a {df1_path}")
print(f"df2 exportado a {df2_path}")
