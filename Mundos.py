import mysql.connector
import heapq

db= mysql.connector.connect(user='root', password='123456', host='localhost', database='', auth_plugin='mysql_native_password')
cursor = db.cursor()


class Graph:
    def __init__(self):
        self.graph = {}

    # Crear 
    def add_edge(self, node, neighbor, distance):
        if node not in self.graph:
            self.graph[node] = []
        self.graph[node].append((neighbor, distance))

    # Leer 
    def get_connections(self, node):
        return self.graph.get(node, [])

    # Actualizar 
    def update_edge(self, node, old_neighbor, new_neighbor, new_distance):
        if node in self.graph:
            for i, (neighbor, distance) in enumerate(self.graph[node]):
                if neighbor == old_neighbor:
                    self.graph[node][i] = (new_neighbor, new_distance)

    # Eliminar 
    def delete_node(self, node):
        if node in self.graph:
            del self.graph[node]
        for connections in self.graph.values():
            for neighbor, _ in connections:
                if neighbor == node:
                    connections.remove((neighbor, _))

    # Mostrar el grafo completo
    def display_graph(self):
        return self.graph

    # Implementación de Dijkstra para encontrar el camino más corto desde un nodo de inicio
    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        # Nodo anterior para reconstruir el camino
        previous_nodes = {node: None for node in self.graph}

        # Cola de prioridad (min-heap),
        queue = [(0, start)] 

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end:
                break

            for neighbor, weight in self.graph.get(current_node, []):
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        path = []
        current_node = end
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]
        path = path[::-1] 

        if distances[end] == float('inf'):
            return None, None

        return path, distances[end]

# Uso
g = Graph()
edges = [
    (0, 1, 4), (0, 2, 3),
    (1, 2, 8),
    (2, 3, 1),
    (3, 4, 5),
    (4, 5, 2),
    (5, 0, 3),
]

for node, neighbor, distance in edges:
    g.add_edge(node, neighbor, distance)

print("Grafo completo:", g.display_graph())

print("Conexiones de 0:", g.get_connections(0))

print("Conexiones de 2 (Ubicación 2):", g.get_connections(2))

print("Actualizando la distancia entre 0 y 2 a 15 ")
g.update_edge(0, 2, 2, 15)  
print("Después de actualizar una conexión:", g.display_graph())

print("Eliminando el nodo 5 ")
g.delete_node(5)
print("Después de eliminar nodo 5:", g.display_graph())

start_node = 0
end_node = 3
path, distance = g.dijkstra(start_node, end_node)

if path:
    print(f"Camino más corto de {start_node} a {end_node}: {path}")
    print(f"Distancia total: {distance}")
else:
    print(f"No hay un camino entre {start_node} y {end_node}.")
