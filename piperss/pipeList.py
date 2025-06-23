import os
import pipeFormat
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
    urls = Prompt.ask("[cyan]Enter RSS feed URLs (comma-separated)[/cyan]")
    new_list = [url.strip() for url in urls.split(",") if url.strip()]
    feeds = load_feeds()
    feeds.extend(url for url in new_list if url not in feeds)
    save_feeds(feeds)
    console.print("[green][+] Feeds added.[/green]\n")


def show_feeds():
    feeds = load_feeds()
    if not feeds:
        console.print("[yellow]No feeds saved yet. Please add some first.[/yellow]\n")
        return feeds

    table = Table(title="Saved Feeds", header_style="bold magenta")
    table.add_column("No.")
    table.add_column("URL")
    for i, url in enumerate(feeds):
        table.add_row("[cyan]" + str(i + 1) + "[/cyan].", url)
    pipeFormat.print_centered_block(table)


def show_articles(feed):
    table = Table(
        title=f"Feed: {feed.feed.get('title', 'No title')}", header_style="bold magenta"
    )
    table.add_column("No.")
    table.add_column("Title")
    for i, entry in enumerate(feed.entries[:10]):
        table.add_row(
            "[cyan]" + str(i + 1) + "[/cyan].", str(entry.get("title", "No Title"))
        )
    pipeFormat.print_centered_block(table)


def delete_feed():
    feeds = load_feeds()
    if not feeds:
        console.print("[yellow]No feeds to delete.[/yellow]\n")
        return

    table = Table(title="Saved Feeds", header_style="bold magenta")
    table.add_column("No.")
    table.add_column("URL")
    for i, url in enumerate(feeds):
        table.add_row("[cyan]" + str(i + 1) + "[/cyan].", url)
    pipeFormat.print_centered_block(table)
    # console.print(table)

    try:
        index = (
            int(
                Prompt.ask(
                    "[yellow]Enter the number of the feed to delete, press [ENTER] to cancel[/yellow]"
                )
            )
            - 1
        )
        if 0 <= index < len(feeds):
            removed = feeds.pop(index)
            save_feeds(feeds)
            console.print(f"[red][X] Removed:[/red] {removed}\n")
        else:
            console.print("[red]Invalid number.[/red]\n")
    except ValueError:
        console.print("[red]Please enter a valid number.[/red]\n")
