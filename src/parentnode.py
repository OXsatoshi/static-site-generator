from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("a parent must have a tag")
        if self.children is None:
            raise ValueError("What a parent without a children")
        result =f"<{self.tag}>"
        for child in self.children:
            result+=child.to_html()
        return result+f"</{self.tag}>"

