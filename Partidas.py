import mysql.connector
from datetime import datetime

db= mysql.connector.connect(user='root', password='123456', host='localhost', database='', auth_plugin='mysql_native_password')
cursor = db.cursor()

class Partida:
    def __init__(self, id_partida, fecha, jugadores, puntajes):
        self.id_partida = id_partida
        self.fecha = fecha 
        self.jugadores = jugadores
        self.puntajes = puntajes

    def __str__(self):
        return f"Partida {self.id_partida} | Fecha: {self.fecha} | Jugadores: {self.jugadores} | Puntajes: {self.puntajes}"


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
partida1 = Partida(1, datetime(2023, 1, 5, 14, 30), ['Juan', 'Pedro'], {'Juan': 10, 'Pedro': 20})
partida2 = Partida(2, datetime(2023, 2, 10, 16, 45), ['Maria', 'Luis'], {'Maria': 15, 'Luis': 18})
partida3 = Partida(3, datetime(2023, 3, 20, 12, 30), ['Carlos', 'Ana'], {'Carlos': 25, 'Ana': 22})
partida4 = Partida(4, datetime(2023, 4, 5, 9, 0), ['Luis', 'Juan'], {'Luis': 20, 'Juan': 15})

arbol.insertar(partida1)
arbol.insertar(partida2)
arbol.insertar(partida3)
arbol.insertar(partida4)

fecha_inicio = datetime(2023, 2, 1)
fecha_fin = datetime(2023, 4, 1)

partidas_rango = arbol.listar_partidas_por_fechas(fecha_inicio, fecha_fin)

print(f"Partidas jugadas entre {fecha_inicio} y {fecha_fin}:")
for partida in partidas_rango:
    print(partida)
