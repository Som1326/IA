import tkinter as tk
import numpy as np
from tkinter import filedialog
from Amplitud import busqueda_amplitud

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

ruta, costo_total = busqueda_amplitud(mapa)
print("Ruta encontrada:", ruta)
print("Costo total:", costo_total)