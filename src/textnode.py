from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"    #"text"
    BOLD = "bold"    #"**bold**"
    ITALIC = "itlc"  #"_italic_"
    CODE = "code"    #"`code`"
    LINK = "link"    #"[anchor](url)"
    IMG = "imag"     #"![alt](url)"

class BlockType(Enum):
    PARAGRAPH = "para"
    HEADING = "head"
    CODE = "code"
    QUOTE = "quot"
    UNORD_LIST = "ulist"
    ORD_LIST = "olist"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text) 
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)  
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url}) 
        case TextType.IMG:
            prop = {
                "src": text_node.url,
                "alt": text_node.text,
            }
            return LeafNode("img", "", prop)



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list= []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        else:
            if delimiter not in node.text:
                new_list.append(node)
                continue
            
            split_txt = node.text.split(delimiter)
            count = 0
            for section in split_txt:
                count += 1
                if section == "": continue #discard empty segments
                if count % 2 == 0:
                    if text_type != TextType.IMG or text_type != TextType.LINK:
                        new_list.append(TextNode(section, text_type))
                else:
                    new_list.append(TextNode(section, TextType.TEXT))

    return new_list


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            md_tuples = extract_markdown_links(node.text)
            #print(md_tuples)
            if md_tuples == None:
                new_nodes.append(node)
                continue
 
            current_txt = node.text
            for tup in md_tuples:
                split_text = current_txt.split(f"[{tup[0]}]({tup[1]})", 1)
                current_txt = split_text[1]
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(tup[0], TextType.LINK, tup[1]))
            
            if current_txt != "":
                new_nodes.append(TextNode(current_txt, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            md_tuples = extract_markdown_images(node.text)

            if md_tuples == None:
                new_nodes.append(node)
                continue
            
            current_txt = node.text
            for tup in md_tuples:
                split_text = current_txt.split(f"![{tup[0]}]({tup[1]})", 1)
                current_txt = split_text[1]
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(tup[0], TextType.IMG, tup[1]))
            
            if current_txt != "":
                new_nodes.append(TextNode(current_txt, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    re_filter = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #re_filter = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(re_filter, text)

def extract_markdown_links(text):
    re_filter = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #re_filter = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(re_filter, text)

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    split_txt = markdown.split("\n\n")
    valid_strings = []
    for section in split_txt:
        sec_txt = section.strip()
        if sec_txt != "":
            valid_strings.append(sec_txt)

    return valid_strings

def block_to_block_type(block):
    if not isinstance(block, str):
        raise Exception('invalid input')
    
    if block.startswith("#"):
        split_txt = block.split()
        lead_segment = split_txt[0]
        if len(lead_segment) > 6:
            return BlockType.PARAGRAPH
        isHeading = True
        for char in lead_segment:
            if char != "#":
                isHeading = False
                break
        if isHeading: return BlockType.HEADING #, len(lead_segment)

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        split_txt = block.split("\n")
        isQuote = True
        for sec in split_txt:
            if not sec.startswith(">"):
                isQuote = False
                break
        if isQuote: return BlockType.QUOTE

    if block.startswith("- "):
        split_txt = block.split("\n")
        isUnList = True
        for sec in split_txt:
            if not sec.startswith("- "):
                isUnList = False
                break
        if isUnList: return BlockType.UNORD_LIST

    if block.startswith("1."):
        split_txt = block.split("\n")
        isOrdList = True
        for sec in split_txt:
            if not (sec[0].isdigit() and sec[1:].startswith(". ")):
                isQuote = False
                break
        if isOrdList: return BlockType.ORD_LIST

    return BlockType.PARAGRAPH
