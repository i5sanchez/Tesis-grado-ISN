# importing functions
from ramp import UseCase, User
import pandas as pd


#Previamente conviene importar datos fotovoltaicos con las características deseadas de la página https://www.renewables.ninja/
#Y con ramp extraer un fichero de demanda eléctrica e importarlo.

path="data/muestra_año_pv_raqaypampa7_50w.csv"

for i in range(10,60,10):
    
    path="data/muestra_año_pv_raqaypampa7_" + str(i) + "w.csv"
    


generacion = pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\generacion_0.05kwp.csv",header=0)
consumo=pd.read_csv("C:\\Users\\Usuario\\.spyder-py3\\data_proysolar\\output_file_t1.csv")
cap_bat=1 #indica la capacidad de la batería en Wh, puede cambiarse.
consumo_f = consumo[consumo.index % 60 == 0]
consumo_f.index=range(1,len(consumo_f)+1)


df_junto = pd.concat([generacion, consumo_f], axis=1)

# Multiplicar por 1000 los valores de la columna 'electricity'
df_junto['electricity']*= 1000  #Para pasar de kW a W, dado que las demandas están en W.
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
    
    # Limitar la carga de la batería entre 0 y 89
    carga_bat_actual = max(0, min(carga_bat_actual, cap_bat))
    
    # Actualizar la carga de la batería en el DataFrame
    df_junto.at[i, 'carga_bat'] = carga_bat_actual

    # Calcular el excedente de energía (si la carga supera el límite)
    if carga_bat_actual == cap_bat:
        df_junto.at[i, 'surplus'] = -(cap_bat - flujos_bat - df_junto.at[i - 1, 'carga_bat']) 
    else:
        df_junto.at[i, 'surplus'] = 0
# Calcular la suma total de la columna 'surplus' o energía desperdiciada en Wh
suma_surplus = round(df_junto['surplus'].sum())

print("Suma total de energía despericiada o surplus energy: {} Wh".format(suma_surplus))
#pp.export_series(df_junto, j=None, fname= None, ofname= 'output_balance_surplus_t1.csv')
df_junto.to_csv('C:\\Users\\Usuario\\Desktop\\Mi ingeniería e. e\\Contenidos por cursos\\Cuarto curso\\Octavo semestre (BOLIVIA)\\RAMP\\excels\\Outputs_balance_surplus\\output_balance_surplus_t1.csv', index=False)

