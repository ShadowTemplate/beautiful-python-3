import abc

from typing import Dict, Generator, List

NodeId = int
NodeValue = str


class Node:
    curr_id: NodeId = 0
    
    def __init__(self, value: NodeValue):
        self.node_id: NodeId = Node.curr_id
        self.value: NodeValue = value
        Node.curr_id += 1
        
    def __repr__(self):
        return "{}({})".format(self.value, self.node_id)


class Graph:
    
    def __init__(self):
        self.nodes: Dict[NodeId, Node] = {}
        self.adjacents: Dict[NodeId, List[NodeId]] = {}
        
    def add_node(self, node: Node) -> None:
        self.nodes[node.node_id] = node
        self.adjacents[node.node_id] = []

    def add_edge(self, node1: Node, node2: Node) -> None:
        assert node1.node_id in self.nodes and node2.node_id in self.nodes
        self.adjacents[node1.node_id].append(node2.node_id)
        self.adjacents[node2.node_id].append(node1.node_id)
        
    def get_adjacents(self, node: Node) -> List[Node]:
        return [self.nodes[i] for i in self.adjacents[node.node_id]]
    
    def __repr__(self):
        nodes_rep = ["{}: {}".format(n, self.adjacents[i]) 
                     for i, n in self.nodes.items()]
        return "Graph: {}".format("\n".join(nodes_rep))


class GraphIterator(abc.ABC):  # Iterator
    
    @abc.abstractmethod
    def get_next(self) -> Node:
        pass
    
    @abc.abstractmethod
    def is_done(self) -> bool:
        pass


class BFSIterator(GraphIterator):  # ConcreteIterator
    
    def __init__(self, graph: Graph, source: Node):
        self.graph: Graph = graph
        self.visited: Dict[NodeId, bool] = {
            i: False for i in graph.nodes.keys()}
        self.queue: List[NodeId] = [source.node_id]
    
    def get_next(self) -> Node:
        assert not self.is_done()
        
        if len(self.queue) == 0:
            # the BFS started from the source is over, but some nodes have not 
            # been visited yet (the graph is disconnected)
            
            # pick a random unvisited node
            unvisited = next(i for i, v in self.visited.items() if not v)
            # prepare a new BFS starting from it
            self.queue.append(unvisited)
        
        head_id = self.queue.pop(0)
        adj_ids = [n.node_id for n in 
                   self.graph.get_adjacents(self.graph.nodes[head_id])]
        self.queue.extend([i for i in adj_ids if not self.visited[i]])
        self.visited[head_id] = True
        return self.graph.nodes[head_id]
    
    def is_done(self) -> bool:
        return all(self.visited.values())


class DFSIterator(GraphIterator):  # ConcreteIterator
    
    def __init__(self, graph: Graph, source: Node):
        self.graph: Graph = graph
        self.visited: Dict[NodeId, bool] = {
            i: False for i in graph.nodes.keys()}
        self.source = source
        # this generator will perform a DFS starting from the source
        self.node_gen = self.get_next_helper(self.source)
    
    def get_next(self) -> Node:
        assert not self.is_done()
        
        for n in self.node_gen:
            return n
        
        # the DFS started from the source is over, but some nodes have not been
        # visited yet (the graph is disconnected)
        
        # pick a random unvisited node
        unvisited = next(i for i, v in self.visited.items() if not v)
        # prepare a new DFS starting from it
        self.node_gen = self.get_next_helper(self.graph.nodes[unvisited])
        return self.get_next()
    
    def get_next_helper(self, curr_node: Node) -> Generator[Node, None, None]:
        if self.visited[curr_node.node_id]:
            return
        
        self.visited[curr_node.node_id] = True
        yield curr_node
        for adj in self.graph.get_adjacents(curr_node):
            yield from self.get_next_helper(adj)
        
    def is_done(self) -> bool:
        return all(self.visited.values())


class GraphTraversal(abc.ABC):  # Aggregate
    
    @abc.abstractmethod
    def get_iterator(self) -> GraphIterator:
        pass


class BFSTraversal(GraphTraversal):  # ConcreteAggregate
    
    def __init__(self, graph: Graph, source: Node):
        self.graph = graph
        self.source = source
    
    def get_iterator(self) -> BFSIterator:
        return BFSIterator(self.graph, self.source)


class DFSTraversal(GraphTraversal):  # ConcreteAggregate
    
    def __init__(self, graph: Graph, source: Node):
        self.graph = graph
        self.source = source
    
    def get_iterator(self) -> DFSIterator:
        return DFSIterator(self.graph, self.source)


class GraphExplorer:  # Client
    
    def __init__(self, traversal: GraphTraversal):
        self.traversal = traversal
        
    def explore(self) -> None:
        it: GraphIterator = self.traversal.get_iterator()
        visited: List[str] = []
        while not it.is_done():
            visited.append(repr(it.get_next()))
        print("Traversal: {}".format(", ".join(visited)))


def main():
    graph = Graph()
    alex = Node("Alex")
    barbara, becky, bruce = Node("Barbara"), Node("Becky"), Node("Bruce")
    carl, charlotte, charles = Node("Carl"), Node("Charlotte"), Node("Charles")
    dafne = Node("Dafne")
    elizabeth = Node("Elizabeth")
    franz = Node("Franz")
    
    graph.add_node(alex)
    graph.add_node(barbara)
    graph.add_node(becky)
    graph.add_node(bruce)
    graph.add_node(carl)
    graph.add_node(charlotte)
    graph.add_node(charles)
    graph.add_node(dafne)
    graph.add_node(elizabeth)
    graph.add_node(franz)
    
    graph.add_edge(alex, barbara)
    graph.add_edge(alex, becky)
    graph.add_edge(alex, bruce)
    graph.add_edge(becky, carl)
    graph.add_edge(becky, charlotte)
    graph.add_edge(bruce, charles)
    graph.add_edge(charlotte, dafne)
    
    print(graph)
    # Graph: Alex(0): [1, 2, 3]
    # Barbara(1): [0]
    # Becky(2): [0, 4, 5]
    # Bruce(3): [0, 6]
    # Carl(4): [2]
    # Charlotte(5): [2, 7]
    # Charles(6): [3]
    # Dafne(7): [5]
    # Elizabeth(8): []
    # Franz(9): []
    
    # Alex ____ _______            Elizabeth
    #  |       \       \
    # Barbara  Becky  Bruce ____       Franz
    #          /  \             \ 
    #       Carl  Charlotte     Charles
    #              |
    #             Dafne

    traversal = BFSTraversal(graph, alex)
    graph_explorer = GraphExplorer(traversal)
    graph_explorer.explore()
    # Traversal: Alex(0), Barbara(1), Becky(2), Bruce(3), Carl(4), 
    # Charlotte(5), Charles(6), Dafne(7), Elizabeth(8), Franz(9)
    
    traversal = DFSTraversal(graph, alex)
    graph_explorer = GraphExplorer(traversal)
    graph_explorer.explore()
    # Traversal: Alex(0), Barbara(1), Becky(2), Carl(4), Charlotte(5), 
    # Dafne(7), Bruce(3), Charles(6), Elizabeth(8), Franz(9)
    

if __name__ == "__main__":
    main()
