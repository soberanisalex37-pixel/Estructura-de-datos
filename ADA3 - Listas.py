class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

class ListaIngredientes:
    def __init__(self):
        self.cabeza = None

    def agregar_ingrediente(self, nombre):
        nuevo = NodoIngrediente(nombre)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        print(f"Ingrediente '{nombre}' agregado.")

    def eliminar_ingrediente(self, nombre):
        if not self.cabeza:
            print("No hay ingredientes.")
            return

        actual = self.cabeza
        anterior = None

        while actual and actual.nombre.lower() != nombre.lower():
            anterior = actual
            actual = actual.siguiente

        if not actual:
            print(f"Ingrediente '{nombre}' no encontrado.")
            return

        if not anterior:
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente

        print(f"Ingrediente '{nombre}' eliminado.")

    def imprimir_ingredientes(self):
        if not self.cabeza:
            print("Sin ingredientes registrados.")
            return

        actual = self.cabeza
        print("Ingredientes:")
        while actual:
            print(f" - {actual.nombre}")
            actual = actual.siguiente

    def eliminar_ingredientes_repetidos(self, nombre_postre):
        if not self.cabeza:
            return []

        vistos = set()
        actual = self.cabeza
        anterior = None
        eliminados = []  

        while actual:
            nombre_normalizado = actual.nombre.strip().lower()
            if nombre_normalizado in vistos:
                eliminados.append(actual.nombre)
                anterior.siguiente = actual.siguiente
            else:
                vistos.add(nombre_normalizado)
                anterior = actual
            actual = actual.siguiente

        
        if eliminados:
            print(f"En el postre '{nombre_postre}' se eliminaron ingredientes repetidos:")
            for ing in eliminados:
                print(f"   - '{ing}'")
        else:
            print(f"En el postre '{nombre_postre}' no había ingredientes duplicados.")

        return eliminados


class NodoPostre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = ListaIngredientes()
        self.siguiente = None


class ListaPostres:
    def __init__(self):
        self.cabeza = None

    def mostrar_ingredientes(self, nombre_postre):
        actual = self.cabeza
        while actual and actual.nombre.lower() != nombre_postre.lower():
            actual = actual.siguiente

        if not actual:
            print(f"El postre '{nombre_postre}' no existe.")
        else:
            print(f"\nIngredientes del postre '{actual.nombre}':")
            actual.ingredientes.imprimir_ingredientes()

    def agregar_ingrediente_a_postre(self, nombre_postre, ingrediente):
        actual = self.cabeza
        while actual and actual.nombre.lower() != nombre_postre.lower():
            actual = actual.siguiente

        if not actual:
            print(f"El postre '{nombre_postre}' no existe.")
        else:
            actual.ingredientes.agregar_ingrediente(ingrediente)

    def eliminar_ingrediente_de_postre(self, nombre_postre, ingrediente):
        actual = self.cabeza
        while actual and actual.nombre.lower() != nombre_postre.lower():
            actual = actual.siguiente

        if not actual:
            print(f"El postre '{nombre_postre}' no existe.")
        else:
            actual.ingredientes.eliminar_ingrediente(ingrediente)

    def alta_postre(self, nombre_postre, lista_ingredientes):
        nuevo = NodoPostre(nombre_postre)
        for ing in lista_ingredientes:
            nuevo.ingredientes.agregar_ingrediente(ing)

        if not self.cabeza or nombre_postre.lower() < self.cabeza.nombre.lower():
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente and actual.siguiente.nombre.lower() < nombre_postre.lower():
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo

        print(f"\n✅ Postre '{nombre_postre}' dado de alta correctamente.")

    def baja_postre(self, nombre_postre):
        if not self.cabeza:
            print("No hay postres registrados.")
            return

        actual = self.cabeza
        anterior = None

        while actual and actual.nombre.lower() != nombre_postre.lower():
            anterior = actual
            actual = actual.siguiente

        if not actual:
            print(f"El postre '{nombre_postre}' no existe.")
            return

        if not anterior:
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente

        print(f"Postre '{nombre_postre}' eliminado correctamente.")

    def mostrar_postres(self):
        if not self.cabeza:
            print("No hay postres registrados.")
            return

        actual = self.cabeza
        print("\n Lista de postres:")
        while actual:
            print(f"{actual.nombre}")
            actual = actual.siguiente

    def eliminar_ingredientes_repetidos_global(self):
        if not self.cabeza:
            print("No hay postres registrados.")
            return

        actual = self.cabeza
        repetidos_global = False

        while actual:
            eliminados = actual.ingredientes.eliminar_ingredientes_repetidos(actual.nombre)
            if eliminados:
                repetidos_global = True
            actual = actual.siguiente

        if repetidos_global:
            print("\n Revisión completa: todos los ingredientes duplicados fueron eliminados.")
        else:
            print("\n No se encontraron ingredientes repetidos en ningún postre.")

def menu():
    postres = ListaPostres()

    while True:
        print("\n" + "=" * 50)
        print(" MENÚ PRINCIPAL - LISTA DE POSTRES ")
        print("=" * 50)
        print("1. Dar de alta un postre")
        print("2. Dar de baja un postre")
        print("3. Mostrar todos los postres")
        print("4. Mostrar ingredientes de un postre")
        print("5. Agregar ingrediente a un postre")
        print("6. Eliminar ingrediente de un postre")
        print("7. Eliminar ingredientes repetidos de todos los postres")
        print("0. Salir")
        print("=" * 50)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del postre: ")
            ingredientes = input("Ingrese los ingredientes separados por comas: ").split(",")
            ingredientes = [i.strip() for i in ingredientes]
            postres.alta_postre(nombre, ingredientes)

        elif opcion == "2":
            nombre = input("Ingrese el nombre del postre a eliminar: ")
            postres.baja_postre(nombre)

        elif opcion == "3":
            postres.mostrar_postres()

        elif opcion == "4":
            nombre = input("Ingrese el nombre del postre: ")
            postres.mostrar_ingredientes(nombre)

        elif opcion == "5":
            nombre = input("Ingrese el nombre del postre: ")
            ingrediente = input("Ingrese el nuevo ingrediente: ")
            postres.agregar_ingrediente_a_postre(nombre, ingrediente)

        elif opcion == "6":
            nombre = input("Ingrese el nombre del postre: ")
            ingrediente = input("Ingrese el ingrediente a eliminar: ")
            postres.eliminar_ingrediente_de_postre(nombre, ingrediente)

        elif opcion == "7":
            postres.eliminar_ingredientes_repetidos_global()

        elif opcion == "0":
            print("\n ¡Gracias por usar el sistema de postres!")
            break

        else:
            print(" Opción no válida, intente nuevamente.")


if __name__ == "__main__":
    menu()

