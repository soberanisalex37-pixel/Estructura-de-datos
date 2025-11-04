from Linked_List import ListaEnlazada


lista = ListaEnlazada()
lista.agregar(10)
lista.agregar(20)
lista.agregar(30)

lista.mostrar()
print("Longitud:", lista.longitud())

nodo = lista.buscar(20)
print("Nodo encontrado:", nodo)

lista.eliminar(10)
lista.mostrar()
