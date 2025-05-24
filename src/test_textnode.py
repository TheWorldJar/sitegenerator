import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a code node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a code node", TextType.LINK, "www.boot.dev")
        self.assertEqual(node, node2)

    def test_diff(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a code node", TextType.LINK, "www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_diff2(self):
        node = TextNode("This is a code node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a code node", TextType.CODE, "www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_empty_node(self):
        node = TextNode(None, None, None)
        node2 = TextNode(None, None, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()