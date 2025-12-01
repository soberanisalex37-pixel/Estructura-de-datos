import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import hashlib
import random
import math
from typing import List, Any, Optional

def compute_file_sha256(path: str, chunk_size: int = 8192) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def human_size(nbytes: int) -> str:
    
    for unit in ['B','KB','MB','GB','TB']:
        if nbytes < 1024.0:
            return f"{nbytes:.1f}{unit}"
        nbytes /= 1024.0
    return f"{nbytes:.1f}PB"

def next_prime(n: int) -> int:
    def is_prime(x):
        if x < 2: return False
        if x % 2 == 0:
            return x == 2
        r = int(math.sqrt(x))
        for i in range(3, r+1, 2):
            if x % i == 0:
                return False
        return True
    while not is_prime(n):
        n += 1
    return n


def parse_list(s: str) -> List[str]:
    if not s.strip():
        return []
    return [item.strip() for item in s.split(",") if item.strip()]

def generate_random_list(n: int, lower=0, upper=999) -> List[str]:
    return [str(random.randint(lower, upper)) for _ in range(n)]


class SimpleHashTable:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.insert_trace = []

    def _idx(self, key: str) -> int:
        return int(key, 16) % self.capacity if all(c in "0123456789abcdef" for c in key.lower()) else hash(key) % self.capacity

    def insert(self, key: str, value: Any):
        idx = self._idx(key)
        bucket = self.buckets[idx]
        if not bucket:
            bucket.append((key, value))
            self.insert_trace.append(f"Insertando clave={key[:10]}... -> bucket {idx} (vacío).")
        else:
        
            for i,(k,v) in enumerate(bucket):
                if k == key:
                    bucket[i] = (key, value)
                    self.insert_trace.append(f"Clave {key[:10]}... ya existía en bucket {idx}, actualizando.")
                    return
            bucket.append((key,value))
            self.insert_trace.append(f"Colisión: bucket {idx} tenía {len(bucket)-1} elemento(s). Añadido {key[:10]}... -> ahora {len(bucket)} elementos.")

    def build_from_pairs(self, pairs: List[tuple]) -> List[str]:
        self.buckets = [[] for _ in range(self.capacity)]
        self.insert_trace = []
        for key, value in pairs:
            self.insert(key, value)
        return list(self.insert_trace)

    def search_trace(self, key: str) -> (Optional[Any], List[str]):
        trace = []
        idx = self._idx(key)
        trace.append(f"Índice bucket calculado: {idx} (capacity={self.capacity})")
        bucket = self.buckets[idx]
        if not bucket:
            trace.append(f"Bucket {idx} vacío → no encontrado.")
            return None, trace
        trace.append(f"Bucket {idx} contenido: {[(k[:10]+'...', v['name']) for k,v in bucket]}")
        for i,(k,v) in enumerate(bucket):
            trace.append(f"Comparando con entrada {i}: clave {k[:10]}... → archivo '{v['name']}'")
            if k == key:
                trace.append(f"→ Encontrado: archivo '{v['name']}', ruta: {v['path']}, tamaño: {human_size(v['size'])}")
                return v, trace
        trace.append("→ No encontrado en bucket.")
        return None, trace

    def final_repr_lines(self) -> List[str]:
        lines = []
        for idx, bucket in enumerate(self.buckets):
            lines.append(f"Bucket {idx}: {[(k[:10]+'...', v['name']) for k,v in bucket]}")
        return lines


class App:
    def __init__(self, root):
        self.root = root
        root.title("Buscador y Hash de Archivos")
        root.geometry("980x640")

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        
        ttk.Label(frame, text="Lista (valores separados por comas) o dejar vacía si usarás carpeta:").grid(row=0, column=0, sticky="w")
        self.entry_list = ttk.Entry(frame, width=96)
        self.entry_list.grid(row=1, column=0, columnspan=6, pady=6, sticky="w")

        ttk.Button(frame, text="Seleccionar carpeta (para Hash)", command=self.select_folder).grid(row=2, column=0, sticky="w", pady=4)
        self.label_folder = ttk.Label(frame, text="Carpeta: (ninguna)")
        self.label_folder.grid(row=2, column=1, columnspan=4, sticky="w")

       
        ttk.Label(frame, text="Generar lista aleatoria (n):").grid(row=3, column=0, sticky="w")
        self.entry_n = ttk.Entry(frame, width=8); self.entry_n.insert(0,"8")
        self.entry_n.grid(row=3, column=1, sticky="w")
        ttk.Button(frame, text="Generar lista", command=self.on_generate).grid(row=3, column=2, sticky="w", padx=6)

        
        ttk.Label(frame, text="Elemento a buscar (valor, nombre de archivo o hash hex):").grid(row=4, column=0, sticky="w", pady=(8,0))
        self.entry_target = ttk.Entry(frame, width=40)
        self.entry_target.grid(row=5, column=0, sticky="w", pady=(2,8))
        
        ttk.Label(frame, text="Método:").grid(row=4, column=2, sticky="w", pady=(8,0))
        self.method_var = tk.StringVar(value="Hash")
        ttk.Radiobutton(frame, text="Secuencial", variable=self.method_var, value="Secuencial").grid(row=4, column=3, sticky="w")
        ttk.Radiobutton(frame, text="Binaria", variable=self.method_var, value="Binaria").grid(row=4, column=4, sticky="w")
        ttk.Radiobutton(frame, text="Hash", variable=self.method_var, value="Hash").grid(row=4, column=5, sticky="w")

       
        self.show_steps = tk.BooleanVar(value=True)
        self.keep_log = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Mostrar pasos", variable=self.show_steps).grid(row=6, column=0, sticky="w")
        ttk.Checkbutton(frame, text="Conservar log", variable=self.keep_log).grid(row=6, column=1, sticky="w")

        ttk.Label(frame, text="Capacidad Hash (0 = auto):").grid(row=6, column=2, sticky="w")
        self.entry_capacity = ttk.Entry(frame, width=8); self.entry_capacity.insert(0,"0")
        self.entry_capacity.grid(row=6, column=3, sticky="w")

        ttk.Button(frame, text="Buscar", command=self.on_search).grid(row=6, column=4, sticky="w", padx=6)
        ttk.Button(frame, text="Limpiar log", command=self.clear_log).grid(row=6, column=5, sticky="w")

        
        ttk.Label(frame, text="Salida / Log:").grid(row=7, column=0, sticky="w", pady=(8,0))
        self.log = tk.Text(frame, height=18, wrap='word', state='disabled')
        self.log.grid(row=8, column=0, columnspan=6, sticky="nsew", pady=(6,0))
        frame.rowconfigure(8, weight=1)
        frame.columnconfigure(5, weight=1)

    
        ttk.Label(frame, text="Archivos detectados (carpeta):").grid(row=9, column=0, sticky="w", pady=(8,0))
        cols = ("name","size","sha256")
        self.tv = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        self.tv.heading("name", text="Nombre")
        self.tv.heading("size", text="Tamaño")
        self.tv.heading("sha256", text="SHA256 (prefix)")
        self.tv.column("name", width=360)
        self.tv.column("size", width=80, anchor="center")
        self.tv.column("sha256", width=420)
        self.tv.grid(row=10, column=0, columnspan=6, sticky="nsew", pady=(4,10))
        frame.rowconfigure(10, weight=0)

       
        self.selected_folder = None
        self.files_info = []  
        self.hash_table = None

        self.append_log("Listo. Selecciona carpeta o ingresa una lista. Para Hash, si hay carpeta seleccionada, se usará ésta.")

   
    def append_log(self, text: str):
        self.log.configure(state='normal')
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state='disabled')

    def clear_log(self):
        self.log.configure(state='normal')
        self.log.delete("1.0", tk.END)
        self.log.configure(state='disabled')

    def select_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta con documentos / archivos")
        if not folder:
            return
        self.selected_folder = folder
        self.label_folder.config(text=f"Carpeta: {folder}")
        self.append_log(f"[UI] Carpeta seleccionada: {folder}")
        self.load_folder_files(folder)

    def load_folder_files(self, folder: str, recursive: bool = False):
      
        self.files_info = []
        self.tv.delete(*self.tv.get_children())
        if recursive:
            walker = os.walk(folder)
        else:
            filenames = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
            walker = [(folder, [], filenames)]
        total = 0
        for root, _, files in walker:
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    size = os.path.getsize(fpath)
                    sha = compute_file_sha256(fpath)
                except Exception as e:
                    self.append_log(f"[Error] No se pudo leer {fpath}: {e}")
                    continue
                info = {"name": fname, "path": fpath, "size": size, "sha256": sha}
                self.files_info.append(info)
                self.tv.insert("", "end", values=(fname, human_size(size), sha[:48] + ("..." if len(sha)>48 else "")))
                total += 1
        self.append_log(f"[Folder] Cargados {total} archivo(s) desde {folder}.")

    def on_generate(self):
        try:
            n = int(self.entry_n.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Introduce entero positivo para generar.")
            return
        arr = generate_random_list(n)
        self.entry_list.delete(0, tk.END)
        self.entry_list.insert(0, ", ".join(arr))
        self.append_log(f"[UI] Generada lista aleatoria ({n}).")

    def on_search(self):
        if not self.keep_log.get():
            self.clear_log()

        method = self.method_var.get()
        target_raw = self.entry_target.get().strip()

        arr_text = self.entry_list.get().strip()
        arr = parse_list(arr_text) if arr_text else []

        self.append_log(f"[UI] Método: {method}. Target: '{target_raw}'. Carpeta seleccionada: {self.selected_folder is not None}")

    
        if method == "Secuencial":
            if not arr:
                messagebox.showwarning("Lista vacía", "Ingresa una lista o genera una.")
                return
            
            found = False
            for i,val in enumerate(arr):
                self.append_log(f"Comparando índice {i}: {val}")
                if val == target_raw:
                    self.append_log(f"→ Encontrado en índice {i}")
                    found = True
                    break
            if not found:
                self.append_log("→ No encontrado")

        elif method == "Binaria":
            if not arr:
                messagebox.showwarning("Lista vacía", "Ingresa una lista o genera una.")
                return
           
            try:
                arr_num = [int(x) for x in arr]
                numeric = True
            except:
                numeric = False

            if numeric:
                arr_sorted = sorted(arr_num)
                try:
                    target = int(target_raw)
                except:
                    self.append_log("[Error] Target no es número válido.")
                    return
            else:
                arr_sorted = sorted(arr)
                target = target_raw
            self.append_log(f"[Binaria] Lista ordenada: {arr_sorted}")
            l,r = 0, len(arr_sorted)-1
            found = False
            while l <= r:
                mid = (l+r)//2
                self.append_log(f"l={l}, r={r}, mid={mid}, arr[mid]={arr_sorted[mid]}")
                if arr_sorted[mid] == target:
                    self.append_log(f"→ Encontrado en índice {mid} (lista ordenada).")
                    found = True
                    break
                elif arr_sorted[mid] < target:
                    l = mid+1
                else:
                    r = mid-1
            if not found:
                self.append_log("→ No encontrado")

       
        elif method == "Hash":
            if self.selected_folder and self.files_info:
               
                self.append_log("[Hash] Usando archivos de la carpeta seleccionada. Calculando tabla...")
               
                pairs = []
                for info in self.files_info:
                    key = info["sha256"]
                    value = {"name": info["name"], "path": info["path"], "size": info["size"]}
                    pairs.append((key, value))
                
                cap_in = 0
                try:
                    cap_in = int(self.entry_capacity.get())
                except:
                    cap_in = 0
                cap = cap_in if cap_in>0 else next_prime(max(7, len(pairs)*2))
                cap = next_prime(max(3, cap))
                ht = SimpleHashTable(capacity=cap)
                ins_trace = ht.build_from_pairs(pairs)
                self.append_log(f"[Hash] Tabla construida con capacity={cap}.")
                if self.show_steps.get():
                    self.append_log("[Hash] Inserciones:")
                    for line in ins_trace:
                        self.append_log("  " + line)
                else:
                    self.append_log(f"[Hash] (Se realizaron {len(ins_trace)} inserciones. Activar 'Mostrar pasos' para detalles.)")

              
                self.show_hash_table_window(ht)

              
                if not target_raw:
                    messagebox.showwarning("Target vacío", "Ingresa un hash o nombre de archivo para buscar.")
                    return

               
                is_hex_hash = all(c in "0123456789abcdef" for c in target_raw.lower()) and len(target_raw) >= 6
                if is_hex_hash:
                    key_to_search = target_raw.lower()
                else:
                   
                    found_info = None
                    for info in self.files_info:
                        if info["name"] == target_raw:
                            found_info = info
                            break
                    if found_info:
                        key_to_search = found_info["sha256"]
                        self.append_log(f"[Hash] Nombre de archivo encontrado; su SHA256 es {key_to_search}")
                    else:
                        self.append_log("[Hash] Nombre de archivo no encontrado en la carpeta.")
                        key_to_search = None

                if key_to_search:
                    v, trace = ht.search_trace(key_to_search)
                    self.append_log("[Hash] Trazado de búsqueda:")
                    for line in trace:
                        self.append_log("  " + line)
                    if v:
                        self.append_log(f"[Resultado] Encontrado: archivo '{v['name']}', ruta: {v['path']}, tamaño: {human_size(v['size'])}")
                    else:
                        self.append_log("[Resultado] No encontrado por hash en la tabla.")

            else:
                
                if not arr:
                    messagebox.showwarning("Sin datos", "No hay carpeta seleccionada ni lista ingresada.")
                    return
                pairs = []
                for i,v in enumerate(arr):
                    key = v
                    value = {"name": v, "index": i}
                    pairs.append((key, value))
                
                cap_in = 0
                try:
                    cap_in = int(self.entry_capacity.get())
                except:
                    cap_in = 0
                cap = cap_in if cap_in>0 else next_prime(max(7, len(pairs)*2))
                cap = next_prime(max(3, cap))
                ht = SimpleHashTable(capacity=cap)
                ins_trace = ht.build_from_pairs(pairs)
                self.append_log(f"[Hash] Tabla construida con capacity={cap} (lista simple).")
                if self.show_steps.get():
                    for line in ins_trace:
                        self.append_log("  " + line)
               
                if not target_raw:
                    messagebox.showwarning("Target vacío", "Ingresa el valor a buscar en la lista.")
                    return
                v, trace = ht.search_trace(target_raw)
                self.append_log("[Hash] Trazado búsqueda:")
                for line in trace:
                    self.append_log("  " + line)
                if v:
                    self.append_log(f"[Resultado] Encontrado: valor '{v['name']}' en índice {v.get('index')}")
                else:
                    self.append_log("[Resultado] No encontrado en la tabla hash.")

        else:
            self.append_log("[Error] Método desconocido.")

    def show_hash_table_window(self, ht: SimpleHashTable):
        w = tk.Toplevel(self.root)
        w.title(f"Tabla Hash - capacity {ht.capacity}")
        w.geometry("720x480")
        frm = ttk.Frame(w, padding=8)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text=f"Tabla Hash - capacity {ht.capacity} (buckets)").pack(anchor="w")
        
        cols = ("bucket","contents")
        tv = ttk.Treeview(frm, columns=cols, show="headings", height=20)
        tv.heading("bucket", text="Bucket")
        tv.heading("contents", text="Contenido (clave prefix, archivo)")
        tv.column("bucket", width=80, anchor="center")
        tv.column("contents", width=600, anchor="w")
        tv.pack(fill=tk.BOTH, expand=True, pady=6)
        for i, bucket in enumerate(ht.buckets):
            tv.insert("", "end", values=(str(i), str([(k[:10]+'...', v['name']) for k,v in bucket])))
        ttk.Button(frm, text="Cerrar", command=w.destroy).pack(pady=6)


def main():
    root = tk.Tk()
    import tkinter.ttk as ttk  
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
