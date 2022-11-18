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
    def __init__(self, barra, area, moduloE, coor_xi, coor_yi, coor_xf, coor_yf, vectorCoordenadas):
        self.bar = barra
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
        print("Barra: ", self.bar)
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
    def __init__(self, tabla_barras, tabla_nodos, tabla_fuerzas, tabla_desplazamientos):
        self.tB = tabla_barras
        self.tN = tabla_nodos
        self.tF = tabla_fuerzas
        self.tD = tabla_desplazamientos

        #contamos el numero de barras
        self.num_barra = len(self.tB)
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

        [self.k11 , self.k12, self.k21, self.k22] = self.matrizRigidezGlobalParcial()

        self.FgC = self.vectorFuerzasGlobalesConocidas()

        self.DgC = self.vectorDesplazamientosGlobalesConocidos()

        [self.DesplazamientosDesconocidos, self.FuerzasDesconocidas, self.FuerzasGlobales, self.DesplazamientosGlobales] = self.reaccionesDesplazamientos()

        self.tc = self.tensionCompresion()

    #definimos el metodo str para devolver una cadena de caracteres
    def __str__(self):
        print("Numero de Barras: ", self.num_barra)
        print("Numero de nodos: ", self.num_nodos)
        print("Numero de grados de libertad: ", self.num_grados)
        print("Numero de reacciones: ", self.num_reacciones)
        print("Numero de fuerzas conocidas: ", self.num_fuerzasConocidas)
        print("Diccionario de nodos: ", self.N)
        print("Matriz de permutacion: \n", self.PI)
        print("Barra 3: ", self.armad[2])
        print("Matriz de rigidez global: \n", self.Kg)
        print("\nMatriz de rigidez k11: \n", self.k11)
        print("\nMatriz de rigidez k12: \n", self.k12)
        print("\nMatriz de rigidez k21: \n", self.k21)
        print("\nMatriz de rigidez k22: \n", self.k22)
        print("\nVector de fuerzas conocidas: \n", self.FgC)
        print("\nVector de desplazamientos conocidos: \n", self.DgC)
        print("\nVector de fuerzas desconocidas: \n", self.FuerzasDesconocidas)
        print("\nVector de desplazamientos desconocidos: \n", self.DesplazamientosDesconocidos)
        print("\nVector de fuerzas globales: \n", self.FuerzasGlobales)
        print("\nVector de desplazamientos globales: \n", self.DesplazamientosGlobales)
        print("\nTensiones y compresiones: \n", self.tc)
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
                dicNodos.setdefault(key_Nodos, [coorx, coory, constante, gradosLibertad])
                constante += 1
                gradosLibertad -= 1

            elif tipo == "DY":
                reacciones += 1
                dicNodos.setdefault(key_Nodos, [coorx, coory, gradosLibertad, constante])
                constante += 1
                gradosLibertad -= 1

        #numero de fuerzas conocidas como la diferencia de numero grados libertad menos reacciones
        numFuerzasConocidas = self.num_grados - reacciones
        return reacciones, numFuerzasConocidas, dicNodos

    def matrizPi(self):
        #creamos una lista vacia
        listaPi = []
        for i in range(self.num_barra):
            ninicial = self.tB[i][3]
            nfinal = self.tB[i][4]
            listaPi.append([self.N[ninicial][2], self.N[ninicial][3], self.N[nfinal][2], self.N[nfinal][3]])
        return listaPi

    def Armaduras(self):
        #lista vacia
        element = []
        for i in range(self.num_barra):
            el = self.tB[i][0]
            #area
            a = self.tB[i][1]
            modE = self.tB[i][2]
            #nodo inicial
            NI = self.tB[i][3]
            #nodo final
            NF = self.tB[i][4]
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

        for e in range(self.num_barra):
            #matriz de rigidez local
            rigGlobal = self.armad[e].rigGlob
            for i in range(4):
                for j in range(4):
                    a = self.PI[e][i]-1 #debemos quitarle una unidad porque python empieza en 0
                    b = self.PI[e][j]-1 
                    k[a][b] = rigGlobal[i,j] + k[a,b]
        return k

    def matrizRigidezGlobalParcial(self):
        k11 = self.Kg[0:self.num_fuerzasConocidas, 0:self.num_fuerzasConocidas]
        k12 = self.Kg[0:self.num_fuerzasConocidas, self.num_fuerzasConocidas:self.num_grados]
        k21 = self.Kg[self.num_fuerzasConocidas:self.num_grados, 0:self.num_fuerzasConocidas]
        k22 = self.Kg[self.num_fuerzasConocidas:self.num_grados, self.num_fuerzasConocidas:self.num_grados]
        return k11, k12, k21, k22
    
    def vectorFuerzasGlobalesConocidas(self):
        FuerzasConocidas = np.zeros((self.num_fuerzasConocidas, 1))
        for i in range(len(self.tF)):
            nodo = self.tF[i][1]
            direccion = self.tF[i][2]
            if direccion == 'DX':
                j = self.N[nodo][2]-1
            elif direccion == 'DY':
                j = self.N[nodo][3]-1
            FuerzasConocidas[j] = self.tF[i][0]
        return FuerzasConocidas


    def vectorDesplazamientosGlobalesConocidos(self):
        DesplazamientosConocidos = np.zeros((self.num_grados - self.num_fuerzasConocidas, 1)) #vector de desplazamientos conocidos
        for i in range(len(self.tD)): #recorremos la tabla de desplazamientos
            nodo = self.tD[i][1]
            direccion = self.tD[i][2]
            if direccion == 'DX':
                j = self.N[nodo][2]-1
            elif direccion == 'DY':
                j = self.N[nodo][3]-1
            DesplazamientosConocidos[j-self.num_fuerzasConocidas] = self.tD[i][0]
        return DesplazamientosConocidos
    
    def reaccionesDesplazamientos(self):
        k11_inv = np.linalg.inv(self.k11)
        DesplazamientosDesconocidos =  np.matmul(k11_inv , (self.FgC - np.matmul(self.k12, self.DgC)))
        FuerzasDesconocidas = np.matmul(self.k21, DesplazamientosDesconocidos) + np.matmul(self.k22, self.DgC)
        FuerzasGlobales = np.concatenate((self.FgC, FuerzasDesconocidas), axis=0)
        DesplazamientosGlobales = np.concatenate((DesplazamientosDesconocidos, self.DgC), axis=0)
        return DesplazamientosDesconocidos, FuerzasDesconocidas, FuerzasGlobales, DesplazamientosGlobales

    def tensionCompresion(self):
        #creamos una lista vacia para ir almacenando los valores de tension y compresion
        listaTC = []
        for e in range(self.num_barra):
            TransElem = self.armad[e].T
            ke_local = self.armad[e].rigLoc
            desplix = self.DesplazamientosGlobales[self.armad[e].vectorC[0] -1]
            despliy = self.DesplazamientosGlobales[self.armad[e].vectorC[1] -1]
            desplfx = self.DesplazamientosGlobales[self.armad[e].vectorC[2] -1]
            desplfy = self.DesplazamientosGlobales[self.armad[e].vectorC[3] -1]
            desplazamientos = np.array([desplix, despliy, desplfx, desplfy])
            ke_local_TransElem = np.matmul(ke_local, TransElem)
            ke_local_TransElem_Despl = np.matmul(ke_local_TransElem, desplazamientos)
            listaTC.append(round(float(ke_local_TransElem_Despl[1]), 2))
        return listaTC 
            



#creamos las tablas en funcion del usuario
# tabla_barras = [
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

tabla_barras = [
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
    [6250.00 , 'N3', 'DX'],
    [-10825.32 , 'N3', 'DY']]

tabla_desplazamientos = [
    [0, 'N1', 'DX'],
    [0, 'N1', 'DY'],
    [0, 'N4', 'DY']]


AE = AnalisisMatricial(tabla_barras, tabla_nodos, tabla_fuerzas, tabla_desplazamientos)
print(AE)
