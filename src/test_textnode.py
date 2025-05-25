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

    def test_to_html_node(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        
    def test_to_html_node_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        
    def test_to_html_node_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        
    def test_to_html_node_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        
    def test_to_html_node_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/image.png")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/image.png", "alt": "This is an image node"})

    def test_to_html_node_image2(self):
        node = TextNode("", TextType.IMAGE, "https://www.boot.dev/image.png")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/image.png", "alt": ""})
        
    def test_to_html_node_invalid(self):
        node = TextNode("This is an invalid node", None)
        self.assertRaises(ValueError, node.to_html_node())

if __name__ == "__main__":
    unittest.main()