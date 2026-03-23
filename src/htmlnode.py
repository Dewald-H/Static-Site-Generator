'''
HTMLNode represents a 'node' in a HTML document tree (like a <p> tag and it's contents, or an <a> tag and it's contents)
'''

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        attrs = ""
        for key, value in self.props.items():
            attrs += f' {key}="{value}"'
        return attrs
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
'''
LeafNode is a type of HTMLNode that represents a single HTML tag with no children. For example, a simple <p> tag with some text inside of it.
'''

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return str(self.value)
        props_str = self.props_to_html()
        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

'''
ParentNode handles the nesting of HTML nodes inside of one another. Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
'''

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("ParentNode must have children.")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
