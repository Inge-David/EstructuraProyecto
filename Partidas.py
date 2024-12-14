import mysql.connector
from datetime import datetime
import json


db = mysql.connector.connect(user='root', password='123456', host='localhost', database='juego', auth_plugin='mysql_native_password')
cursor = db.cursor()

class Partida:
    def __init__(self, id_partida, fecha, jugadores, puntajes):
        self.id_partida = id_partida
        self.fecha = fecha
        self.jugadores = jugadores
        self.puntajes = puntajes

    def __str__(self):
        return f"Partida {self.id_partida} | Fecha: {self.fecha} | Jugadores: {self.jugadores} | Puntajes: {self.puntajes}"

   
    def guardar_en_db(self):
        query = """
        INSERT INTO partidas (fecha, equipo1, equipo2, resultado)
        VALUES (%s, %s, %s, %s)
        """
        equipo1 = ', '.join(self.jugadores[:len(self.jugadores)//2])
        equipo2 = ', '.join(self.jugadores[len(self.jugadores)//2:])
        resultado = json.dumps(self.puntajes) 
        cursor.execute(query, (self.fecha, equipo1, equipo2, resultado))
        db.commit()
        self.id_partida = cursor.lastrowid 

   
    @classmethod
    def cargar_de_db(cls, id_partida):
        query = "SELECT id, fecha, equipo1, equipo2, resultado FROM partidas WHERE id = %s"
        cursor.execute(query, (id_partida,))
        result = cursor.fetchone()
        if result:
            fecha = result[1]
            equipo1 = result[2].split(", ")
            equipo2 = result[3].split(", ")
            resultado = json.loads(result[4]) 
            return cls(result[0], fecha, equipo1 + equipo2, resultado)
        return None

    @classmethod
    def listar_partidas_por_fechas(cls, fecha_inicio, fecha_fin):
        query = "SELECT id, fecha, equipo1, equipo2, resultado FROM partidas WHERE fecha BETWEEN %s AND %s ORDER BY fecha"
        cursor.execute(query, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        partidas = []
        for result in resultados:
            fecha = result[1]
            equipo1 = result[2].split(", ")
            equipo2 = result[3].split(", ")
            resultado = json.loads(result[4])   
            partidas.append(cls(result[0], fecha, equipo1 + equipo2, resultado))
        return partidas





fecha_inicio = datetime(2023, 2, 1)
fecha_fin = datetime(2023, 4, 1)

partidas_rango = Partida.listar_partidas_por_fechas(fecha_inicio, fecha_fin)

print(f"Partidas jugadas entre {fecha_inicio} y {fecha_fin}:")
for partida in partidas_rango:
    print(partida)


db.close()


