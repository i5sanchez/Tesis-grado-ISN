# -*- coding: utf-8 -*-
"""
Created on Fri May 24 17:08:14 2024

@author: Usuario
"""

import matplotlib.pyplot as plt
import numpy as np

dist_nodo = 100  # m
long_cables = 2 * dist_nodo


cable_1_5mm=[13.3*(1+1.7e-5*70),21*0.9,21.36,1.5,0.2] #[0] es la R en ohm/km a 90º, [1] es la Iz con los cables al sol, [2] USD/metro de cable
cable_2_5mm=[7.98*(1+1.7e-5*70),30*0.9,12.88,2.5,0.31]
cable_4mm=[4.95*(1+1.7e-5*70),40*0.9,8.1,4,0.58]
cable_6mm=[3.3*(1+1.7e-5*70),52*0.9,5.51,6,0.9]
cable_10mm=[1.91*(1+1.7e-5*70),72*0.9,3.31,10,1.89]
cable_16mm=[1.21*(1+1.7e-5*70),97*0.9,2.12,16,2.45]
cable_25mm=[0.78*(1+1.7e-5*70),122*0.9,1.37,25,4.18]
cable_35mm=[0.55*(1+1.7e-5*70),153*0.9,1.01,35,8.96]
cable_50mm=[0.38*(1+1.7e-5*70),188*0.9,0.77,50,11.49]
cable_70mm=[0.27*(1+1.7e-5*70),243*0.9,0.56,70,12.86]
cable_95mm=[0.2*(1+1.7e-5*70),298*0.9,0.43,95,16.93] 
cable_120mm=[0.16*(1+1.7e-5*70),350*0.9,0.36,120,20.99]
cable_150mm=[0.12*(1+1.7e-5*70),401*0.9,0.31,150,45.99]
cable_185mm=[0.1*(1+1.7e-5*70),460*0.9,0.26,185,51.58]
cable_240mm=[0.08*(1+1.7e-5*70),545*0.9,0.22,240,53.73]

cables = [
    [13.3 * (1 + 1.7e-5 * 70), 21 * 0.9, 21.36, 1.5, 0.2],
    [7.98 * (1 + 1.7e-5 * 70), 30 * 0.9, 12.88, 2.5, 0.31],
    [4.95 * (1 + 1.7e-5 * 70), 40 * 0.9, 8.1, 4, 0.58],
    [3.3 * (1 + 1.7e-5 * 70), 52 * 0.9, 5.51, 6, 0.9],
    [1.91 * (1 + 1.7e-5 * 70), 72 * 0.9, 3.31, 10, 1.89],
    [1.21 * (1 + 1.7e-5 * 70), 97 * 0.9, 2.12, 16, 2.45],
    [0.78 * (1 + 1.7e-5 * 70), 122 * 0.9, 1.37, 25, 4.18],
    [0.55 * (1 + 1.7e-5 * 70), 153 * 0.9, 1.01, 35, 8.96],
    [0.38 * (1 + 1.7e-5 * 70), 188 * 0.9, 0.77, 50, 11.49],
    [0.27 * (1 + 1.7e-5 * 70), 243 * 0.9, 0.56, 70, 12.86],
    [0.2 * (1 + 1.7e-5 * 70), 298 * 0.9, 0.43, 95, 16.93],
    [0.16 * (1 + 1.7e-5 * 70), 350 * 0.9, 0.36, 120, 20.99],
    [0.12 * (1 + 1.7e-5 * 70), 401 * 0.9, 0.31, 150, 45.99],
    [0.1 * (1 + 1.7e-5 * 70), 460 * 0.9, 0.26, 185, 51.58],
    [0.08 * (1 + 1.7e-5 * 70), 545 * 0.9, 0.22, 240, 53.73]
]

def paralelo(cable1, cable2):
    R = (cable1[0] * cable2[0]) / (cable1[0] + cable2[0])
    Iz = cable1[1] + cable2[1]
    prec_met = cable1[2] + cable2[2]
    cable_final = [R, Iz, prec_met]
    return cable_final

P = 12 * 50

def calc_corr_AC(Vdc, Idc, fdp, Vac):
    Iac = round((Vdc * Idc) / (Vac * fdp), 1)
    return Iac

def caidas_tension(I, V, cable, long_cables):
    long_km = long_cables / 1000
    caida_voltios = cable[2] * long_km * I
    caida_porc = (caida_voltios / V) * 100
    precio = cable[4] * long_cables
    dif = I + 2 - cable[1]
    validez_term = dif <= 0
    validez_caida = caida_porc < 5
    return caida_voltios, caida_porc, precio, validez_caida, validez_term

def calc_prec(V, long_cables, cable, Idc):
    caida_voltios, caida_porc, precio_cab, validez_caida, validez_term = caidas_tension(calc_corr_AC(12, Idc, 0.8, V), V, cable, long_cables)
    precio_dc_ac12_230 = 62.05
    precio_diodos_schottky = 0
    termomag = 6.86 * 2
    contador = 25.31
    ac_dc = 21.23 * 2
    diferenciales = 39.52 * 2
    contactores = 20 * 2
    trafo230_460 = 150
    trafo230_690 = 200
    trafo230_920 = 250

    precio = precio_cab + contador + precio_diodos_schottky + termomag + ac_dc + diferenciales + contactores

    if V == 230:
        precio += precio_dc_ac12_230
    elif V == 460:
        precio += precio_dc_ac12_230 + trafo230_460 * 2
    elif V == 690:
        precio += precio_dc_ac12_230 + trafo230_690 * 2
    elif V==920:
        precio += precio_dc_ac12_230+trafo230_920*2
    if validez_caida==True and validez_term==True:
        vale = 'Sí'
    else:
        vale='No'
    print(f'Para el caso de 12 V a {V} V y una distancia de {long_cables // 2} metros, la caída porcentual de tensión es del {caida_porc:.2f} % y valdrían los cables y convertidores un total de {precio:.2f} USD. {vale} es válido')

def calc_prec_(V, long_cables, cable, Idc):
    caida_voltios, caida_porc, precio_cab, validez_caida, validez_term = caidas_tension(calc_corr_AC(12, Idc, 0.8, V), V, cable, long_cables)
    precio_dc_ac12_230 = 62.05
    precio_diodos_schottky = 0
    termomag = 6.86 * 2
    contador = 25.31
    ac_dc = 21.23 * 2
    diferenciales = 39.52 * 2
    contactores = 20 * 2
    if V==230:
        trafo=0
    elif V==460:
        trafo = 150
    elif V==690:
        trafo = 200
    elif V==920:
        
        trafo = 250
    precio = precio_cab + contador + precio_diodos_schottky + termomag + ac_dc + diferenciales + contactores

    precios_dc_ac = {
        230: precio_dc_ac12_230,
        460: precio_dc_ac12_230 + trafo * 2,
        690: precio_dc_ac12_230 + trafo * 2, 920: precio_dc_ac12_230+trafo*2
    }
    precio += precios_dc_ac.get(V, 0)
    NPC = precio*1.1 + (precio_diodos_schottky*2 + trafo*2*(20/25) + precios_dc_ac[V]*4 + ac_dc*4 + diferenciales*(2/3) + termomag*(2/3) +contador*3)*1.1 # para 20 años
    return precio, long_cables // 2, validez_term, validez_caida, caida_porc,NPC

calc_prec(230, long_cables, cable_1_5mm, 40)

# Definir la estructura de datos para almacenar los resultados
resultados_por_tension = {}

# Iterar sobre cada nivel de tensión (230, 460, 690)
for V in range(230, 921, 230):
    # Inicializar la estructura de datos para este nivel de tensión
    resultados_por_distancia = {}
    
    # Iterar sobre cada distancia de 10 metros a 1500 metros
    for distancia in range(10, 2500, 10):
        # Inicializar la lista de vectores de cable para esta distancia
        vectores_cable = []
        
        # Iterar sobre cada tipo de cable
        for cable in cables:
            # Calcular precio, caída de tensión porcentual, validez térmica y validez de caídas
            precio, _, validez_term, validez_caida, caida_porc,NPC = calc_prec_(V, distancia * 2, cable, 40)
            
            # Almacenar los resultados en un vector
            vector_cable = {
                'seccion': cable[3],
                'precio': precio,
                'caida_porc': caida_porc,
                'validez_term': validez_term,
                'validez_caida': validez_caida
            }
            
            # Agregar el vector a la lista de vectores de cable
            vectores_cable.append(vector_cable)
        
        # Filtrar los resultados para eliminar vectores que no cumplen las valideces
        vectores_filtrados = [vector for vector in vectores_cable if vector['validez_term'] and vector['validez_caida']]
        
        # Si hay vectores filtrados, mantener solo el que tenga el precio más bajo
        if vectores_filtrados:
            vector_mas_barato = min(vectores_filtrados, key=lambda x: x['precio'])
            resultados_por_distancia[distancia] = vector_mas_barato
    
    # Agregar los resultados de esta tensión al diccionario principal
    resultados_por_tension[V] = resultados_por_distancia

# Graficar los resultados
plt.figure(figsize=(12*10, 8*10))
# Listas para almacenar los precios mínimos y distancias óptimas
precios_optimos = []
distancias_optimas = []

# Iterar sobre cada distancia y encontrar el precio mínimo global entre todas las tensiones
for distancia in range(10, 2500, 10):
    precio_minimo_global = float('inf')  # Precio mínimo global entre todas las tensiones
    distancia_optima = None  # Distancia óptima donde se encuentra el precio mínimo global
    
    # Iterar sobre cada nivel de tensión y sus resultados para encontrar el precio mínimo en esta distancia
    for tension, resultados_por_distancia in resultados_por_tension.items():
        if distancia in resultados_por_distancia:
            precio = resultados_por_distancia[distancia]['precio']
            if precio < precio_minimo_global:
                precio_minimo_global = precio
                distancia_optima = distancia
                tension_optima = tension
    
    if distancia_optima:
        # Mostrar el número de nivel de tensión en el punto óptimo
        plt.text(distancia_optima, precio_minimo_global, f'{tension_optima} V', fontsize=8, ha='right', va='bottom')
    
    # Almacenar el precio mínimo global y la distancia óptima
    precios_optimos.append(precio_minimo_global)
    distancias_optimas.append(distancia_optima)

# Trazar los puntos óptimos
plt.plot(distancias_optimas, precios_optimos, marker='o', color='blue', label='Puntos óptimos')
# Establecer límites en los ejes x e y
plt.xlim(0, 2500)  # Límites en el eje x desde 0 hasta 1500
plt.ylim(240, max(precios_optimos) + 500)  # Límites en el eje y, ajustado dinámicamente

# Etiquetas de los ejes y título del gráfico
plt.xlabel('Distancia (m)')
plt.ylabel('Precio (USD)')
plt.title('Precio en función de la distancia para la opción más barata en cada tramo')
# Ajustar los intervalos de los ticks en los ejes x e y
plt.xticks(np.arange(0, 2500, 10))  # Intervalo de 100 en 100 metros en el eje x
plt.yticks(np.arange(240, max(precios_optimos) + 500, 20))  # Intervalo de 2500 en 2500 USD en el eje y

# Leyenda y cuadrícula
plt.legend(loc='upper left')
plt.grid(True)

# Mostrar la gráfica
plt.show()
