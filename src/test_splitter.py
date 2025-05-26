import unittest

from splitter import split_into_nodes, extract_markdown_images, extract_markdown_links, split_into_images, split_into_links
from textnode import TextNode, TextType

class TestSplitter(unittest.TestCase):
    def test_normal_text(self):
        text = ["This is normal text"]
        result = split_into_nodes(text, "", TextType.NORMAL)
        expected = [TextNode("This is normal text", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_multiple_normal_texts(self):
        text = ["First text", "Second text", "Third text"]
        result = split_into_nodes(text, "", TextType.NORMAL)
        expected = [
            TextNode("First text", TextType.NORMAL),
            TextNode("Second text", TextType.NORMAL),
            TextNode("Third text", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = ["This is **bold** text"]
        result = split_into_nodes(text, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = ["This is _italic_ text"]
        result = split_into_nodes(text, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.ITALIC),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.ITALIC)
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = ["This is `code` text"]
        result = split_into_nodes(text, "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.CODE),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_segments(self):
        text = ["This is **bold** and this is also **bold**"]
        result = split_into_nodes(text, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is also ", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_invalid_bold_delimiter(self):
        text = ["This is **bold** text"]
        with self.assertRaises(Exception) as context:
            split_into_nodes(text, "_", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid delimiter: _ for text type: TextType.BOLD")

    def test_invalid_italic_delimiter(self):
        text = ["This is _italic_ text"]
        with self.assertRaises(Exception) as context:
            split_into_nodes(text, "**", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Invalid delimiter: ** for text type: TextType.ITALIC")

    def test_invalid_code_delimiter(self):
        text = ["This is `code` text"]
        with self.assertRaises(Exception) as context:
            split_into_nodes(text, "**", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid delimiter: ** for text type: TextType.CODE")

    def test_empty_text_list(self):
        text = []
        result = split_into_nodes(text, "", TextType.NORMAL)
        self.assertEqual(result, [])

    def test_empty_text_chunk(self):
        text = [""]
        result = split_into_nodes(text, "", TextType.NORMAL)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = ["This is an image ![alt text](https://example.com/image.png)"]
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text = [
            "First image ![alt1](https://example.com/image1.png)",
            "Second image ![alt2](https://example.com/image2.png)"
        ]
        result = extract_markdown_images(text)
        expected = [
            ("alt1", "https://example.com/image1.png"),
            ("alt2", "https://example.com/image2.png")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images_in_single_line(self):
        text = ["![alt1](https://example.com/image1.png) and ![alt2](https://example.com/image2.png)"]
        result = extract_markdown_images(text)
        expected = [
            ("alt1", "https://example.com/image1.png"),
            ("alt2", "https://example.com/image2.png")
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        text = ["This is a text without any images"]
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_empty_text(self):
        text = [""]
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_empty_list(self):
        text = []
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_invalid_image_syntax(self):
        text = ["This is not an image [alt](https://example.com/image.png)"]
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = ["This is a link [link text](https://example.com)"]
        result = extract_markdown_links(text)
        expected = [("link text", "https://example.com")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text = [
            "First link [link1](https://example.com/1)",
            "Second link [link2](https://example.com/2)"
        ]
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2")
        ]
        self.assertEqual(result, expected)

    def test_multiple_links_in_single_line(self):
        text = ["[link1](https://example.com/1) and [link2](https://example.com/2)"]
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2")
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        text = ["This is a text without any links"]
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_empty_text(self):
        text = [""]
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_empty_list(self):
        text = []
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_links_with_special_chars(self):
        text = ["[link!@#$%](https://example.com/path!@#$%)"]
        result = extract_markdown_links(text)
        expected = [("link!@#$%", "https://example.com/path!@#$%")]
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        text = [
            "Here's a link [link1](https://example.com/1)",
            "And an image ![alt](https://example.com/image.png)",
            "And another link [link2](https://example.com/2)"
        ]
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2")
        ]
        self.assertEqual(result, expected)
        result = extract_markdown_images(text)
        expected = [("alt", "https://example.com/image.png")]
        self.assertEqual(result, expected)

class TestSplitIntoImages(unittest.TestCase):
    def test_single_image(self):
        text_nodes = [TextNode("This is an image ![alt text](https://example.com/image.png)", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text_nodes = [TextNode("![alt1](https://example.com/image1.png) and ![alt2](https://example.com/image2.png)", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("", TextType.NORMAL),
            TextNode("alt1", TextType.IMAGE, "https://example.com/image1.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("alt2", TextType.IMAGE, "https://example.com/image2.png")
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        text_nodes = [TextNode("This is text without any images", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [TextNode("This is text without any images", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text_nodes = [TextNode("", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        text_nodes = []
        result = split_into_images(text_nodes)
        self.assertEqual(result, [])

    def test_multiple_nodes(self):
        text_nodes = [
            TextNode("First node ![alt1](https://example.com/image1.png)", TextType.NORMAL),
            TextNode("Second node ![alt2](https://example.com/image2.png)", TextType.NORMAL)
        ]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("First node ", TextType.NORMAL),
            TextNode("alt1", TextType.IMAGE, "https://example.com/image1.png"),
            TextNode("Second node ", TextType.NORMAL),
            TextNode("alt2", TextType.IMAGE, "https://example.com/image2.png")
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        text_nodes = [TextNode("![alt](https://example.com/image.png) This is text after the image", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("", TextType.NORMAL),
            TextNode("alt", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" This is text after the image", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        text_nodes = [TextNode("This is text before the image ![alt](https://example.com/image.png)", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("This is text before the image ", TextType.NORMAL),
            TextNode("alt", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(result, expected)

class TestSplitIntoLinks(unittest.TestCase):
    def test_single_link(self):
        text_nodes = [TextNode("This is a link [link text](https://example.com)", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("This is a link ", TextType.NORMAL),
            TextNode("link text", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text_nodes = [TextNode("[link1](https://example.com/1) and [link2](https://example.com/2)", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "https://example.com/2")
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        text_nodes = [TextNode("This is text without any links", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [TextNode("This is text without any links", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text_nodes = [TextNode("", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        text_nodes = []
        result = split_into_links(text_nodes)
        self.assertEqual(result, [])

    def test_multiple_nodes(self):
        text_nodes = [
            TextNode("First node [link1](https://example.com/1)", TextType.NORMAL),
            TextNode("Second node [link2](https://example.com/2)", TextType.NORMAL)
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("First node ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode("Second node ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "https://example.com/2")
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        text_nodes = [TextNode("[link](https://example.com) This is text after the link", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" This is text after the link", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        text_nodes = [TextNode("This is text before the link [link](https://example.com)", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("This is text before the link ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        text_nodes = [
            TextNode("Here's a link [link1](https://example.com/1)", TextType.NORMAL),
            TextNode("And an image ![alt](https://example.com/image.png)", TextType.NORMAL),
            TextNode("And another link [link2](https://example.com/2)", TextType.NORMAL)
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("Here's a link ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode("And an image ![alt](https://example.com/image.png)", TextType.NORMAL),
            TextNode("And another link ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "https://example.com/2")
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
    