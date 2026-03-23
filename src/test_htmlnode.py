import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.boot.dev"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.boot.dev"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_repr_output(self):
        node = HTMLNode("p", "Hello", None, {"class": "text"})
        expected = "HTMLNode(p, Hello, None, {'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title")
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_leaf_to_html_anchor_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click me</a>'
        )

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("button", "Submit", {"type": "submit", "class": "btn"})
        result = node.to_html()
        self.assertTrue(
            result == '<button type="submit" class="btn">Submit</button>' or
            result == '<button class="btn" type="submit">Submit</button>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "one")
        child_node2 = LeafNode("span", "two")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>one</span><span>two</span></div>"
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>'
        )
    
    def test_to_html_multiple_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")]).to_html()

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_to_html_mixed_children(self):
        leaf = LeafNode("span", "text")
        nested = ParentNode("b", [LeafNode(None, "bold")])
        parent = ParentNode("div", [leaf, nested])
        self.assertEqual(
            parent.to_html(),
            "<div><span>text</span><b>bold</b></div>"
        )

    def test_child_with_props(self):
        child = LeafNode("span", "child", {"class": "highlight"})
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            '<div><span class="highlight">child</span></div>'
        )

if __name__ == "__main__":
    unittest.main()