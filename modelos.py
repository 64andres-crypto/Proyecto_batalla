# modelos.py
# Este archivo contiene la clase Personaje que representa a cada personaje del juego

class Personaje:
    def __init__(self, nombre, pelicula, rol, vida, ataque, defensa):
        # Atributos básicos del personaje
        self.nombre = nombre
        self.pelicula = pelicula
        self.rol = rol
        self.vida_maxima = vida      # Vida máxima para poder restaurarla después
        self.vida = vida             # Vida actual
        self.ataque = ataque
        self.defensa = defensa
        self.ko = False              # Si está en KO no puede pelear

    def recibir_danio(self, danio):
        # Resta el daño recibido a la vida actual
        self.vida -= danio
        if self.vida <= 0:
            self.vida = 0
            self.ko = True           # Si la vida llega a 0 el personaje queda KO

    def calcular_danio(self, defensor):
        # Fórmula del daño: ATK atacante - DEF defensor, mínimo 1
        danio = self.ataque - defensor.defensa
        if danio < 1:
            danio = 1                # Daño mínimo siempre es 1
        return danio

    def restaurar_vida(self):
        # Restaura la vida al máximo cuando un entrenador se adueña del personaje
        self.vida = self.vida_maxima
        self.ko = False

    def __str__(self):
        # Para imprimir el personaje de forma legible
        return f"{self.nombre} | HP: {self.vida}/{self.vida_maxima} | ATK: {self.ataque} | DEF: {self.defensa}"


def cargar_personajes(archivo="personajes.txt"):
    # Lee el archivo de texto y crea objetos Personaje por cada línea
    personajes = []
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()         # Elimina espacios y saltos de línea
            if linea:                      # Ignora líneas vacías
                datos = linea.split(",")  # Separa por comas
                nombre = datos[0]
                pelicula = datos[1]
                rol = datos[2]
                vida = int(datos[3])
                ataque = int(datos[4])
                defensa = int(datos[5])
                personajes.append(Personaje(nombre, pelicula, rol, vida, ataque, defensa))
    return personajes