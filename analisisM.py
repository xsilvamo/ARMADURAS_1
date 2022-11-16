#!/usr/bin/python3

import numpy as np
import math

__version__ = '0.1.0'


"""
LISTADO DE FUNCIONES PARA ANALICIS MATRICIAL

vectorCoordenadasGlobales() COMPLETADA
matrizPi() Matriz de permutacion COMPLETADA
Armaduras() # accede a la clase armaduras COMPLETADA
matrizRigidezGlobal() Indica la matriz de rigidez global
matrizRigidezGlobalParcial()
vectorFuerzasGlobalesConocidas()
vectorDesplazamientosGlobalesConocidos()
reaccionesDesplazamientos() Indica las reacciones y desplazamientos
tensionCompresion() Indica si la barra esta en tension o compresion

"""

class ARMADURAS():
    #definimos variables
    def __init__(self, elemento, area, moduloE, coor_xi, coor_yi, coor_xf, coor_yf, vectorCoordenadas):
        self.elem = elemento
        self.A = area
        self.E = moduloE
        self.xi = coor_xi
        self.yi = coor_yi
        self.xf = coor_xf
        self.yf = coor_yf
        self.vectorC = vectorCoordenadas

        #propiedades
        self.L = self.Longitud()
        self.rigLoc = self.RigidezLocal()
        self.l_x = self.Lambda_x()
        self.l_y = self.Lambda_y()
        self.T = self.MatrizTransformacion()
        self.rigGlob = self.RigidezGlobal()

    #definimos el metodo str para devolver una cadena de caracteres
    def __str__(self):
        print("Elemento: ", self.elem)
        print("Area: ", self.A)
        print("Modulo de elasticidad: ", self.E)
        print("Coordenadas iniciales: ({}, {})".format(self.xi, self.yi))
        print("Coordenadas finales: ({}, {})".format(self.xf, self.yf))
        print("Vector de coordenadas: ", self.vectorC)
        print("Longitud: ", self.L)
        print("Rigidez local: ", self.rigLoc)
        print("Lambda x: ", self.l_x)
        print("Lambda y: ", self.l_y)
        print("Matriz de transformacion: ", self.T)
        print("Rigidez global: ", self.rigGlob)
        return ""

    #propiedades
    def Longitud(self):
        return math.sqrt((self.xf-self.xi)**2+(self.yf-self.yi)**2)

    def RigidezLocal(self):
        return ((self.A*self.E)/self.L) * np.array([[1, -1], [-1, 1]])

    def Lambda_x(self):
        return (self.xf-self.xi)/self.L

    def Lambda_y(self):
        return (self.yf-self.yi)/self.L

    def MatrizTransformacion(self):
        return np.array([[self.Lambda_x(), self.Lambda_y(), 0, 0], [0, 0, self.Lambda_x(), self.Lambda_y()]])

    def RigidezGlobal(self):
        TransT = np.transpose(self.T)
        TransT_RigLoc = np.matmul(TransT, self.rigLoc)
        return np.matmul(TransT_RigLoc, self.T)


#creamos la clase de analisis de la matriz
class AnalisisMatricial():
    #definimos variables
    def __init__(self, tabla_elem, tabla_nodos, tabla_fuerzas, tabla_desplazamientos):
        self.tE = tabla_elem
        self.tN = tabla_nodos
        self.tF = tabla_fuerzas
        self.tD = tabla_desplazamientos

        #contamos el numero de elementos
        self.num_elem = len(self.tE)
        #contamos el numero de nodos
        self.num_nodos = len(self.tN)
        #contamos el numero de grados de libertad
        self.num_grados = self.num_nodos*2
        #contamos el numero de reacciones
        [self.num_reacciones, self.num_fuerzasConocidas, self.N] = self.vectorCoordenadasGlobales()
        #matriz de permutacion
        self.PI = np.array(self.matrizPi())

        self.armad = self.Armaduras()

        self.Kg = self.matrizRigidezGlobal()

    #definimos el metodo str para devolver una cadena de caracteres
    def __str__(self):
        print("Numero de elementos: ", self.num_elem)
        print("Numero de nodos: ", self.num_nodos)
        print("Numero de grados de libertad: ", self.num_grados)
        print("Numero de reacciones: ", self.num_reacciones)
        print("Numero de fuerzas conocidas: ", self.num_fuerzasConocidas)
        print("Diccionario de nodos: ", self.N)
        print("Matriz de permutacion: ", self.PI)
        print("Elemento 3: ", self.armad[2])
        print("Matriz de rigidez global: ", self.Kg)
        
        return ""

    #definimos el metodo para calcular el vector de coordenadas globales
    def vectorCoordenadasGlobales(self): #FUNCION TERMINADA
        reacciones = 0
        #diccionario de nodos
        dicNodos = {}
        #inicializamos una constante en 1
        #inicializamos una variable de grados de libertad con el total de grados de libertad
        constante = 1
        gradosLibertad = self.num_grados


        for i in range(self.num_nodos):
            tipo = self.tN[i][3]

            #definimos la combinacion para mostrar los nodos
            key_Nodos = self.tN[i][0]
            coorx = self.tN[i][1]
            coory = self.tN[i][2]


            if tipo == "Libre":
                reacciones += 0
                dicNodos.setdefault(key_Nodos, [coorx, coory, constante, constante+1])
                constante += 2
            
            elif tipo == "Fijo":
                reacciones += 2
                dicNodos.setdefault(key_Nodos, [coorx, coory, gradosLibertad-1, gradosLibertad])
                #los nodos que tiene reaccion fija siempre se van a ubicar al final
                gradosLibertad -= 2


            elif tipo == "DX":
                reacciones += 1
                dicNodos.setdefault(key_Nodos, [coorx, coory])

            elif tipo == "DY":
                reacciones += 1
                dicNodos.setdefault(key_Nodos, [coorx, coory])

        #numero de fuerzas conocidas como la diferencia de numero grados libertad menos reacciones
        numFuerzasConocidas = self.num_grados - reacciones
        return reacciones, numFuerzasConocidas, dicNodos

    def matrizPi(self):
        #creamos una lista vacia
        listaPi = []
        for i in range(self.num_elem):
            ninicial = self.tE[i][3]
            nfinal = self.tE[i][4]
            listaPi.append([self.N[ninicial][2], self.N[ninicial][3], self.N[nfinal][2], self.N[nfinal][3]])
        return listaPi

    def Armaduras(self):
        #lista vacia
        element = []
        for i in range(self.num_elem):
            el = self.tE[i][0]
            #area
            a = self.tE[i][1]
            modE = self.tE[i][2]
            #nodo inicial
            NI = self.tE[i][3]
            #nodo final
            NF = self.tE[i][4]
            xi = self.N[NI][0]
            yi = self.N[NI][1]
            xf = self.N[NF][0]
            yf = self.N[NF][1]
            #coordenadas locales
            xil = self.N[NI][2]
            yil = self.N[NI][3]
            xfl = self.N[NF][2]
            yfl = self.N[NF][3]
            #infocar clase ARMADURA
            element.append(ARMADURAS(el, a, modE, xi, yi, xf, yf, [xil, yil, xfl, yfl]))
        return element

    def matrizRigidezGlobal(self):
        #matriz rigidez global vacia (k)
        k = np.zeros((self.num_grados, self.num_grados))

        for e in range(self.num_elem):
            #matriz de rigidez local
            rigGlobal = self.armad[e].rigGlob
            for i in range(4):
                for j in range(4):
                    a = self.PI[e][i]-1 #debemos quitarle una unidad porque python empieza en 0
                    b = self.PI[e][j]-1 
                    k[a][b] = rigGlobal[i,j] + k[a,b]
        return k

#creamos las tablas en funcion del usuario
# tabla_elem = [
#     ['E1', 1, 1, 'N5', 'N1'], 
#     ['E2', 1, 1, 'N2', 'N1'],
#     ['E3', 1, 1, 'N3', 'N2'],
#     ['E4', 1, 1, 'N2', 'N5'],
#     ['E5', 1, 1, 'N3', 'N5'],
#     ['E6', 1, 1, 'N4', 'N5'],
#     ['E7', 1, 1, 'N4', 'N3']]

# tabla_nodos = [
#     ['N1', 14, 7, "Libre"],
#     ['N2', 7, 7, "Libre"],
#     ['N3', 0, 7, "Fijo"],
#     ['N4', 0, 0, "Fijo"],
#     ['N5', 7, 0, "Libre"]]

# tabla_fuerzas = [
#     [-3, 'N2', 'DY'],
#     [-2, 'N1', 'DY']]

# tabla_desplazamientos = [
#     [0, 'N3', 'DX'],
#     [0, 'N3', 'DY'],
#     [0, 'N4', 'DX'],
#     [0, 'N4', 'DY']]

tabla_nodos = [
    ['N1', 0, 0, "Fijo"],
    ['N2', 150, 0, "Libre"],
    ['N3', 300, 0, "Libre"],
    ['N4', 450, 0, "Fijo"],
    ['N5', 300, 75, "Libre"],
    ['N6', 150, 75, "Libre"]
    ]

tabla_elem = [
    ['E1', 1, 1, 'N1', 'N2'],
    ['E2', 1, 1, 'N2', 'N3'],
    ['E3', 1, 1, 'N2', 'N5'],
    ['E4', 1, 1, 'N2', 'N6'],
    ['E5', 1, 1, 'N3', 'N4'],
    ['E6', 1, 1, 'N3', 'N5'],
    ['E7', 1, 1, 'N4', 'N5'],
    ['E8', 1, 1, 'N5', 'N6'],
    ['E9', 1, 1, 'N6', 'N1']
]

tabla_fuerzas = [
    [6.250,00, 'N3', 'DX'],
    [-10.825,32, 'N3', 'DY']]

tabla_desplazamientos = [
    [0, 'N1', 'DX'],
    [0, 'N1', 'DY'],
    [0, 'N4', 'DY']]


AE = AnalisisMatricial(tabla_elem, tabla_nodos, tabla_fuerzas, tabla_desplazamientos)
print(AE)
