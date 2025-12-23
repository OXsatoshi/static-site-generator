from markdownparser import split_nodes_delimiter 
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


