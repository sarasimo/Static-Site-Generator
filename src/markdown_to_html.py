from textnode import TextNode, TextType, BlockType, text_to_textnodes, block_to_block_type, markdown_to_blocks, text_node_to_html_node
from htmlnode import HtmlNode, LeafNode, ParentNode
import os


def blocks_to_html_node(blocks):

    all_parent_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH: tag = "p"
            case BlockType.HEADING:
                tag_end = block.index(' ')   
                tag = f"h{tag_end}" #first found space corrisponds to num of #s
                block = block[tag_end+1:]
            case BlockType.CODE:      tag = "code"                
            case BlockType.QUOTE:     
                tag = "blockquote"
                block = clean_quote_block(block)
            case BlockType.UNORD_LIST: tag = "ul"
            case BlockType.ORD_LIST:   tag = "ol"               
        
        if type == BlockType.ORD_LIST or type == BlockType.UNORD_LIST:
            sub_nodes = convert_list_block(block)
            all_parent_nodes.append(ParentNode(tag, sub_nodes, None))
        elif type != BlockType.CODE:   
            txt_nodes = text_to_textnodes(block)
            sub_nodes = textnodes_to_leafnodes(txt_nodes)
            all_parent_nodes.append(ParentNode(tag, sub_nodes, None))
        else:
            code_node = LeafNode(tag, block.replace("```", "").strip())
            all_parent_nodes.append(ParentNode("pre", [code_node], None))
        

    return  ParentNode("div", all_parent_nodes, None)
        

def markdown_to_title_and_content(markdown):
    blocks = markdown_to_blocks(markdown)
    title = extract_title(blocks)
    node = blocks_to_html_node(blocks)
    return title, node.to_html()


#TextNode(text, type, url?)
#LeafNode(tag, value, props?)
def textnodes_to_leafnodes(text_nodes):
    leaf_nodes = []
    for txt_nd in text_nodes:
        html_nd = text_node_to_html_node(txt_nd)
        leaf_nodes.append(html_nd)
    
    return leaf_nodes

def convert_list_block(block):
    split_txt = block.split("\n")
    children = []
    for line in split_txt:
        line = line.strip()
        new_line = str(line[line.index(" "):]).strip()
        txt_nodes = text_to_textnodes(new_line)
        leaf_nodes = textnodes_to_leafnodes(txt_nodes)
        children.append(ParentNode("li", leaf_nodes))

    return children

def clean_quote_block(block):
    split_txt = block.split(">")
    children = []
    for line in split_txt:
        new_line = line.strip()
        if new_line == "": continue
        children.append(new_line)
    new_block = "\n".join(children)
    #print(new_block)
    return new_block

def extract_title(md_blocks):
    if md_blocks[0].startswith("# "):
        title = str(md_blocks[0])
        return title.replace("#", "").strip()
    else: return "Untitled"


