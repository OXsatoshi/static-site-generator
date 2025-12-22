from htmlnode import HTMLNode

import unittest


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        exprect = ' href="https://www.google.com" target="_blank"' 
        my_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=my_props)
        actual = node.props_to_html()
        self.assertEqual(exprect,actual)
    def test_props_to_html_none(self):
        node = HTMLNode(props = None)
        self.assertEqual(node.props_to_html(),"")
