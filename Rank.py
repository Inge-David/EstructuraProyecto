import mysql.connector
import Jugador

# Conexión a la base de datos MySQL
db = mysql.connector.connect(user='root', password='123456', host='localhost', database='juego', auth_plugin='mysql_native_password')
cursor = db.cursor()

class Ranking:
    def __init__(self, id_jugador, puntuacion, posicion):
        self.id_jugador = id_jugador
        self.puntuacion = puntuacion
        self.posicion = posicion

    def __str__(self):
        return f"Jugador {self.id_jugador} | Puntuación: {self.puntuacion} | Posición: {self.posición}"

# Busca un Ranking por id de Jugador
def load_from_db(jugador_id):
        cursor.execute('SELECT * FROM ranking Where id_jugador = %s', (jugador_id,))
        return cursor.fetchone()

# Guardar ranking en la BD
def save_to_db(rank):
        cursor.execute('INSERT INTO ranking (id_jugador, puntuacion, posicion) VALUES (%s, %s, %s)',
                       (rank.id_jugador, rank.puntuacion, rank.posicion))
        result = db.commit()
        print(result)

# Actualiza ranking en la BD
def update_to_db(rank):
        cursor.execute('UPDATE ranking SET puntuacion = %s, posicion = %s WHERE id_jugador = %s',
                       (rank.puntuacion, rank.posicion, rank.id_jugador))
        result = db.commit()
        print(result)

# Muestra el ranking ordenado de mayor puntaje a menor puntaje
def load_ranking():
        cursor.execute('SELECT id_jugador, puntuacion FROM ranking ORDER BY puntuacion DESC LIMIT 10')
        result = cursor.fetchall()
        print("Ranking de Jugadores")
        for fila in result:
            jugador = Jugador.load_from_db(fila[0])
            print("Jugador: ", jugador[1], " Puntaje: ", fila[1])
