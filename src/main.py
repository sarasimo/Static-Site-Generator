from textnode import TextNode, TextType
print("hello world")

def main():
    new = TextNode("Get some text", TextType.LINK, "https://www.boot.dev")
    print(new)

main()
