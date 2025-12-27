from markdownparser import split_nodes_delimiter,extract_markdown_images ,extract_markdown_links,split_nodes_image,split_nodes_links,text_to_textnodes
from markdownparser import markdown_to_blocks,markdown_to_html_node
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
            "![first](https://link1.com) middle text ![last](https://link2.com) another thing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("first", TextType.IMAGE, "https://link1.com"),
            TextNode(" middle text ", TextType.TEXT),
            TextNode("last", TextType.IMAGE, "https://link2.com"),

            TextNode(" another thing", TextType.TEXT),
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
    def test_split_links(self):
        node = TextNode(
        "Check out [Google](https://www.google.com) and [Boot.dev](https://www.boot.dev)",
        TextType.TEXT,
    )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
        [
            TextNode("Check out ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
        ],
        new_nodes,
    )
    def test_split_links_at_edges(self):
        node = TextNode(
        "[First Link](https://first.com) then text [Last Link](https://last.com)",
        TextType.TEXT,
    )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
        [
            TextNode("First Link", TextType.LINK, "https://first.com"),
            TextNode(" then text ", TextType.TEXT),
            TextNode("Last Link", TextType.LINK, "https://last.com"),
        ],
        new_nodes,
    )
    def test_split_no_links(self):
        node = TextNode("This is just plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)

    
    def test_text_to_textnodes(self):

        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),],nodes,)
    def test_text_to_textnodes(self):
        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], # <--- Make sure there is no ] on the lines above this!
        nodes,
        )
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        pass
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
    )
