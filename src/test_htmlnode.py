import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()