from enum import Enum
import re
class BlockType(Enum):
    PARAGRAPH = "paragraph" 
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")
    ):
        return BlockType.HEADING

    # Must start and end with ```
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Every line must start with >
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # Every line must start with "* " or "- "
    if block.startswith("* ") or block.startswith("- "):
        for line in lines:
            if not (line.startswith("* ") or line.startswith("- ")):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # Every line must start with "i. " where i starts at 1 and increments
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    # Default to Paragraph
    return BlockType.PARAGRAPH
