# grafo_mexico_final_v2.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from PIL import Image
import math, time, itertools, random
import networkx as nx
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------
# CENTROIDES (lat, lon)
# -----------------------
CENTROIDES = {
    "Aguascalientes": (21.8823, -102.2826),
    "Baja California": (30.8406, -115.2838),
    "Baja California Sur": (25.3470, -111.6667),
    "Campeche": (19.8301, -90.5349),
    "Chiapas": (16.7569, -93.1292),
    "Chihuahua": (28.6327, -106.0691),
    "Coahuila": (26.8600, -101.4108),
    "Colima": (19.1226, -103.6173),
    "Durango": (24.0277, -104.6532),
    "Guanajuato": (21.0190, -101.2574),
    "Guerrero": (17.4445, -99.5354),
    "Hidalgo": (20.0911, -98.7629),
    "Jalisco": (20.6597, -103.3496),
    "Mexico": (19.4969, -99.7233),
    "Ciudad de México": (19.4326, -99.1332),
    "Michoacán": (19.5665, -101.7068),
    "Morelos": (18.6814, -99.1013),
    "Nayarit": (21.7514, -104.8455),
    "Nuevo León": (25.5922, -99.9962),
    "Oaxaca": (17.0732, -96.7266),
    "Puebla": (19.0413, -98.2062),
    "Querétaro": (20.5888, -100.3899),
    "Quintana Roo": (19.1817, -88.4791),
    "San Luis Potosí": (22.1566, -100.9855),
    "Sinaloa": (25.1721, -107.4795),
    "Sonora": (29.2972, -110.3309),
    "Tabasco": (17.8409, -92.6189),
    "Tamaulipas": (23.7369, -99.1411),
    "Tlaxcala": (19.3166, -98.2376),
    "Veracruz": (19.1738, -96.1342),
    "Yucatán": (20.7099, -89.0943),
    "Zacatecas": (22.7709, -102.5832)
}

# -----------------------
# Parámetros / extent
# -----------------------
EXTENT = [-118, -86, 14, 33]
MAX_DIST_KM = 350.0

# -----------------------
# Funciones geográficas
# -----------------------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c

def estado_mas_cercano(lat_click, lon_click):
    best = None
    best_d = float('inf')
    for est, (elat, elon) in CENTROIDES.items():
        d = haversine_km(lat_click, lon_click, elat, elon)
        if d < best_d:
            best_d = d
            best = est
    return best, best_d

# -----------------------
# App
# -----------------------
class GrafosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grafo interactivo - México (mapa)")

        # Load image
        try:
            pil_img = Image.open("mapa.png").convert("RGBA")
        except Exception as e:
            messagebox.showerror("Error", f"No se encontró 'mapa.png': {e}")
            root.destroy()
            return
        self.pil_img = pil_img
        self.img_w, self.img_h = pil_img.size
        self.img_arr = np.array(pil_img)
        self.map_img = mpimg.imread("mapa.png")

        # Variables
        self.G = nx.Graph()
        self.positions = {}
        self.selected_node = None

        # Top controls
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, padx=6, pady=6)
        tk.Label(top_frame, text="Estados a seleccionar (recomendado 7):").pack(side=tk.LEFT)
        self.var_num = tk.IntVar(value=7)
        self.spin_num = tk.Spinbox(top_frame, from_=1, to=32, width=4, textvariable=self.var_num)
        self.spin_num.pack(side=tk.LEFT, padx=(4,12))
        tk.Label(top_frame, text="Precio por km ($):").pack(side=tk.LEFT)
        self.var_price = tk.DoubleVar(value=5.0)
        self.entry_price = tk.Entry(top_frame, textvariable=self.var_price, width=8)
        self.entry_price.pack(side=tk.LEFT, padx=(4,12))

        btn_calc = tk.Button(top_frame, text="Calcular recorridos", command=self.on_calcular)
        btn_calc.pack(side=tk.RIGHT, padx=6)
        btn_clear = tk.Button(top_frame, text="Limpiar todo", command=self.limpiar_todo)
        btn_clear.pack(side=tk.RIGHT)

        # Botones eliminar
        btn_frame_del = tk.Frame(root)
        btn_frame_del.pack(fill=tk.X, padx=6, pady=(0,6))
        self.btn_del_node = tk.Button(btn_frame_del, text="Eliminar nodo", command=self.eliminar_nodo)
        self.btn_del_node.pack(side=tk.LEFT, padx=6)
        self.btn_del_edge = tk.Button(btn_frame_del, text="Eliminar arista", command=self.eliminar_arista)
        self.btn_del_edge.pack(side=tk.LEFT, padx=6)

        # Botones animaciones
        btn_frame2 = tk.Frame(root)
        btn_frame2.pack(fill=tk.X, padx=6, pady=(0,6))
        self.btn_ham = tk.Button(btn_frame2, text="Recorrido sin repetición (Hamiltoniano)", command=self.run_hamiltonian_animation)
        self.btn_ham.pack(side=tk.LEFT, padx=6)
        self.btn_walk = tk.Button(btn_frame2, text="Recorrido con repetición (aleatorio)", command=self.run_walk_animation)
        self.btn_walk.pack(side=tk.LEFT, padx=6)

        # Main area
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        map_frame = tk.Frame(main_frame)
        map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.canvas = FigureCanvasTkAgg(self.fig, map_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.imshow(self.map_img, extent=EXTENT, aspect='auto')
        self.ax.set_title("Clic izquierdo: agregar nodo | Clic derecho: seleccionar/conectar")
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Right panel
        right_frame = tk.Frame(main_frame, width=360)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(right_frame, text="Resultados", font=("Arial", 12, "bold")).pack(pady=(6,2))
        cols = ("tipo","km","costo")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=6)
        for c, t in zip(cols, ["Recorrido","Distancia (km)","Costo ($)"]):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(padx=6, pady=6)
        self.txt_log = tk.Text(right_frame, height=14, width=44)
        self.txt_log.pack(padx=6, pady=6, fill=tk.Y)
        self.txt_log.insert(tk.END,
            "Instrucciones:\n"
            "- Clic izquierdo: agregar nodo\n"
            "- Clic derecho: seleccionar/conectar\n"
            "- Ajusta 'Estados a seleccionar' y 'Precio por km'\n"
            "- Botones animación separados.\n"
        )
        self.txt_log.config(state=tk.DISABLED)

        self.draw()

    # -----------------------
    # Coordenadas y clic sobre imagen
    # -----------------------
    def lonlat_to_pixel(self, lon, lat):
        lon_min, lon_max, lat_min, lat_max = EXTENT[0], EXTENT[1], EXTENT[2], EXTENT[3]
        u = (lon - lon_min) / (lon_max - lon_min)
        v = (lat_max - lat) / (lat_max - lat_min)
        px = int(u*(self.img_w-1))
        py = int(v*(self.img_h-1))
        return px, py

    def click_over_image(self, lon, lat, alpha_thresh=10, whiteness_thresh=0.95):
        px, py = self.lonlat_to_pixel(lon, lat)
        if px<0 or px>=self.img_w or py<0 or py>=self.img_h: return False
        pixel = self.img_arr[py, px]
        alpha = pixel[3] if pixel.shape[0]>=4 else 255
        if alpha < alpha_thresh: return False
        r,g,b = pixel[0]/255,pixel[1]/255,pixel[2]/255
        return (r+g+b)/3.0 <= whiteness_thresh

    # -----------------------
    # Clic izquierdo/derecho
    # -----------------------
    def on_click(self, event):
        if event.inaxes != self.ax: return
        lon, lat = event.xdata, event.ydata
        if lon is None or lat is None: return

        # Clic izquierdo: agregar nodo
        if event.button==1:
            max_nodes = int(self.var_num.get())
            if len(self.G.nodes) >= max_nodes:
                messagebox.showinfo("Límite alcanzado", f"Ya se alcanzó el límite de {max_nodes} nodos.")
                return
            if not (EXTENT[0]<=lon<=EXTENT[1] and EXTENT[2]<=lat<=EXTENT[3]) or not self.click_over_image(lon, lat):
                messagebox.showwarning("Fuera del mapa","Clic fuera del contorno del mapa.")
                return
            estado, dkm = estado_mas_cercano(lat, lon)
            if dkm>MAX_DIST_KM:
                messagebox.showinfo("Muy lejos", f"El nodo más cercano es {estado}, a {dkm:.0f} km. No se agregará.")
                return
            if estado in self.G.nodes:
                messagebox.showinfo("Nodo existente", f"El nodo {estado} ya fue agregado.")
                return
            self.G.add_node(estado)
            self.positions[estado] = (lon, lat)
            self.log(f"Nodo agregado: {estado} (≈{dkm:.0f} km)")
            self.draw()
            if len(self.G.nodes)==max_nodes:
                messagebox.showinfo("Nodos completos", f"Se han agregado todos los nodos ({max_nodes}). Conecta con clic derecho.")

        # Clic derecho: seleccionar/conectar
        elif event.button==3:
            nodo = self.node_nearby(lon, lat)
            if nodo is None: 
                self.log("No hay nodo cercano para seleccionar.")
                return
            if self.selected_node is None:
                self.selected_node = nodo
                self.log(f"Nodo seleccionado: {nodo}. Clic derecho en otro nodo para conectar.")
                self.ax.set_title(f"Nodo seleccionado: {nodo}")
                self.canvas.draw_idle()
            else:
                if nodo==self.selected_node:
                    self.selected_node=None
                    self.ax.set_title("Clic izquierdo: agregar nodo | Clic derecho: seleccionar/conectar")
                    self.canvas.draw_idle()
                    self.log("Deseleccionado.")
                else:
                    lon1,lat1=self.positions[self.selected_node]
                    lon2,lat2=self.positions[nodo]
                    dkm = haversine_km(lat1, lon1, lat2, lon2)
                    self.G.add_edge(self.selected_node, nodo, weight=round(dkm,2))
                    self.log(f"Conectado: {self.selected_node} ↔ {nodo} = {dkm:.1f} km")
                    self.selected_node=None
                    self.ax.set_title("Clic izquierdo: agregar nodo | Clic derecho: seleccionar/conectar")
                    self.draw()

    # -----------------------
    # Buscar nodo cercano
    # -----------------------
    def node_nearby(self, lon, lat, tol_deg=0.6):
        for n,(nx_,ny_) in self.positions.items():
            if abs(nx_-lon)<=tol_deg and abs(ny_-lat)<=tol_deg:
                return n
        return None

    # -----------------------
    # Dibujar
    # -----------------------
    def draw(self):
        self.ax.clear()
        self.ax.imshow(self.map_img, extent=EXTENT, aspect='auto')
        if self.positions:
            nx.draw(self.G, self.positions, with_labels=True, node_color='tab:blue', font_color='white', ax=self.ax, node_size=300)
            edge_labels = nx.get_edge_attributes(self.G,'weight')
            if edge_labels: nx.draw_networkx_edge_labels(self.G,self.positions,edge_labels=edge_labels,ax=self.ax,font_color='red')
        self.canvas.draw_idle()

    # -----------------------
    # Logs
    # -----------------------
    def log(self,text):
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END,f"{text}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    # -----------------------
    # Limpiar todo
    # -----------------------
    def limpiar_todo(self):
        self.G.clear()
        self.positions.clear()
        self.selected_node=None
        self.tree.delete(*self.tree.get_children())
        self.draw()
        self.log("Todo limpiado.")

    # -----------------------
    # Eliminar nodo/arista
    # -----------------------
    def eliminar_nodo(self):
        if not self.G.nodes:
            messagebox.showinfo("Info","No hay nodos para eliminar")
            return
        nodo = self.selected_node
        if nodo is None:
            messagebox.showinfo("Info","Selecciona un nodo (clic derecho) para eliminar")
            return
        self.G.remove_node(nodo)
        del self.positions[nodo]
        self.selected_node=None
        self.draw()
        self.log(f"Nodo eliminado: {nodo}")

    def eliminar_arista(self):
        if not self.G.edges:
            messagebox.showinfo("Info","No hay aristas para eliminar")
            return
        if self.selected_node is None:
            messagebox.showinfo("Info","Selecciona un nodo (clic derecho) como inicio de la arista a eliminar")
            return
        nodo1 = self.selected_node
        nodo2 = simpledialog.askstring("Eliminar arista", f"Escribe el nodo final conectado a {nodo1} a eliminar:")
        if nodo2 not in self.G.nodes or not self.G.has_edge(nodo1,nodo2):
            messagebox.showwarning("Error","No existe esa arista")
            return
        self.G.remove_edge(nodo1,nodo2)
        self.selected_node=None
        self.draw()
        self.log(f"Arista eliminada: {nodo1} ↔ {nodo2}")

    # -----------------------
    # Recorridos Hamiltoniano y aleatorio
    # -----------------------
    def best_hamiltonian(self):
        nodes=list(self.G.nodes)
        if not nodes: return None,None
        if len(nodes)>9:
            if not messagebox.askyesno("Aviso","Búsqueda exhaustiva puede tardar mucho con >9 nodos. Continuar?"): return None,None
        best=None; best_cost=float('inf')
        for perm in itertools.permutations(nodes):
            valid=True; cost=0.0
            for i in range(len(perm)-1):
                u,v=perm[i],perm[i+1]
                if not self.G.has_edge(u,v): valid=False; break
                cost+=self.G[u][v]['weight']
            if valid and cost<best_cost:
                best_cost=cost; best=perm
        return list(best) if best else None, round(best_cost,2) if best else None

    def random_walk_until_cover(self,max_steps=10000):
        nodes=list(self.G.nodes)
        if not nodes: return None,None
        start=random.choice(nodes)
        walk=[start]; visited={start}; total=0.0; steps=0
        neigh={n:list(self.G.neighbors(n)) for n in nodes}
        if any(len(neigh[n])==0 for n in nodes): return None,None
        current=start
        while len(visited)<len(nodes) and steps<max_steps:
            choices=neigh[current]
            if not choices: break
            nxt=random.choice(choices)
            walk.append(nxt)
            total+=self.G[current][nxt]['weight'] if self.G.has_edge(current,nxt) else 0
            visited.add(nxt)
            current=nxt; steps+=1
        if len(visited)==len(nodes): return walk,round(total,2)
        else: return None,None

    # -----------------------
    # Animaciones
    # -----------------------
    def animate_path(self,path,color='yellow',speed=0.0035,steps=30):
        if not path or len(path)<2: return
        dot, = self.ax.plot([],[],marker='o',color='magenta',markersize=10,zorder=12)
        self.root.config(cursor="watch")
        for i in range(len(path)-1):
            a,b=path[i],path[i+1]
            lon1,lat1=self.positions[a]; lon2,lat2=self.positions[b]
            self.ax.plot([lon1,lon2],[lat1,lat2],color=color,linewidth=3,zorder=6)
            for t in range(steps+1):
                frac=t/steps; x=lon1+(lon2-lon1)*frac; y=lat1+(lat2-lat1)*frac
                dot.set_data([x],[y])
                self.canvas.draw(); self.root.update(); time.sleep(speed)
        dot.remove(); self.canvas.draw(); self.root.config(cursor="")

    # -----------------------
    # Run animations
    # -----------------------
    def run_hamiltonian_animation(self):
        ham_path, ham_cost=self.best_hamiltonian()
        price=float(self.var_price.get())
        self.tree.delete(*self.tree.get_children())
        if ham_path:
            ham_money=round(ham_cost*price,2)
            self.tree.insert("",tk.END,values=("Sin repetir",f"{ham_cost:.2f}",f"{ham_money:.2f}"))
            self.log(f"Hamiltoniano: {' → '.join(ham_path)} | {ham_cost:.2f} km | ${ham_money:.2f}")
            self.animate_path(ham_path,color='yellow',speed=0.0035,steps=30)
        else:
            self.tree.insert("",tk.END,values=("Sin repetir","No hay","No hay"))
            self.log("Hamiltoniano: no encontrado o cancelado.")

    def run_walk_animation(self):
        walk, walk_cost=self.random_walk_until_cover()
        price=float(self.var_price.get())
        self.tree.delete(*self.tree.get_children())
        ham_path, ham_cost=self.best_hamiltonian()
        if ham_path:
            ham_money=round(ham_cost*price,2)
            self.tree.insert("",tk.END,values=("Sin repetir",f"{ham_cost:.2f}",f"{ham_money:.2f}"))
        else:
            self.tree.insert("",tk.END,values=("Sin repetir","No hay","No hay"))
        if walk:
            walk_money=round(walk_cost*price,2)
            self.tree.insert("",tk.END,values=("Repitiendo (aleatorio)",f"{walk_cost:.2f}",f"{walk_money:.2f}"))
            self.log(f"Walk: {' → '.join(walk)} | {walk_cost:.2f} km | ${walk_money:.2f}")
            self.animate_path(walk,color='cyan',speed=0.0035,steps=30)
        else:
            self.tree.insert("",tk.END,values=("Repitiendo (aleatorio)","No hay","No hay"))
            self.log("Walk: no se pudo generar")

    def on_calcular(self):
        ham_path, ham_cost=self.best_hamiltonian()
        walk, walk_cost=self.random_walk_until_cover()
        price=float(self.var_price.get())
        self.tree.delete(*self.tree.get_children())
        if ham_path:
            ham_money=round(ham_cost*price,2)
            self.tree.insert("",tk.END,values=("Sin repetir",f"{ham_cost:.2f}",f"{ham_money:.2f}"))
            self.log(f"Hamiltoniano: {' → '.join(ham_path)} | {ham_cost:.2f} km | ${ham_money:.2f}")
        else:
            self.tree.insert("",tk.END,values=("Sin repetir","No hay","No hay"))
        if walk:
            walk_money=round(walk_cost*price,2)
            self.tree.insert("",tk.END,values=("Repitiendo (aleatorio)",f"{walk_cost:.2f}",f"{walk_money:.2f}"))
            self.log(f"Walk: {' → '.join(walk)} | {walk_cost:.2f} km | ${walk_money:.2f}")
        else:
            self.tree.insert("",tk.END,values=("Repitiendo (aleatorio)","No hay","No hay"))
            self.log("Walk: no se pudo generar")

# -----------------------
# Ejecutar app
# -----------------------
if __name__=="__main__":
    root=tk.Tk()
    app=GrafosApp(root)
    root.mainloop()
