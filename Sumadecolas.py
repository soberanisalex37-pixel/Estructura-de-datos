class Cola:
    def __init__(self):
        self.elementos = []

    def esta_vacia(self):
        return len(self.elementos) == 0

    def encolar(self, item):
        self.elementos.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        else:
            return None

    def ver_frente(self):
        if not self.esta_vacia():
            return self.elementos[0]
        else:
            return None

    def mostrar(self):
        return self.elementos

def sumar_colas(cola1, cola2):
    cola_resultado = Cola()

    while not cola1.esta_vacia() and not cola2.esta_vacia():
        valor1 = cola1.desencolar()
        valor2 = cola2.desencolar()
        suma = valor1 + valor2
        cola_resultado.encolar(suma)

    return cola_resultado

print("=== SUMA DE COLAS ===")

cola_a = Cola()
n = int(input("¿Cuántos elementos tendrá la Cola A? "))
for i in range(n):
    valor = int(input(f"Ingrese el elemento {i+1} de la Cola A: "))
    cola_a.encolar(valor)
    print("\nCola A ingresada:", cola_a.mostrar())


cola_b = Cola()
m = int(input("¿Cuántos elementos tendrá la Cola B? "))
for i in range(m):
    valor = int(input(f"Ingrese el elemento {i+1} de la Cola B: "))
    cola_b.encolar(valor)
    print("\nCola B ingresada:", cola_b.mostrar())


if n != m:
    print("\nLas colas deben tener la misma cantidad de elementos para sumarse.")
else:
    print("\nLas colas ingresadas son:", cola_a.mostrar(), cola_b.mostrar())
    cola_resultado = sumar_colas(cola_a, cola_b)

    print("\nCola A:", cola_a.mostrar())
    print("Cola B:", cola_b.mostrar())
    print("Cola Resultado:", cola_resultado.mostrar())