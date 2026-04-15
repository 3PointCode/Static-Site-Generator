import unittest

from textnode import TextNode, TextType 
from textnode import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_is_url_none(self):
        node = TextNode("Test", TextType.PLAIN_TEXT)
        self.assertIsNone(node.url)

    def test_neq_text_type(self):
        node = TextNode("This is a different node", TextType.ITALIC)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_a(self):
        node = TextNode("This is a node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})
    
    def test_split_nodes_delimeter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimeter_with_empty_part(self):
        node = TextNode("`code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_raises(self):
        with self.assertRaises(Exception) as err:
            node = TextNode("`code block word", TextType.PLAIN_TEXT)
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Invalid markdown text provided", str(err.exception))

    def test_split_nodes_delimeter_mutiple(self):
        node = TextNode("**This** is **text** with a **bold text** word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.facebook.com)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second link", TextType.LINK, "https://www.facebook.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_with_text_after(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.facebook.com) that's nice",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode("second link", TextType.LINK, "https://www.facebook.com"),
                TextNode(" that's nice", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_no_links(self):
        node = TextNode(
            "There are no links in here",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("There are no links in here", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_link_at_beginning(self):
        node = TextNode(
            "[starting link](https://www.google.com) and no more",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("starting link", TextType.LINK, "https://www.google.com"),
                TextNode(" and no more", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_link_only(self):
        node = TextNode(
            "[only link](https://www.google.com)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_links_with_bold_node(self):
        node = TextNode(
            "[only link](https://www.google.com)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("[only link](https://www.google.com)", TextType.BOLD),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()