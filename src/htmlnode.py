

class HTMLNode:
    def __init__(self,tag = None,value= None,children= None,props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        if len(self.props.keys()) == 0 :
            return "" 
        
        result = ""
        for key in self.props.keys():
            result+=f' {key}="{self.props[key]}"'

        return result
    
    def __repr__(self):
        result = ""
        if self.tag is not None:
            result+=f"<{self.tag} {self.props_to_html()}>"
        
        else:
            result+="---RAW TEXT---"
        if self.value is not None:
            result+=f"\n {self.value}"
        else: 
            result+="\n"
        if self.children is not None:
            result+=f"\n {self.children}"
        else:
            result+="\n"
        return result



    
