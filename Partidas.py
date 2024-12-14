import mysql.connector
from datetime import datetime


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
        resultado = str(self.puntajes)  
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
            resultado = eval(result[4])  
            return cls(result[0], fecha, equipo1 + equipo2, resultado)
        return None

class Nodo:
    def __init__(self, partida):
        self.partida = partida
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, partida):
        nuevo_nodo = Nodo(partida)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)

    def _insertar_recursivo(self, nodo_actual, nuevo_nodo):
        if nuevo_nodo.partida.fecha < nodo_actual.partida.fecha:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nuevo_nodo
            else:
                self._insertar_recursivo(nodo_actual.izquierda, nuevo_nodo)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nuevo_nodo
            else:
                self._insertar_recursivo(nodo_actual.derecha, nuevo_nodo)

    def listar_partidas_por_fechas(self, fecha_inicio, fecha_fin):
        partidas_rango = []
        self._listar_partidas_por_fechas_recursivo(self.raiz, fecha_inicio, fecha_fin, partidas_rango)
        return partidas_rango
    
    def _listar_partidas_por_fechas_recursivo(self, nodo, fecha_inicio, fecha_fin, partidas_rango):
        if nodo is not None:
            if fecha_inicio <= nodo.partida.fecha <= fecha_fin:
                partidas_rango.append(nodo.partida)

            if nodo.partida.fecha > fecha_inicio:
                self._listar_partidas_por_fechas_recursivo(nodo.izquierda, fecha_inicio, fecha_fin, partidas_rango)
                
            if nodo.partida.fecha < fecha_fin:
                self._listar_partidas_por_fechas_recursivo(nodo.derecha, fecha_inicio, fecha_fin, partidas_rango)


arbol = ArbolBinario()


partida1 = Partida(None, datetime(2023, 1, 5, 14, 30), ['Juan', 'Pedro', 'Maria'], {'Juan': 10, 'Pedro': 20, 'Maria': 15})
partida2 = Partida(None, datetime(2023, 2, 10, 16, 45), ['Maria', 'Luis'], {'Maria': 15, 'Luis': 18})
partida3 = Partida(None, datetime(2023, 3, 20, 12, 30), ['Carlos', 'Ana'], {'Carlos': 25, 'Ana': 22})
partida4 = Partida(None, datetime(2023, 4, 5, 9, 0), ['Luis', 'Juan'], {'Luis': 20, 'Juan': 15})

partida1.guardar_en_db()
partida2.guardar_en_db()
partida3.guardar_en_db()
partida4.guardar_en_db()

partida1_db = Partida.cargar_de_db(partida1.id_partida)
partida2_db = Partida.cargar_de_db(partida2.id_partida)
partida3_db = Partida.cargar_de_db(partida3.id_partida)
partida4_db = Partida.cargar_de_db(partida4.id_partida)

arbol.insertar(partida1_db)
arbol.insertar(partida2_db)
arbol.insertar(partida3_db)
arbol.insertar(partida4_db)

# Definir el rango de fechas para consultar las partidas
fecha_inicio = datetime(2023, 2, 1)
fecha_fin = datetime(2023, 4, 1)

# Listar las partidas que están dentro del rango de fechas
partidas_rango = arbol.listar_partidas_por_fechas(fecha_inicio, fecha_fin)

print(f"Partidas jugadas entre {fecha_inicio} y {fecha_fin}:")
for partida in partidas_rango:
    print(partida)

db.close()
