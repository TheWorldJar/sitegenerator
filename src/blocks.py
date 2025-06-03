import re
from enum import Enum


class BlockType(Enum):
    PARA = "paragraph"
    HEAD1 = "heading1"
    HEAD2 = "heading2"
    HEAD3 = "heading3"
    HEAD4 = "heading4"
    HEAD5 = "heading5"
    HEAD6 = "heading6"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"


def block_to_block_type(block: str) -> BlockType:
    # This function assumes we only receive properly formatted markdown.
    # This function does not handle errors for improperly formatted or mixed markdown.

    # The first line of the block must start with 1–6 '#'
    if re.findall(r"^#{1,6}\s", block, re.M):
        if re.findall(r"^#{1}\s", block, re.M):
            return BlockType.HEAD1
        elif re.findall(r"^#{2}\s", block, re.M):
            return BlockType.HEAD2
        elif re.findall(r"^#{3}\s", block, re.M):
            return BlockType.HEAD3
        elif re.findall(r"^#{4}\s", block, re.M):
            return BlockType.HEAD4
        elif re.findall(r"^#{5}\s", block, re.M):
            return BlockType.HEAD5
        elif re.findall(r"^#{6}\s", block, re.M):
            return BlockType.HEAD6

    # The block must be any text starting and ending with '````
    elif re.findall(r"`{3}.*?`{3}", block, re.S):
        return BlockType.CODE

    # The block must have every new line including the first line start with '>'
    elif len(re.findall(r"^>", block, re.M)) == len(block.split("\n")):
        return BlockType.QUOTE

    # The block must have every new line including the first line start with '- '
    elif len(re.findall(r"^-\s", block, re.M)) == len(block.split("\n")):
        return BlockType.ULIST

    # The block must have every new line including the first line start with a number followed by a dot and a space
    elif len(re.findall(r"^\d\.\s", block, re.M)) == len(block.split("\n")):
        return BlockType.OLIST

    # Anything else is a plain paragraph
    else:
        return BlockType.PARA


def prepare_blocks(block: tuple[str, BlockType]) -> tuple[str, BlockType]:
    out = ()
    match block[1]:
        case (
            BlockType.HEAD1
            | BlockType.HEAD2
            | BlockType.HEAD3
            | BlockType.HEAD4
            | BlockType.HEAD5
            | BlockType.HEAD6
        ):
            out = (re.sub(r"^#{1,6}\s", "", block[0]), block[1])
        case BlockType.CODE:
            out = (re.sub(r"`{3}", "", block[0]), block[1])
        case BlockType.QUOTE:
            # This does not support inline >
            out = (re.sub(r">\s|>", "", block[0]), block[1])
        case BlockType.ULIST:
            out = (re.sub(r"-\s", "", block[0]), block[1])
        case BlockType.OLIST:
            out = (re.sub(r"\d\.\s", "", block[0]), block[1])
        case _:
            out = (block[0], block[1])
    return out
