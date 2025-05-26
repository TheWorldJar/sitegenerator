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

def split_into_images(text_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in text_nodes:
        images = extract_markdown_images([node.text])
        if len(images) > 0:
            split = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            new_nodes.append(TextNode(split[0], TextType.NORMAL))
            new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
            if split[1] != "":
                new_nodes.append(TextNode(split[1], TextType.NORMAL))
            for i in range (1, len(images)):
                split = new_nodes[-1].text.split(f"![{images[i][0]}]({images[i][1]})", 1)
                new_nodes.pop()
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
            new_nodes.append(TextNode(split[0], TextType.NORMAL))
            new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
            if split[1] != "":
                new_nodes.append(TextNode(split[1], TextType.NORMAL))
            for i in range (1, len(links)):
                split = new_nodes[-1].text.split(f"[{links[i][0]}]({links[i][1]})", 1)
                new_nodes.pop()
                new_nodes.append(TextNode(split[0], TextType.NORMAL))
                new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                if split[1] != "":
                    new_nodes.append(TextNode(split[1], TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes
