import os
import argparse
import feedparser
import requests
from readability import Document
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import re
import textwrap
import math
import html2text

console = Console()


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

    return formatted_blocks  # List of blocks (each is a list of lines)


def get_feed_file_path():
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    config_dir = os.path.join(xdg_config_home, "piperss")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "feeds.txt")


def load_feeds():
    feed_file = get_feed_file_path()
    if not os.path.exists(feed_file):
        return []
    with open(feed_file, "r") as f:
        return [line.strip() for line in f if line.strip()]


def save_feeds(feeds):
    feed_file = get_feed_file_path()
    with open(feed_file, "w") as f:
        for feed in feeds:
            f.write(feed + "\n")


def add_feeds():
    urls = Prompt.ask("[cyan]Enter RSS feed URLs (comma-separated)[/cyan]")
    new_list = [url.strip() for url in urls.split(",") if url.strip()]
    feeds = load_feeds()
    feeds.extend(url for url in new_list if url not in feeds)
    save_feeds(feeds)
    console.print("[green][+] Feeds added.[/green]\n")


def delete_feed():
    feeds = load_feeds()
    if not feeds:
        console.print("[yellow]No feeds to delete.[/yellow]\n")
        return

    table = Table(title="Saved Feeds", header_style="bold magenta")
    table.add_column("No.")
    table.add_column("URL")
    for i, url in enumerate(feeds):
        table.add_row(str(i + 1), url)
    console.print(table)

    try:
        index = (
            int(Prompt.ask("Enter the number of the feed to delete, 0 to cancel")) - 1
        )
        if 0 <= index < len(feeds):
            removed = feeds.pop(index)
            save_feeds(feeds)
            console.print(f"[red][X] Removed:[/red] {removed}\n")
        else:
            console.print("[red]Invalid number.[/red]\n")
    except ValueError:
        console.print("[red]Please enter a valid number.[/red]\n")


def fetch_rss(url):
    feed = feedparser.parse(url)
    if feed.bozo:
        console.print("[red][X] Failed to parse RSS feed.[/red]")
        return None
    return feed


def print_centered_block(lines):
    term_width = console.size.width
    term_height = console.size.height

    pad_top = max((term_height - len(lines)) // 2, 0)
    max_len = max(len(line) for line in lines) if lines else 0
    pad_left = max((term_width - max_len) // 2, 0)

    console.clear()
    console.print("\n" * pad_top, end="")

    for line in lines:
        console.print(" " * pad_left + line)


def fetch_full_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        doc = Document(response.text)
        summary_html = doc.summary()
        # Convert HTML to Markdown for better CLI formatting
        text = html2text.html2text(summary_html)
        return text.strip()
    except Exception as e:
        return f"[⚠️ Error fetching article: {e}]"


def display_article(entry, entries, feed_url):
    full_text = fetch_full_article(entry.link)
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

    paragraphs = minimal_markdown_format(paragraphs)

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
    header_text.append(entry.title + "\n", style="bold underline yellow")
    if published_str:
        header_text.append(published_str, style="dim")

    header = Panel(
        header_text,
        title="Article",
        border_style="magenta",
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
                "[bold yellow]Press [Enter] to continue, 'b' to go back, 'm' for menu, or 'q' to quit[/bold yellow]",
                default="",
            )
        else:
            resp = Prompt.ask(
                "[bold yellow]End of article. Press [Enter] to return, 'b' to go back, 'm' for menu, or 'q' to quit[/bold yellow]",
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


def select_feed_and_read():
    feeds = load_feeds()
    if not feeds:
        console.print("[yellow]No feeds saved yet. Please add some first.[/yellow]\n")
        return

    while True:
        lines = ["Saved Feeds", ""]
        for i, url in enumerate(feeds):
            lines.append(f"{i + 1}. {url}")
        lines.append("")
        lines.append(
            "[yellow]Select feed number to read, 'b' to go back, 'q' to quit[/yellow]"
        )

        print_centered_block(lines)

        try:
            feedChoice = Prompt.ask("")

            if feedChoice.lower() == "b":
                break
            if feedChoice.lower() == "q":
                exit(0)

            index = int(feedChoice) - 1
            if 0 <= index < len(feeds):
                feed_url = feeds[index]
                feed = fetch_rss(feed_url)
                if feed:
                    while True:
                        article_lines = [
                            f"Feed: {feed.feed.get('title', 'No title')}",
                            "",
                        ]
                        for i, entry in enumerate(feed.entries[:10]):
                            article_lines.append(f"{i + 1}. {entry.title}")
                        article_lines.append("")
                        article_lines.append(
                            "[yellow]Enter article number to read, 'b' to go back, 'm' for main menu, 'q' to quit[/yellow]"
                        )

                        print_centered_block(article_lines)

                        choice = Prompt.ask("")
                        if choice.lower() == "b":
                            break
                        if choice.lower() == "m":
                            return
                        if choice.lower() == "q":
                            exit(0)
                        if choice.isdigit():
                            idx = int(choice) - 1
                            if 0 <= idx < len(feed.entries[:10]):
                                action = display_article(
                                    feed.entries[idx], feed.entries, feed_url
                                )
                                if action == "back_to_articles":
                                    continue
                                elif action == "main_menu":
                                    return
                            else:
                                console.print("[red]Invalid article number.[/red]")
                        else:
                            console.print(
                                "[red]Please enter a valid number, 'b', 'm', or 'q'.[/red]"
                            )
            else:
                console.print("[red]Invalid selection.[/red]\n")
        except ValueError:
            console.print("[red]Please enter a valid number or option.[/red]\n")


def main_menu():
    while True:
        menu_lines = [
            "PipeRSS Menu",
            "",
            "1. [-] Explore RSS Feeds",
            "2. [+] Add RSS Feed URL(s)",
            "3. [X] Delete RSS Saved Feed",
            "4. [>] Quit",
            "",
            "[yellow]Choose an option[/yellow]",
        ]

        print_centered_block(menu_lines)

        choice = Prompt.ask("")

        if choice == "1":
            select_feed_and_read()
        elif choice == "2":
            add_feeds()
        elif choice == "3":
            delete_feed()
        elif choice == "4":
            console.print(
                "\n" + "Thank you for using PipeRSS!".center(console.size.width) + "\n"
            )
            break
        else:
            console.print(
                "\n"
                + "[red]Invalid option. Please select 1–4.[/red]".center(
                    console.size.width
                )
                + "\n"
            )


def main():
    parser = argparse.ArgumentParser(
        prog="piperss",
        description="PipeRSS - A minimalistic terminal-based RSS reader.",
        epilog="Visit your feeds from the command line with style.",
    )

    parser.add_argument("--version", "-v", action="version", version="PipeRSS 0.1.0")

    parser.add_argument("--add", action="store_true", help="Add RSS feed URLs")

    parser.add_argument("--list", action="store_true", help="List saved RSS feed URLs")

    parser.add_argument(
        "--read", action="store_true", help="Browse and read articles from saved feeds"
    )

    args = parser.parse_args()

    if args.add:
        add_feeds()
    elif args.list:
        feeds = load_feeds()
        if not feeds:
            console.print("[yellow]No feeds saved yet.[/yellow]")
        else:
            table = Table(title="Saved Feeds", header_style="bold magenta")
            table.add_column("No.")
            table.add_column("URL")
            for i, url in enumerate(feeds):
                table.add_row(str(i + 1), url)
            console.print(table)
    elif args.read:
        select_feed_and_read()
    else:
        main_menu()


if __name__ == "__main__":
    main()
