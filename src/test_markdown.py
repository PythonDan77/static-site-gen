import unittest
from markdown import *
from textnode import *

#===============================Extract Markdown images/links=============================
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

#===============================split_nodes_images_links=============================

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


class Test_markdown_to_html_node_func(unittest.TestCase):
    def test_paragraphs(self):
        md =  """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_header_block(self):
        md = """
# This is a _heading_ with **bold**

###### This is an H6 with `code` and _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <i>heading</i> with <b>bold</b></h1><h6>This is an H6 with <code>code</code> and <i>italic</i></h6></div>",
        )

    def test_quote_block(self):
        md = """
> This is a **quote**
> that continues _italicly_
> and ends with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>quote</b> that continues <i>italicly</i> and ends with <code>code</code></blockquote></div>",
        )

    def test_ordered_list_block(self):
        md = """
1. This is **bold** item
2. Another _italic_ item
3. Final `code` item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bold</b> item</li><li>Another <i>italic</i> item</li><li>Final <code>code</code> item</li></ol></div>",
        )

    def test_unordered_list_block(self):
        md = """
- This is **bold** item
- Another _italic_ item
- Final `code` item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bold</b> item</li><li>Another <i>italic</i> item</li><li>Final <code>code</code> item</li></ul></div>",
        )

#------------------------------------Block Function tests-------------------------------------------

#==============================block_to_blocks======================================
class Test_Block_to_Block_Func(unittest.TestCase):
    def test_block_to_block_h1(self):
        result = block_to_block_type("# HEADING 1")
        self.assertEqual(result, BlockType.HEADING1)

    def test_block_to_block_h3(self):
        result = block_to_block_type("### HEADING 3")
        self.assertEqual(result, BlockType.HEADING3)

    def test_block_to_block_h6(self):
        result = block_to_block_type("###### HEADING 6")
        self.assertEqual(result, BlockType.HEADING6)

    def test_block_to_block_h7(self):
        result = block_to_block_type("######## HEADING 7")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_code(self):
        result = block_to_block_type("```code```")
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_quote(self):
        result = block_to_block_type(">Here is a quote")
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_block_to_block_unordered(self):
        result = block_to_block_type("- item one\n- item two\n- item three")
        self.assertEqual(result, BlockType.UNORDERED)

    def test_block_to_block_ordered_single(self):
        result = block_to_block_type("1. item one\n")
        self.assertEqual(result, BlockType.ORDERED)

    def test_block_to_block_ordered_multuple(self):
        result = block_to_block_type("1. item one\n2. item two\n3. item three")
        self.assertEqual(result, BlockType.ORDERED)

    def test_block_to_block_ordered_higher_start_number(self):
        result = block_to_block_type("12. item one")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_ordered_higher_start_number_multiple(self):
        result = block_to_block_type("12. item one\n13. item two")
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_block_to_block_ordered_higher_sequence_wrong(self):
        result = block_to_block_type("1. item one\n2. item two\n4. item two")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_paragraph(self):
        result = block_to_block_type("Hello, how are you?")
        self.assertEqual(result, BlockType.PARAGRAPH)


#==============================markdown_to_blocks====================================

class Test_Mark_to_Blocks_Func(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_bad_input(self):
        md = 45
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is paragraph one

    

This is paragraph two with    space   

    

- List item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is paragraph one",
                 "This is paragraph two with    space",
                 "- List item",
            ],
        )

    


if __name__ == "__main__":
    unittest.main()