import heapq
                
def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    camino = {}
                
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
                
        if distancia_actual > distancias[nodo_actual]:
            continue
                
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
                
        if distancia < distancias[vecino]:
            distancias[vecino] = distancia
            camino[vecino] = nodo_actual
            heapq.heappush(cola_prioridad, (distancia, vecino))
                
    return distancias, camino
                
# Ejemplo de uso
grafo = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'D': 3, 'E': 2},
    'C': {'A': 2, 'D': 4},
    'D': {'B': 3, 'C': 4, 'E': 3},
    'E': {'B': 2, 'D': 3}
}
                
distancias, camino = dijkstra(grafo, 'A')
print("Distancias desde A:", distancias)
print("Camino más corto:", camino)
