class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

    def __str__(self):
        return str(self.valor)


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, valor):
        nuevo = Nodo(valor)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

    def eliminar(self, valor):
        if self.esta_vacia():
            print("La lista está vacía. No se puede eliminar.")
            return

        actual = self.cabeza
        anterior = None

        while actual is not None:
            if actual.valor == valor:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                print(f"Elemento {valor} eliminado correctamente.")
                return
            anterior = actual
            actual = actual.siguiente

        print(f"Elemento {valor} no encontrado en la lista.")

    def buscar(self, valor):
        actual = self.cabeza
        while actual is not None:
            if actual.valor == valor:
                return actual
            actual = actual.siguiente
        return None

    def longitud(self):
        contador = 0
        actual = self.cabeza
        while actual is not None:
            contador += 1
            actual = actual.siguiente
        return contador

    def mostrar(self):
        if self.esta_vacia():
            print("La lista está vacía.")
            return

        actual = self.cabeza
        representacion = ""
        while actual is not None:
            representacion += f"[{actual.valor}] -> "
            actual = actual.siguiente
        representacion += "None"
        print(representacion)

             
        