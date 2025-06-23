import re
from rich.console import Console
from rich.table import Table
from rich.align import Align

console = Console()


def print_centered_block(content):
    term_height = console.size.height

    if isinstance(content, Table):
        with console.capture() as capture:
            console.print(content)
        rendered = capture.get()
        content_lines = rendered.splitlines()
        block_height = len(content_lines)
        aligned = Align.center(content, vertical="top")  # horizontal only
    else:
        block_height = len(content)
        text = "\n".join(content)
        aligned = Align.center(text, vertical="top")  # horizontal only

    pad_top = max((term_height - block_height) // 2, 0)

    console.clear()
    console.print("\n" * pad_top, end="")  # manual vertical centering
    console.print(aligned)


def minimal_markdown_format(paragraphs):
    formatted_blocks = []
    in_code_block = False

    for para in paragraphs:
        lines = para.splitlines()
        block = []

        for line in lines:
            stripped = line.strip()

            # Toggle code block mode
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                block.append("    " + line)
                continue

            if re.match(r"^#{1,6} ", stripped):
                header_text = re.sub(r"^#{1,6} ", "", stripped).upper()
                underline = "-" * len(header_text)
                block.append(header_text)
                block.append(underline)
                continue

            if stripped.startswith(("- ", "* ", "+ ")):
                block.append("  • " + stripped[2:])
                continue

            m = re.match(r"^(\d+)\. (.*)", stripped)
            if m:
                block.append(f"  {m.group(1)}. {m.group(2)}")
                continue

            if "`" in line:
                line = re.sub(r"`([^`]+)`", r"'\1'", line)

            block.append(line)

        if block:
            formatted_blocks.append(block)

    return formatted_blocks  # List of blocks (each is a lis
