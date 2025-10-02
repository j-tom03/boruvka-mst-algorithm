## Graph implementation class

class Graph:
    def __init__(self, vertices: list, edges: list) -> None:
        """Constructor for a Graph object

        Args:
            vertices (list): list of integer values, naming each vertex
            edges (list): list of tuples representing edges between vertices [(v1,u1,w1), (v2,u2,w2), ..., (vn,un,wn)]
        """
        # setting the variables for the object
        self.vertices = vertices
        self.edges = edges
        self.edge_dict = {v: [] for v in vertices}
        for a,b,w in edges:
            # creating an edge dictionary for quick access
            self.edge_dict[a] += [(b,w)]
            self.edge_dict[b] += [(a,w)]
            
    def get_vertices(self) -> list:
        """Get method for vertices"""
        return self.vertices
    
    def get_edges(self) -> list:
        """Get method for edges"""
        return self.edges
    
    def get_edge_dict(self) -> dict:
        """Get method for the edge dictionary"""
        return self.edge_dict
    
    def get_neighbours(self, vertex: int) -> list:
        """Get method for neighbours of a vertex"""
        return self.get_edge_dict()[vertex]
    
    def get_total_weight(self) -> float:
        """Get method for the total weight of the graph"""
        return sum(x[2] for x in self.edges)
    
    @staticmethod
    def tiebreak(v1: int, v2: int) -> int:
        """Static method favouring the vertex of the lower number"""
        if v1 > v2:
            return v2
        else:
            return v1
    
    def get_min_edge_from_to(self, vertex: int, others: list) -> tuple:
        """Gets the minimum edge linking the vertex to any vertex in the list

        Args:
            vertex (int): vertex to be searched for
            others (list): list of other vertexes in the search space

        Raises:
            Exception: if there are no neighbours from that vertex

        Returns:
            tuple: the minimum edge from the vertex to any vertex in the list
        """
        neighbours = self.get_neighbours(vertex)
        neighbours = [x for x in neighbours if x[0] in others]
        # edge case of the vertex having no neighbours
        if len(neighbours)==0:
            raise Exception("No neighbours from edge")
        # setting a minimum from the first value
        min_v1, min_w = neighbours[0]
        # iterating neighbours
        for v1, w in neighbours[1:]:
            if w == min_w:
                # resolving tiebreaks 
                min_v1 = self.tiebreak(min_v1, v1)
            elif w < min_w:
                min_v1, min_w = v1, w
            else:
                pass
        # returning the minimum edge tuple
        return (vertex, min_v1, min_w)
    
    def add_edge(self, edge: tuple) -> None:
        """Adds the edge to the graph
        Useful for using a loop to define a graph or for adding edges to an MST

        Args:
            edge (tuple): the edge to be added
        """
        a, b, w = edge
        # stopping directed edges
        if (b,a,w) not in self.edges:
            # adding the edge
            self.edges += [edge]
            self.edge_dict[a] += [(b,w)]
            self.edge_dict[b] += [(a,w)]