from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_link, block_to_block_type, markdown_to_blocks
from htmlnode import HtmlNode, LeafNode, ParentNode
from generate_pages import generate_page, generate_all_pages
from managedirectories import copy_directory
import sys



def main():
    print("-" * 100)
  
    arguments = sys.argv
    if len(arguments) > 1: 
        basepath = arguments[1]
        dest_directory = "docs"
    else: #for local testing
        basepath = "/"
        dest_directory = "public" 

    print(basepath)
    print("-" * 100)

    #copies images and css 
    copy_directory("static", "docs") 
    #converts .md content to html places them in page template and writes files to public dir
    src_directory = "content"
    
    generate_all_pages(src_directory, "template.html", dest_directory, basepath)
    

main()
