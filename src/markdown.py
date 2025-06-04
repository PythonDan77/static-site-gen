import re
from enum import Enum  
from textnode import *
from htmlnode import *


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING1 = "h1"
    HEADING2 = "h2"
    HEADING3 = "h3"
    HEADING4 = "h4"
    HEADING5 = "h5"
    HEADING6 = "h6"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED = "ul"
    ORDERED = "ol"

def extract_markdown_images(text):
    if not isinstance(text, str):
        raise Exception("Image input must be a string.")
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    if not isinstance(text, str):
        raise Exception("Link input must be a string.")
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            result.append(old)
            continue
        if not delimiter:
            raise Exception("Delimiter required")
        if old.text.count(delimiter) % 2 != 0 or delimiter not in ["**", "_", "`"]:
            raise Exception("Invalid markdown syntax")
        if old.text.count(delimiter) == 0:
            result.append(TextNode(old.text, TextType.TEXT))
            continue

        split_text = old.text.split(delimiter)

        for i, phrase in enumerate(split_text):
            if phrase == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(phrase, TextType.TEXT))
            else:
                result.append(TextNode(phrase, text_type))
    return result

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue

        text_copy = node.text
        
        for alt, link in images:
            sections = text_copy.split(f"![{alt}]({link})", 1)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(alt, TextType.IMAGE, link))
            text_copy = sections[1]
        if text_copy:
            result.append(TextNode(text_copy, TextType.TEXT))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            result.append(node)
            continue

        text_copy = node.text
        for alt, link in links:
            sections = text_copy.split(f"[{alt}]({link})", 1)

            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(alt, TextType.LINK, link))
            text_copy = sections[1]
        if text_copy:
            result.append(TextNode(text_copy, TextType.TEXT))
    return result

def text_to_textnodes(text):
    result = []

    if text:
        new_node = TextNode(text,TextType.TEXT)

        bold_check = split_nodes_delimiter([new_node],"**", TextType.BOLD)
        italic_check = split_nodes_delimiter(bold_check,"_", TextType.ITALIC)
        code_check = split_nodes_delimiter(italic_check,"`", TextType.CODE)
        image_check = split_nodes_image(code_check)
        link_check = split_nodes_link(image_check)
        result.extend(link_check)

    return result

#---------------------------------NEW-------------------------------------------


def markdown_to_html_node(markdown):
    markdown = markdown.strip()
    blocks = markdown_to_blocks(markdown)  
    result = []

    for block in blocks:

        block_type = block_to_block_type(block)  

        if block_type == BlockType.CODE:
            result.append(ParentNode("pre",[text_node_to_html_node(TextNode(unchanged_code(block),TextType.CODE))]))    
        elif block_type == BlockType.ORDERED:
            result.append(ParentNode("ol", list_children(block)))
        elif block_type == BlockType.UNORDERED:
            result.append(ParentNode("ul", list_children(block)))
        elif "h" in block_type.value:
            result.append(ParentNode(block_type.value, heading_children(block)))
        elif block_type == BlockType.PARAGRAPH:
            result.append(ParentNode("p", paragraph_children(block)))
        elif block_type == BlockType.QUOTE:
            result.append(ParentNode("blockquote", paragraph_children(block)))

    return ParentNode("div",result)

def unchanged_code(markdown):
    markdown = re.sub(r'^```|```$', '', markdown).strip()
    nodes = markdown.split("\n")
    new_markdown = "".join(node.lstrip() + "\n" for node in nodes)
    return new_markdown
    
def paragraph_children(markdown):
    all_nodes = []
    item = markdown.replace("\n", " ").replace("> ", "")
    item = re.sub(r'\s+', ' ', item).strip()
    new_node = text_to_textnodes(item)  
    for node in new_node:
        all_nodes.append(text_node_to_html_node(node))
    return all_nodes

def list_children(markdown):
    final_parent = []
    items = markdown.split("\n")
    
    for item in items:
        match = re.findall(r"^(?:\d+\.\s|[-*]\s)(.+)", item)
        new_node = text_to_textnodes(match[0])
        list_items = [text_node_to_html_node(node) for node in new_node]
        final_parent.append(ParentNode("li", list_items))
    return final_parent

def heading_children(markdown):
    text = re.sub(r'^#{1,6}\s+', '', markdown)
    new_node = text_to_textnodes(text)  
    all_nodes = [text_node_to_html_node(node) for node in new_node]
    return all_nodes

#-------------------------------Block Functions-----------------------

def block_to_block_type(block):
    if block.startswith("#" * 6 + " "):
        return BlockType.HEADING6
    if block.startswith("#" * 5 + " "):
        return BlockType.HEADING5
    if block.startswith("#" * 4 + " "):
        return BlockType.HEADING4
    if block.startswith("#" * 3 + " "):
        return BlockType.HEADING3
    if block.startswith("#" * 2 + " "):
        return BlockType.HEADING2
    if block.startswith("# "):
        return BlockType.HEADING1
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
