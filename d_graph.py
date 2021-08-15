# Course: CS261 - Data Structures
# Author: Alexander Shen
# Assignment: 6
# Description: Replicate the data structure of a directed graph.

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        # Add 1 to the vertex counter.
        self.v_count += 1

        # If the matrix is empty put an empty list in it.
        if self.v_count == 1:
            self.adj_matrix.append([])
        else:
            # Add a new list to the matrix and fill it in with 0 according to the amount of verticies.
            self.adj_matrix.append([0 for num in range(self.v_count - 1)])

        # For every exisiting row, add an extra 0 to the end.
        for vertex in range(0, self.v_count):
            self.adj_matrix[vertex].append(0)
        
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        # Check if the weight is negative, the src and dst are valid, and if the src and dst are the same.
        # If they are then do nothing, else update the matrix with the weight.
        if weight < 0:
            return
        if src < 0 or src > len(self.adj_matrix) - 1:
            return
        if dst < 0 or dst > len(self.adj_matrix) - 1:
            return
        if src == dst:
            return
        
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        # Check if the src and dst are valid, and if the src and dst are the same.
        # If they are then do nothing, else update the matrix with the weight to 0.
        if src < 0 or src > len(self.adj_matrix) - 1:
            return
        if dst < 0 or dst > len(self.adj_matrix) - 1:
            return
        if src == dst:
            return
        
        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        # return a list with vertices.
        new_list = []
        for num in range(self.v_count):
            new_list.append(num)

        return new_list

    def get_edges(self) -> []:
        # Iterate through all the matrices and only append to the new list when the element is not 0.
        new_list = []
        row = 0
        for rows in self.adj_matrix:
            col = 0
            for elements in rows:
                if elements != 0:
                    new_list.append((row, col, elements))
                col += 1
            row += 1
        return new_list

    def is_valid_path(self, path: []) -> bool:
        # If the path is empty then return True.
        if path == []:
            return True

        index = 1
        for key in path:
            # If the key is invalid, then return False.
            if key < 0 or key > len(self.adj_matrix) - 1:
                return False

            # If We have reached the end, return True.
            if key == path[len(path) - 1] and index == len(path):
                return True

            # If the next key is invalid, then return False.
            next = path[index]
            if next < 0 or next > len(self.adj_matrix) - 1:
                return False
            
            # If there is no weight for the next spot, then return False.
            if self.adj_matrix[key][next] == 0:
                return False

            index += 1

    """ The following DFS and BFS are the exact same as the undirected graph, only accounting for the matrix"""
    def dfs_helper(self, curr, end, already):
        if curr == end:
            return

        if curr not in already:
            already.append(curr)

            curr_list = self.adj_matrix[curr]
            list_size = len(curr_list)
            for vertex in range(list_size):
                if self.adj_matrix[curr][vertex] != 0:
                    self.dfs_helper(vertex, end, already)

    def dfs(self, v_start, v_end=None) -> []:
        if v_start < 0 or v_start > len(self.adj_matrix) - 1:
            return []

        visit = []
        self.dfs_helper(v_start, v_end, visit)
        return visit


    def bfs(self, v_start, v_end=None) -> []:
        if v_start < 0 or v_start > len(self.adj_matrix) - 1:
            return []

        visit = []
        queue = []
        final = []

        queue.append(v_start)
        visit.append(v_start)

        while queue:
            value = queue.pop(0)
            final.append(value)

            cur_list = self.adj_matrix[value]
            list_size = len(cur_list)
            for vertex in range(list_size):
                if self.adj_matrix[value][vertex] != 0:
                    if vertex not in visit:
                        visit.append(vertex)
                        queue.append(vertex)

        if v_end is not None:
            if v_end not in final:
                return final
            else:
                for num in range(len(final) - 1, -1, -1):
                    if final[num] != v_end:
                        final.pop()
                    else:
                        return final
        else:
            return final
            
    """ 
    Is the same exact as the undirected graph, but instead of tracking the parent vertex we have a stack to keep 
    track of the vertices in the recursion. Since the directed graph has directions and cannot loop back.
    
    """
    def has_cycle_helper(self, curr, track, already):
        if curr not in already:
            already.append(curr)
        
        track.append(curr)

        curr_list = self.adj_matrix[curr]
        list_size = len(curr_list)

        for num in range(list_size):
            if self.adj_matrix[curr][num] != 0:
                if num not in already:
                    if self.has_cycle_helper(num, track, already):
                        return True
                elif num in track:
                    return True

        track.remove(curr)
        return False

    def has_cycle(self):
        visit = []
        track = []
        vertices = self.get_vertices()

        for vertex in vertices:
            if vertex not in visit:
                if self.has_cycle_helper(vertex, track, visit):
                    return True
        return False


    def dijkstra(self, src: int) -> []:
        # Fill in a list of distanced where every vertices has the work inf and the current source is 0
        new_list = [float('inf') for vertex in range(len(self.adj_matrix))]
        new_list[src] = 0

        # Load a heap tuple with (DISTANCE, SOURCE)
        heap_list = [(0, src)]

        while len(heap_list) > 0:
            # Pop the tutple and get the distance and the vertex
            distance, vertex = heapq.heappop(heap_list)

            # If the current distance is less than or equal to the value in the new_list, then check for paths.
            if distance <= new_list[vertex]:
                
                # Get the list of adj vertices
                curr_list = self.adj_matrix[vertex]
                list_size = len(curr_list)

                # Iterate through adj vertices that have weights.
                # Add the weight by the current path.
                for num in range(list_size):
                    weight = self.adj_matrix[vertex][num]
                    if weight != 0:
                        total_distance = distance + weight

                        # If the new updated distance is greater than the distance in new_list update, update it in new_list and push this back into the heap.
                        # else ignore the update.
                        if total_distance < new_list[num]:
                            new_list[num] = total_distance
                            heapq.heappush(heap_list, (total_distance, num))
    
        return new_list


if __name__ == '__main__':
    
    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)
    
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    
    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
