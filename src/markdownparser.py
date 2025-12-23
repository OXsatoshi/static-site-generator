
from textnode import TextNode,TextType 

import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
  
    result = []
    for node in old_nodes:
        number_of_delimiter = len([ch for ch in node.text if ch == delimiter])
        if number_of_delimiter %2 != 0:
            raise Exception("delimiter doesnt mutch")
        node_text_list = node.text.split(delimiter)
        i = 0
        while i < len(node_text_list):
            if i %2 == 0:
                result.append(TextNode(node_text_list[i],node.text_type))
            else:
                result.append(TextNode(node_text_list[i],text_type))
            i+=1
    return result

def extract_markdown_images(text):
    marches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return marches
def extract_markdown_links(link):
    marches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",link)
    return marches

def split_nodes_image(old_nodes):
    splited_dict  = {}
    result = []
    for i in range(len(old_nodes)):
        splited_dict[i] = {}
        splited_dict[i]["images"]=extract_markdown_images(old_nodes[i].text)
        if len(splited_dict[i]["images"]) == 0:
            result.append(old_nodes[i])
        else:
            original_text = old_nodes[i].text
            for img in splited_dict[i]["images"]:
                text = original_text.split(f"![{img[0]}]({img[1]})",maxsplit=1)
                original_text = text[1] 
                if text[0] !='':
                    result.append(TextNode(text[0],TextType.TEXT,None))
                result.append(TextNode(img[0],TextType.IMAGE,img[1]))
    
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


