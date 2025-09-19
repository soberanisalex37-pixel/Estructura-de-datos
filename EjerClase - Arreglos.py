import random
import time


num_alumnos = 500
num_materias = 6


matriz = [[random.randint(0, 100) for _ in range(num_materias)] for _ in range(num_alumnos)]


print("Tabla de Calificaciones (Filas = Alumnos, Columnas = Materias):\n")
print("Alumno\tM1\tM2\tM3\tM4\tM5\tM6")
for i in range(num_alumnos):
    print(f"A{i+1}\t" + "\t".join(str(m) for m in matriz[i]))


alumno_buscar = 321
materia_buscar = 5

inicio = time.time()
calificacion = matriz[alumno_buscar - 1][materia_buscar - 1]
fin = time.time()

print(f"\nCalificación del Alumno {alumno_buscar} en Materia {materia_buscar}: {calificacion}")
print(f"Tiempo de búsqueda: {fin - inicio:.10f} segundos")

