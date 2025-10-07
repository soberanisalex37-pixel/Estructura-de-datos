class Cola:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        else:
            return None

    def mostrar(self):
        return self.items


print("SISTEMA DE ATENCIÓN DE SEGUROS")
print("Opciones:")
print("  Cn → llega cliente al servicio n (ej. C1)")
print("  An → atender cliente del servicio n (ej. A1)")
print("  SALIR → terminar el programa\n")

colas_servicios = {
    1: Cola(),
    2: Cola(),
    3: Cola()
}

contador_servicio = {
    1: 0,
    2: 0,
    3: 0
}

while True:
    comando = input("Ingrese comando: ").strip().upper()

    if comando == "SALIR":
        print("Saliendo del sistema...")
        break


    if len(comando) != 2:
        print("Comando inválido. Use Cn o An (por ejemplo, C1 o A2).")
        continue

    accion = comando[0]
    try:
        servicio = int(comando[1])  
    except ValueError:
        print("Número de servicio inválido.")
        continue

    if servicio not in colas_servicios:
        print(f"El servicio {servicio} no existe.")
        continue


    if accion == "C":
        contador_servicio[servicio] += 1
        numero = contador_servicio[servicio]
        colas_servicios[servicio].encolar(numero)
        print(f"Cliente agregado al Servicio {servicio}. Número de atención: {numero}")

    elif accion == "A":
        if colas_servicios[servicio].esta_vacia():
            print(f"No hay clientes esperando en el Servicio {servicio}.")
        else:
            numero = colas_servicios[servicio].desencolar()
            print(f"Atendiendo al cliente {numero} del Servicio {servicio}.")

    else:
        print("Comando no reconocido. Use Cn o An.")

    
    print("\nEstado actual de las colas:")
    for s, cola in colas_servicios.items():
        print(f"  Servicio {s}: {cola.mostrar()}")
    print()