# import unittest
# from blocks import *

# #==============================block_to_blocks======================================
# class Test_Block_to_Block_Func(unittest.TestCase):
#     def test_block_to_block_h1(self):
#         result = block_to_block_type("# HEADING 1")
#         self.assertEqual(result, BlockType.HEADING1)

#     def test_block_to_block_h3(self):
#         result = block_to_block_type("### HEADING 3")
#         self.assertEqual(result, BlockType.HEADING3)

#     def test_block_to_block_h6(self):
#         result = block_to_block_type("###### HEADING 6")
#         self.assertEqual(result, BlockType.HEADING6)

#     def test_block_to_block_h7(self):
#         result = block_to_block_type("######## HEADING 7")
#         self.assertEqual(result, BlockType.PARAGRAPH)

#     def test_block_to_block_code(self):
#         result = block_to_block_type("```code```")
#         self.assertEqual(result, BlockType.CODE)

#     def test_block_to_block_quote(self):
#         result = block_to_block_type(">Here is a quote")
#         self.assertEqual(result, BlockType.QUOTE)
    
#     def test_block_to_block_unordered(self):
#         result = block_to_block_type("- item one\n- item two\n- item three")
#         self.assertEqual(result, BlockType.UNORDERED)

#     def test_block_to_block_ordered_single(self):
#         result = block_to_block_type("1. item one\n")
#         self.assertEqual(result, BlockType.ORDERED)

#     def test_block_to_block_ordered_multuple(self):
#         result = block_to_block_type("1. item one\n2. item two\n3. item three")
#         self.assertEqual(result, BlockType.ORDERED)

#     def test_block_to_block_ordered_higher_start_number(self):
#         result = block_to_block_type("12. item one")
#         self.assertEqual(result, BlockType.PARAGRAPH)

#     def test_block_to_block_ordered_higher_start_number_multiple(self):
#         result = block_to_block_type("12. item one\n13. item two")
#         self.assertEqual(result, BlockType.PARAGRAPH)
    
#     def test_block_to_block_ordered_higher_sequence_wrong(self):
#         result = block_to_block_type("1. item one\n2. item two\n4. item two")
#         self.assertEqual(result, BlockType.PARAGRAPH)

#     def test_block_to_block_paragraph(self):
#         result = block_to_block_type("Hello, how are you?")
#         self.assertEqual(result, BlockType.PARAGRAPH)


# #==============================markdown_to_blocks====================================

# class Test_Mark_to_Blocks_Func(unittest.TestCase):
#     def test_markdown_to_blocks(self):
#         md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items
# """
#         blocks = markdown_to_blocks(md)
#         self.assertEqual(
#             blocks,
#             [
#                 "This is **bolded** paragraph",
#                 "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
#                 "- This is a list\n- with items",
#             ],
#         )

#     def test_markdown_to_blocks_bad_input(self):
#         md = 45
#         blocks = markdown_to_blocks(md)
#         self.assertEqual(
#             blocks,
#             []
#         )

#     def test_markdown_to_blocks_excessive_newlines(self):
#         md = """
# This is paragraph one

    

# This is paragraph two with    space   

    

# - List item
# """
#         blocks = markdown_to_blocks(md)
#         self.assertEqual(
#             blocks,
#             [
#                 "This is paragraph one",
#                  "This is paragraph two with    space",
#                  "- List item",
#             ],
#         )
    

    
# if __name__ == "__main__":
#     unittest.main()