from textnode import TextNode 
from htmlnode import HTMLNode
def main():
    my_node = TextNode("This some text","link","https://www.boot.dev.com")
    node = HTMLNode("h1")
    print(node)
    print(my_node)

main()
