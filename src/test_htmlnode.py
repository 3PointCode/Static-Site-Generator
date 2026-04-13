import unittest

from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()