#!/usr/bin/python3

__version__ = '0.1.0'

import math
import numpy as np

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


A = 1
E = 1
xi = 0
yi = 0
xf = 4
yf = 3 
vectorC = [5, 6, 1, 2]

e1 = ARMADURAS("Elem 1", A, E, xi, yi, xf, yf, vectorC)
print(e1)