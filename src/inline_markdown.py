import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown text provided")

        for i in range(len(parts)):
            if i % 2 != 0:
                new_nodes.append(TextNode(parts[i], text_type))
            else:
                if len(parts[i]) == 0:
                    continue
                new_nodes.append(TextNode(parts[i], TextType.PLAIN_TEXT))
    
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)

        if not matches:
            new_nodes.append(node)
            continue
        
        remaining = node.text

        for alt, url in matches:
            sections = remaining.split(f"![{alt}]({url})", 1)
            if len(sections[0]) != 0:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = sections[1]

        if len(remaining) != 0:
            new_nodes.append(TextNode(remaining, TextType.PLAIN_TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        if not matches:
            new_nodes.append(node)
            continue
        
        remaining = node.text

        for alt, url in matches:
            sections = remaining.split(f"[{alt}]({url})", 1)
            if len(sections[0]) != 0:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            remaining = sections[1]

        if len(remaining) != 0:
            new_nodes.append(TextNode(remaining, TextType.PLAIN_TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes