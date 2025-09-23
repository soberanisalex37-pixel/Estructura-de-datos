class superficie_terreno:
    def __init__ (self):
        self.largo =  0
        self.ancho = 0
        self. generacion = 0
        self.herederos = 0
        self.area_inicial = 0
        
    def calcular_area(self):
        self.largo = float(input("Ingrese el largo del terreno: "))
        if self.largo > 0:
            print(f"El largo de su terreno es de {self.largo}m")
        else:
            print("Coloque un valor valido")    
        
        self.ancho = float(input("Ingrese el ancho del terreno: "))
        if self.ancho > 0:
            print(f"El ancho de su terreno es de {self.ancho}m")
        else:
            print("Coloque un valor valido")
            
        self.area_inicial = self.largo * self.ancho
        print(f"\nLa superficie inicial del terreno es de {self.area_inicial} m²")
        
        self.generacion = int(input("\nIngrese el número de generación (0 a 50): "))
        if not (0 <= self.generacion <= 50):
            print("El número de generación debe estar entre 0 y 50.")
            return
        
        self.herederos = int(input("Ingrese el número de herederos por generación: "))
        if self.herederos <= 0:
            print("Debe ingresar un número válido de herederos.")
            return
        
        area_final = self.area_inicial / (self.herederos ** self.generacion)

        print(f"\nDespués de {self.generacion} generaciones,")
        print(f"cada heredero recibirá una superficie de {area_final} m²")
    
terreno = superficie_terreno()
terreno.calcular_area()
