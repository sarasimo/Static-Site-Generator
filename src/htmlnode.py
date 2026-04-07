

class HtmlNode():
    def __init__(self, tag =None, value =None, children =None, props =None):
        self.tag = tag #string rep of HTML tag ex p, h1 ect
        self.value =value #string to format 
        self.children =children #list of HtmlNode obj
        self.props = props # dictionary shoeing attributes of tag

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ""

        if self.props == None:
            return string

        for key, value in self.props.items():
   
            string += f' {key}="{value}"'

        return string

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        
        if self.tag == None:
            return self.value
        
        match self.tag:
            case "a": 
                return f"<a{self.props_to_html()}>{self.value}</a>"
            case "img":
                return f"<img{self.props_to_html()} />"

            case _: #all other tags follow this format
                return f"<{self.tag}>{self.value}</{self.tag}>"
            


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError
        
        children_string = ""
        
        if self.children == None :
            raise ValueError(f"list is empty")
        
        for child in self.children:
            children_string += child.to_html()

        return f"<{self.tag}>{children_string}</{self.tag}>"
            
# <div><b>grandchild</b><span><b>grandchild</b></span></div>
# <div><span><b>grandchild</b></span></div>
