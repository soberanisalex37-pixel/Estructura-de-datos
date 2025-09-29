pila = []
tamaño = 10

while True:
    print("PROGRAMA PILA")
    print("1. INSERTAR DATO")
    print("2. SACAR DATO")
    print("3. MOSTRAR PILA")
    print("4. SALIR")
    opción = int(input("SELECCIONA OPCION: "))
    print()
    
    if opción == 1:
        if len(pila) == tamaño:
            print("PILA LLENA: NO SE PUEDE AGREGAR")
        else:
            dato = int(input("Insertar numero a la pila: "))
            pila.append(dato)
            print(f"Se insertó {dato} en la pila")

    elif opción == 2:
        if not pila:
            print("PILA VACÍA: NO SE PUEDE SACAR")
        else:
            dato = pila.pop()
            print(f"Se sacó {dato} de la pila")

    elif opción == 3:
        print("ELEMENTOS DE LA PILA")
        print("LA CIMA ES:", len(pila))
        for dato in reversed(pila):
            print(dato)

    elif opción == 4:
        print("Saliendo del programa...")
        break

    else:
        print("Opción no válida. Intente de nuevo.")
