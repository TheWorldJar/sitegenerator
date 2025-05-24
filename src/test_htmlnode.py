import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "Hello, world!", [], {})
        node2 = HTMLNode("div", "Hello, world!", [], {})
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = HTMLNode(None, "Hello, world!", [], {"href": "https://www.google.com",
    "target": "_blank"})
        node2 = HTMLNode(None, "Hello, world!", [], {"href": "https://www.google.com",
    "target": "_blank"})
        self.assertEqual(node, node2)

    def test_diff(self):
        node = HTMLNode("div", "Hello, world!", [], {})
        node2 = HTMLNode("div", "Hello, world!", [], {"href": "https://www.google.com",
    "target": "_blank"})
        self.assertNotEqual(node, node2)
    
    def test_diff2(self):
        node = HTMLNode("div", "Hello, world!", ["this", "is", "a", "list"], {})
        node2 = HTMLNode("div", "Hello, world!", [], {})
        self.assertNotEqual(node, node2)
    
    def test_empty_node(self):
        node = HTMLNode(None, None, None, None)
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com",
    "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("div", "Hello, world!", {})
        node2 = LeafNode("div", "Hello, world!", {})
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = LeafNode("div", "Hello, world!", {"href": "https://www.google.com",
    "target": "_blank"})
        node2 = LeafNode("div", "Hello, world!", {"href": "https://www.google.com",
    "target": "_blank"})
        self.assertEqual(node, node2)
    
    def test_diff(self):
        node = LeafNode("div", "Hello, world!", {})
        node2 = LeafNode("div", "Hello, world!", {"href": "https://www.google.com",
    "target": "_blank"})
        self.assertNotEqual(node, node2)
    
    def test_children(self):
        node = LeafNode("div", "Hello, world!", {})
        self.assertEqual(node.children, [])
    
    def test_to_html(self):
        node = LeafNode("div", "Hello, world!", {})
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_to_html2(self):
        node = LeafNode("div", "", {})
        self.assertRaises(ValueError, node.to_html)

    def test_to_html3(self):
        node = LeafNode("div", None, {})
        self.assertRaises(ValueError, node.to_html)

    def test_to_html4(self):
        node = LeafNode("div", "Hello, world!", {"href": "https://www.google.com",
    "target": "_blank"})
        self.assertEqual(node.to_html(), "<div href=\"https://www.google.com\" target=\"_blank\">Hello, world!</div>")

    def test_to_html5(self):
        node = LeafNode(None, "Hello, world!", {"href": "https://www.google.com",
    "target": "_blank"})
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html6(self):
        node = LeafNode(None, None, {})
        self.assertRaises(ValueError, node.to_html)

    def test_to_html7(self):
        node = LeafNode("", "Hello, world!", {})
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()