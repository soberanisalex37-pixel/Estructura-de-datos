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

class SistemaHorarios:
    def __init__(self):
        self.maestros = []
        self.alumnos = []
        self.materias_grupos = {}  
    
    def agregar_maestro(self, nombre, id, materia, paga):
        """Agrega un nuevo maestro al sistema"""
        maestro = Maestro(nombre, id, materia, paga)
        self.maestros.append(maestro)
        
        
        if materia not in self.materias_grupos:
            self.materias_grupos[materia] = {}
        
        return maestro
    
    def agregar_alumno(self, nombre, id, grado, grupo):
        """Agrega un nuevo alumno al sistema"""
        alumno = Alumno(nombre, id, grado, grupo)
        self.alumnos.append(alumno)
        return alumno
    
    def asignar_horario_maestro(self, id_maestro, dia, hora_inicio, hora_fin, grupo):
        """Asigna un horario a un maestro"""
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
        """Actualiza los horarios de todos los alumnos del grupo"""
        for alumno in self.alumnos:
            if alumno.grupo == grupo:
                if dia not in alumno.horario:
                    alumno.horario[dia] = []
                
                alumno.horario[dia].append((hora_inicio, materia, nombre_maestro))
                alumno.horario[dia].sort(key=lambda x: x[0])
    
    def _verificar_conflicto_maestro(self, maestro, dia, hora_inicio, hora_fin):
        """Verifica si hay conflicto con horarios existentes del maestro"""
        for horario_existente in maestro.horarios:
            dia_existente, inicio_existente, fin_existente, _ = horario_existente
            if dia_existente == dia:
                if (hora_inicio < fin_existente and hora_fin > inicio_existente):
                    return True
        return False
    
    def buscar_maestro(self, id):
        """Busca un maestro por ID"""
        for maestro in self.maestros:
            if maestro.id == id:
                return maestro
        return None
    
    def buscar_alumno(self, id):
        """Busca un alumno por ID"""
        for alumno in self.alumnos:
            if alumno.id == id:
                return alumno
        return None
    
    def mostrar_horarios_maestro(self, id_maestro):
        """Muestra los horarios de un maestro específico"""
        maestro = self.buscar_maestro(id_maestro)
        if maestro:
            print(f"\nHorarios de {maestro.nombre} ({maestro.materia}):")
            if maestro.horarios:
                for i, (dia, inicio, fin, grupo) in enumerate(maestro.horarios, 1):
                    print(f"{i}. {dia}: {inicio} - {fin} (Grupo {grupo})")
            else:
                print("No tiene horarios asignados")
        else:
            print(f"Maestro con ID {id_maestro} no encontrado")
    
    def mostrar_horarios_alumno(self, id_alumno):
        """Muestra los horarios de un alumno específico"""
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
    
    def mostrar_todos_horarios_maestros(self):
        """Muestra todos los horarios de todos los maestros"""
        print("\n=== HORARIOS DE TODOS LOS MAESTROS ===")
        for maestro in self.maestros:
            self.mostrar_horarios_maestro(maestro.id)
            print("-" * 40)
    
    def calcular_pago_semanal(self, id_maestro):
        """Calcula el pago semanal de un maestro basado en sus horas"""
        maestro = self.buscar_maestro(id_maestro)
        if maestro:
            total_horas = 0
            for dia, inicio, fin, grupo in maestro.horarios:
                total_horas += (fin - inicio)
            
            pago_semanal = total_horas * maestro.paga
            print(f"\nPago semanal para {maestro.nombre}:")
            print(f"Total de horas: {total_horas}")
            print(f"Pago por hora: ${maestro.paga}")
            print(f"Pago semanal: ${pago_semanal:.2f}")
            return pago_semanal
        else:
            print(f"Maestro con ID {id_maestro} no encontrado")
            return 0

def menu_principal():
    sistema = SistemaHorarios()
    
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
        print("\n=== SISTEMA DE GESTIÓN DE HORARIOS ESCOLARES ===")
        print("1. Gestión de Maestros")
        print("2. Gestión de Alumnos")
        print("3. Consultar horario de alumno")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            menu_maestros(sistema)
        elif opcion == "2":
            menu_alumnos(sistema)
        elif opcion == "3":
            id_alumno = input("ID del alumno: ")
            sistema.mostrar_horarios_alumno(id_alumno)
        elif opcion == "4":
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

if __name__ == "__main__":
    menu_principal()