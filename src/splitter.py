import re
from textnode import TextNode, TextType


def split_by_text(
    text_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    # This function does not allow for nested elements.
    new_nodes = []
    for node in text_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            match (delimiter, text_type):
                case ("**", TextType.BOLD):
                    matches = re.findall(r"\*\*(.*?)\*\*", node.text)
                case ("_", TextType.ITALIC):
                    matches = re.findall(r"\_(.*?)\_", node.text)
                case ("`", TextType.CODE):
                    matches = re.findall(r"\`(.*?)\`", node.text)
                case _:
                    raise Exception(
                        f"Invalid delimiter: {delimiter} for text type: {text_type}"
                    )
            if len(matches) > 0:
                split = node.text.split(matches[0], 1)
                new_nodes.append(TextNode(split[0].strip(delimiter), TextType.NORMAL))
                new_nodes.append(TextNode(matches[0], text_type))
                if split[1] != "" or split[1] != delimiter:
                    new_nodes.append(
                        TextNode(split[1].strip(delimiter), TextType.NORMAL)
                    )
                for i in range(1, len(matches)):
                    split = new_nodes[-1].text.split(matches[i], 1)
                    new_nodes.pop()
                    new_nodes.append(
                        TextNode(split[0].strip(delimiter), TextType.NORMAL)
                    )
                    new_nodes.append(TextNode(matches[i], text_type))
                    if split[1] != "" or split[1] != delimiter:
                        new_nodes.append(
                            TextNode(split[1].strip(delimiter), TextType.NORMAL)
                        )
            else:
                new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text: list[str]) -> list[tuple[str, str]]:
    new_images = []
    for text_chunk in text:
        new_images.extend(re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text_chunk))
    return new_images


def extract_markdown_links(text: list[str]) -> list[tuple[str, str]]:
    new_links = []
    for text_chunk in text:
        new_links.extend(re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text_chunk))
    return new_links


def split_into_images(text_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in text_nodes:
        images = extract_markdown_images([node.text])
        if len(images) > 0:
            split = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.NORMAL))
            new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
            if split[1] != "":
                new_nodes.append(TextNode(split[1], TextType.NORMAL))
            for i in range(1, len(images)):
                split = new_nodes[-1].text.split(
                    f"![{images[i][0]}]({images[i][1]})", 1
                )
                new_nodes.pop()
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.NORMAL))
                new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                if split[1] != "":
                    new_nodes.append(TextNode(split[1], TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes


def split_into_links(text_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in text_nodes:
        links = extract_markdown_links([node.text])
        if len(links) > 0:
            split = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.NORMAL))
            new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
            if split[1] != "":
                new_nodes.append(TextNode(split[1], TextType.NORMAL))
            for i in range(1, len(links)):
                split = new_nodes[-1].text.split(f"[{links[i][0]}]({links[i][1]})", 1)
                new_nodes.pop()
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.NORMAL))
                new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                if split[1] != "":
                    new_nodes.append(TextNode(split[1], TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_nodes(text: str) -> list[TextNode]:
    return split_by_text(
        split_by_text(
            split_by_text(
                split_into_links(split_into_images([TextNode(text, TextType.NORMAL)])),
                "**",
                TextType.BOLD,
            ),
            "_",
            TextType.ITALIC,
        ),
        "`",
        TextType.CODE,
    )


def markdown_to_blocks(text: str) -> list[str]:
    # Splits a full markdown file into its individual blocks
    new_blocks = []
    sections = text.split("\n\n")
    for section in sections:
        # strips leading and trailing spaces and newlines
        # tabs should be preserved for nested lists, I think
        stripped_section = section.strip(" \n")
        if stripped_section != "":
            new_blocks.append(stripped_section)
    return new_blocks

def extract_title(text: str) -> tuple[str, str]:
    split_text = text.split('\n\n')
    if re.findall(r"^#{1}\s", split_text[0]):
        if len(split_text) == 2:
            return (split_text[0].strip(" \n#"), split_text[1])
        else:
            return (split_text[0].strip(" \n#"), "")
    else:
        raise Exception("Document title not found on the fist line!")
