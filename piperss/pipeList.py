import os
from piperss import pipeFormat
from piperss import theme
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


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
    urls = Prompt.ask(f"[{theme.theme_accent}]Enter RSS feed URLs (comma-separated)[/]")
    new_list = [url.strip() for url in urls.split(",") if url.strip()]
    feeds = load_feeds()
    feeds.extend(url for url in new_list if url not in feeds)
    save_feeds(feeds)
    console.print(f"[{theme.theme_accent}][+] Feeds added.[/]\n")


def show_feeds():
    feeds = load_feeds()
    if not feeds:
        console.print(
            f"[{theme.theme_error}]No feeds saved yet. Please add some first.[/]\n"
        )
        return feeds

    table = Table(
        title=f"[{theme.theme_title}]Saved Feeds[/]",
        header_style=theme.theme_header,
    )
    table.add_column("No.")
    table.add_column("URL")
    for i, url in enumerate(feeds):
        table.add_row(f"[{theme.theme_accent}]" + str(i + 1) + "[/].", url)
    pipeFormat.print_centered_block(table)


def show_articles(feed):
    table = Table(
        title=f"[{theme.theme_title}]Feed: {feed.feed.get('title', 'No title')}[/]",
        header_style="yellow",
    )
    table.add_column("No.")
    table.add_column("Title")
    for i, entry in enumerate(feed.entries[:10]):
        table.add_row(
            f"[{theme.theme_accent}]" + str(i + 1) + "[/].",
            str(entry.get("title", "No Title")),
        )
    pipeFormat.print_centered_block(table)


def delete_feed():
    feeds = load_feeds()
    if not feeds:
        console.print(f"[{theme.theme_error}]No feeds to delete.[/]\n")
        return

    table = Table(
        title=f"[{theme.theme_title}]Saved Feeds[/]",
        header_style=theme.theme_header,
        border_style=theme.theme_border,
    )
    table.add_column("No.")
    table.add_column("URL")
    for i, url in enumerate(feeds):
        table.add_row(f"[{theme.theme_accent}]" + str(i + 1) + "[/].", url)
    pipeFormat.print_centered_block(table)
    # console.print(table)

    try:
        index = (
            int(
                Prompt.ask(
                    f"[{theme.theme_accent}]Enter the number of the feed to delete, press [ENTER] to cancel[/]"
                )
            )
            - 1
        )
        if 0 <= index < len(feeds):
            removed = feeds.pop(index)
            save_feeds(feeds)
            console.print(f"[{theme.theme_error}][X] Removed:[/] {removed}\n")
        else:
            console.print(f"[{theme.theme_error}]Invalid number.[/]\n")
    except ValueError:
        console.print(f"[{theme.theme_error}]Please enter a valid number.[/]\n")
