import unittest
from markdownparser import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a simple paragraph.</p></div>")

    def test_heading(self):
        md = "### This is a header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is a header</h3></div>")

    def test_bold_in_paragraph(self):
        md = "This has **bold** text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This has <b>bold</b> text.</p></div>")

    def test_blockquote(self):
        md = "> This is a quote\n> with two lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote with two lines</blockquote></div>")

    def test_unordered_list(self):
        md = "- First item\n- Second item with **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><ul><li>First item</li><li>Second item with <b>bold</b></li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. First\n2. Second"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>First</li><li>Second</li></ol></div>")

    def test_code_block(self):
        md = "```\ncode block here\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>code block here</code></pre></div>")

    def test_mixed_blocks(self):
        md = """
# Main Title

This is a paragraph with _italics_.

* List item 1
* List item 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Main Title</h1><p>This is a paragraph with <i>italics</i>.</p><ul><li>List item 1</li><li>List item 2</li></ul></div>"
        self.assertEqual(html, expected)
