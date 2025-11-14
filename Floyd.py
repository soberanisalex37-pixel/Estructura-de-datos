def floyd_warshall(grafo):
    
    dist = [fila[:] for fila in grafo]
    n = len(dist)
    
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


# Ejemplo de uso:
INF = float('inf')

grafo = [
    [0,   3, INF, 7],
    [8,   0,   2, INF],
    [5, INF,   0,  1],
    [2, INF, INF, 0]
]

resultado = floyd_warshall(grafo)

print("Matriz de distancias más cortas:")
for fila in resultado:
    print(fila)

