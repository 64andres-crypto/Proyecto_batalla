# main.py
# Este es el archivo principal que une todas las pantallas
# Aquí se crea la ventana principal y se maneja la navegación entre pantallas

import tkinter as tk
from pantalla_inicio import PantallaInicio
from pantalla_mapa import PantallaMapa
from pantalla_batalla import PantallaBatalla

class Juego:
    def __init__(self):
        # Creamos la ventana principal de tkinter
        self.root = tk.Tk()
        self.root.title("Disney's Epic Adventure")
        
        # Datos del jugador que se llenan en la pantalla de inicio
        self.nombre_jugador = ""
        self.avatar = ""
        self.personajes_jugador = []
        
        # Empezamos con la pantalla de inicio
        self.mostrar_inicio()
        
        # Esto mantiene la ventana abierta
        self.root.mainloop()

    def mostrar_inicio(self):
        # Limpia la ventana y muestra la pantalla de inicio
        self.limpiar_ventana()
        PantallaInicio(self.root, self.iniciar_juego)

    def iniciar_juego(self, nombre, avatar, personajes):
        # Se llama cuando el jugador presiona INICIAR
        # Guarda los datos del jugador y muestra el mapa
        self.nombre_jugador = nombre
        self.avatar = avatar
        self.personajes_jugador = personajes
        self.mostrar_mapa()

    def mostrar_mapa(self):
        # Limpia la ventana y muestra el mapa
        self.limpiar_ventana()
        self.mapa = PantallaMapa(
            self.root,
            self.nombre_jugador,
            self.avatar,
            self.personajes_jugador,
            self.iniciar_batalla
        )

    def iniciar_batalla(self, indice_hollow, ubicaciones, callback_actualizar_mapa):
        ventana_batalla = tk.Toplevel(self.root)
        
        def fin_batalla(indice):
            # Marca el hollow como derrotado y actualiza el mapa
            ubicaciones[indice]["derrotado"] = True
            callback_actualizar_mapa()
        
        PantallaBatalla(
            ventana_batalla,
            self.nombre_jugador,
            self.personajes_jugador,
            indice_hollow,
            ubicaciones,
            fin_batalla
        )

    def limpiar_ventana(self):
        # Elimina todos los widgets de la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()

# Punto de entrada del programa
if __name__ == "__main__":
    Juego()