from blocks import BlockType, block_to_block_type
from splitter import text_to_nodes, markdown_to_blocks
from htmlnode import ParentNode
from textnode import TextNode, TextType

def markdown_to_html_node(text: str) -> ParentNode:

    # receives the full markdown document and converts it to markdown blocks.
    blocks = markdown_to_blocks(text)

    # convert each block into a tuple with (the block, the block's type).
    block_groups = list(map(lambda x: (x, block_to_block_type(x)), blocks))

    # the block in each group is converted into a list of TextNodes
    for i in range(0, len(block_groups)):
        if block_groups[i][1] is BlockType.CODE:
            block_groups[i] = ([TextNode(block_groups[i][0], TextType.NORMAL)], block_groups[i][1])
        else:
            block_groups[i] = (text_to_nodes(block_groups[i][0]), block_groups[i][1])

    # each tuple is converted to a ParentNode, with sepcial behaviour for Code Blocks.
    # child nodes are automatically turned into LeafNode.
    html_nodes = []
    for group in block_groups:
        html_nodes.extend(parent_node_builder(group[0], group[1]))
    return ParentNode("div", html_nodes)

def parent_node_builder(nodes: list[TextNode], block_type: BlockType) -> list[ParentNode]:
    if block_type is BlockType.CODE:
        return [ParentNode("pre", [ParentNode("code", list(map(lambda x: x.to_html_node(), nodes)))])]
    elif block_type is BlockType.ULIST or block_type is BlockType.OLIST:
        # Does not support markdown nested in a list. FIX LATER
        return [ParentNode("p", [ParentNode(type_to_tag(block_type), list(map(lambda x: ParentNode("li", [x.to_html_node()]), split_text_node(nodes[0]))))])]
    else:
        return [ParentNode(type_to_tag(block_type), list(map(lambda x: x.to_html_node(), nodes)))]
    
def split_text_node(node: TextNode) -> list[TextNode]:
    lines = node.text.split("\n")
    new_nodes = []
    for line in lines:
        new_nodes.append(TextNode(line, TextType.NORMAL))
    return new_nodes

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