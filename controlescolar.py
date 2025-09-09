class Persona:
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

class Maestro(Persona):
    def __init__(self, nombre, id, materia, paga):
        super().__init__(nombre, id)
        self.materia = materia 
        self.paga = paga
        self.horarios = []  

class Alumno(Persona):
    def __init__(self, nombre, id, grado, grupo):
        super().__init__(nombre, id)
        self.grado = grado
        self.grupo = grupo
        self.horario = {}  
        self.factura = None   

class Factura:
    def __init__(self, alumno, inscripcion=0, otros_cargos=0):
        self.alumno = alumno
        self.inscripcion = inscripcion
        self.otros_cargos = otros_cargos
        
    def calcular_total(self):
        return self.inscripcion + self.otros_cargos
    
    def mostrar_factura(self):
        print("\n------ FACTURA SEMESTRAL ------")
        print(f"Alumno: {self.alumno.nombre}")
        print(f"Matrícula: {self.alumno.id}")
        print(f"Inscripción: ${self.inscripcion:.2f}")
        print(f"Otros cargos: ${self.otros_cargos:.2f}")
        print("-------------------------------")
        print(f"TOTAL A PAGAR: ${self.calcular_total():.2f}")

class SistemaHorarios:
    def __init__(self):
        self.maestros = []
        self.alumnos = []
        self.materias_grupos = {}  
    
    def agregar_maestro(self, nombre, id, materia, paga):
        maestro = Maestro(nombre, id, materia, paga)
        self.maestros.append(maestro)
        
        if materia not in self.materias_grupos:
            self.materias_grupos[materia] = {}
        
        return maestro
    
    def agregar_alumno(self, nombre, id, grado, grupo):
        alumno = Alumno(nombre, id, grado, grupo)
        self.alumnos.append(alumno)
        return alumno
    
    
    def generar_factura(self, id_alumno, inscripcion, otros):
        alumno = self.buscar_alumno(id_alumno)
        if alumno:
            alumno.factura = Factura(alumno, inscripcion, otros)
            print(f"\nFactura generada exitosamente para {alumno.nombre}.")
        else:
            print("Alumno no encontrado.")
    
    def mostrar_factura_alumno(self, id_alumno):
        alumno = self.buscar_alumno(id_alumno)
        if alumno:
            if alumno.factura:
                alumno.factura.mostrar_factura()
            else:
                print("El alumno no tiene factura registrada.")
        else:
            print("Alumno no encontrado.")
    
    
    def asignar_horario_maestro(self, id_maestro, dia, hora_inicio, hora_fin, grupo):
        maestro = self.buscar_maestro(id_maestro)
        if maestro:
            if not self._verificar_conflicto_maestro(maestro, dia, hora_inicio, hora_fin):
                maestro.horarios.append((dia, hora_inicio, hora_fin, grupo))
                
                if grupo not in self.materias_grupos[maestro.materia]:
                    self.materias_grupos[maestro.materia][grupo] = maestro
                
                print(f"Horario asignado a {maestro.nombre}: {dia} {hora_inicio}-{hora_fin} con grupo {grupo}")
                
                self._actualizar_horarios_alumnos(maestro.materia, grupo, dia, hora_inicio, hora_fin, maestro.nombre)
            else:
                print(f"¡Conflicto de horario para {maestro.nombre}!")
        else:
            print(f"Maestro con ID {id_maestro} no encontrado")
    
    def _actualizar_horarios_alumnos(self, materia, grupo, dia, hora_inicio, hora_fin, nombre_maestro):
        for alumno in self.alumnos:
            if alumno.grupo == grupo:
                if dia not in alumno.horario:
                    alumno.horario[dia] = []
                alumno.horario[dia].append((hora_inicio, materia, nombre_maestro))
                alumno.horario[dia].sort(key=lambda x: x[0])
    
    def _verificar_conflicto_maestro(self, maestro, dia, hora_inicio, hora_fin):
        for dia_existente, inicio_existente, fin_existente, _ in maestro.horarios:
            if dia_existente == dia:
                if (hora_inicio < fin_existente and hora_fin > inicio_existente):
                    return True
        return False
    
    def buscar_maestro(self, id):
        for maestro in self.maestros:
            if maestro.id == id:
                return maestro
        return None
    
    def buscar_alumno(self, id):
        for alumno in self.alumnos:
            if alumno.id == id:
                return alumno
        return None
    
    def mostrar_horarios_alumno(self, id_alumno):
        alumno = self.buscar_alumno(id_alumno)
        if alumno:
            print(f"\nHorario de {alumno.nombre} ({alumno.grado}° - Grupo {alumno.grupo}):")
            
            if not alumno.horario:
                print("No tiene horarios asignados")
                return
                
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
            
            for dia in dias_semana:
                if dia in alumno.horario:
                    print(f"\n{dia}:")
                    for hora, materia, maestro in alumno.horario[dia]:
                        print(f"  {hora}:00 - {materia} ({maestro})")
        else:
            print(f"Alumno con ID {id_alumno} no encontrado")

    
    def mostrar_horarios_maestro(self, id_maestro):
        maestro = self.buscar_maestro(id_maestro)
        if maestro:
            print(f"\nHorarios de {maestro.nombre} ({maestro.materia}):")
            if not maestro.horarios:
                print("No tiene horarios asignados.")
            for dia, inicio, fin, grupo in maestro.horarios:
                print(f"  {dia}: {inicio}:00 - {fin}:00 con grupo {grupo}")
        else:
            print("Maestro no encontrado.")

    def mostrar_todos_horarios_maestros(self):
        if not self.maestros:
            print("No hay maestros registrados.")
            return
        for maestro in self.maestros:
            self.mostrar_horarios_maestro(maestro.id)

    def calcular_pago_semanal(self, id_maestro):
        maestro = self.buscar_maestro(id_maestro)
        if maestro:
            total_horas = 0
            for _, inicio, fin, _ in maestro.horarios:
                total_horas += fin - inicio
            pago = total_horas * maestro.paga
            print(f"\nEl pago semanal de {maestro.nombre} es: ${pago:.2f}")
        else:
            print("Maestro no encontrado.")


def menu_principal():
    sistema = SistemaHorarios()
    
    # Datos de prueba
    sistema.agregar_maestro("Juan Pérez", "MP001", "Matemáticas", 50) 
    sistema.agregar_maestro("María García", "MP002", "Historia", 45) 
    sistema.agregar_maestro("Carlos López", "MP003", "Ciencias", 55) 
    
    sistema.agregar_alumno("Ana Torres", "AL001", "1", "A") 
    sistema.agregar_alumno("Luis Mendoza", "AL002", "1", "A") 
    sistema.agregar_alumno("Sofía Ramírez", "AL003", "1", "B") 
    
    sistema.asignar_horario_maestro("MP001", "Lunes", 9, 11, "A") 
    sistema.asignar_horario_maestro("MP001", "Miércoles", 9, 11, "A") 
    sistema.asignar_horario_maestro("MP002", "Martes", 14, 16, "A") 
    sistema.asignar_horario_maestro("MP003", "Jueves", 10, 12, "A") 
    sistema.asignar_horario_maestro("MP001", "Lunes", 11, 13, "B")
    
    while True:
        print("\n=== SISTEMA ESCOLAR ===")
        print("1. Gestión de Maestros")
        print("2. Gestión de Alumnos")
        print("3. Consultar horario de alumno")
        print("4. Facturación de alumnos")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            menu_maestros(sistema)
        elif opcion == "2":
            menu_alumnos(sistema)
        elif opcion == "3":
            id_alumno = input("ID del alumno: ")
            sistema.mostrar_horarios_alumno(id_alumno)
        elif opcion == "4":
            menu_facturacion(sistema)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def menu_maestros(sistema):
    while True:
        print("\n--- GESTIÓN DE MAESTROS ---")
        print("1. Agregar maestro")
        print("2. Asignar horario a maestro")
        print("3. Ver horarios de maestro")
        print("4. Ver todos los horarios de maestros")
        print("5. Calcular pago semanal")
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del maestro: ")
            id_maestro = input("ID del maestro: ")
            materia = input("Materia que imparte: ")
            paga = float(input("Pago por hora: $"))
            sistema.agregar_maestro(nombre, id_maestro, materia, paga)
            print(f"Maestro {nombre} agregado exitosamente!")
        
        elif opcion == "2":
            id_maestro = input("ID del maestro: ")
            dia = input("Día (Lunes, Martes, etc.): ")
            hora_inicio = int(input("Hora de inicio (formato 24h, ej: 9): "))
            hora_fin = int(input("Hora de fin (formato 24h, ej: 11): "))
            grupo = input("Grupo: ")
            sistema.asignar_horario_maestro(id_maestro, dia, hora_inicio, hora_fin, grupo)
        
        elif opcion == "3":
            id_maestro = input("ID del maestro: ")
            sistema.mostrar_horarios_maestro(id_maestro)
        
        elif opcion == "4":
            sistema.mostrar_todos_horarios_maestros()
        
        elif opcion == "5":
            id_maestro = input("ID del maestro: ")
            sistema.calcular_pago_semanal(id_maestro)
        
        elif opcion == "6":
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

def menu_alumnos(sistema):
    while True:
        print("\n--- GESTIÓN DE ALUMNOS ---")
        print("1. Agregar alumno")
        print("2. Ver horario de alumno")
        print("3. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del alumno: ")
            id_alumno = input("ID del alumno: ")
            grado = input("Grado: ")
            grupo = input("Grupo: ")
            sistema.agregar_alumno(nombre, id_alumno, grado, grupo)
            print(f"Alumno {nombre} agregado exitosamente!")
        
        elif opcion == "2":
            id_alumno = input("ID del alumno: ")
            sistema.mostrar_horarios_alumno(id_alumno)
        
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def menu_facturacion(sistema):
    while True:
        print("\n--- FACTURACIÓN ---")
        print("1. Generar factura para alumno")
        print("2. Mostrar factura de alumno")
        print("3. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id_alumno = input("ID del alumno: ")
            inscripcion = float(input("Costo de inscripción: "))
            otros = float(input("Otros cargos (si no hay, poner 0): "))
            sistema.generar_factura(id_alumno, inscripcion, otros)
        
        elif opcion == "2":
            id_alumno = input("ID del alumno: ")
            sistema.mostrar_factura_alumno(id_alumno)
        
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()
