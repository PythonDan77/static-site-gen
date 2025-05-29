import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "some text")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "some text")
    
    def test_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag, None)
        self.assertIsNone(node.value, None)
        self.assertIsNone(node.children, None)
        self.assertIsNone(node.props, None)

    def test_children(self):
        new_list = ["h2", "h3", "h4"]
        node = HTMLNode(children=new_list)
        self.assertIsInstance(node.children, list)
        self.assertEqual(node.children, ["h2", "h3", "h4"])

    def test_no_props_to_html(self):
        node = HTMLNode("h1", "some text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        new_dict = {"href": "https://google.com", "target": "_blank"}
        node = HTMLNode(props=new_dict)
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_repr(self):
        new_list = ["h2", "h3", "h4"]
        node = HTMLNode(tag="h1", value="some text", children=new_list)
        expected= "HTMLNode(h1, some text, ['h2', 'h3', 'h4'], None)"
        self.assertEqual(node.__repr__(), expected)


    

if __name__ == "__main__":
    unittest.main()