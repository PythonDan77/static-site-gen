import re

def extract_markdown_images(text):
    if not isinstance(text, str):
        raise Exception("Image input must be a string.")
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    if not isinstance(text, str):
        raise Exception("Link input must be a string.")
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

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
            result.append(TextNode(alt, TextType.LINK, link))
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