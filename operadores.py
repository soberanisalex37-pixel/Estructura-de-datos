class Pila:
    def __init__(self):
        self.items = []
    def esta_vacia(self):
        return len(self.items) == 0
    def apilar(self, item):
        self.items.append(item)
    def desapilar(self):
        return self.items.pop() if not self.esta_vacia() else None
    def cima(self):
        return self.items[-1] if not self.esta_vacia() else None


prioridad = {'+':1, '-':1, '*':2, '/':2, '^':3, '()':4}

def infija_a_posfija(expresion):
    salida = []
    pila = Pila()
    for token in expresion.split():
        if token.isalnum():  
            salida.append(token)
        elif token in prioridad:
            while (not pila.esta_vacia() and pila.cima() in prioridad and
                   prioridad[pila.cima()] >= prioridad[token]):
                salida.append(pila.desapilar())
            pila.apilar(token)
        elif token == '(':
            pila.apilar(token)
        elif token == ')':
            while not pila.esta_vacia() and pila.cima() != '(':
                salida.append(pila.desapilar())
            pila.desapilar()
    while not pila.esta_vacia():
        salida.append(pila.desapilar())
    return " ".join(salida)


def infija_a_prefija(expresion):
    tokens = expresion.split()[::-1]
    for i in range(len(tokens)):
        if tokens[i] == '(':
            tokens[i] = ')'
        elif tokens[i] == ')':
            tokens[i] = '('
    posfija = infija_a_posfija(" ".join(tokens))
    return " ".join(posfija.split()[::-1])

while True:
    print("OPERADORES")
    print("1. INFIJA A POSFIJA")
    print("2. INFIJA A POSFIJA")
    print("3. SALIR")
    opción = int(input("SELECCIONA OPCION: "))
    print()
    
    if opción == 1:
        exp = input("Escribe la expresión infija (usa espacios entre tokens): ")
        print("Posfija:", infija_a_posfija(exp))

    elif opción == 2:
        exp = input("Escribe la expresión infija (usa espacios entre tokens): ")
        print("Prefija:", infija_a_prefija(exp))

    elif opción == 3:
        print("Saliendo...")
        break

    else: 
        print("Opción inválida, intenta de nuevo.")
    









