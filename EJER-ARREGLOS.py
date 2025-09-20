import random

class SistemaVentas:
    def __init__(self):
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.departamentos = ["Ropa", "Deportes", "Juguetería"]
        self.matriz = [[random.randint(1000, 5000) for _ in self.departamentos] for _ in self.meses]

    
    def insertar_venta(self, mes, depto, valor):
        self.matriz[mes][depto] = valor
        print(f"Venta de {valor} registrada en {self.meses[mes]} - {self.departamentos[depto]}.")

    def buscar_venta(self, valor):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                if self.matriz[i][j] == valor:
                    return f"Venta {valor} encontrada en {self.meses[i]} - {self.departamentos[j]}"
        return "Venta no encontrada."

    def eliminar_venta(self, mes, depto):
        self.matriz[mes][depto] = 0
        print(f"Venta eliminada en {self.meses[mes]} - {self.departamentos[depto]}.")

    def agregar_departamento(self, nombre_depto):
        self.departamentos.append(nombre_depto)
        for fila in self.matriz:
            fila.append(0)
        print(f"Departamento '{nombre_depto}' agregado.")

    def mostrar_tabla(self):
        encabezado = f"{'Mes':<12}" + "".join([f"{d:<12}" for d in self.departamentos])
        print(encabezado)
        print("-" * len(encabezado))
        for i in range(len(self.meses)):
            fila = f"{self.meses[i]:<12}" + "".join([f"{self.matriz[i][j]:<12}" for j in range(len(self.departamentos))])
            print(fila)

    def ejecutar_menu(self):
        while True:
            print("\n=== MENÚ DE VENTAS ===")
            print("1. Mostrar tabla de ventas")
            print("2. Insertar/Actualizar venta")
            print("3. Buscar una venta")
            print("4. Eliminar una venta")
            print("5. Agregar nuevo departamento")
            print("6. Salir")

            opcion = input("Elige una opción: ")

            if opcion == "1":
                self.mostrar_tabla()

            elif opcion == "2":
                mes = int(input("Ingresa número de mes (1-12): ")) - 1
                for i, d in enumerate(self.departamentos):
                    print(f"{i+1}. {d}")
                depto = int(input("Elige departamento: ")) - 1
                valor = int(input("Ingresa la venta: "))
                self.insertar_venta(mes, depto, valor)

            elif opcion == "3":
                valor = int(input("Ingresa el valor de la venta a buscar: "))
                print(self.buscar_venta(valor))

            elif opcion == "4":
                mes = int(input("Ingresa número de mes (1-12): ")) - 1
                for i, d in enumerate(self.departamentos):
                    print(f"{i+1}. {d}")
                depto = int(input("Elige departamento: ")) - 1
                self.eliminar_venta(mes, depto)

            elif opcion == "5":
                nombre = input("Ingrese el nombre del nuevo departamento: ")
                self.agregar_departamento(nombre)

            elif opcion == "6":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida. Intenta de nuevo.")


sistema = SistemaVentas()
sistema.ejecutar_menu()
