class Pila:
    def __init__(self, capacidad):
        self.items = []
        self.capacidad = capacidad
        self.tope = 0  
    def insertar(self, elemento):
        if self.tope == self.capacidad:
            print(f"Error: Desbordamiento al intentar insertar {elemento}")
        else:
            self.items.append(elemento)
            self.tope += 1
            print(f"Insertar({elemento}) -> {self.items}, TOPE={self.tope}")

    def eliminar(self, variable):
        if self.tope == 0:
            print(f"Error: Subdesbordamiento al intentar eliminar {variable}")
        else:
            eliminado = self.items.pop()
            self.tope -= 1
            print(f"Eliminar({variable}={eliminado}) -> {self.items}, TOPE={self.tope}")


pila = Pila(8)

pila.insertar("X")
pila.insertar("Y")
pila.eliminar("Z")
pila.eliminar("T")
pila.eliminar("U")
pila.insertar("V")
pila.insertar("W")
pila.eliminar("P")
pila.insertar("R")

print("\nEstado final de la pila:", pila.items)
print("Número de elementos en la pila:", pila.tope)
