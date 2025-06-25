import argparse
from piperss.__version__ import __version__
from piperss import pipeList
from piperss import pipeSelection
from piperss import theme
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich.console import Group

console = Console()


def main_menu():
    while True:
        console.clear()
        term_height = console.size.height

        title_panel = Panel(
            Text("PipeRSS", style=theme.theme_title, justify="center"),
            border_style=theme.theme_border,
            width=60,
        )

        menu_text = "\n".join(
            [
                "1. [-] Explore RSS Feeds",
                "2. [+] Add RSS Feed URL(s)",
                "3. [X] Delete RSS Saved Feed",
                "4. [>] Quit",
            ]
        )
        menu_panel = Panel(
            Text(menu_text, justify="left"),
            border_style=theme.theme_border,
            width=60,
        )

        menu_group = Group(title_panel, menu_panel)

        with console.capture() as capture:
            console.print(menu_group)
        lines = capture.get().splitlines()
        vertical_padding = max((term_height - len(lines)) // 2, 0)

        console.print("\n" * vertical_padding, end="")
        console.print(Align.center(menu_group))

        choice = Prompt.ask(
            f"[{theme.theme_accent}]Enter the number of a menu option to continue[/]"
        )

        if choice == "1":
            pipeSelection.select_feed_and_read()
        elif choice == "2":
            pipeList.add_feeds()
        elif choice == "3":
            pipeList.delete_feed()
        elif choice == "4":
            console.print(
                "\n"
                + f"[{theme.theme_accent}]Thank you for using PipeRSS![/]".center(
                    console.size.width
                )
                + "\n"
            )
            break
        else:
            console.print(
                "\n"
                + f"[{theme.theme_error}]Invalid option. Please select 1–4.[/]".center(
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

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"PipeRSS {__version__} Copyright (c) 2025 Keith Henderson. This program may be freely redistributed under the terms of the MIT License.",
    )

    parser.add_argument("--add", action="store_true", help="Add RSS feed URLs")

    parser.add_argument("--list", action="store_true", help="List saved RSS feed URLs")

    parser.add_argument(
        "--read", action="store_true", help="Browse and read articles from saved feeds"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show info about where your feed list is stored",
    )
    args = parser.parse_args()

    if args.add:
        pipeList.add_feeds()
    elif args.list:
        feeds = pipeList.load_feeds()
        if not feeds:
            console.print(f"[{theme.theme_accent}]No feeds saved yet.[/]")
        else:
            table = Table(
                title=f"[{theme.theme_title}]Saved Feeds[/]",
                header_style=theme.theme_header,
            )
            table.add_column("No.")
            table.add_column("URL")
            for i, url in enumerate(feeds):
                table.add_row(str(i + 1), url)
            console.print(table)
    elif args.read:
        pipeSelection.select_feed_and_read()
    elif args.info:
        print(
            "The feed list is stored in ~/.config/piperss.\nIf you already have a list, you can add it there manually."
        )
    else:
        main_menu()


if __name__ == "__main__":
    main()
