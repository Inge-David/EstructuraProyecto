import mysql.connector
import json

# Conexión a la base de datos MySQL
db = mysql.connector.connect(user='root', password='123456', host='localhost', database='juego', auth_plugin='mysql_native_password')
cursor = db.cursor()

class Jugador:
    def __init__(self, id_jugador, nombre, nivel, puntuacion, equipo, inventario):
        self.id_jugador = id_jugador
        self.nombre = nombre
        self.nivel = nivel 
        self.puntuacion = puntuacion
        self.equipo = equipo
        self.inventario = inventario

    def __str__(self):
        return f"Jugador {self.nombre} | nivel: {self.nivel} | puntuacion: {self.puntuacion} | equipo: {self.equipo}| inventario: {self.inventario}"


# Busca un jugador por id
def load_from_db(jugador_id):
        cursor.execute('SELECT * FROM jugadores WHERE id = %s', (jugador_id,))
        return cursor.fetchone()

# Guardar jugador en la BD
def save_to_db(jugador):
        cursor.execute('INSERT INTO jugadores (nombre, nivel, puntuacion, equipo, inventario) VALUES (%s, %s, %s, %s, %s)',
                       (jugador.nombre, jugador.nivel, jugador.puntuacion, jugador.equipo, json.dumps(jugador.inventario)))
        return db.commit()


# player1 = Jugador(1,"Juan",12, 200, "Equipo A",  {"Espada":"espada comun"})
# player2 = Jugador(2,"Maria",20, 500, "Equipo D",  {"Arco":"arco largo"})

# save_to_db(player2)
# save_to_db(player2)

# load_from_db(1)
