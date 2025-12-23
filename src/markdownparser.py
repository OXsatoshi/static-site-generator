
from textnode import TextNode,TextType 

import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # CRITICAL: If the node is not TEXT, we leave it alone.
        # This allows the pipeline to process Bold, then Italic, etc.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Check for matching delimiters
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"delimiter doesnt mutch")
        
        parts = node.text.split(delimiter)
        split_nodes = []
        for i in range(len(parts)):
            # Skip empty strings to keep the node list clean
            if parts[i] == "":
                continue
            
            # Alternating logic: Even = Text, Odd = The new type (Bold/Italic/Code)
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        
        new_nodes.extend(split_nodes)
        
    return new_nodes
def extract_markdown_images(text):
    marches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return marches
def extract_markdown_links(link):
    marches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",link)
    return marches

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            result.append(node)
            continue

        for img in images:
            sections = original_text.split(f"![{img[0]}]({img[1]})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            
            result.append(TextNode(img[0], TextType.IMAGE, img[1]))
            
            original_text = sections[1]

        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))

    return result
def split_nodes_links(old_nodes):
    splited_dict  = {}
    result = []
    for i in range(len(old_nodes)):
        splited_dict[i] = {}
        splited_dict[i]["links"]=extract_markdown_links(old_nodes[i].text)
        if len(splited_dict[i]["links"]) == 0:
            result.append(old_nodes[i])
        else:
            original_text = old_nodes[i].text
            for link in splited_dict[i]["links"]:
                text = original_text.split(f"[{link[0]}]({link[1]})",maxsplit=1)
                original_text = text[1] 
                if text[0] !='':
                    result.append(TextNode(text[0],TextType.TEXT,None))
                result.append(TextNode(link[0],TextType.LINK,link[1]))
    
    return result
def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            result.append(node)
            continue

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            
            original_text = sections[1]

        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))

    return result
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes
