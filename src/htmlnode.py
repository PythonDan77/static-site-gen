
class HTMLNode:
    def __init__(self, tag:str=None,value:str=None, children:list=None,props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            return "".join(f' {key}="{value}"' for key, value in self.props.items())
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html() if self.props is not None else ''}>{self.value}</{self.tag}>"
        

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag == None:
            raise ValueError("ParentNode-tag must have a value.")
        elif children == None:
            raise ValueError("ParentNode-children must have a value.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        joined_html = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}>{joined_html}</{self.tag}>'
        


        