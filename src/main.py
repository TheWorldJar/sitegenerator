from filemanip import copy_static_to_public
from page import generate_page


def main():
    # md = "1. This\n2. _Is_\n3. A **bold**\n4. Quote\n\nA **bold** choice of _words_!\n\n- ![image1](https://fake.adress.com/image1.png)\n\n```\nThis is a code block\n```\n\n>This\n>Is\n>A\n>Proper\n>Quote"
    # print(markdown_to_html_node(md).to_html())
    copy_static_to_public()
    generate_page("./content/index.md", "template.html", "./public/index.html")


if __name__ == "__main__":
    main()
