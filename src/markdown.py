import re
from textnode import *
from blocks import *


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




