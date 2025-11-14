class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))
        self.rango = [0] * n

    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])
        return self.padre[x]

    def union(self, x, y):
        raizX = self.find(x)
        raizY = self.find(y)

        if raizX != raizY:
            if self.rango[raizX] < self.rango[raizY]:
                self.padre[raizX] = raizY
            elif self.rango[raizX] > self.rango[raizY]:
                self.padre[raizY] = raizX
            else:
                self.padre[raizY] = raizX
                self.rango[raizX] += 1
            return True
        return False


def kruskal(n, aristas):
    
    aristas.sort()
    uf = UnionFind(n)
    mst = []

    for peso, u, v in aristas:
        if uf.union(u, v):  
            mst.append((u, v, peso))

    return mst


n = 5

aristas = [
    (1, 0, 1),
    (3, 0, 2),
    (2, 1, 2),
    (4, 1, 3),
    (5, 2, 3),
    (7, 3, 4),
    (6, 2, 4)
]

mst = kruskal(n, aristas)

print("Árbol de expansión mínima (Kruskal):")
costo_total = 0
for u, v, peso in mst:
    print(f"{u} -- {v}  (peso: {peso})")
    costo_total += peso

print(f"\nCosto total del MST: {costo_total}")

