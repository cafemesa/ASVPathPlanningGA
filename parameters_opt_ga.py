#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:14:34 2017

@author: mario
"""
import numpy as np
import csv

#==============================================================================
# # PARAMETROS
#==============================================================================

#INPUT1 = 'arr_alg_pattern_size5.csv'
INPUT2 = 'sampled_grid_event_tracking.csv'
INPUT3 = 'combination.csv'
INPUT4 = 'ListaCoordenadasConvRefMetros3.csv'
INPUT5 = 'intersection_routes.csv'
INPUT6 = 'best_last_pop.csv'
#INPUT7 = 'sampled_grid_event_tracking2.csv'

OUTPUT1 = 'best_indiv_test_ngen100_sim1.csv'
OUTPUT2 = 'improve_rate_ngen100_sim1.csv'
OUTPUT3 = 'ImproveRate_Solution_ngen100_sim1.png'
OUTPUT4 = 'Best_Solution_ngen100_sim1.csv'
OUTPUT5 = 'best_last_pop2.csv'

N_BEACON = 60 
N_SIM = 3
CXPB = 0.8
MUTPB =  0.2
NGEN = 10
POPU = 100
ELIT_RATE = 0.2 
FRANJA = 20
ATT_FACTOR = 1000 # Intentos para encontrar siguiente baliza en poblacion inicial valida
ATT_POPU = 10000 # Intentos para encontrar una poblacion inicial validad  de POPU individuos
LAKE_SIZE = 68720000

LAKE_SIZE_X = 12000
LAKE_SIZE_Y = 14000

GRID_SIZE = 200 # metros
GRID_X_DIV = LAKE_SIZE_X/GRID_SIZE # numero de cuadros sobre el eje x
GRID_Y_DIV = LAKE_SIZE_Y/GRID_SIZE # numero de cuadros sobre el eje y

FIT_FUNC_TYPE = 2
STRATEGY_PHASE = 1 #NO CAMBIAR HASTA ENCONTRAR FUNCION DE SUB_GRUPO
'''
1 - Death Penalty + Penalty Factor - km2
2 - Penalty Factor - coverage %
3 - Exponential Penalty Factor - coverage %
4 - Penalty Factor - size km2
5 - Penalty Factor - ROI
6-  Death Penalty
'''

#==============================================================================
# # CONSTANTES
#==============================================================================
arr_sampled_grid_pattern = np.loadtxt(INPUT2, dtype = 'uint8', 
                                      delimiter =',')

###############################################################################

if STRATEGY_PHASE == 1:
        arr_subgroup = np.arange(60,dtype='uint8') 

else:
    #PENDIENTE MECANISMO DE SELECCION DE SUBGRUPO DE BALIZAS!!!!!
    
    arr_reg1= np.loadtxt('reg1_ev_track.csv' ,dtype = 'uint8', delimiter =',')
    arr_reg2= np.loadtxt('reg2_ev_track.csv' ,dtype = 'uint8', delimiter =',')
    
    
    arr_subgroup = np.concatenate((arr_reg1,arr_reg2))


###############################################################################

arr_allowed_routes = np.loadtxt(INPUT3,dtype = 'uint8',delimiter =',' )

###############################################################################

lst_centers = []
for x in range(GRID_X_DIV):
    sublst_centers = []
    for y in range(GRID_Y_DIV):
        sublst_centers.append([x, y])
    lst_centers.append(sublst_centers)

arr_centers = np.array(lst_centers)
arr_centers_coord = GRID_SIZE*arr_centers+GRID_SIZE/2


###############################################################################

ifile  = open(INPUT5, "rb") #
reader = csv.reader(ifile)


intersec_routes = [] # lista con intersecciones entre rutas (matrix 3,600 x 3,600)

for lst_intersec_ori in reader: 
    sub_lst_intersec = [] # sublista correspondiente a una linea de la matriz
    for lst_intersec_dst in lst_intersec_ori:
       if lst_intersec_dst != '':       
           sub_lst_intersec.append(lst_intersec_dst) 
    intersec_routes.append(sub_lst_intersec)
ifile.close()
###############################################################################

#==============================================================================
# ###########Importar Coordenadas de Archivo###################################
#   Importa archivoListaCoordenadasConvRefMetros.csv
#   ListaCoordenadasConvRefMetros.csv = Matriz 60 x 2
#   Cada linea de la matriz representa las coordenadas en metros de cada baliza
#   Ej.: b0 = (4860, 13500)
#   El origen es un punto de referencia
#==============================================================================

with open(INPUT4, 'rb') as f: 
    reader = csv.reader(f)
    coord_orig = list(reader)
    
###Coordenadas para el calculo del rango de accion en numeros decimales########
    
list_coord = [] # lista de coordenadas de balizas en formato (x,y)

for n in coord_orig:
    coord = [float(n[0]), float(n[1])]
    list_coord.append(coord)

#############Coordenadas para el algoritmo genetico en numeros complejos#######


    
list_coord2 = [] # lista de coordenadas de balizas en formato (x + jy) 
#                   (numero complejo)

for n in coord_orig:
    list_coord2.append(complex(float(n[0]),float(n[1])))
    
    
    
list_coord_subgroup =[]
    
for element in arr_subgroup:
        list_coord_subgroup.append(list_coord2[element])

    
cities = list_coord2 # 1- coordenadas de la ciudad en el TSP, se utiliza para
#    create_tour y graficar
#    cities = list_coord_subgroup # 2- subgrupo de balizas

#print 'len cities', len(cities)