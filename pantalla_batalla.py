# pantalla_batalla.py
# Esta pantalla maneja toda la lógica de la batalla por turnos
# Incluye imágenes de personajes y fondo de batalla según la ubicación

import tkinter as tk
from tkinter import messagebox
import random
from modelos import cargar_personajes
from PIL import Image, ImageTk

class PantallaBatalla:
    def __init__(self, root, jugador_nombre, personajes_jugador, indice_hollow, ubicaciones, callback_fin):
        self.root = root
        self.root.title("Batalla!")
        self.root.geometry("700x650")
        self.root.configure(bg="#1a1a2e")
        
        self.jugador_nombre = jugador_nombre
        self.callback_fin = callback_fin
        self.indice_hollow = indice_hollow
        self.ubicaciones = ubicaciones
        
        self.puntaje_jugador = 0
        self.puntaje_hollow = 0
        
        self.personajes_jugador = personajes_jugador
        
        todos = cargar_personajes()
        self.personajes_hollow = random.sample(todos, 3)
        
        self.personaje_jugador_activo = self.personajes_jugador[0]
        self.personaje_hollow_activo = self.personajes_hollow[0]
        
        self.turno = "jugador"
        self.img_jugador = None
        self.img_hollow = None
        self.img_fondo = None
        
        self.construir_pantalla()

    def cargar_fondo(self):
        # Carga la imagen de fondo según la ubicación actual
        nombres_fondo = [
            "planeta_namek",
            "final_fantasy", 
            "aldea_de_la_hoja",
            "ciudad_de_tokio",
            "green_hill_zone"
        ]
        try:
            nombre = nombres_fondo[self.indice_hollow]
            # Intenta jpg primero, luego png
            try:
                img = Image.open(f"imagenes/{nombre}.jpg")
            except:
                img = Image.open(f"imagenes/{nombre}.png")
            img = img.resize((700, 650))
            return ImageTk.PhotoImage(img)
        except:
            return None

    def cargar_imagen(self, nombre_personaje, lado):
        # Carga la imagen del personaje
        try:
            nombre_archivo = nombre_personaje.lower().replace(" ", "_")
            ruta = f"imagenes/{nombre_archivo}.png"
            img = Image.open(ruta)
            img = img.resize((150, 150))
            if lado == "derecha":
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            return ImageTk.PhotoImage(img)
        except:
            return None

    def construir_pantalla(self):
        # Canvas para el fondo de batalla
        self.canvas = tk.Canvas(self.root, width=700, height=650)
        self.canvas.place(x=0, y=0)
        
        # Carga y muestra el fondo
        self.img_fondo = self.cargar_fondo()
        if self.img_fondo:
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_fondo)
        else:
            self.canvas.configure(bg="#1a1a2e")

        # Título
        hollow_nombre = self.ubicaciones[self.indice_hollow]["hollow"]
        tk.Label(self.root, text=f"¡Batalla contra {hollow_nombre}!",
                font=("Arial", 16, "bold"),
                bg="#1a1a2e", fg="#e94560").place(x=150, y=10)

        # Puntaje
        self.label_puntaje = tk.Label(self.root,
                text=f"{self.jugador_nombre}: {self.puntaje_jugador} | Hollow: {self.puntaje_hollow}",
                font=("Arial", 12),
                bg="#1a1a2e", fg="white")
        self.label_puntaje.place(x=200, y=45)

        # Frame jugador
        frame_jugador = tk.Frame(self.root, bg="#16213e", padx=10, pady=10)
        frame_jugador.place(x=30, y=80)
        
        tk.Label(frame_jugador, text=self.jugador_nombre,
                font=("Arial", 12, "bold"),
                bg="#16213e", fg="#e94560").pack()
        
        self.label_img_jugador = tk.Label(frame_jugador, bg="#16213e")
        self.label_img_jugador.pack()
        
        self.label_personaje_jugador = tk.Label(frame_jugador, text="",
                font=("Arial", 10), bg="#16213e", fg="white")
        self.label_personaje_jugador.pack()

        # VS
        tk.Label(self.root, text="VS",
                font=("Arial", 20, "bold"),
                bg="#1a1a2e", fg="#e94560").place(x=320, y=180)

        # Frame hollow
        frame_hollow = tk.Frame(self.root, bg="#16213e", padx=10, pady=10)
        frame_hollow.place(x=470, y=80)
        
        tk.Label(frame_hollow, text="Hollow",
                font=("Arial", 12, "bold"),
                bg="#16213e", fg="#e94560").pack()
        
        self.label_img_hollow = tk.Label(frame_hollow, bg="#16213e")
        self.label_img_hollow.pack()
        
        self.label_personaje_hollow = tk.Label(frame_hollow, text="",
                font=("Arial", 10), bg="#16213e", fg="white")
        self.label_personaje_hollow.pack()

        # Log de batalla
        self.log = tk.Text(self.root, height=8, width=70,
                          bg="#0f3460", fg="white",
                          font=("Arial", 10))
        self.log.place(x=10, y=400)

        # Botones
        tk.Button(self.root, text="⚔ ATACAR",
                 font=("Arial", 12, "bold"),
                 bg="#e94560", fg="white",
                 command=self.atacar).place(x=200, y=590)

        tk.Button(self.root, text="🔄 CAMBIAR",
                 font=("Arial", 12, "bold"),
                 bg="#16213e", fg="white",
                 command=self.cambiar_personaje).place(x=380, y=590)

        self.actualizar_info()

    def actualizar_info(self):
        p = self.personaje_jugador_activo
        self.label_personaje_jugador.config(
            text=f"{p.nombre}\nHP: {p.vida}/{p.vida_maxima}\nATK: {p.ataque} DEF: {p.defensa}")
        
        self.img_jugador = self.cargar_imagen(p.nombre, "izquierda")
        if self.img_jugador:
            self.label_img_jugador.config(image=self.img_jugador)
        else:
            self.label_img_jugador.config(text="🧍", font=("Arial", 60))

        h = self.personaje_hollow_activo
        self.label_personaje_hollow.config(
            text=f"{h.nombre}\nHP: {h.vida}/{h.vida_maxima}\nATK: {h.ataque} DEF: {h.defensa}")
        
        self.img_hollow = self.cargar_imagen(h.nombre, "derecha")
        if self.img_hollow:
            self.label_img_hollow.config(image=self.img_hollow)
        else:
            self.label_img_hollow.config(text="👾", font=("Arial", 60))

        self.label_puntaje.config(
            text=f"{self.jugador_nombre}: {self.puntaje_jugador} | Hollow: {self.puntaje_hollow}")

    def agregar_log(self, mensaje):
        self.log.insert(tk.END, mensaje + "\n")
        self.log.see(tk.END)

    def atacar(self):
        if self.turno != "jugador":
            return
        
        danio = self.personaje_jugador_activo.calcular_danio(self.personaje_hollow_activo)
        self.personaje_hollow_activo.recibir_danio(danio)
        self.agregar_log(f"{self.personaje_jugador_activo.nombre} ataca a {self.personaje_hollow_activo.nombre} por {danio} de daño!")
        
        if self.personaje_hollow_activo.ko:
            self.agregar_log(f"¡{self.personaje_hollow_activo.nombre} quedó KO!")
            self.personaje_jugador_activo.restaurar_vida()
            self.puntaje_jugador += 1
            self.agregar_log(f"¡{self.jugador_nombre} se adueñó de {self.personaje_hollow_activo.nombre}!")
            self.verificar_fin_batalla_hollow(0)
            return
        
        self.turno = "hollow"
        self.actualizar_info()
        self.root.after(1000, self.turno_hollow)

    def turno_hollow(self):
        accion = random.choice(["atacar", "cambiar"])
        disponibles = [p for p in self.personajes_hollow if not p.ko and p != self.personaje_hollow_activo]
        
        if accion == "cambiar" and not disponibles:
            accion = "atacar"
        
        if accion == "atacar":
            danio = self.personaje_hollow_activo.calcular_danio(self.personaje_jugador_activo)
            self.personaje_jugador_activo.recibir_danio(danio)
            self.agregar_log(f"Hollow: {self.personaje_hollow_activo.nombre} ataca a {self.personaje_jugador_activo.nombre} por {danio} de daño!")
            
            if self.personaje_jugador_activo.ko:
                self.agregar_log(f"¡{self.personaje_jugador_activo.nombre} quedó KO!")
                self.personaje_hollow_activo.restaurar_vida()
                self.puntaje_hollow += 1
                self.agregar_log(f"¡El Hollow se adueñó de {self.personaje_jugador_activo.nombre}!")
                self.verificar_fin_batalla_jugador(0)
                return
        else:
            self.personaje_hollow_activo = random.choice(disponibles)
            self.agregar_log(f"Hollow cambia a {self.personaje_hollow_activo.nombre}!")
        
        self.turno = "jugador"
        self.actualizar_info()

    def cambiar_personaje(self):
        disponibles = [p for p in self.personajes_jugador if not p.ko and p != self.personaje_jugador_activo]
        
        if not disponibles:
            messagebox.showwarning("Sin personajes", "No tenés otros personajes disponibles!")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Cambiar personaje")
        ventana.configure(bg="#1a1a2e")
        
        tk.Label(ventana, text="Elegí un personaje:",
                font=("Arial", 12),
                bg="#1a1a2e", fg="white").pack(pady=10)
        
        for personaje in disponibles:
            tk.Button(ventana,
                     text=f"{personaje.nombre} | HP: {personaje.vida} ATK: {personaje.ataque} DEF: {personaje.defensa}",
                     bg="#16213e", fg="white",
                     command=lambda p=personaje: self.confirmar_cambio(p, ventana)).pack(pady=5)

    def confirmar_cambio(self, personaje, ventana):
        self.personaje_jugador_activo = personaje
        self.agregar_log(f"{self.jugador_nombre} cambia a {personaje.nombre}!")
        ventana.destroy()
        self.turno = "hollow"
        self.actualizar_info()
        self.root.after(1000, self.turno_hollow)

    def verificar_fin_batalla_hollow(self, indice):
        # Recursividad: revisa si el hollow tiene algún personaje disponible
        if indice >= len(self.personajes_hollow):
            self.agregar_log("¡Derrotaste al Hollow!")
            messagebox.showinfo("Victoria!", "¡Ganaste la batalla!")
            self.callback_fin(self.indice_hollow)
            self.root.destroy()
            return
        
        if not self.personajes_hollow[indice].ko:
            self.personaje_hollow_activo = self.personajes_hollow[indice]
            self.agregar_log(f"Hollow envía a {self.personaje_hollow_activo.nombre}!")
            self.turno = "jugador"
            self.actualizar_info()
            return
        
        self.verificar_fin_batalla_hollow(indice + 1)

    def verificar_fin_batalla_jugador(self, indice):
        # Recursividad: revisa si el jugador tiene algún personaje disponible
        if indice >= len(self.personajes_jugador):
            self.agregar_log("¡Perdiste la batalla!")
            messagebox.showinfo("Derrota", "¡El Hollow te derrotó!")
            self.root.destroy()
            return
        
        if not self.personajes_jugador[indice].ko:
            self.personaje_jugador_activo = self.personajes_jugador[indice]
            self.agregar_log(f"¡{self.jugador_nombre} envía a {self.personaje_jugador_activo.nombre}!")
            self.turno = "jugador"
            self.actualizar_info()
            return
        
        self.verificar_fin_batalla_jugador(indice + 1)