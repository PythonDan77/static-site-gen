# from enum import Enum  
# import re
# from markdown import *
# from textnode import *
# from htmlnode import *


# class BlockType(Enum):
#     PARAGRAPH = "p"
#     HEADING1 = "h1"
#     HEADING2 = "h2"
#     HEADING3 = "h3"
#     HEADING4 = "h4"
#     HEADING5 = "h5"
#     HEADING6 = "h6"
#     CODE = "code"
#     QUOTE = "blockquote"
#     UNORDERED = "ul"
#     ORDERED = "ol"

# def block_to_block_type(block):
#     if block.startswith("#" * 6 + " "):
#         return BlockType.HEADING6
#     if block.startswith("#" * 5 + " "):
#         return BlockType.HEADING5
#     if block.startswith("#" * 4 + " "):
#         return BlockType.HEADING4
#     if block.startswith("#" * 3 + " "):
#         return BlockType.HEADING3
#     if block.startswith("#" * 2 + " "):
#         return BlockType.HEADING2
#     if block.startswith("# "):
#         return BlockType.HEADING1
#     if block.startswith("```") and block.endswith("```"):
#         return BlockType.CODE
#     if block.startswith(">"):
#         return BlockType.QUOTE
#     if block.startswith("- ") or block.startswith("* "):
#         return BlockType.UNORDERED
#     if re.match(r"^(\d+)\.\s", block, re.MULTILINE):
#         matches = re.findall(r"^(\d+)\.\s+.+", block, re.MULTILINE)
#         if matches and int(matches[0]) == 1:
#             for i in range(1, len(matches)):
#                 if int(matches[i]) != int(matches[i-1]) + 1:
#                     return BlockType.PARAGRAPH
#             return BlockType.ORDERED
#     return BlockType.PARAGRAPH
    
# def markdown_to_blocks(markdown):
#     modified = []
#     if isinstance(markdown, str):
#         modified = [line.strip() for line in markdown.split("\n\n") if line.strip()]
#     return modified