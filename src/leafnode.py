from htmlnode import HTMLNode 

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)
    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node must contain a value")

        resutl = ""
        if self.tag is None:
            return f"{self.value}"
        else :
            return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
 
