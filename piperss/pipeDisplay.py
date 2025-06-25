from piperss import pipeSelection
from piperss import pipeFormat
from piperss import theme
import textwrap
import math
from rich.console import Console
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.align import Align


console = Console()


def display_article(entry, entries, feed_url):
    full_text = pipeSelection.fetch_full_article(entry.link)
    if not full_text.strip():
        full_text = getattr(entry, "summary", "[No summary available]")

    # Normalize line endings
    full_text = full_text.replace("\r\n", "\n").replace("\r", "\n")

    # Split into paragraphs on double newlines
    paragraphs = [p.strip() for p in full_text.split("\n\n") if p.strip()]

    # If still no good paragraphs, split into chunks
    if not paragraphs or (len(paragraphs) == 1 and len(paragraphs[0]) > 1000):
        text = paragraphs[0] if paragraphs else full_text
        chunk_size = 400
        words = text.split()
        current_chunk = []
        current_length = 0
        paragraphs = []

        for word in words:
            if current_length + len(word) > chunk_size and current_chunk:
                paragraphs.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        if current_chunk:
            paragraphs.append(" ".join(current_chunk))

    paragraphs = pipeFormat.minimal_markdown_format(paragraphs)

    # Wrap lines without breaking words or URLs
    wrapper = textwrap.TextWrapper(
        width=80, break_long_words=False, break_on_hyphens=False
    )
    wrapped_lines = []

    for block in paragraphs:  # each block is a list of lines
        for line in block:
            wrapped = wrapper.wrap(line)
            wrapped_lines.extend(wrapped if wrapped else [""])
        wrapped_lines.append("")  # add a blank line between paragraph blocks

    # Remove trailing empty line if any
    if wrapped_lines and not wrapped_lines[-1].strip():
        wrapped_lines.pop()

    reserved_lines = 9  # header, prompt, etc.
    page_size = max(console.size.height - reserved_lines, 10)
    total_lines = len(wrapped_lines)
    total_pages = max(1, math.ceil(total_lines / page_size))
    page = 0

    # Format published time if available
    published_str = ""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        from datetime import datetime

        dt = datetime(*entry.published_parsed[:6])
        published_str = dt.strftime("%B %d, %Y %H:%M")
    elif hasattr(entry, "published"):
        published_str = entry.published

    # Compose header text
    header_text = Text()
    header_text.append(entry.title + "\n", style=theme.theme_title)
    if published_str:
        header_text.append(published_str, style="dim")

    header = Panel(
        header_text,
        title="Article",
        border_style=theme.theme_header,
        padding=(0, 2),
    )

    while True:
        console.clear()
        console.print(Align.center(header))
        console.print()

        start = page * page_size
        end = min(start + page_size, total_lines)
        current_lines = wrapped_lines[start:end]

        # Calculate indent for whole block centering
        max_line_length = (
            max(len(line) for line in current_lines if line.strip())
            if current_lines
            else 0
        )
        term_width = console.size.width
        pad_left = max((term_width - max_line_length) // 2, 0)

        # Print lines with left indent
        for line in current_lines:
            console.print(" " * pad_left + line)

        console.print()

        # Center the page numbers with the same padding as the article text
        page_text = f"--- Page {page + 1}/{total_pages} ---"
        page_padding = max((term_width - len(page_text)) // 2, 0)
        console.print(" " * page_padding + page_text)

        console.print()

        # Navigation prompt
        if end < total_lines:
            resp = Prompt.ask(
                f"[{theme.theme_accent}]Press [Enter] to continue, 'b' to go back, 'm' for menu, or 'q' to quit[/]",
                default="",
            )
        else:
            resp = Prompt.ask(
                f"[{theme.theme_accent}]End of article. Press [Enter] to return, 'b' to go back, 'm' for menu, or 'q' to quit[/]",
                default="",
            )

        resp = resp.lower()
        if resp == "q":
            exit(0)
        elif resp == "m":
            return "main_menu"
        elif resp == "b":
            if page > 0:
                page -= 1
            else:
                return "back_to_articles"
        else:
            if end < total_lines:
                page += 1
            else:
                return "back_to_articles"
