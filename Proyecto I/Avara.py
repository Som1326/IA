import numpy as np
import heapq  # Para usar una cola de prioridad

# Movimientos posibles (arriba, derecha, abajo, izquierda)
MOVIMIENTOS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def es_valida(pos, ciudad):
    filas, cols = len(ciudad), len(ciudad[0])
    x, y = pos
    return 0 <= x < filas and 0 <= y < cols and ciudad[x][y] != 1  # Verificamos si es una posición válida

def costo(casilla):
    if casilla == 0:
        return 1  # tráfico liviano
    elif casilla == 3:
        return 4  # tráfico medio
    elif casilla == 4:
        return 7  # tráfico pesado
    elif casilla == 5:
        return 1  # el costo de la casilla del pasajero es como una vía libre
    elif casilla == 6:
        return 1  # el costo de la casilla del destino es como una vía libre
    return float('inf')  # Infinito para posiciones no válidas

def heuristica(pos, destino):
    # Distancia de Manhattan
    return abs(pos[0] - destino[0]) + abs(pos[1] - destino[1])

def encontrar_posiciones(ciudad):
    inicio = None
    pasajero = None
    destino = None

    # Recorremos la matriz para encontrar las posiciones de inicio, pasajero y destino
    for i in range(len(ciudad)):
        for j in range(len(ciudad[0])):
            if ciudad[i][j] == 2:
                inicio = (i, j)
            elif ciudad[i][j] == 5:
                pasajero = (i, j)
            elif ciudad[i][j] == 6:
                destino = (i, j)

    return inicio, pasajero, destino

def busqueda_avara(ciudad):
    # Extraemos las posiciones de inicio, pasajero y destino
    inicio, pasajero, destino = encontrar_posiciones(ciudad)

    if not inicio or not pasajero or not destino:
        print("No se encontraron todas las posiciones necesarias en el mapa.")
        return "Falló la búsqueda"

    # Cola de prioridad para la búsqueda avara
    cola_prioridad = []
    # Inicializamos la cola con el nodo inicial
    heapq.heappush(cola_prioridad, (heuristica(inicio, pasajero), inicio, False, [], 0))  # (h(n), posición, tiene pasajero, ruta)
    visitados = set()

    while cola_prioridad:
        h_n, (x, y), tiene_pasajero, ruta, costo_acumulado = heapq.heappop(cola_prioridad)

        # Si encontramos al pasajero y luego el destino
        if (x, y) == destino and tiene_pasajero:
            return ruta + [(x, y)], heuristica(destino, destino), costo_acumulado

        # Expandir el nodo
        for dx, dy in MOVIMIENTOS:
            nuevo_x, nuevo_y = x + dx, y + dy
            if es_valida((nuevo_x, nuevo_y), ciudad):
                nueva_pos = (nuevo_x, nuevo_y)
                nuevo_costo = costo_acumulado + costo(ciudad[nuevo_x][nuevo_y])
                
                # Verificar si alcanzamos al pasajero
                nuevo_tiene_pasajero = tiene_pasajero
                if ciudad[nuevo_x][nuevo_y] == 5:
                    nuevo_tiene_pasajero = True
                
                # Solo continuar si no hemos visitado este estado
                if (nueva_pos, nuevo_tiene_pasajero) not in visitados:
                    visitados.add((nueva_pos, nuevo_tiene_pasajero))
                    nueva_ruta = ruta + [(x, y)]
                    if nuevo_tiene_pasajero:
                        # Añadir a la cola de prioridad con el valor de la heurística
                        heapq.heappush(cola_prioridad, (heuristica(nueva_pos, destino), nueva_pos, nuevo_tiene_pasajero, nueva_ruta, nuevo_costo))
                    else:
                        # Añadir a la cola de prioridad con el valor de la heurística al pasajero
                        heapq.heappush(cola_prioridad, (heuristica(nueva_pos, pasajero), nueva_pos, nuevo_tiene_pasajero, nueva_ruta, nuevo_costo))

    return "Falló la búsqueda"