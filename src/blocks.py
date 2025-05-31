from enum import Enum  
import re


class BlockType(Enum):

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(block):
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("- ") or block.startswith("* "):
        return BlockType.UNORDERED
    if re.match(r"^(\d+)\.\s", block, re.MULTILINE):
        matches = re.findall(r"^(\d+)\.\s+.+", block, re.MULTILINE)
        if matches and int(matches[0]) == 1:
            for i in range(1, len(matches)):
                if int(matches[i]) != int(matches[i-1]) + 1:
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED  
    return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    modified = []
    if isinstance(markdown, str):
        modified = [line.strip() for line in markdown.split("\n\n") if line.strip()]
    return modified