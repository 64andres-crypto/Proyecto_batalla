# pantalla_mapa.py
# Esta pantalla muestra el mapa con los 5 Hollows que el jugador debe derrotar
# El jugador solo puede moverse entre las 5 ubicaciones

import tkinter as tk
from tkinter import messagebox

class PantallaMapa:
    def __init__(self, root, nombre_jugador, avatar, personajes, callback_batalla):
        self.root = root
        self.root.title("Mapa - Disney's Epic Adventure")
        self.root.geometry("600x500")
        self.root.configure(bg="#1a1a2e")
        
        self.nombre_jugador = nombre_jugador
        self.avatar = avatar
        self.personajes = personajes
        self.callback_batalla = callback_batalla  # Función que abre la batalla
        
        # Las 5 ubicaciones con sus Hollows
        self.ubicaciones = [
    {"nombre": "Planeta Namek", "hollow": "Hollow de Diamante", "derrotado": False},
    {"nombre": "Final Fantasy", "hollow": "Hollow del Reino de Fuego", "derrotado": False},
    {"nombre": "Aldea de la Hoja", "hollow": "Hollow Ben 10", "derrotado": False},
    {"nombre": "Ciudad de Tokio", "hollow": "Hollow del Hambre", "derrotado": False},
    {"nombre": "Green Hill Zone", "hollow": "Hollow de la Noche", "derrotado": False},
]
        
        # El jugador empieza en la ubicación 0
        self.ubicacion_actual = 0
        
        self.construir_pantalla()

    def construir_pantalla(self):
        # Título
        tk.Label(self.root, text="Mapa del Reino", 
                font=("Arial", 20, "bold"),
                bg="#1a1a2e", fg="#e94560").pack(pady=15)

        # Info del jugador
        tk.Label(self.root, 
                text=f"Guardián: {self.nombre_jugador} | Avatar: {self.avatar}",
                font=("Arial", 11),
                bg="#1a1a2e", fg="white").pack()

        # Frame donde van los botones de ubicaciones
        self.frame_mapa = tk.Frame(self.root, bg="#1a1a2e")
        self.frame_mapa.pack(pady=20)

        self.botones = []
        for i, ubicacion in enumerate(self.ubicaciones):
            # Cada ubicación es un botón
            btn = tk.Button(self.frame_mapa,
                          text=f"{ubicacion['nombre']}\n{ubicacion['hollow']}",
                          font=("Arial", 10),
                          width=20, height=3,
                          bg="#16213e", fg="white",
                          command=lambda i=i: self.seleccionar_ubicacion(i))
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            self.botones.append(btn)

        self.actualizar_mapa()

    def actualizar_mapa(self):
        # Actualiza el color de los botones según el estado
        for i, ubicacion in enumerate(self.ubicaciones):
            if ubicacion["derrotado"]:
                # Verde si el hollow fue derrotado
                self.botones[i].configure(bg="#2d6a4f", text=f"{ubicacion['nombre']}\n✓ Derrotado")
            elif i == self.ubicacion_actual:
                # Rojo si es la ubicación actual
                self.botones[i].configure(bg="#e94560")
            else:
                self.botones[i].configure(bg="#16213e")

    def seleccionar_ubicacion(self, indice):
        # El jugador solo puede moverse a ubicaciones adyacentes
        if abs(indice - self.ubicacion_actual) > 1:
            messagebox.showwarning("Movimiento inválido", 
                                 "Solo podés moverte a ubicaciones adyacentes!")
            return
        
        self.ubicacion_actual = indice
        self.actualizar_mapa()
        
        # Si el hollow no fue derrotado pregunta si quiere batallar
        if not self.ubicaciones[indice]["derrotado"]:
            respuesta = messagebox.askyesno("Batalla!", 
                f"¿Querés enfrentarte al {self.ubicaciones[indice]['hollow']}?")
            if respuesta:
                self.callback_batalla(indice, self.ubicaciones, self.actualizar_mapa)

    def marcar_derrotado(self, indice):
        # Marca el hollow como derrotado y actualiza el mapa
        self.ubicaciones[indice]["derrotado"] = True
        self.actualizar_mapa()
        
        # Verifica si ganó el juego
        if all(u["derrotado"] for u in self.ubicaciones):
            messagebox.showinfo("Victoria!", 
                "¡Derrotaste a todos los Hollows!\n¡Restauraste las historias!")