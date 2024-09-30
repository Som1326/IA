import tkinter as tk
import numpy as np
from tkinter import filedialog
from Amplitud import busqueda_amplitud
from Costo import busqueda_costo_uniforme
from Profundidad import busqueda_preferente_por_profundidad
from Avara import busqueda_avara
from A_Estrella import busqueda_A_estrella

def abrir_archivo():
    # Inicializamos la ventana de tkinter
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal
    
    # Abrimos el diálogo para seleccionar el archivo
    archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    # Leemos el archivo seleccionado y retornamos la matriz ciudad
    if archivo:
        return iniciar_variables(archivo)
    else:
        print("No se seleccionó ningún archivo.")
        return None

def iniciar_variables(archivo):
    if archivo:
        with open(archivo, 'r') as file:
            lineas = file.readlines()  # Leemos todas las líneas del archivo

            # Creamos una lista para almacenar los valores del mapa
            ciudad = []
            
            for linea in lineas:
                # Eliminamos espacios en blanco y convertimos la línea en una lista de enteros
                valores_fila = list(map(int, linea.strip().split()))
                
                # Añadimos la fila a la lista ciudad
                ciudad.append(valores_fila)

            # Convertimos la lista a un array de numpy para un manejo más fácil
            ciudad = np.array(ciudad)
            print("Mapa de la ciudad cargado correctamente:")
            print(ciudad)
            
            # Devolvemos la matriz ciudad
            return ciudad
    else:
        print("Archivo no encontrado o inválido.")
        return None

mapa = abrir_archivo()

print("\n------------------------------------------------")
print("Resultados de las búsquedas no informadas:\n")
print("Busqueda en amplitud:")
rutaAmplitud, costo_totalAmplitud = busqueda_amplitud(mapa)
print("Ruta encontrada:", rutaAmplitud)
print("Costo total:", costo_totalAmplitud, "\n")
print("------------------------------------------------")
print("Busqueda en costo:")
rutaCosto, costo_totalCosto = busqueda_costo_uniforme(mapa)
print("Ruta encontrada:", rutaCosto)
print("Costo total:", costo_totalCosto, "\n")
print("------------------------------------------------")
print("Busqueda en profundidad:")
rutaProfundidad, costo_totalProfundidad = busqueda_preferente_por_profundidad(mapa)
print("Ruta encontrada:", rutaProfundidad)
print("Costo total:", costo_totalProfundidad, "\n")
print("------------------------------------------------")

print("\n------------------------------------------------")
print("Resultados de las búsquedas informadas:\n")
print("Busqueda en Avara:")
rutaAvara, heuristicaAvara, costo_totalAvara = busqueda_avara(mapa)
print("Ruta encontrada:", rutaAvara)
# print("Heuristica:", heuristicaAvara)
print("Costo total:", costo_totalAvara, "\n")
print("------------------------------------------------")
print("Busqueda en A*:")
rutaA_Estrella, heuristicaAEstrella, costo_totalA_Estrella = busqueda_A_estrella(mapa)
print("Ruta encontrada:", rutaA_Estrella)
# print("Heuristica:", heuristicaAEstrella)
print("Costo total:", costo_totalA_Estrella, "\n")
print("------------------------------------------------")