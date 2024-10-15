import numpy as np
from collections import deque
import heapq
import time

class SmartCar:
    MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def iniciar_variables(self,archivo):
        if archivo:
            with open(archivo, 'r') as file:
                lineas = file.readlines()
                ciudad = [list(map(int, linea.strip().split())) for linea in lineas]
                ciudad = np.array(ciudad)
                return ciudad
        else:
            print("Archivo no encontrado o inválido.")
            return None
    
    def es_valida(self, pos, ciudad):
        filas, cols = len(ciudad), len(ciudad[0])
        x, y = pos
        return 0 <= x < filas and 0 <= y < cols and ciudad[x][y] != 1  # Verificamos si es una posición válida

    def costo(self, casilla):
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

    def heuristica(self, pos, destino):
        # Distancia de Manhattan
        return abs(pos[0] - destino[0]) + abs(pos[1] - destino[1])

    def encontrar_posiciones(self, ciudad):
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
    
    def busqueda_amplitud(self, ciudad):
        # Extraemos las posiciones de inicio, pasajero y destino
        inicio, pasajero, destino = self.encontrar_posiciones(ciudad)
        
        if not inicio or not pasajero or not destino:
            print("No se encontraron todas las posiciones necesarias en el mapa.")
            return "Falló la búsqueda"

        tiempo_inicio = time.time()
        nodos_expandidos = 0
        profundidad_arbol = 0
        cola = deque([(inicio, 0, False, [])])  # (posición, costo acumulado, tiene pasajero, ruta)
        visitados = set()
        visitados.add((inicio, False))  # (posición, tiene pasajero)

        while cola:
            (x, y), costo_acumulado, tiene_pasajero, ruta = cola.popleft()
            nodos_expandidos += 1

            if len(ruta) > profundidad_arbol:
                profundidad_arbol = len(ruta)
                
            if (x, y) == destino and tiene_pasajero:
                tiempo_fin = time.time()
                tiempo_total = tiempo_fin - tiempo_inicio
                return {
                    "ruta": ruta + [(x, y)],
                    "costo": costo_acumulado,
                    "nodos_expandidos": nodos_expandidos,
                    "profundidad_arbol": profundidad_arbol,
                    "tiempo_computo": tiempo_total
                }
            
            # Expandir el nodo
            for dx, dy in self.MOVIMIENTOS:
                nuevo_x, nuevo_y = x + dx, y + dy
                if self.es_valida((nuevo_x, nuevo_y), ciudad):
                    nueva_pos = (nuevo_x, nuevo_y)
                    nuevo_costo = costo_acumulado + self.costo(ciudad[nuevo_x][nuevo_y])
                    
                    nuevo_tiene_pasajero = tiene_pasajero
                    # Verificar si alcanzamos al pasajero
                    if ciudad[nuevo_x][nuevo_y] == 5:
                        nuevo_tiene_pasajero = True
                    
                    # Solo continuar si no hemos visitado este estado
                    if (nueva_pos, nuevo_tiene_pasajero) not in visitados:
                        visitados.add((nueva_pos, nuevo_tiene_pasajero))
                        # Añadir la nueva posición a la ruta
                        nueva_ruta = ruta + [(x, y)]
                        cola.append((nueva_pos, nuevo_costo, nuevo_tiene_pasajero, nueva_ruta))

        return "Falló la búsqueda"

    def busqueda_costo_uniforme(self, ciudad):
        # Extraemos las posiciones de inicio, pasajero y destino
        inicio, pasajero, destino = self.encontrar_posiciones(ciudad)
        
        if not inicio or not pasajero or not destino:
            print("No se encontraron todas las posiciones necesarias en el mapa.")
            return "Falló la búsqueda"

        tiempo_inicio = time.time()
        nodos_expandidos = 0
        profundidad_arbol = 0
        # Cola de prioridad (costo acumulado, posición, tiene pasajero, ruta)
        cola_prioridad = [(0, inicio, False, [])]
        visitados = set()
        visitados.add((inicio, False))  # (posición, tiene pasajero)

        while cola_prioridad:
            # Extraemos el nodo con menor costo acumulado
            costo_acumulado, (x, y), tiene_pasajero, ruta = heapq.heappop(cola_prioridad)
            nodos_expandidos += 1
            
            if len(ruta) > profundidad_arbol:
                profundidad_arbol = len(ruta)

            # Si encontramos al pasajero y luego el destino
            if (x, y) == destino and tiene_pasajero:
                tiempo_fin = time.time()
                tiempo_total = tiempo_fin - tiempo_inicio
                return {
                    "ruta": ruta + [(x, y)],
                    "costo": costo_acumulado,
                    "nodos_expandidos": nodos_expandidos,
                    "profundidad_arbol": profundidad_arbol,
                    "tiempo_computo": tiempo_total
                }
            
            # Expandir el nodo
            for dx, dy in self.MOVIMIENTOS:
                nuevo_x, nuevo_y = x + dx, y + dy
                if self.es_valida((nuevo_x, nuevo_y), ciudad):
                    nueva_pos = (nuevo_x, nuevo_y)
                    nuevo_costo = costo_acumulado + self.costo(ciudad[nuevo_x][nuevo_y])
                    
                    nuevo_tiene_pasajero = tiene_pasajero
                    # Verificar si alcanzamos al pasajero
                    if ciudad[nuevo_x][nuevo_y] == 5:
                        nuevo_tiene_pasajero = True
                    
                    # Solo continuar si no hemos visitado este estado
                    if (nueva_pos, nuevo_tiene_pasajero) not in visitados:
                        visitados.add((nueva_pos, nuevo_tiene_pasajero))
                        # Añadir el nuevo nodo a la cola de prioridad
                        heapq.heappush(cola_prioridad, (nuevo_costo, nueva_pos, nuevo_tiene_pasajero, ruta + [(x, y)]))

        return "Falló la búsqueda"

    def busqueda_preferente_por_profundidad(self, ciudad):
        MOVIMIENTOS_P = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # Extraemos las posiciones de inicio, pasajero y destino
        inicio, pasajero, destino = self.encontrar_posiciones(ciudad)

        if not inicio or not pasajero or not destino:
            print("No se encontraron todas las posiciones necesarias en el mapa.")
            return "Falló la búsqueda"
        
        tiempo_inicio = time.time()
        nodos_expandidos = 0
        profundidad_arbol = 0
        # Pila para búsqueda por profundidad
        pila = [(inicio, 0, False, [])]  # (posición, costo acumulado, tiene pasajero, ruta)
        visitados = set()
        
        while pila:
            (x, y), costo_acumulado, tiene_pasajero, ruta = pila.pop()
            nodos_expandidos += 1
            
            if len(ruta) > profundidad_arbol:
                profundidad_arbol = len(ruta)

            # Si encontramos al pasajero y luego el destino
            if (x, y) == destino and tiene_pasajero:
                tiempo_fin = time.time()
                tiempo_total = tiempo_fin - tiempo_inicio
                return {
                    "ruta": ruta + [(x, y)],
                    "costo": costo_acumulado,
                    "nodos_expandidos": nodos_expandidos,
                    "profundidad_arbol": profundidad_arbol,
                    "tiempo_computo": tiempo_total
                }
            
            # Expandir el nodo
            for dx, dy in MOVIMIENTOS_P:
                nuevo_x, nuevo_y = x + dx, y + dy
                if self.es_valida((nuevo_x, nuevo_y), ciudad):
                    nueva_pos = (nuevo_x, nuevo_y)
                    nuevo_costo = costo_acumulado + self.costo(ciudad[nuevo_x][nuevo_y])
                    
                    nuevo_tiene_pasajero = tiene_pasajero
                    # Verificar si alcanzamos al pasajero
                    if ciudad[nuevo_x][nuevo_y] == 5:
                        nuevo_tiene_pasajero = True
                    
                    # Solo continuar si no hemos visitado este estado
                    if (nueva_pos, nuevo_tiene_pasajero) not in visitados:
                        visitados.add((nueva_pos, nuevo_tiene_pasajero))
                        # Añadir la nueva posición a la ruta
                        nueva_ruta = ruta + [(x, y)]
                        pila.append((nueva_pos, nuevo_costo, nuevo_tiene_pasajero, nueva_ruta))

        return "Falló la búsqueda"
    
    def busqueda_avara(self, ciudad):
        # Extraemos las posiciones de inicio, pasajero y destino
        inicio, pasajero, destino = self.encontrar_posiciones(ciudad)

        if not inicio or not pasajero or not destino:
            print("No se encontraron todas las posiciones necesarias en el mapa.")
            return "Falló la búsqueda"

        tiempo_inicio = time.time()
        nodos_expandidos = 0
        profundidad_arbol = 0
        # Cola de prioridad para la búsqueda avara
        cola_prioridad = []
        # Inicializamos la cola con el nodo inicial
        heapq.heappush(cola_prioridad, (self.heuristica(inicio, pasajero), inicio, False, [], 0))  # (h(n), posición, tiene pasajero, ruta)
        visitados = set()

        while cola_prioridad:
            h_n, (x, y), tiene_pasajero, ruta, costo_acumulado = heapq.heappop(cola_prioridad)
            nodos_expandidos += 1
            
            if len(ruta) > profundidad_arbol:
                profundidad_arbol = len(ruta)
                
            if (x, y) == destino and tiene_pasajero:
                tiempo_fin = time.time()
                tiempo_total = tiempo_fin - tiempo_inicio
                return {
                    "ruta": ruta + [(x, y)],
                    "heuristica": self.heuristica(destino, destino),
                    "costo": costo_acumulado,
                    "nodos_expandidos": nodos_expandidos,
                    "profundidad_arbol": profundidad_arbol,
                    "tiempo_computo": tiempo_total
                }

            # Expandir el nodo
            for dx, dy in self.MOVIMIENTOS:
                nuevo_x, nuevo_y = x + dx, y + dy
                if self.es_valida((nuevo_x, nuevo_y), ciudad):
                    nueva_pos = (nuevo_x, nuevo_y)
                    nuevo_costo = costo_acumulado + self.costo(ciudad[nuevo_x][nuevo_y])
                    
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
                            heapq.heappush(cola_prioridad, (self.heuristica(nueva_pos, destino), nueva_pos, nuevo_tiene_pasajero, nueva_ruta, nuevo_costo))
                        else:
                            # Añadir a la cola de prioridad con el valor de la heurística al pasajero
                            heapq.heappush(cola_prioridad, (self.heuristica(nueva_pos, pasajero), nueva_pos, nuevo_tiene_pasajero, nueva_ruta, nuevo_costo))

        return "Falló la búsqueda"
    
    def busqueda_A_estrella(self, ciudad):
        # Extraemos las posiciones de inicio, pasajero y destino
        inicio, pasajero, destino = self.encontrar_posiciones(ciudad)

        if not inicio or not pasajero or not destino:
            print("No se encontraron todas las posiciones necesarias en el mapa.")
            return "Falló la búsqueda"

        tiempo_inicio = time.time()
        nodos_expandidos = 0
        profundidad_arbol = 0
        # Cola de prioridad para la búsqueda avara
        cola_prioridad = []
        # Inicializamos la cola con el nodo inicial
        heapq.heappush(cola_prioridad, (0 + self.heuristica(inicio, pasajero), inicio, False, [], 0))  # (h(n), posición, tiene pasajero, ruta)
        visitados = set()

        while cola_prioridad:
            h_n, (x, y), tiene_pasajero, ruta, costo_acumulado = heapq.heappop(cola_prioridad)
            nodos_expandidos += 1
            
            if len(ruta) > profundidad_arbol:
                profundidad_arbol = len(ruta)
            
            # Si encontramos al pasajero y luego el destino
            if (x, y) == destino and tiene_pasajero:
                tiempo_fin = time.time()
                tiempo_total = tiempo_fin - tiempo_inicio
                return {
                    "ruta": ruta + [(x, y)],
                    "heuristica": self.heuristica(destino, destino),
                    "costo": costo_acumulado,
                    "nodos_expandidos": nodos_expandidos,
                    "profundidad_arbol": profundidad_arbol,
                    "tiempo_computo": tiempo_total
                }

            # Expandir el nodo
            for dx, dy in self.MOVIMIENTOS:
                nuevo_x, nuevo_y = x + dx, y + dy
                if self.es_valida((nuevo_x, nuevo_y), ciudad):
                    nueva_pos = (nuevo_x, nuevo_y)
                    nuevo_costo = costo_acumulado + self.costo(ciudad[nuevo_x][nuevo_y])
                    
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
                            heapq.heappush(cola_prioridad, (nuevo_costo + self.heuristica(nueva_pos, destino), nueva_pos, nuevo_tiene_pasajero, nueva_ruta, nuevo_costo))
                        else:
                            # Añadir a la cola de prioridad con el valor de la heurística al pasajero
                            heapq.heappush(cola_prioridad, (nuevo_costo + self.heuristica(nueva_pos, pasajero), nueva_pos, nuevo_tiene_pasajero, nueva_ruta, nuevo_costo))

        return "Falló la búsqueda"