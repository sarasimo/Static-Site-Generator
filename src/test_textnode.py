import unittest
from textnode import (TextNode, TextType, BlockType,
                      split_nodes_delimiter, split_nodes_link, split_nodes_image,
                      extract_markdown_images, extract_markdown_links,
                      text_to_textnodes, markdown_to_blocks, block_to_block_type)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a node", TextType.LINK, "web.com")
        node2 = TextNode("This is a node", TextType.LINK, "web.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a node", TextType.LINK, "web.com")
        node2 = TextNode("This is a node", TextType.LINK, "myweb.com")
        self.assertNotEqual(node, node2)


class TestSplitNodes(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            """This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)
            check out this one ![cool guy](cool-guy.com/pic) see more [HERE](cool-guy.com/more)"""
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("cool guy", "cool-guy.com/pic")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            """This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)
            check out this one ![cool guy](cool-guy.com/pic) see more [HERE](cool-guy.com/more)"""
        )
        self.assertListEqual([("HERE", "cool-guy.com/more")], matches)

    def test_split_node_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes =[
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_test_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(nodes, expected_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_block_type(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

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
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            type = block_to_block_type(block)
            types.append(type)
        
        expected_types = [
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.UNORD_LIST,
            BlockType.ORD_LIST,
            BlockType.CODE,
            BlockType.PARAGRAPH,
        ]
        self.assertListEqual(types, expected_types)

if __name__ == "__main__":
    unittest.main()
