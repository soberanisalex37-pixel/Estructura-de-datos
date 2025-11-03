import tkinter as tk
from tkinter import Toplevel, Canvas
from collections import deque

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def es_vacio(self):
        return self.raiz is None

    # Insertar (BST)
    def insertar(self, dato):
        if self.raiz is None:
            self.raiz = Nodo(dato)
        else:
            self._insertar(self.raiz, dato)

    def _insertar(self, nodo, dato):
        if dato < nodo.dato:
            if nodo.izq:
                self._insertar(nodo.izq, dato)
            else:
                nodo.izq = Nodo(dato)
        elif dato > nodo.dato:
            if nodo.der:
                self._insertar(nodo.der, dato)
            else:
                nodo.der = Nodo(dato)

    def buscar(self, dato):
        return self._buscar(self.raiz, dato)

    def _buscar(self, nodo, dato):
        if nodo is None:
            return False
        if nodo.dato == dato:
            return True
        elif dato < nodo.dato:
            return self._buscar(nodo.izq, dato)
        else:
            return self._buscar(nodo.der, dato)

  
    def preorden_nodes(self, nodo, lista):
        if nodo:
            lista.append(nodo)
            self.preorden_nodes(nodo.izq, lista)
            self.preorden_nodes(nodo.der, lista)

    def inorden_nodes(self, nodo, lista):
        if nodo:
            self.inorden_nodes(nodo.izq, lista)
            lista.append(nodo)
            self.inorden_nodes(nodo.der, lista)

    def postorden_nodes(self, nodo, lista):
        if nodo:
            self.postorden_nodes(nodo.izq, lista)
            self.postorden_nodes(nodo.der, lista)
            lista.append(nodo)

  
    def recorrido_por_niveles_nodes(self):
        if self.raiz is None:
            return []
        cola = deque([self.raiz])
        resultado = []
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo)
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
        return resultado

  
    def preorden(self, nodo, lista):
        if nodo:
            lista.append(nodo.dato)
            self.preorden(nodo.izq, lista)
            self.preorden(nodo.der, lista)

    def inorden(self, nodo, lista):
        if nodo:
            self.inorden(nodo.izq, lista)
            lista.append(nodo.dato)
            self.inorden(nodo.der, lista)

    def postorden(self, nodo, lista):
        if nodo:
            self.postorden(nodo.izq, lista)
            self.postorden(nodo.der, lista)
            lista.append(nodo.dato)

    def recorrido_por_niveles(self):
        if self.raiz is None:
            return []
        cola = deque([self.raiz])
        resultado = []
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.dato)
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
        return resultado

 
    def eliminar(self, dato, modo='predecesor'):
        self.raiz = self._eliminar(self.raiz, dato, modo)

    def _eliminar(self, nodo, dato, modo):
        if nodo is None:
            return nodo
        if dato < nodo.dato:
            nodo.izq = self._eliminar(nodo.izq, dato, modo)
        elif dato > nodo.dato:
            nodo.der = self._eliminar(nodo.der, dato, modo)
        else:
            
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq

            if modo == 'predecesor':
                temp = self.maximo(nodo.izq)
                nodo.dato = temp.dato
                nodo.izq = self._eliminar(nodo.izq, temp.dato, modo)
            else:
                temp = self.minimo(nodo.der)
                nodo.dato = temp.dato
                nodo.der = self._eliminar(nodo.der, temp.dato, modo)
        return nodo

    def minimo(self, nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    def maximo(self, nodo):
        while nodo.der:
            nodo = nodo.der
        return nodo

    def altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self.altura(nodo.izq), self.altura(nodo.der))

    def contar_hojas(self, nodo):
        if nodo is None:
            return 0
        if nodo.izq is None and nodo.der is None:
            return 1
        return self.contar_hojas(nodo.izq) + self.contar_hojas(nodo.der)

    def contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self.contar_nodos(nodo.izq) + self.contar_nodos(nodo.der)


    def es_completo(self):
        if self.raiz is None:
            return True
        cola = deque([self.raiz])
        encontrado_vacio = False
        while cola:
            nodo = cola.popleft()
            if nodo.izq:
                if encontrado_vacio:
                    return False
                cola.append(nodo.izq)
            else:
                encontrado_vacio = True
            if nodo.der:
                if encontrado_vacio:
                    return False
                cola.append(nodo.der)
            else:
                encontrado_vacio = True
        return True

    def es_lleno(self, nodo):
        if nodo is None:
            return True
        if nodo.izq is None and nodo.der is None:
            return True
        if nodo.izq and nodo.der:
            return self.es_lleno(nodo.izq) and self.es_lleno(nodo.der)
        return False

    def eliminar_arbol(self):
        self.raiz = None

class Interfaz:
    def __init__(self, root):
        self.arbol = ArbolBinario()
        self.root = root
        self.root.title("Árbol Binario Visual - Búsqueda directa resaltada")
        self.root.geometry("1150x800")
        self.root.config(bg="#e8f0fe")

        frame_top = tk.Frame(root, bg="#e8f0fe")
        frame_top.pack(pady=8, fill="x")

        tk.Label(frame_top, text="Dato:", bg="#e8f0fe", font=("Arial", 12)).pack(side=tk.LEFT, padx=(10,4))
        self.entry = tk.Entry(frame_top, width=10, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=(0,10))
        tk.Button(frame_top, text="Insertar", command=self.insertar, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=4)
        tk.Button(frame_top, text="Eliminar (Predecesor)", command=lambda: self.eliminar("predecesor"), bg="#ff7043").pack(side=tk.LEFT, padx=4)
        tk.Button(frame_top, text="Eliminar (Sucesor)", command=lambda: self.eliminar("sucesor"), bg="#ff7043").pack(side=tk.LEFT, padx=4)
     
        tk.Button(frame_top, text="Buscar (resaltar)", command=self.buscar_resaltar, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=4)
        tk.Button(frame_top, text="Ver árbol acostado 🌲", command=self.mostrar_arbol_acostado, bg="#7e57c2", fg="white").pack(side=tk.LEFT, padx=8)

        
        self.mostrar_contador_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame_top, text="Mostrar conteo subnodos", variable=self.mostrar_contador_var,
                       bg="#e8f0fe").pack(side=tk.LEFT, padx=6)

       
        frame_canvas = tk.Frame(root, bg="#e8f0fe")
        frame_canvas.pack(pady=8)

        self.scrollbar = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

      
        self.canvas = tk.Canvas(frame_canvas, bg="white", width=1080, height=500,
                                yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT)
        self.scrollbar.config(command=self.canvas.yview)

        
        self.text = tk.Text(root, height=8, width=135, font=("Consolas", 11))
        self.text.pack(pady=8)

        frame_bottom = tk.Frame(root, bg="#e8f0fe")
        frame_bottom.pack(pady=6)

        botones = [
            ("PreOrden (anim)", self.animar_preorden),
            ("InOrden (anim)", self.animar_inorden),
            ("PostOrden (anim)", self.animar_postorden),
            ("Por Niveles (anim)", self.animar_niveles),
            ("PreOrden (texto)", self.preorden_texto),
            ("InOrden (texto)", self.inorden_texto),
            ("PostOrden (texto)", self.postorden_texto),
            ("Por Niveles (texto)", self.niveles_texto)
        ]
        for txt, cmd in botones:
            tk.Button(frame_bottom, text=txt, command=cmd, bg="#90caf9", width=16).pack(side=tk.LEFT, padx=4, pady=4)

      
        frame_more = tk.Frame(root, bg="#e8f0fe")
        frame_more.pack(pady=4)
        tk.Button(frame_more, text="Altura", command=self.altura, bg="#aed581", width=12).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_more, text="Hojas", command=self.hojas, bg="#aed581", width=12).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_more, text="Nodos", command=self.nodos, bg="#aed581", width=12).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_more, text="¿Completo?", command=self.completo, bg="#ffcc80", width=12).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_more, text="¿Lleno?", command=self.lleno, bg="#ffcc80", width=12).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_more, text="Eliminar Árbol", command=self.eliminar_arbol, bg="#ef9a9a", width=14).pack(side=tk.LEFT, padx=8)

     
        self.colores_niveles = ["#81c784", "#4fc3f7", "#ba68c8", "#ffb74d", "#ef5350", "#aed581", "#7986cb", "#f06292"]

      
        self.mapa_nodos = {}
      
        self.mapa_pos = {}

    
        self.canvas.config(scrollregion=(0, 0, 2000, 2000))


    def show_modal(self, title, message, kind="info"):
        
        modal = Toplevel(self.root)
        modal.transient(self.root)
        modal.grab_set()
        modal.title(title)
        modal.config(bg="#ffffff")
       
        modal.geometry("360x120")
        modal.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (360 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (120 // 2)
        modal.geometry(f"+{x}+{y}")

        frame = tk.Frame(modal, bg="#ffffff", padx=12, pady=10)
        frame.pack(expand=True, fill="both")
        lbl = tk.Label(frame, text=message, bg="#ffffff", font=("Arial", 11), wraplength=320, justify="center")
        lbl.pack(expand=True, fill="both")
        btn_bg = "#4fc3f7" if kind == "info" else "#ef5350"
        tk.Button(frame, text="Aceptar", bg=btn_bg, fg="white", command=modal.destroy, width=10).pack(pady=(6,0))
        self.root.wait_window(modal)

   
    def insertar(self):
        try:
            dato = int(self.entry.get())
        except ValueError:
            self.show_modal("Error", "Ingrese un número válido (entero).", kind="error")
            return

        
        if self.arbol.buscar(dato):
            self.show_modal("Duplicado", f"El valor {dato} ya existe en el árbol. No se inserta duplicado.", kind="error")
            return

        self.arbol.insertar(dato)
        self.entry.delete(0, tk.END)
        self.dibujar()

    def eliminar(self, modo):
        try:
            dato = int(self.entry.get())
            self.arbol.eliminar(dato, modo)
            self.entry.delete(0, tk.END)
            self.dibujar()
        except ValueError:
            self.show_modal("Error", "Ingrese un número válido (entero).", kind="error")

    
    def buscar_resaltar(self):
        try:
            target = int(self.entry.get())
        except ValueError:
            self.show_modal("Error", "Ingrese un número válido (entero).", kind="error")
            return

        if self.arbol.raiz is None:
            self.show_modal("Vacío", "El árbol está vacío 🌱", kind="info")
            return

   
        node = self.arbol.raiz
        found_node = None
        while node:
            if node.dato == target:
                found_node = node
                break
            elif target < node.dato:
                node = node.izq
            else:
                node = node.der

     
        if found_node is None:
            self.show_modal("Buscar", f"Valor {target} NO encontrado ❌", kind="info")
            return

        self.dibujar()

        if found_node not in self.mapa_nodos:
            self.dibujar()

        if found_node not in self.mapa_nodos:
           
            self.show_modal("Buscar", f"Valor {target} encontrado (pero no se pudo resaltar visualmente).", kind="info")
            return

        oval_id, text_id, color_original = self.mapa_nodos[found_node]

        highlight = "#00e676" 
        flashes = 3
        interval = 450  

        def flash_step(i):
            if i >= flashes * 2:

                self.canvas.itemconfig(oval_id, fill=color_original)
                self.show_modal("Buscar", f"Valor {target} encontrado ✅", kind="info")
                return
            if i % 2 == 0:
                self.canvas.itemconfig(oval_id, fill=highlight)
            else:
                self.canvas.itemconfig(oval_id, fill=color_original)
            self.root.after(interval, lambda: flash_step(i + 1))

        flash_step(0)

    def buscar(self):
   
        try:
            dato = int(self.entry.get())
            encontrado = self.arbol.buscar(dato)
            self.text.insert(tk.END, f"Buscar {dato}: {'Encontrado ✅' if encontrado else 'No encontrado ❌'}\n")
        except ValueError:
            self.show_modal("Error", "Ingrese un número válido (entero).", kind="error")

    def altura(self):
        h = self.arbol.altura(self.arbol.raiz)
        self.text.insert(tk.END, f"Altura del árbol: {h}\n")

   
    def hojas(self):
        h = self.arbol.contar_hojas(self.arbol.raiz)
        self.text.insert(tk.END, f"Hojas: {h}\n")
      
        if self.arbol.raiz:
            all_nodes = self.arbol.recorrido_por_niveles_nodes()
            hojas_nodes = [n for n in all_nodes if (n.izq is None and n.der is None)]
            if hojas_nodes:
                self._animar_lista_nodes(hojas_nodes, delay_ms=700)

    def nodos(self):
        n = self.arbol.contar_nodos(self.arbol.raiz)
        self.text.insert(tk.END, f"Nodos: {n}\n")

        if self.arbol.raiz:
            nodes = self.arbol.recorrido_por_niveles_nodes()
            if nodes:
                self._animar_lista_nodes(nodes, delay_ms=500)

    def completo(self):
        c = self.arbol.es_completo()
        self.text.insert(tk.END, f"¿Es completo?: {'Sí ✅' if c else 'No ❌'}\n")

    def lleno(self):
        l = self.arbol.es_lleno(self.arbol.raiz)
        self.text.insert(tk.END, f"¿Es lleno?: {'Sí ✅' if l else 'No ❌'}\n")

    def eliminar_arbol(self):
        self.arbol.eliminar_arbol()
        self.canvas.delete("all")
        self.mapa_nodos.clear()
        self.mapa_pos.clear()
        self.text.insert(tk.END, "Árbol eliminado 🗑️\n")


    def dibujar(self):
        self.canvas.delete("all")
        self.mapa_nodos.clear()
        self.mapa_pos.clear()
        if not self.arbol.raiz:
            return
     
        self._dibujar_nodo(self.arbol.raiz, 540, 40, 220, 0)

        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.config(scrollregion=bbox)

    def _dibujar_nodo(self, nodo, x, y, separacion, nivel):
        if nodo is None:
            return
        r = 22
        color_nivel = self.colores_niveles[nivel % len(self.colores_niveles)]

        
        if nodo.izq:
            self.canvas.create_line(x, y, x - separacion, y + 90)
            self._dibujar_nodo(nodo.izq, x - separacion, y + 90, separacion / 1.7, nivel + 1)
        if nodo.der:
            self.canvas.create_line(x, y, x + separacion, y + 90)
            self._dibujar_nodo(nodo.der, x + separacion, y + 90, separacion / 1.7, nivel + 1)

       
        oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color_nivel, outline="#263238", width=2)
        text_id = self.canvas.create_text(x, y, text=str(nodo.dato), font=("Arial", 12, "bold"), fill="white")
        self.mapa_nodos[nodo] = (oval, text_id, color_nivel)
        self.mapa_pos[nodo] = (x, y)

        if self.mostrar_contador_var.get():
            cnt = self.arbol.contar_nodos(nodo)
           
            self.canvas.create_text(x, y + r + 10, text=str(cnt), font=("Arial", 8), fill="#37474f")

   
    def mostrar_arbol_acostado(self):
        if not self.arbol.raiz:
            self.show_modal("Vacío", "El árbol está vacío 🌱", kind="info")
            return

        ventana = Toplevel(self.root)
        ventana.title("Árbol Acostado 🌲 (Raíz a la izquierda)")
      
        canvas = Canvas(ventana, width=1000, height=700, bg="white")
        canvas.pack(fill="both", expand=True, side=tk.LEFT)
        scroll_y = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
        scroll_y.pack(side="right", fill="y")
        canvas.config(yscrollcommand=scroll_y.set)

      
        self._dibujar_acostado(canvas, self.arbol.raiz, 60, 360, 140, 0)
        bbox = canvas.bbox("all")
        if bbox:
            canvas.config(scrollregion=bbox)

    def _dibujar_acostado(self, canvas, nodo, x, y, sep, nivel):
        if nodo is None:
            return
        r = 20
        color = self.colores_niveles[nivel % len(self.colores_niveles)]

      
        if nodo.der:
            canvas.create_line(x + r, y, x + sep, y - 90)
            self._dibujar_acostado(canvas, nodo.der, x + sep, y - 90, sep, nivel + 1)

       
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="#263238", width=2)
        canvas.create_text(x, y, text=str(nodo.dato), font=("Arial", 11, "bold"), fill="white")

      
        if nodo.izq:
            canvas.create_line(x + r, y, x + sep, y + 90)
            self._dibujar_acostado(canvas, nodo.izq, x + sep, y + 90, sep, nivel + 1)

 
    def animar_preorden(self):
        if not self.arbol.raiz:
            self.show_modal("Vacío", "El árbol está vacío 🌱", kind="info")
            return
        nodes = []
        self.arbol.preorden_nodes(self.arbol.raiz, nodes)
        self.text.insert(tk.END, f"PreOrden: {[n.dato for n in nodes]}\n")
        self._animar_lista_nodes(nodes)

    def animar_inorden(self):
        if not self.arbol.raiz:
            self.show_modal("Vacío", "El árbol está vacío 🌱", kind="info")
            return
        nodes = []
        self.arbol.inorden_nodes(self.arbol.raiz, nodes)
        self.text.insert(tk.END, f"InOrden: {[n.dato for n in nodes]}\n")
        self._animar_lista_nodes(nodes)

    def animar_postorden(self):
        if not self.arbol.raiz:
            self.show_modal("Vacío", "El árbol está vacío 🌱", kind="info")
            return
        nodes = []
        self.arbol.postorden_nodes(self.arbol.raiz, nodes)
        self.text.insert(tk.END, f"PostOrden: {[n.dato for n in nodes]}\n")
        self._animar_lista_nodes(nodes)

    def animar_niveles(self):
        if not self.arbol.raiz:
            self.show_modal("Vacío", "El árbol está vacío 🌱", kind="info")
            return
        nodes = self.arbol.recorrido_por_niveles_nodes()
        self.text.insert(tk.END, f"Por Niveles: {[n.dato for n in nodes]}\n")
        self._animar_lista_nodes(nodes)

    def _animar_lista_nodes(self, nodes, delay_ms=650, callback=None):
     
        self.dibujar()

        
        if not nodes:
            if callback:
                callback()
            return

        etiquetas_temporales = []

        def anim_step(i):
            if i >= len(nodes):
             
                self.root.after(400, lambda: [self.canvas.delete(eid) for eid in etiquetas_temporales])
                if callback:
                 
                    self.root.after(450, callback)
                return

            nodo = nodes[i]
            if nodo not in self.mapa_nodos:
                self.root.after(delay_ms, lambda: anim_step(i + 1))
                return

            oval_id, texto_id, color_original = self.mapa_nodos[nodo]
           
            highlight_color = "#ffd54f"  
            self.canvas.itemconfig(oval_id, fill=highlight_color)

          
            x, y = self.mapa_pos.get(nodo, (0, 0))
            etiqueta = self.canvas.create_text(x + 28, y - 18, text=f"{i+1}", font=("Arial", 10, "bold"),
                                               fill="#000000", anchor="nw", tags=("etiqueta_orden",))
            etiquetas_temporales.append(etiqueta)

          
            self.root.after(delay_ms // 2, lambda oid=oval_id, col=color_original: self.canvas.itemconfig(oid, fill=col))
          
            self.root.after(delay_ms, lambda: anim_step(i + 1))

      
        anim_step(0)

    def preorden_texto(self):
        lista = []
        self.arbol.preorden(self.arbol.raiz, lista)
        self.text.insert(tk.END, f"PreOrden: {lista}\n")

    def inorden_texto(self):
        lista = []
        self.arbol.inorden(self.arbol.raiz, lista)
        self.text.insert(tk.END, f"InOrden: {lista}\n")

    def postorden_texto(self):
        lista = []
        self.arbol.postorden(self.arbol.raiz, lista)
        self.text.insert(tk.END, f"PostOrden: {lista}\n")

    def niveles_texto(self):
        lista = self.arbol.recorrido_por_niveles()
        self.text.insert(tk.END, f"Por niveles: {lista}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()

