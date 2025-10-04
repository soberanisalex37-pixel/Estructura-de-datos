class Pila:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        return self.items.pop() if not self.esta_vacia() else None

    def ver_items(self):
        return self.items.copy()

    def __str__(self):
        return str(self.items)

def mostrar_torres(A, B, C):
    print("\nEstado actual:")
    print("A:", A.ver_items())
    print("B:", B.ver_items())
    print("C:", C.ver_items())
    print("-" * 30)

def hanoi(n, origen, auxiliar, destino, nombre_origen, nombre_aux, nombre_dest):
    if n == 1:
        disco = origen.desapilar()
        destino.apilar(disco)
        print(f"\nMover disco {disco} de {nombre_origen} a {nombre_dest}")
        mostrar_torres(torre_A, torre_B, torre_C)
    else:
        hanoi(n - 1, origen, destino, auxiliar, nombre_origen, nombre_dest, nombre_aux)
        hanoi(1, origen, auxiliar, destino, nombre_origen, nombre_aux, nombre_dest)
        hanoi(n - 1, auxiliar, origen, destino, nombre_aux, nombre_origen, nombre_dest)

torre_A = Pila()
torre_B = Pila()
torre_C = Pila()

for disco in range(3, 0, -1):
    torre_A.apilar(disco)

print("Estado inicial:")
mostrar_torres(torre_A, torre_B, torre_C)


print("\nResolviendo Torres de Hanoi:\n")
hanoi(3, torre_A, torre_B, torre_C, "A", "B", "C")

print("\nEstado final:")
mostrar_torres(torre_A, torre_B, torre_C)
