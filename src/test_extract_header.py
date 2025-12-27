from main import extract_header_from_md
import unittest


class TestExtractHeader(unittest.TestCase):
    def test_extraction_should_find_header(self):
        md ="""
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts
    """
        header = extract_header_from_md(md)
        self.assertEqual("Tolkien Fan Club",header)
    


