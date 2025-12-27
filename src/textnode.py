from enum import Enum
from leafnode import LeafNode
class TextType(Enum):
    TEXT = "text" 
    BOLD= "bold_text"
    ITALIC= "italic_text"
    CODE= "code_text"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self,other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
       return f"TextNode({self.text}, {self.text_type}, {self.url})" 


def text_node_to_html_node(text_node):
    if (text_node.text_type != TextType.TEXT and text_node.text_type !=TextType.BOLD 
            and text_node.text_type !=TextType.ITALIC and text_node.text_type != TextType.LINK 
            and text_node.text_type != TextType.IMAGE and text_node.text_type !=TextType.CODE):
        raise Exception("uknown text node ")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text,None) 
        case TextType.BOLD:
            return LeafNode("b",text_node.text,None)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text,None)
        case TextType.CODE:
            return LeafNode("code",text_node.text,None)

        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":f"{text_node.url}"})

        case TextType.IMAGE:
            return LeafNode("img",text_node.text,{"src":f"{text_node.url}","alt":""})

