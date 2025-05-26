import re
from textnode import TextNode, TextType

def split_into_nodes(text: list[str], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for text_chunk in text:
        if text_type not in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
            new_nodes.append(TextNode(text_chunk, text_type))
        else:
            if (delimiter == "**" and text_type == TextType.BOLD) or \
                (delimiter == "_" and text_type == TextType.ITALIC) or \
                (delimiter == "`" and text_type == TextType.CODE):
                new_nodes.extend(map(lambda x: TextNode(x, text_type), text_chunk.split(delimiter)))
            else:
                raise Exception(f"Invalid delimiter: {delimiter} for text type: {text_type}")
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