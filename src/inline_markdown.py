import re
from textnode import TextType, TextNode

'''
split_nodes_delimeter creates TextNodes form raw markdown strings
'''
def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimeter)

        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: unmatched '{delimeter}'")
        
        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

'''
'extract_markdown_images' extracts image links from markdown text
'''
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

'''
'extract_markdown_links' extracts regular links from markdown text
'''
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

'''
'split_nodes_image' splits TextNodes containing markdown images into separate nodes.
'''
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            sections = text.split(f"![{alt}]({url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE_TEXT, url))

            text = sections[1]

        if text:
            new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))
            
    return new_nodes


'''
'split_nodes_link' splits TextNodes containing markdown links into separate nodes.
'''
def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for anchor, url in links:
            sections = text.split(f"[{anchor}]({url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK_TEXT, url))

            text = sections[1]

        if text:
            new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimeter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimeter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimeter(nodes, "`", TextType.CODE_TEXT)

    return nodes