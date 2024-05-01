# PALISSON Antoine

## Graph DFS
def graph_dfs(graph, start_node):
    visited = set()  # {} is an empty dictionary, not an empty set
    stack = [start_node]
    traversal = []

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            traversal.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited :
                    stack.extend(neighbor)

    return traversal

def graph_dfs_recursive(graph, current_node, visited = set(), traversal = []):
    traversal.append(current_node)
    visited.add(current_node)
    for node in graph[current_node]:
        if node not in visited:
            graph_dfs_recursive(graph, node, visited, traversal)
    return traversal

## Tree DFS
def graph_bfs(graph, start_node):
    visited = set()
    queue = [start_node]
    traversal = []

    while queue:
        node = queue.pop(0)

        if node not in visited:
            visited.add(node)
            traversal.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited :
                    queue.extend(neighbor)

    return traversal

## Dijkstra's Algorithm
import math

def dijkstra(graph, start):
    distances = {node: math.inf for node in graph}
    distances[start] = 0
    nodes = set(graph.keys())

    while nodes:
        # searching the unvisited node with the shortest distance
        min_node = None
        for node in nodes:
            if min_node is None or distances[node] < distances[min_node]:
                min_node = node
        if distances[min_node] == math.inf:
            break

        # finding the shortest path
        for neighbor, weight in graph[min_node]:
            new_distance = distances[min_node] + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

        nodes.remove(min_node)

    return distances

if __name__ == "__main__":
    graph = {
        'A': ['B', 'D'],
        'B': ['C', 'A'],
        'C': ['B'],
        'D': ['A', 'E', 'F'],
        'E': ['D', 'F'],
        'F': ['D', 'E']
    }
    print(f"DFS traversal      : {graph_dfs(graph, 'A')}")
    # print(f"DFS traversal (rec): {graph_dfs_recursive(graph, 'A')}")
    print(f"BFS traversal      : {graph_bfs(graph, 'A')}")

    graph = {
        'A': [('B',  5), ('C',  7), ('D',  15)],
        'B': [('A',  5), ('D',  8), ('F',  6)],
        'C': [('A',  7), ('E',  5)],
        'D': [('A',  15), ('B',  8), ('G',  4), ('E', 3)],
        'E': [('C',  5), ('D',  3), ('G',  10)],
        'F': [('B',  6), ('G',  9)],
        'G': [('D',  4), ('F',  9), ('E',  10)]
    }

    start = 'A'
    print(f"Shortest Path from '{start}' : {dijkstra(graph, start)}")