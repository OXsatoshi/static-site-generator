
from block import block_to_block_type,BlockType
from textnode import TextNode,TextType 
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"delimiter doesnt mutch")
        
        parts = node.text.split(delimiter)
        split_nodes = []
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            
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
def markdown_to_blocks(markdown):
    list_of_blocks = markdown.split("\n\n")
    result = []
    for block in list_of_blocks:
        block = block.strip()
        if block != "":
            result.append(block)
    return result 
def markdown_to_html_nodes(markdown):
    all_blocks = markdown_to_blocks(markdown)
    html_tree = []
    for block in all_blocks:
        list_of_html_node_for_block = []
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                heading_order = block.count("#")
                children = text_to_children(block)
                parend_node = ParentNode(f"h{heading_order}",children)
                html_tree.append(parend_node)
            case BlockType.PARAGRAPH:
                children = text_to_children(block.strip())
                parend_node = ParentNode("p",children)
                html_tree.append(parend_node)
            case BlockType.CODE:
                code_block = ''.join(block.split('```')).strip()
                html_tree.append(ParentNode("pre",[LeafNode("code",code_block)]))
            case BlockType.QUOTE:
                children = text_to_children(block)
                parend_node = ParentNode("blockquote",children)
                html_tree.append(parend_node)
            case BlockType.UNORDERED_LIST:
                lines_of_list = block.splitline()
                children = []
                for l in lines_of_list:
                    children.append(LeafNode("li",l))
                parend_node = ParentNode("ul",children)
                html_tree.append(parend_node)
            case BlockType.ORDRDERED_LIST:
                lines_of_list = block.splitline()
                children = []
                for l in lines_of_list:
                    children.append(LeafNode("li",l))
                parend_node = ParentNode("ol",children)
                html_tree.append(parend_node)

    return ParentNode("div",html_tree) 
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.HEADING:
                # Count '#' to get h1-h6
                level = 0
                for char in block:
                    if char == "#":
                        level += 1
                    else:
                        break
                # Remove the hashes and the space: "### Heading" -> "Heading"
                content = block[level + 1:].strip()
                children = text_to_children(content)
                block_nodes.append(ParentNode(f"h{level}", children))

            case BlockType.PARAGRAPH:
                # Standard paragraph
                children = text_to_children(block)
                block_nodes.append(ParentNode("p", children))

            case BlockType.CODE:
                # Remove the ``` fences
                content = block.strip("`").strip()
                # Code blocks usually don't have inline formatting, so we use LeafNode
                code_leaf = LeafNode("code", content)
                block_nodes.append(ParentNode("pre", [code_leaf]))

            case BlockType.QUOTE:
                # Remove '>' from every line
                lines = block.split("\n")
                clean_lines = [line.lstrip(">").strip() for line in lines]
                content = " ".join(clean_lines)
                children = text_to_children(content)
                block_nodes.append(ParentNode("blockquote", children))

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    # Strip the "* " or "- " (first 2 chars)
                    content = line[2:].strip()
                    li_nodes.append(ParentNode("li", text_to_children(content)))
                block_nodes.append(ParentNode("ul", li_nodes))

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    # Remove "1. ", "2. ", etc. (strip until the first space)
                    content = line[line.find(" ") + 1:].strip()
                    li_nodes.append(ParentNode("li", text_to_children(content)))
                block_nodes.append(ParentNode("ol", li_nodes))

    return ParentNode("div", block_nodes)

def text_to_children(text):
    result = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        result.append(text_node_to_html_node(node))

    return result

