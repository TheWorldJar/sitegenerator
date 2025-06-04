import re
from blocks import BlockType, block_to_block_type, prepare_blocks
from splitter import text_to_nodes, markdown_to_blocks
from htmlnode import ParentNode
from textnode import TextNode, TextType


def markdown_to_html_node(text: str) -> ParentNode:

    # receives the full markdown document and converts it to markdown blocks.
    blocks = markdown_to_blocks(text)

    # convert each block into a tuple with (the block, the block's type).
    block_groups = list(map(lambda x: (x, block_to_block_type(x)), blocks))

    block_groups = list(map(prepare_blocks, block_groups))

    # the block in each group is converted into a list of TextNodes
    for i in range(0, len(block_groups)):
        if block_groups[i][1] is BlockType.CODE:
            block_groups[i] = (
                [TextNode(block_groups[i][0], TextType.NORMAL)],
                block_groups[i][1],
            )
        elif block_groups[i][1] is BlockType.ULIST or block_groups[i][1] is BlockType.OLIST:
            new_nodes = []
            if re.findall(r"\n", block_groups[i][0]):
                list_elements = block_groups[i][0].split("\n")
                for element in list_elements:
                    new_nodes.append(TextNode(element, TextType.NORMAL))
                block_groups[i] = (new_nodes, block_groups[i][1])
            else:
                block_groups[i] = (
                [TextNode(block_groups[i][0], TextType.NORMAL)],
                block_groups[i][1],
            )
        else:
            block_groups[i] = (text_to_nodes(block_groups[i][0]), block_groups[i][1])

    # each tuple is converted to a ParentNode, with sepcial behaviour for Code Blocks.
    # child nodes are automatically turned into LeafNode.
    html_nodes = []
    for group in block_groups:
        html_nodes.extend(parent_node_builder(group[0], group[1]))
    return ParentNode("div", html_nodes)


def parent_node_builder(
    nodes: list[TextNode], block_type: BlockType
) -> list[ParentNode]:
    if block_type is BlockType.CODE:
        return [
            ParentNode(
                "pre",
                [ParentNode("code", list(map(lambda x: x.to_html_node(), nodes)))],
            )
        ]
    elif block_type is BlockType.ULIST or block_type is BlockType.OLIST:
        # Does not support markdown nested in a list. FIX LATER
        return [
            ParentNode(
                "p",
                [
                    ParentNode(
                        type_to_tag(block_type),
                        li_nodes_builder(nodes),
                    )
                ],
            )
        ]
    else:
        return [
            ParentNode(
                type_to_tag(block_type), list(map(lambda x: x.to_html_node(), nodes))
            )
        ]


def li_nodes_builder(nodes: list[TextNode]) -> list[ParentNode]:
    li_nodes = []
    for node in nodes:
        new_nodes = text_to_nodes(node.text)
        li_nodes.append(ParentNode("li", list(map(lambda x: x.to_html_node(), new_nodes))))
    return li_nodes


def type_to_tag(block_type: BlockType) -> str:
    match block_type:
        case BlockType.PARA:
            return "p"
        case BlockType.HEAD1:
            return "h1"
        case BlockType.HEAD2:
            return "h2"
        case BlockType.HEAD3:
            return "h3"
        case BlockType.HEAD4:
            return "h4"
        case BlockType.HEAD5:
            return "h5"
        case BlockType.HEAD6:
            return "h6"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.ULIST:
            return "ul"
        case BlockType.OLIST:
            return "ol"
