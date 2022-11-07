import armaduras
import numpy as np

#creamos la clase de analisis de la matriz
class AnalisisMatricial():
    def __init__(self, tabla_elem, tabla_nodos, tabla_fuerzas, tabla_desplazamientos):
        self.tE = tabla_elem
        self.tN = tabla_nodos
        self.tF = tabla_fuerzas
        self.tD = tabla_desplazamientos


#creamos las tablas en funcion del usuario
tabla_elem = [
    ['E1', 1, 1, 'N5', 'N1'],
    ['E2', 1, 1, 'N2', 'N1'],
    ['E3', 1, 1, 'N3', 'N2'],
    ['E4', 1, 1, 'N2', 'N5'],
    ['E5', 1, 1, 'N3', 'N5']
    ['E6', 1, 1, 'N4', 'N5'],
    ['E7', 1, 1, 'N4', 'N3']]

tabla_nodos = []
tabla_fuerzas = []
tabla_desplazamientos = []