import armaduras
import numpy as np

#creamos la clase de analisis de la matriz
class AnalisisMatricial():
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
        self.num_reacciones = self.vectorCoordenadasGlobales()

    def __str__(self):
        print("Numero de elementos: ", self.num_elem)
        print("Numero de nodos: ", self.num_nodos)
        print("Numero de grados de libertad: ", self.num_grados)
        print("Numero de reacciones: ", self.num_reacciones)
        return ""

    def vectorCoordenadasGlobales(self):
        reacciones = 0
        for i in range(self.num_nodos):
            tipo = self.tN[i][3]

            if tipo == "Libre":
                reacciones += 0
            elif tipo == "Fijo":
                reacciones += 2
            elif tipo == "DX":
                reacciones += 1
            elif tipo == "DY":
                reacciones += 1
        return reacciones


#creamos las tablas en funcion del usuario
tabla_elem = [
    ['E1', 1, 1, 'N5', 'N1'], 
    ['E2', 1, 1, 'N2', 'N1'],
    ['E3', 1, 1, 'N3', 'N2'],
    ['E4', 1, 1, 'N2', 'N5'],
    ['E5', 1, 1, 'N3', 'N5'],
    ['E6', 1, 1, 'N4', 'N5'],
    ['E7', 1, 1, 'N4', 'N3']]

tabla_nodos = [
    ['N1', 0, 0, "Libre"],
    ['N2', 0, 1, "Libre"],
    ['N3', 1, 1, "Fijo"],
    ['N4', 1, 0, "Fijo"],
    ['N5', 0.5, 0.5, "Libre"]]

tabla_fuerzas = [
    [-3, 'N2', 'DY'],
    [-2, 'N3', 'DY']]

tabla_desplazamientos = [
    [0, 'N1', 'DX'],
    [0, 'N1', 'DY'],
    [0, 'N4', 'DX'],
    [0, 'N4', 'DY']]


AE = AnalisisMatricial(tabla_elem, tabla_nodos, tabla_fuerzas, tabla_desplazamientos)
print(AE)
