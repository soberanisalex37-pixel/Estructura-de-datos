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