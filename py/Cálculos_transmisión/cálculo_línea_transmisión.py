# -*- coding: utf-8 -*-
"""
Created on Tue May 14 22:43:37 2024

@author: Usuario
"""
import matplotlib.pyplot as plt
import numpy as np  # Importar NumPy

dist_nodo=500 #m
long_cables=2*(dist_nodo)

cable_1_5mm=[13.7*(1+1.7e-5*70),30*0.9,1.5,0.2] #[0] es la R en ohm/km a 90º, [1] es la Iz con los cables al sol, [2] USD/metro de cable
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

cables = [
    [13.7*(1+1.7e-5*70), 30*0.9,1.5, 0.2],  # cable_1_5mm
    [8.21*(1+1.7e-5*70), 41*0.9,2.5, 0.31],  # cable_2_5mm
    [5.09*(1+1.7e-5*70), 55*0.9,4, 0.58],  # cable_4mm
    [3.39*(1+1.7e-5*70), 70*0.9,6, 0.9],   # cable_6mm
    [1.95*(1+1.7e-5*70), 98*0.9,10, 1.89],  # cable_10mm
    [1.24*(1+1.7e-5*70), 132*0.9,16, 2.45], # cable_16mm
    [0.795*(1+1.7e-5*70), 176*0.9,25, 4.18],# cable_25mm
    [0.565*(1+1.7e-5*70), 218*0.9,35, 8.96],# cable_35mm
    [0.393*(1+1.7e-5*70), 276*0.9,50, 11.49],# cable_50mm
    [0.277*(1+1.7e-5*70), 347*0.9,70, 12.86],# cable_70mm
    [0.210*(1+1.7e-5*70), 416*0.9,95, 16.93],# cable_95mm
    [0.164*(1+1.7e-5*70), 488*0.9,120, 20.99],# cable_120mm
    [0.132*(1+1.7e-5*70), 566*0.9,150, 45.99],# cable_150mm
    [0.108*(1+1.7e-5*70), 644*0.9,185, 51.58],# cable_185mm
    [0.0817*(1+1.7e-5*70), 644*0.9,240, 53.73] # cable_240mm
]
def paralelo(cable1,cable2):
    R=(cable1[0]*cable2[0])/(cable1[0]+cable2[0])
    Iz=cable1[1]+cable2[1]
    prec_met=cable1[2]+cable2[2]
    cable_final = [R,Iz,prec_met]
    return cable_final
tension_dc=12 #V
tension_dc2=24
tension_dc3=48
def calc_corr(Vdc,I12V):
    P=12*I12V
    I=P/Vdc
    return I
P=12*50
I1=P/tension_dc #A
I2=P/tension_dc2
I3=P/tension_dc3
def caidas_tensión(I,V, cable, long_cables):
    Rohm_m = cable[0] / 1000
    R = Rohm_m * long_cables
    perd_pot = I * I * R
    caida = I * R
    caida_porc = ((caida) / V) * 100
    precio = cable[2] * long_cables*0.9

    validez_term = (I + 2 < cable[1])  # Comprobación para todos los elementos de la serie
    if caida_porc<5:
        validez_caida=True
        vale = 'Sí'
    else:
        validez_caida=False
        vale='No'

    return caida, caida_porc, precio, validez_term, perd_pot,validez_caida,vale

def calc_prec(V,long_cables,cable):


    I=calc_corr(12,50)
    caida, caida_porc, precio_cab,validez_term, perd_pot,validez_caida,vale = caidas_tensión(I,V, cable, long_cables) #12V

    precio_dc_dc12_24= 150.11
    precio_dc_dc12_48_TDK= 150.11
    precio_dc_dc_96_12_delta=299.03
    precio_dc_dc_200_425_12=275
    #precio_dc_dc_bidireccional=4312.7
    precio = precio_cab
    if V==12:
        precio=precio_cab
    elif V==24:
        precio=precio_cab+precio_dc_dc12_24*8
    elif V==48:
        precio=precio_cab+precio_dc_dc12_24*8
    elif V==96:
        precio=precio_cab+precio_dc_dc12_48_TDK*4+precio_dc_dc_96_12_delta*2
    elif V==144:
        precio=precio_cab+precio_dc_dc12_48_TDK*12
    elif V==192:
        precio=precio_cab+precio_dc_dc12_48_TDK*8+4*precio_dc_dc_96_12_delta
    elif V==240:
        precio=precio_cab+precio_dc_dc12_48_TDK*10+4*precio_dc_dc_200_425_12
    elif V==288:
        precio =  precio_cab+precio_dc_dc12_48_TDK*12+4*precio_dc_dc_200_425_12
    elif V==336:
        precio=precio_cab+precio_dc_dc12_48_TDK*14+4*precio_dc_dc_200_425_12
    elif V==384:
        precio=precio_cab+precio_dc_dc12_48_TDK*16+4*precio_dc_dc_200_425_12
    elif V==432:
        precio=precio_cab+precio_dc_dc12_48_TDK*18+4*precio_dc_dc_200_425_12
    elif V==480:
        precio=precio_cab+precio_dc_dc12_48_TDK*20+4*precio_dc_dc_200_425_12
    elif V==528:
        precio=precio_cab+precio_dc_dc12_48_TDK*22+4*precio_dc_dc_200_425_12
    elif V==576:
        precio=precio_cab+precio_dc_dc12_48_TDK*24+4*precio_dc_dc_200_425_12
    elif V==624:
        precio=precio_cab+precio_dc_dc12_48_TDK*26+4*precio_dc_dc_200_425_12
    elif V==672:
        precio=precio_cab+precio_dc_dc12_48_TDK*28+4*precio_dc_dc_200_425_12
    elif V==720:
        precio=precio_cab+precio_dc_dc12_48_TDK*30+4*precio_dc_dc_200_425_12
    elif V==768:
        precio=precio_cab+precio_dc_dc12_48_TDK*32+4*precio_dc_dc_200_425_12
    elif V==816:
        precio=precio_cab+precio_dc_dc12_48_TDK*34+4*precio_dc_dc_200_425_12
    elif V==868:
        precio=precio_cab+precio_dc_dc12_48_TDK*36+6*precio_dc_dc_200_425_12
    elif V==912:
        precio=precio_cab+precio_dc_dc12_48_TDK*38+6*precio_dc_dc_200_425_12
    elif V==960:
        precio=precio_cab+precio_dc_dc12_48_TDK*40+6*precio_dc_dc_200_425_12
    elif V==1008:
        precio=precio_cab+precio_dc_dc12_48_TDK*42+6*precio_dc_dc_200_425_12
    elif V==1056:
        precio=precio_cab+precio_dc_dc12_48_TDK*44+6*precio_dc_dc_200_425_12
    elif V==1104:
        precio=precio_cab+precio_dc_dc12_48_TDK*46+6*precio_dc_dc_200_425_12
    elif V==1152:
        precio=precio_cab+precio_dc_dc12_48_TDK*48+6*precio_dc_dc_200_425_12
    elif V==1200:
        precio=precio_cab+precio_dc_dc12_48_TDK*50+6*precio_dc_dc_200_425_12
    elif V==1248:
        precio=precio_cab+precio_dc_dc12_48_TDK*52+6*precio_dc_dc_200_425_12
    elif V==1296:
        precio=precio_cab+precio_dc_dc12_48_TDK*54+8*precio_dc_dc_200_425_12
    elif V==1344:
         precio=precio_cab+precio_dc_dc12_48_TDK*56+8*precio_dc_dc_200_425_12
    elif V==1392:
         precio=precio_cab+precio_dc_dc12_48_TDK*58+8*precio_dc_dc_200_425_12
    elif V==1440:
         precio=precio_cab+precio_dc_dc12_48_TDK*60+8*precio_dc_dc_200_425_12
    elif V==1488:
         precio=precio_cab+precio_dc_dc12_48_TDK*62+8*precio_dc_dc_200_425_12
    elif V==1536:
         precio=precio_cab+precio_dc_dc12_48_TDK*64+8*precio_dc_dc_200_425_12
    elif V==1584:
         precio=precio_cab+precio_dc_dc12_48_TDK*66+8*precio_dc_dc_200_425_12
    elif V==1632:
         precio=precio_cab+precio_dc_dc12_48_TDK*68+8*precio_dc_dc_200_425_12
    elif V==1680:
         precio=precio_cab+precio_dc_dc12_48_TDK*70+8*precio_dc_dc_200_425_12
    elif V==1728:
         precio=precio_cab+precio_dc_dc12_48_TDK*72+10*precio_dc_dc_200_425_12
    elif V==1776:
         precio=precio_cab+precio_dc_dc12_48_TDK*74+10*precio_dc_dc_200_425_12
         
    
    print('Para el caso de 12 V a {} V y una distancia de {} metros, la caída porcentual de tensión es del {} % y valdrían los cables y convertidores un total de {} USD. {} es válido'.format(V,round(long_cables/2),round(caida_porc,2),round(precio,2),vale))

def calc_prec_(V, long_cables, cable):
    I = calc_corr(12, 50)
    caida, caida_porc, precio_cab, validez_term, perd_pot, validez_caida, vale = caidas_tensión(I, V, cable, long_cables)  # 12V

    precio_dc_dc12_24 = 150.11
    precio_dc_dc12_48_TDK = 150.11
    precio_dc_dc_96_12_delta = 299.03
    precio_dc_dc_200_425_12 = 275

    precios_dc_dc = {
        12: 0,
        24: precio_dc_dc12_24 * 8,
        48: precio_dc_dc12_24 * 8,
        96: precio_dc_dc12_48_TDK * 4 + precio_dc_dc_96_12_delta * 2,
        144: precio_dc_dc12_48_TDK * 12,
        192: precio_dc_dc12_48_TDK * 8 + 4 * precio_dc_dc_96_12_delta,
        240: precio_dc_dc12_48_TDK * 10 + 4 * precio_dc_dc_200_425_12,
        288: precio_dc_dc12_48_TDK * 12 + 4 * precio_dc_dc_200_425_12,
        336: precio_dc_dc12_48_TDK * 14 + 4 * precio_dc_dc_200_425_12,
        384: precio_dc_dc12_48_TDK * 16 + 4 * precio_dc_dc_200_425_12,
        432: precio_dc_dc12_48_TDK * 18 + 4 * precio_dc_dc_200_425_12,
        480: precio_dc_dc12_48_TDK * 20 + 4 * precio_dc_dc_200_425_12,
        528: precio_dc_dc12_48_TDK * 22 + 4 * precio_dc_dc_200_425_12,
        576: precio_dc_dc12_48_TDK * 24 + 4 * precio_dc_dc_200_425_12,
        624: precio_dc_dc12_48_TDK * 26 + 4 * precio_dc_dc_200_425_12,
        672: precio_dc_dc12_48_TDK * 28 + 4 * precio_dc_dc_200_425_12,
        720: precio_dc_dc12_48_TDK * 30 + 4 * precio_dc_dc_200_425_12,
        768: precio_dc_dc12_48_TDK * 32 + 4 * precio_dc_dc_200_425_12,
        816: precio_dc_dc12_48_TDK * 34 + 4 * precio_dc_dc_200_425_12,
        864: precio_dc_dc12_48_TDK * 36 + 6 * precio_dc_dc_200_425_12,
        912: precio_dc_dc12_48_TDK * 38 + 6 * precio_dc_dc_200_425_12,
        960: precio_dc_dc12_48_TDK * 40 + 6 * precio_dc_dc_200_425_12,
        1008: precio_dc_dc12_48_TDK * 42 + 6 * precio_dc_dc_200_425_12,
        1056: precio_dc_dc12_48_TDK * 44 + 6 * precio_dc_dc_200_425_12,
        1104: precio_dc_dc12_48_TDK * 46 + 6 * precio_dc_dc_200_425_12,
        1152: precio_dc_dc12_48_TDK * 48 + 6 * precio_dc_dc_200_425_12,
        1200: precio_dc_dc12_48_TDK * 50 + 6 * precio_dc_dc_200_425_12,
        1248: precio_dc_dc12_48_TDK * 52 + 6 * precio_dc_dc_200_425_12,
        1296: precio_dc_dc12_48_TDK * 54 + 8 * precio_dc_dc_200_425_12,
        1344: precio_dc_dc12_48_TDK * 56 + 8 * precio_dc_dc_200_425_12,
        1392: precio_dc_dc12_48_TDK * 58 + 8 * precio_dc_dc_200_425_12,
        1440: precio_dc_dc12_48_TDK * 60 + 8 * precio_dc_dc_200_425_12,
        1488: precio_dc_dc12_48_TDK * 62 + 8 * precio_dc_dc_200_425_12,
        1536: precio_dc_dc12_48_TDK * 64 + 8 * precio_dc_dc_200_425_12,
        1584: precio_dc_dc12_48_TDK * 66 + 8 * precio_dc_dc_200_425_12,
        1632: precio_dc_dc12_48_TDK * 68 + 8 * precio_dc_dc_200_425_12,
        1680: precio_dc_dc12_48_TDK * 70 + 8 * precio_dc_dc_200_425_12,
        1728: precio_dc_dc12_48_TDK * 72 + 10 * precio_dc_dc_200_425_12,
        1776: precio_dc_dc12_48_TDK * 74 + 10 * precio_dc_dc_200_425_12,
    }

    precio = precio_cab + precios_dc_dc[V]
    return precio, long_cables / 2, validez_term, validez_caida, caida_porc

"""



calc_prec(12,long_cables,cable_120mm)
calc_prec(24, long_cables, cable_50mm)
calc_prec(48, long_cables, cable_70mm)
calc_prec(96, long_cables, cable_35mm)

calc_prec(144, long_cables, cable_25mm)
calc_prec(192, long_cables, cable_50mm)
calc_prec(240, long_cables, cable_35mm)  
calc_prec(288, long_cables, cable_25mm)
    
calc_prec(336,long_cables, cable_25mm)    
calc_prec(384,long_cables, cable_25mm)
calc_prec(432,long_cables, cable_25mm)  
calc_prec(480,long_cables, cable_25mm) 

calc_prec(528,long_cables, cable_95mm) 
calc_prec(576,long_cables, cable_16mm)
calc_prec(624,long_cables, cable_70mm) 
calc_prec(672,long_cables, cable_70mm) 

calc_prec(720,long_cables, cable_70mm) 
calc_prec(768,long_cables, cable_10mm) 
calc_prec(816,long_cables, cable_50mm)
calc_prec(868,long_cables, cable_50mm)

calc_prec(912,long_cables, cable_50mm)
calc_prec(960,long_cables, cable_50mm)
calc_prec(1008,long_cables, cable_50mm)
calc_prec(1056, long_cables, cable_50mm)

calc_prec(1104, long_cables, cable_50mm)
calc_prec(1152, long_cables, cable_35mm)
calc_prec(1200, long_cables, cable_35mm)
calc_prec(1248, long_cables, cable_35mm)

calc_prec(1296, long_cables, cable_35mm)
calc_prec(1344, long_cables, cable_35mm)
calc_prec(1392, long_cables, cable_35mm)
calc_prec(1440, long_cables, cable_35mm)

calc_prec(1488, long_cables, cable_35mm)
calc_prec(1536, long_cables, cable_35mm)
calc_prec(1584, long_cables, cable_35mm)
calc_prec(1632, long_cables, cable_25mm)

calc_prec(1680, long_cables, cable_25mm)
calc_prec(1728, long_cables, cable_25mm)
calc_prec(1728, long_cables, cable_25mm)
calc_prec(1776, long_cables, cable_25mm)
"""

# Definir la estructura de datos para almacenar los resultados
resultados_por_tension = {}

# Definir el último nivel de tensión
ultimo_nivel_tension = 1776

# Iterar sobre cada nivel de tensión
for V in range(48, ultimo_nivel_tension + 1, 48):
    # Inicializar la estructura de datos para este nivel de tensión
    resultados_por_distancia = {}
    
    # Iterar sobre cada distancia de 10 metros a 1500 metros
    for distancia in range(10, 1501, 10):
        # Inicializar la lista de vectores de cable para esta distancia
        vectores_cable = []
        
        # Iterar sobre cada tipo de cable
        for cable_info in cables:
            # Calcular precio, caída de tensión porcentual, validez térmica y validez de caídas
            precio, _, validez_term, validez_caida, caida_porc = calc_prec_(V, distancia, cable_info)
            
            # Almacenar los resultados en un vector
            vector_cable = {
                'seccion': cable_info[0],
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
plt.figure(figsize=(12*7, 8*5))
# Listas para almacenar los precios mínimos y distancias óptimas
precios_optimos = []
distancias_optimas = []

# Iterar sobre cada distancia y encontrar el precio mínimo global entre todas las tensiones
for distancia in range(10, 1500, 10):
    precio_minimo_global = float('inf')  # Precio mínimo global entre todas las tensiones
    distancia_optima = None  # Distancia óptima donde se encuentra el precio mínimo global
    
    # Iterar sobre cada nivel de tensión y sus resultados para encontrar el precio mínimo en esta distancia
    for tension, resultados_por_distancia in resultados_por_tension.items():
        
        if distancia in resultados_por_distancia:
            precio = resultados_por_distancia[distancia]['precio']
            if resultados_por_distancia[distancia]['precio']!=precio_minimo_global:
                del resultados_por_distancia[distancia]['precio']
            
            if precio < precio_minimo_global:
                precio_minimo_global = precio
                distancia_optima = distancia
        
                # Mostrar el número de nivel de tensión en el punto óptimo
                plt.text(distancia_optima, precio_minimo_global, f'{tension} V', fontsize=8, ha='right', va='bottom')
    
    # Almacenar el precio mínimo global y la distancia óptima
    precios_optimos.append(precio_minimo_global)
    distancias_optimas.append(distancia)

# Trazar los puntos óptimos
plt.plot(distancias_optimas, precios_optimos, marker='o', color='blue', label='Puntos óptimos')
# Establecer límites en los ejes x e y
plt.xlim(0, 1500)  # Límites en el eje x desde 0 hasta 1500
plt.ylim(0, 50000)  # Límites en el eje y desde 0 hasta 50000

# Etiquetas de los ejes y título del gráfico
plt.xlabel('Distancia (m)')
plt.ylabel('Precio (USD)')
plt.title('Precio en función de la distancia para la opción más barata en cada tramo')
# Ajustar los intervalos de los ticks en los ejes x e y
plt.xticks(np.arange(0, 1501, 10))  # Intervalo de 100 en 100 metros en el eje x
plt.yticks(np.arange(0, 50001, 500))  # Intervalo de 2500 en 2500 USD en el eje y

# Leyenda y cuadrícula
plt.legend(loc='upper left')
plt.grid(True)

# Mostrar la gráfica
plt.show()
