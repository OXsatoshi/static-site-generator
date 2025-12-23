from markdownparser import split_nodes_delimiter,extract_markdown_images ,extract_markdown_links,split_nodes_image
from textnode import TextNode,TextType 
import unittest


class TestHTMLNode(unittest.TestCase):

    def test_parse_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        actual_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ] 
        self.assertEqual(new_nodes,actual_list)
    def test_rase_error_without_closing_delemiter(self):
        node = TextNode("This is text with a code block` word", TextType.TEXT)
        with self.assertRaises(Exception) as exp:
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(str(exp.exception),"delimiter doesnt mutch")

    def test_parse_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        actual_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ] 
        self.assertEqual(new_nodes,actual_list)

    def test_parse_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        actual_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ] 
        self.assertEqual(new_nodes,actual_list)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"

        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev","https://www.boot.dev"),("to youtube","https://www.youtube.com/@bootdotdev")] ,matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_image_at_edges(self):
        node = TextNode(
            "![first](https://link1.com) middle text ![last](https://link2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("first", TextType.IMAGE, "https://link1.com"),
            TextNode(" middle text ", TextType.TEXT),
            TextNode("last", TextType.IMAGE, "https://link2.com"),
        ],
        new_nodes,
    )
    def test_split_single_image(self):
        node = TextNode("![only one](https://only.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("only one", TextType.IMAGE, "https://only.com"),
        ],
        new_nodes,
    )
    def test_split_multiple_nodes(self):
        node1 = TextNode("Text with ![img](https://url.com)", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
        [
            TextNode("Text with ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://url.com"),
            TextNode("Already bold", TextType.BOLD),
        ],
        new_nodes,
    )
