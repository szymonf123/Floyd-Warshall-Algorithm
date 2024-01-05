import unittest
from io import StringIO
import sys
from GraphImplementation import Graph

class TestDirectedGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directed_graph1 = Graph(True)
        cls.directed_graph2 = Graph(True)
        for e in (("A", "B", 1), ("B", "D", 1), ("A", "C", 18), ("C", "E", 7), ("A", "D", 3), ("D", "E", 1), ("E", "C", 7)):
            cls.directed_graph1.add_edge(e)
            cls.directed_graph2.add_edge(e)
        cls.directed_graph2.add_edge(("A", "F", 1))
        cls.directed_graph2.add_edge(("F", "C", -2))
        
        cls.directed_graph3 = Graph(True)
        for ch in ("A", "B", "C", "D", "E", "Z"):
            cls.directed_graph3.add_node(ch)
    
    def setUp(self):
        pass

    def test_add_node(self):
        self.assertEqual(self.directed_graph3._structure, {"A" : [], "B" : [], "C" : [], "D" : [], "E" : [], "Z" : []})

    def test_add_edge(self):
        self.assertEqual(self.directed_graph1._structure, {"A": [("B", 1), ("C", 18), ("D", 3)], "B": [("D", 1)], "D": [("E", 1)], "C": [("E", 7)], "E": [("C", 7)]})
    
    def test_list_nodes(self):
        self.assertEqual(self.directed_graph1.list_nodes(), {"A" : [], "B" : [], "C" : [], "D" : [], "E" : []}.keys())
        self.assertEqual(self.directed_graph3.list_nodes(), {"A" : [], "B" : [], "C" : [], "D" : [], "E" : [], "Z" : []}.keys())
    
    def test_list_edges(self):
        self.assertEqual(set(self.directed_graph1.list_edges()), set([("A", "B", 1), ("A", "C", 18), ("A", "D", 3), ("B", "D", 1), ("D", "E", 1), ("C", "E", 7), ("E", "C", 7)]))
        self.assertEqual(set(self.directed_graph3.list_edges()), set())
    
    def test_print_graph(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.directed_graph1.print_graph()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "A : B(1) C(18) D(3) \nB : D(1) \nD : E(1) \nC : E(7) \nE : C(7)")

        captured_output = StringIO()
        sys.stdout = captured_output
        self.directed_graph3.print_graph()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "A : \nB : \nC : \nD : \nE : \nZ :")
    
    def test_floyd_distance(self):
        self.assertEqual(self.directed_graph1.floyd_distance("A", "D"), 2)
        self.assertEqual(self.directed_graph1.floyd_distance("A", "C"), 10)
        self.assertEqual(self.directed_graph2.floyd_distance("A", "C"), -1)

        with self.assertRaises(ValueError):
            self.directed_graph1.floyd_distance("D", "A")
    
    def test_floyd_path(self):
        self.assertEqual(self.directed_graph1.floyd_path("A", "D"), [("A", "B", 1), ("B", "D", 1)])
        self.assertEqual(self.directed_graph1.floyd_path("A", "C"), [("A", "B", 1), ("B", "D", 1), ("D", "E", 1), ("E", "C", 7)])
        self.assertEqual(self.directed_graph2.floyd_path("A", "C"), [("A", "F", 1), ("F", "C", -2)])

        with self.assertRaises(ValueError):
            self.directed_graph1.floyd_path("D", "A")


class TestUndirectedGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directed_graph1 = Graph(False)
        cls.directed_graph2 = Graph(False)
        for e in (("A", "B", 1), ("B", "D", 1), ("A", "C", 18), ("C", "E", 7), ("A", "D", 3), ("D", "E", 1)):
            cls.directed_graph1.add_edge(e)
            cls.directed_graph2.add_edge(e)
        cls.directed_graph2.add_edge(("A", "F", 1))
        cls.directed_graph2.add_edge(("F", "C", -2))
        
        cls.directed_graph3 = Graph(False)
        for ch in ("A", "B", "C", "D", "E", "Z"):
            cls.directed_graph3.add_node(ch)
    
    def setUp(self):
        pass

    def test_add_node(self):
        self.assertEqual(self.directed_graph3._structure, {"A" : [], "B" : [], "C" : [], "D" : [], "E" : [], "Z" : []})

    def test_add_edge(self):
        self.assertEqual(self.directed_graph1._structure, {"A": [("B", 1), ("C", 18), ("D", 3)], "B": [("A", 1), ("D", 1)], "D": [("B", 1), ("A", 3), ("E", 1)], "C": [("A", 18), ("E", 7)], "E": [("C", 7), ("D", 1)]})
    
    def test_list_nodes(self):
        self.assertEqual(self.directed_graph1.list_nodes(), {"A" : [], "B" : [], "C" : [], "D" : [], "E" : []}.keys())
        self.assertEqual(self.directed_graph3.list_nodes(), {"A" : [], "B" : [], "C" : [], "D" : [], "E" : [], "Z" : []}.keys())
    
    def test_list_edges(self):
        self.assertEqual(set(self.directed_graph1.list_edges()), set([("A", "B", 1), ("B", "A", 1), ("A", "C", 18), ("C", "A", 18), ("A", "D", 3), ("D", "A", 3), ("B", "D", 1), ("D", "B", 1), ("D", "E", 1), ("E", "D", 1), ("C", "E", 7), ("E", "C", 7)]))
        self.assertEqual(set(self.directed_graph3.list_edges()), set())
    
    def test_print_graph(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.directed_graph1.print_graph()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "A : B(1) C(18) D(3) \nB : A(1) D(1) \nD : B(1) A(3) E(1) \nC : A(18) E(7) \nE : C(7) D(1)")

        captured_output = StringIO()
        sys.stdout = captured_output
        self.directed_graph3.print_graph()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "A : \nB : \nC : \nD : \nE : \nZ :")
    
    def test_floyd_distance(self):
        self.assertEqual(self.directed_graph1.floyd_distance("A", "D"), 2)
        self.assertEqual(self.directed_graph1.floyd_distance("D", "A"), 2)

        with self.assertRaises(ValueError):
            self.assertEqual(self.directed_graph2.floyd_distance("E", "D"), 1)
        with self.assertRaises(ValueError):
            self.directed_graph2.floyd_distance("C", "A")
    
    def test_floyd_path(self):
        self.assertEqual(self.directed_graph1.floyd_path("A", "D"), [("A", "B", 1), ("B", "D", 1)])
        self.assertEqual(self.directed_graph1.floyd_path("C", "A"), [("C", "E", 7), ("E", "D", 1), ("D", "B", 1), ("B", "A", 1)])

        with self.assertRaises(ValueError):
            self.directed_graph2.floyd_path("F", "D")
        with self.assertRaises(ValueError):
            self.directed_graph2.floyd_path("D", "A")

if __name__ == "__main__":
    unittest.main()