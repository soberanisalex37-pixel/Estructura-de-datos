import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
import threading
import traceback



def burbuja_steps(arr):
    a = arr[:] 
    steps = []
    n = len(a)
    start = time.perf_counter()
    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append((f"Comparar índices {j} y {j+1}: {a[j]} > {a[j+1]} ?", a[:]))
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                steps.append((f"  → Intercambio: ahora {a}", a[:]))
        steps.append((f"Fin pasada {i+1}, estado: {a}", a[:]))
    end = time.perf_counter()
    elapsed = end - start
    return a, steps, elapsed

def insercion_steps(arr):
    a = arr[:]
    steps = []
    start = time.perf_counter()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        steps.append((f"Tomar key=indice {i} → {key}", a[:]))
        while j >= 0 and a[j] > key:
            steps.append((f"  {key} < {a[j]} -> desplazar {a[j]} de índice {j} a {j+1}", a[:]))
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
        steps.append((f"Insertar key={key} en índice {j+1}, estado: {a}", a[:]))
    end = time.perf_counter()
    elapsed = end - start
    return a, steps, elapsed



def seleccion_steps(arr):
    a = arr[:]               
    steps = []
    start = time.perf_counter()
    n = len(a)

    for i in range(n - 1):
        min_idx = i

        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j

        if min_idx != i:
            min_val = a[min_idx]
            a[i], a[min_idx] = a[min_idx], a[i]
            steps.append((f"Pasada {i+1}: mínimo {min_val} en índice {min_idx} — intercambiar con índice {i} → {a}", a[:]))
        else:
            steps.append((f"Pasada {i+1}: el elemento en índice {i} ({a[i]}) ya es mínimo — sin intercambio → {a}", a[:]))

    end = time.perf_counter()
    elapsed = end - start
    return a, steps, elapsed


class OrdenadorApp:
    def __init__(self, root):
        self.root = root
        root.title("Ordenamiento paso a paso")
        root.geometry("760x620")
        root.resizable(False, False)

        frm_top = tk.Frame(root)
        frm_top.pack(padx=10, pady=8, fill="x")

        tk.Label(frm_top, text="Ingresa la lista de números (separados por comas):").grid(row=0, column=0, sticky="w")
        self.entry = tk.Entry(frm_top, width=60)
        self.entry.grid(row=1, column=0, columnspan=4, sticky="w", pady=4)
        self.entry.insert(0, "10, 3, 5, 2, 8, 1") 

        tk.Label(frm_top, text="Elige el algoritmo:").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.alg_var = tk.StringVar(value="Burbuja")
        tk.Radiobutton(frm_top, text="Burbuja", variable=self.alg_var, value="Burbuja").grid(row=3, column=0, sticky="w")
        tk.Radiobutton(frm_top, text="Inserción", variable=self.alg_var, value="Inserción").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(frm_top, text="Selección", variable=self.alg_var, value="Selección").grid(row=3, column=2, sticky="w")

       
        self.animate_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frm_top, text="Animar pasos al ejecutarlo", variable=self.animate_var).grid(row=4, column=0, sticky="w", pady=(6,0))
        tk.Label(frm_top, text="Velocidad animación (ms):").grid(row=4, column=1, sticky="e")
        self.speed_scale = tk.Scale(frm_top, from_=50, to=1000, orient="horizontal", length=200)
        self.speed_scale.set(300)
        self.speed_scale.grid(row=4, column=2, sticky="w")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=6)
        self.run_btn = tk.Button(btn_frame, text="Ordenar y mostrar pasos", command=self.on_run, width=22, bg="#4caf50", fg="white")
        self.run_btn.pack(side="left", padx=6)
        self.clear_btn = tk.Button(btn_frame, text="Limpiar pasos", command=self.clear_steps, width=12)
        self.clear_btn.pack(side="left", padx=6)

        self.steps_box = scrolledtext.ScrolledText(root, width=96, height=26, state="normal", wrap="none", font=("Consolas", 10))
        self.steps_box.pack(padx=10, pady=6)

        info_frame = tk.Frame(root)
        info_frame.pack(fill="x", padx=10, pady=(0,10))
        tk.Label(info_frame, text="Lista ordenada:").grid(row=0, column=0, sticky="w")
        self.result_label = tk.Label(info_frame, text="-", fg="blue")
        self.result_label.grid(row=0, column=1, sticky="w", padx=(6,0))

        tk.Label(info_frame, text="Tiempo (solo algoritmo):").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.time_label = tk.Label(info_frame, text="-", fg="brown")
        self.time_label.grid(row=1, column=1, sticky="w", padx=(6,0), pady=(6,0))

        tk.Label(info_frame, text="Pasos totales:").grid(row=2, column=0, sticky="w")
        self.steps_count_label = tk.Label(info_frame, text="0")
        self.steps_count_label.grid(row=2, column=1, sticky="w", padx=(6,0))

        self.sort_thread = None

    def clear_steps(self):
        self.steps_box.delete("1.0", tk.END)
        self.result_label.config(text="-")
        self.time_label.config(text="-")
        self.steps_count_label.config(text="0")

    def on_run(self):
        text = self.entry.get().strip()
        if text == "":
            messagebox.showerror("Error", "Ingresa una lista de números separados por comas.")
            return
        try:
            numbers = [int(x.strip()) for x in text.split(",") if x.strip() != ""]
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar solo números (enteros) separados por comas.")
            return
        
        self.run_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")
        self.steps_box.delete("1.0", tk.END)
        self.result_label.config(text="Procesando...")
        self.time_label.config(text="-")
        self.steps_count_label.config(text="0")

        self.sort_thread = threading.Thread(target=self.run_sort, args=(numbers, self.alg_var.get(), self.animate_var.get(), self.speed_scale.get()))
        self.sort_thread.start()

    def run_sort(self, numbers, algorithm, animate, speed_ms):
        if algorithm == "Burbuja":
            sort_fn = burbuja_steps
        elif algorithm == "Inserción":
            sort_fn = insercion_steps
        else:
            sort_fn = seleccion_steps

        try:
            sorted_list, steps, alg_time = sort_fn(numbers)
            self.root.after(0, lambda: self.time_label.config(text=f"{alg_time:.8f} s"))
            self.root.after(0, lambda: self.result_label.config(text=str(sorted_list)))
            self.root.after(0, lambda: self.steps_count_label.config(text=str(len(steps))))

        except Exception as e:
            tb = traceback.format_exc()
            self.root.after(0, lambda: self.steps_box.insert(tk.END, f"ERROR al ejecutar el algoritmo:\n{tb}\n"))
            self.root.after(0, lambda: self.steps_box.see(tk.END))
            self.root.after(0, lambda: messagebox.showerror("Error en algoritmo", f"Ha ocurrido un error: {e}\nRevisa la caja de pasos para la traza."))
            self.root.after(0, lambda: self.time_label.config(text="ERROR"))
            self.root.after(0, self.reenable_buttons)
            return
        if animate:
            delay = max(1, int(speed_ms))
            for idx, (desc, state) in enumerate(steps, start=1):
                line = f"[{idx:03d}] {desc}\n"
                self.root.after(0, lambda l=line: self.steps_box.insert(tk.END, l))
                self.root.after(0, lambda: self.steps_box.see(tk.END))
                time.sleep(delay / 1000.0)
            self.root.after(0, lambda: self.steps_box.insert(tk.END, f"\n--- Fin de pasos ({len(steps)} pasos) ---\n"))
            self.root.after(0, lambda: self.steps_box.see(tk.END))
        else:
            lines = []
            for idx, (desc, state) in enumerate(steps, start=1):
                lines.append(f"[{idx:03d}] {desc}")
            text_all = "\n".join(lines) + f"\n\n--- Fin de pasos ({len(steps)} pasos) ---\n"
            self.root.after(0, lambda: self.steps_box.insert(tk.END, text_all))
            self.root.after(0, lambda: self.steps_box.see(tk.END))
        self.root.after(0, self.reenable_buttons)

    def reenable_buttons(self):
        self.run_btn.config(state="normal")
        self.clear_btn.config(state="normal")

def main():
    root = tk.Tk()
    app = OrdenadorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
