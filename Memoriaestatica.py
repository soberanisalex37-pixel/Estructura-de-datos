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