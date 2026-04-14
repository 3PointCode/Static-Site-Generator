import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_eq(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        output = node.props_to_html()
        self.assertEqual(output, ' href="https://www.google.com" target="_blank"')
    
    def test_props_neq(self):
        props = {
            "href": "https://www.google.com",
            "target": "_black",
        }
        node = HTMLNode(props=props)
        output = node.props_to_html()
        self.assertNotEqual(output, ' href="https://www.google.com" target="_blank"')

    def test_props2_eq(self):
        props = {
            "href": "https://www.google.com",
            "target": "_nada",
            "custom": "something"
        }
        node = HTMLNode(props=props)
        output = node.props_to_html()
        self.assertEqual(output, ' href="https://www.google.com" target="_nada" custom="something"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello!")
        self.assertEqual(node.to_html(), "<b>Hello!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click it!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click it!</a>')

    def test_leaf_node_without_tag(self):
        node = LeafNode(tag=None, value="Hello")
        self.assertEqual(node.to_html(), "Hello")

class TestParentNode(unittest.TestCase):
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
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError) as err:
            parent_node = ParentNode("span", None)
            parent_node.to_html()
        self.assertIn("Invalid HTML: children list has no values", str(err.exception))

    def test_to_html_with_no_tag(self):
        with self.assertRaises(ValueError) as err:
            child_node = LeafNode("b", "child")
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()
        self.assertIn("Invalid HTML: no tag provided", str(err.exception))

if __name__ == "__main__":
    unittest.main()