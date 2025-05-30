import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Another text node", TextType.BOLD)
        node2 = TextNode("Another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_no_url(self):
        node = TextNode("Another text node", TextType.BOLD)
        self.assertIsNone(node.url, None)
    
    def test_url(self):
        node = TextNode("Another text node", TextType.BOLD, "http://Youtube.com")
        self.assertIsNotNone(node.url)

#===============================text_node_to_html_node=============================
class Testtext_node_to_html_node(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_tag(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
    
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="http://Youtube.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": "http://Youtube.com"})

    def test_link_fail(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a link node", TextType.LINK)
            html_node = text_node_to_html_node(node)

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, url="http://Youtube.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"src": "http://Youtube.com", "alt": "image"})

    def test_image_fail(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a image node", TextType.IMAGE)
            html_node = text_node_to_html_node(node)

    def test_wrong_value(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a image node", TextType.TEXT)
            node.text_type = "something_else"
            html_node = text_node_to_html_node(node)

#===============================split_nodes_delimiter=============================
class Testsplit_nodes_delimiter(unittest.TestCase):

    def test_wrong_type(self):
        node = TextNode("This is a `code` node", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])
    
    def test_inequal_delimiter(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a `code node", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_no_delimiter(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a `code` node", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "", TextType.CODE)

    def test_wrong_delimiter(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a `code` node", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "!", TextType.CODE)

    def test_bold_delimiter(self):
        node = TextNode("This is a **bold** node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" node", TextType.TEXT)])

    def test_double_bold_delimiter(self):
        node = TextNode("This is a **bold** node with double **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" node with double ", TextType.TEXT),
                                     TextNode("bold", TextType.BOLD)])

    def test_italic_delimiter(self):
        node = TextNode("This is an _italic_ node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" node", TextType.TEXT)])

    def test_code_delimiter(self):
        node = TextNode("This is a `code` node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" node", TextType.TEXT)])
    
    def test_text_no_delimiter(self):
        node = TextNode("This is a code node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is a code node", TextType.TEXT)])


if __name__ == "__main__":
    unittest.main()
