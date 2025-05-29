import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    #============================LeafNode Testing =================================

    def test_leaf_initialize_fail(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="a", value=None)
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        new_dict = {"href": "https://google.com"}
        node = LeafNode("a", "Google", new_dict)
        self.assertEqual(node.to_html(), '<a href="https://google.com">Google</a>')

    #===============================ParentNode Testing ===============================
    def test_parent_no_tag(self):
        new_list = ["h2", "h3", "h4"]
        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=new_list)

    def test_parent_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag="a", children=None)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)


    

if __name__ == "__main__":
    unittest.main()