from textnode import TextNode, TextType, BlockType, text_to_textnodes, block_to_block_type, markdown_to_blocks, text_node_to_html_node
from htmlnode import HtmlNode, LeafNode, ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
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
            case BlockType.QUOTE:     tag = "blockquote"
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
            all_parent_nodes.append(LeafNode(tag, block.replace("```", ""), None))
        

    return  ParentNode("div", all_parent_nodes, None)
        

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
