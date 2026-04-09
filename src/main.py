from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_link, block_to_block_type, markdown_to_blocks
from htmlnode import HtmlNode, LeafNode, ParentNode
from generate_pages import generate_page, generate_all_pages
from managedirectories import copy_directory
import re

#print("hello world")

def main():
  
    md = """
# A beautifil title, the best title.

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
    #title, content = markdown_to_title_and_content(md)

    print("-" * 100)
    
   ##print(content)

    print("-" * 100)

    copy_directory("static", "public")
    generate_all_pages("content", "template.html", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")

main()
