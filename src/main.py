from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
print("hello world")

def main():
    #new = TextNode("Get some text", TextType.LINK, "https://www.boot.dev")
    #new = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    pnode = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(pnode.to_html())
    #print(new.props_to_html())
    #print(new.to_html())

main()
