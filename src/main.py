from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_link, block_to_block_type, markdown_to_blocks
from htmlnode import HtmlNode, LeafNode, ParentNode
from markdown_to_html import markdown_to_html_node
import re

#print("hello world")

def main():
  
    md = """
##### Heading 5 

This is **bolded** paragraph

#### heading 4

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

# Heading 1

 1. 1st elemant
 2. second element

 ```
this = that
if that > other:
    this.stop
```

more regular paragraphs for me.
in smae blockk
"""
    #blocks = markdown_to_blocks(md)
    node = markdown_to_html_node(md)

    print("-" * 100)
    
    print(node.to_html())

main()
