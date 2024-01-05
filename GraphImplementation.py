import math

class Graph:
    def __init__(self, directed : bool):
        self._is_directed = directed
        self._structure = {}
        self._is_floyded = False
        self._floyd_distances = {}
        self._floyd_predecessors = {}

    def add_node(self, node):
        if node not in self._structure.keys():
            self._is_floyded = False
            self._structure[node] = []
    
    def add_edge(self, edge):
        source, target, weight = edge
        self._is_floyded = False
        self.add_node(source)
        self.add_node(target)
        if source == target:
            raise ValueError("pętle są zabronione")
        if (target, weight) not in self._structure[source]:
            self._structure[source].append((target, weight))
        if not self._is_directed and (source, weight) not in self._structure[target]:
            self._structure[target].append((source, weight))
        
    def list_nodes(self):
        return self._structure.keys()

    def list_edges(self):
        L = []
        for source in self._structure:
            for (target, weight) in self._structure[source]:
                L.append((source, target, weight))
        return L
    
    def print_graph(self):
        L = []
        for source in self._structure:
            L.append("{} : ".format(source))
            for (target, weight) in self._structure[source]:
                L.append("{}({}) ".format(target, weight))
            L.append("\n")
        print("".join(L))
    
    def get_weight(self, v1, v2):
        for (v, weight) in self._structure[v1]:
            if v == v2:
                return weight
        return None
    
    def _floyd(self):
        self._floyd_distances = {}
        self._floyd_predecessors = {}

        for v1 in self.list_nodes():
            for v2 in self.list_nodes():
                self._floyd_distances[(v1, v2)] = math.inf
                self._floyd_predecessors[(v1, v2)] = None
            self._floyd_distances[(v1, v1)] = 0
            self._floyd_predecessors[(v1, v1)] = v1
        
        for edge in self.list_edges():
            source, target, weight = edge
            self._floyd_distances[(source, target)] = weight
            self._floyd_predecessors[(source, target)] = source
        
        for u in self.list_nodes():
            for v1 in self.list_nodes():
                for v2 in self.list_nodes():
                    if self._floyd_distances[(v1, v2)] > self._floyd_distances[(v1, u)] + self._floyd_distances[(u, v2)]:
                        self._floyd_distances[(v1, v2)] = self._floyd_distances[(v1, u)] + self._floyd_distances[(u, v2)]
                        if self._floyd_distances[(v2, v2)] < 0:
                            raise ValueError("Wykryto cykl ujemny")
                        self._floyd_predecessors[(v1, v2)] = self._floyd_predecessors[(u, v2)]

        self._is_floyded = True
    
    def floyd_distance(self, source, target):
        if not self._is_floyded:
            self._floyd()

        if self._floyd_distances[(source, target)] != math.inf:
            return self._floyd_distances[(source, target)]
        raise ValueError("Dana ścieżka nie istnieje")
    
    def floyd_path(self, source, target):
        if not self._is_floyded:
            self._floyd()

        if self._floyd_predecessors[(source, target)] == None:
            raise ValueError("Dana ścieżka nie istnieje")
        path = []
        while source != target:
            u = self._floyd_predecessors[(source, target)]
            path.insert(0, (u, target, self.get_weight(u, target)))
            target = u
        return path