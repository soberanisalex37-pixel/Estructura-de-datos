def warshall(matriz):
    n = len(matriz)
    alcanzable = [fila[:] for fila in matriz]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if alcanzable[i][k] == 1 and alcanzable[k][j] == 1:
                    alcanzable[i][j] = 1

    return alcanzable


# EJEMPLO DE MATRIZ
matriz = [
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, 0]
]

resultado = warshall(matriz)

print("Matriz de alcanzabilidad:")
for fila in resultado:
    print(fila)

