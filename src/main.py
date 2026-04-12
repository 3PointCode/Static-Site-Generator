from textnode import TextNode, TextType

def main():
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.google.com")
    print(dummy)

if __name__ == "__main__":
    main()