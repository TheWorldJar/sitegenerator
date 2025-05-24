import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()