import tkinter as tk
from tkinter import messagebox
import time

class Pila:
    def __init__(self):
        self.items = []

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None

    def borrar_todo(self):
        self.items.clear()

    def cima(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

    def esta_vacia(self):
        return len(self.items) == 0

    def mostrar(self):
        return self.items


class App:
    def __init__(self, root):
        self.pila = Pila()
        self.root = root
        self.root.title("Pila Visual (Abajo hacia arriba)")
        self.root.geometry("400x500")

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=10)

        botones = tk.Frame(root)
        botones.pack()

        tk.Button(botones, text="Apilar", command=self.apilar, width=12, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(botones, text="Desapilar", command=self.desapilar, width=12, bg="#F44336", fg="white").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(botones, text="Ver cima", command=self.ver_cima, width=12, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5, pady=5)
        tk.Button(botones, text="Borrar pila", command=self.borrar_pila, width=12, bg="#FF9800", fg="white").grid(row=1, column=1, padx=5, pady=5)

        self.canvas = tk.Canvas(root, width=300, height=350, bg="white")
        self.canvas.pack(pady=20)

        tk.Button(root, text="Salir", command=root.quit, width=15, bg="#9E9E9E", fg="white").pack(pady=5)

    def actualizar_pila(self, highlight_top=False):
        self.canvas.delete("all")
        elementos = self.pila.mostrar()
        base_y = 300
        altura = 40

        for i, elem in enumerate(elementos):
            x1, y1 = 50, base_y - i * altura
            x2, y2 = 250, y1 + altura
            color = "red" if highlight_top and i == len(elementos)-1 else "skyblue"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(elem), font=("Arial", 12))

    def apilar(self):
        elemento = self.entry.get()
        if elemento.strip():
            self.pila.apilar(elemento)
            self.entry.delete(0, tk.END)
            self.actualizar_pila()
        else:
            messagebox.showwarning("Error", "Ingresa un valor válido")

    def desapilar(self):
        if self.pila.esta_vacia():
            messagebox.showwarning("Error", "La pila está vacía")
            return

        self.actualizar_pila(highlight_top=True)
        self.root.update()
        time.sleep(0.5)

        elemento = self.pila.desapilar()
        self.actualizar_pila()
        messagebox.showinfo("Desapilado", f"Se quitó: {elemento}")

    def ver_cima(self):
        cima = self.pila.cima()
        if cima:
            messagebox.showinfo("Cima", f"Elemento en cima: {cima}")
        else:
            messagebox.showwarning("Error", "La pila está vacía")

    def borrar_pila(self):
        if self.pila.esta_vacia():
            messagebox.showinfo("Borrar pila", "La pila ya está vacía")
        else:
            self.pila.borrar_todo()
            self.actualizar_pila()
            messagebox.showinfo("Borrar pila", "Se borró toda la pila")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


