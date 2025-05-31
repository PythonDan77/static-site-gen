import unittest
from markdown import *
from textnode import *

class Test_MarkDown_Func(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_bad_input(self):
        with self.assertRaises(Exception):
            matches = extract_markdown_images([1, 2, 3])

    def test_extract_markdown_images_wrong_input(self):
        matches = extract_markdown_images("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_input(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](http://Youtube.com)")
        self.assertListEqual([("link", "http://Youtube.com")], matches)

    def test_extract_markdown_links_bad_input(self):
        with self.assertRaises(Exception):
            matches = extract_markdown_links([1, 2, 3])

    def test_extract_markdown_links_no_input(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_wrong_input(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

class Test_Split_Nodes_Func(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_start_withimage(self):
        node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_end_withtext(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) end with text",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" end with text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        ), TextNode(
        "This is more text with an ![image](https://imgur.com/zkkcJKZ.png) and another ![second image](https://imgur.com/5flNhQu.png)",
        TextType.TEXT)]
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is more text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imgur.com/zkkcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://imgur.com/5flNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_split_images_wrong_type(self):
        node = TextNode(
        "This is text with a **bold** in it.",
        TextType.BOLD,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with a **bold** in it.", TextType.BOLD) ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
        "This is text with no images and is only regular text.",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no images and is only regular text.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_links_all_images(self):
        node = TextNode(
            "![first](https://imgur.com/zkkcJKZ.png)![second](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://imgur.com/zkkcJKZ.png"),
                TextNode("second", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_start_withlink(self):
        node = TextNode(
        "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_end_withtext(self):
        node = TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) ending text",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ending text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = [TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        ), TextNode(
        "This is more text with an [link](https://imgur.com/zkkcJKZ.png) and another [second link](https://imgur.com/5flNhQu.png)",
        TextType.TEXT)]
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is more text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://imgur.com/zkkcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://imgur.com/5flNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_split_links_wrong_type(self):
        node = TextNode(
        "This is text with a **bold** in it.",
        TextType.BOLD,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with a **bold** in it.", TextType.BOLD) ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
        "This is text with no links and is only regular text.",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with no links and is only regular text.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_links_all_links(self):
        node = TextNode(
            "[first](https://imgur.com/zkkcJKZ.png)[second](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://imgur.com/zkkcJKZ.png"),
                TextNode("second", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
#==============================text_to_textnodes====================================
class Test_Text_TextNodes_Func(unittest.TestCase):

    def test_no_input_textnodes(self): 
        new_text = text_to_textnodes("")
        self.assertEqual([], new_text)

    def test_input_textnodes(self): 
        new_text = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual([
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                        ],
                           new_text)

    
if __name__ == "__main__":
    unittest.main()