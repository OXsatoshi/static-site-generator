import unittest
from block import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    
    def test_block_to_block_type_paragraph(self):
        markdown = "This is a simple paragraph of text."
        actual = block_to_block_type(markdown)
        self.assertEqual(BlockType.PARAGRAPH, actual)

    def test_block_to_block_type_heading(self):
        # Test various heading levels
        self.assertEqual(BlockType.HEADING, block_to_block_type("# Heading 1"))
        self.assertEqual(BlockType.HEADING, block_to_block_type("### Heading 3"))
        self.assertEqual(BlockType.HEADING, block_to_block_type("###### Heading 6"))

    def test_block_to_block_type_code(self):
        markdown = "```\nprint('hello world')\n```"
        actual = block_to_block_type(markdown)
        self.assertEqual(BlockType.CODE, actual)

    def test_block_to_block_type_quote(self):
        markdown = "> This is a quote\n> that spans multiple lines"
        actual = block_to_block_type(markdown)
        self.assertEqual(BlockType.QUOTE, actual)

    def test_block_to_block_type_unordered_list(self):
        # Testing both * and - markers
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type("- Item 1\n- Item 2"))

    def test_block_to_block_type_ordered_list(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        actual = block_to_block_type(markdown)
        self.assertEqual(BlockType.ORDERED_LIST, actual)

    def test_block_to_block_type_ordered_list_fail(self):
        # This should fall back to paragraph because the numbers are wrong
        markdown = "1. First item\n3. Wrong number"
        actual = block_to_block_type(markdown)
        self.assertEqual(BlockType.PARAGRAPH, actual)
