# pantalla_inicio.py
# Esta pantalla es la primera que ve el jugador, aquí ingresa su nombre,
# elige 3 personajes y selecciona su avatar

import tkinter as tk
from tkinter import messagebox
from modelos import cargar_personajes

class PantallaInicio:
    def __init__(self, root, callback_iniciar):
        # root es la ventana principal de tkinter
        # callback_iniciar es la función que se llama cuando el jugador presiona INICIAR
        self.root = root
        self.root.title("Disney's Epic Adventure")
        self.root.geometry("600x700")
        self.root.configure(bg="#1a1a2e")
        self.callback_iniciar = callback_iniciar
        
        # Cargamos los personajes del archivo de texto
        self.todos_personajes = cargar_personajes()
        
        # Lista para guardar los personajes seleccionados
        self.seleccionados = []
        
        # Variable para el avatar seleccionado
        self.avatar_var = tk.StringVar(value="Guardián")
        
        self.construir_pantalla()

    def construir_pantalla(self):
        # Título del juego
        tk.Label(self.root, text="Disney's Epic Adventure", 
                font=("Arial", 24, "bold"), 
                bg="#1a1a2e", fg="#e94560").pack(pady=20)

        # Campo para ingresar el nombre
        tk.Label(self.root, text="Ingresá tu nombre:", 
                font=("Arial", 12), 
                bg="#1a1a2e", fg="white").pack()
        
        self.entrada_nombre = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.entrada_nombre.pack(pady=10)

        # Selección de avatar
        tk.Label(self.root, text="Elegí tu avatar:", 
                font=("Arial", 12), 
                bg="#1a1a2e", fg="white").pack()
        
        avatares = ["Guardián", "Explorador", "Héroe"]
        for avatar in avatares:
            tk.Radiobutton(self.root, text=avatar, 
                          variable=self.avatar_var, value=avatar,
                          bg="#1a1a2e", fg="white", 
                          selectcolor="#e94560").pack()

        # Lista de personajes para elegir
        tk.Label(self.root, text="Elegí 3 personajes:", 
                font=("Arial", 12), 
                bg="#1a1a2e", fg="white").pack(pady=10)

        # Frame con scroll para la lista de personajes
        frame_lista = tk.Frame(self.root, bg="#1a1a2e")
        frame_lista.pack()

        self.vars_personajes = []
        for personaje in self.todos_personajes:
            var = tk.BooleanVar()
            self.vars_personajes.append((var, personaje))
            tk.Checkbutton(frame_lista, 
                          text=f"{personaje.nombre} | {personaje.rol} | HP:{personaje.vida} ATK:{personaje.ataque} DEF:{personaje.defensa}",
                          variable=var,
                          bg="#1a1a2e", fg="white",
                          selectcolor="#e94560",
                          command=self.verificar_seleccion).pack(anchor="w")

        # Botones de INICIAR y ABOUT
        frame_botones = tk.Frame(self.root, bg="#1a1a2e")
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="INICIAR", 
                 font=("Arial", 14, "bold"),
                 bg="#e94560", fg="white",
                 command=self.iniciar_juego).pack(side="left", padx=10)

        tk.Button(frame_botones, text="ABOUT", 
                 font=("Arial", 14, "bold"),
                 bg="#16213e", fg="white",
                 command=self.mostrar_about).pack(side="left", padx=10)

    def verificar_seleccion(self):
        # Si ya seleccionó 3 personajes, desactiva los demás
        seleccionados = [var for var, p in self.vars_personajes if var.get()]
        if len(seleccionados) > 3:
            # Si intenta seleccionar más de 3 lo avisa
            messagebox.showwarning("Límite", "Solo podés elegir 3 personajes!")
            # Desmarca el último seleccionado
            seleccionados[-1].set(False)

    def iniciar_juego(self):
        # Verifica que el nombre no esté vacío
        nombre = self.entrada_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Ingresá tu nombre!")
            return

        # Verifica que haya elegido exactamente 3 personajes
        self.seleccionados = [p for var, p in self.vars_personajes if var.get()]
        if len(self.seleccionados) != 3:
            messagebox.showerror("Error", "Debés elegir exactamente 3 personajes!")
            return

        # Si todo está bien llama al callback con los datos del jugador
        self.callback_iniciar(nombre, self.avatar_var.get(), self.seleccionados)

    def mostrar_about(self):
        # Muestra información del proyecto
        messagebox.showinfo("About", 
            "Disney's Epic Adventure\n\nProyecto: Imaginary Battle\nCurso: Programación\nDesarrollado con Python y Tkinter")