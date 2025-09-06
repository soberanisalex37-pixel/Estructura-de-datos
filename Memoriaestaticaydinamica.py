class MemoriaEstatica:
    
    def main():
        calificaciones = [0] * 5  

        for i in range(5):
            calificaciones[i] = int(input(f"Captura la calificación {i+1}: "))

        print("\nLas calificaciones capturadas son:")
        for cal in calificaciones:
            print(cal)


if __name__ == "__main__":
    MemoriaEstatica.main()


class MemoriaDinamica:
    
    def main():
        
        frutas = []

        
        frutas.append("Mango")
        frutas.append("Manzana")
        frutas.append("Banana")
        frutas.append("Uvas")

        print("Lista inicial:", frutas)

       
        frutas.pop(0)  
        frutas.pop(1)  

        
        frutas.append("sandia")

        print("Lista final:", frutas)


if __name__ == "__main__":
    MemoriaDinamica.main()

