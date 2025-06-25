import feedparser
import requests
import html2text
from piperss import main
from piperss import pipeList
from piperss import pipeDisplay
from piperss import theme
from rich.console import Console
from rich.prompt import Prompt
from readability import Document


console = Console()


def fetch_rss(url):
    feed = feedparser.parse(url)
    if feed.bozo:
        console.print(f"[{theme.theme_error}][X] Failed to parse RSS feed.[/]")
        return None
    return feed


def fetch_full_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        doc = Document(response.text)
        summary_html = doc.summary()
        # Convert HTML to Markdown for better CLI pipeFormat
        text = html2text.html2text(summary_html)
        return text.strip()
    except Exception as e:
        return f"[{theme.theme_error}][Error fetching article: {e}][/]"


def select_feed_and_read():
    pipeList.show_feeds()
    feeds = pipeList.load_feeds()

    while True:

        try:
            feedChoice = Prompt.ask(
                f"[{theme.theme_accent}]Select feed number to read, 'b' to go back, 'q' to quit[/]"
            )

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
                        pipeList.show_articles(feed)
                        choice = Prompt.ask(
                            f"[{theme.theme_accent}]Enter article number to read, 'b' to go back, 'm' for main menu, 'q' to quit[/]"
                        )
                        if choice.lower() == "b":
                            pipeList.show_feeds()
                            break
                        if choice.lower() == "m":
                            main.main_menu()
                            return
                        if choice.lower() == "q":
                            exit(0)
                        if choice.isdigit():
                            idx = int(choice) - 1
                            if 0 <= idx < len(feed.entries[:10]):
                                action = pipeDisplay.display_article(
                                    feed.entries[idx], feed.entries, feed_url
                                )
                                if action == "back_to_articles":
                                    continue
                                elif action == "main_menu":
                                    return
                            else:
                                console.print(
                                    f"[{theme.theme_error}]Invalid article number.[/]"
                                )
                        else:
                            console.print(
                                f"[{theme.theme_error}]Please enter a valid number, 'b', 'm', or 'q'.[/]"
                            )
            else:
                console.print(f"[{theme.theme_error}]Invalid selection.[/]\n")
        except ValueError:
            console.print("[red]Please enter a valid number or option.[/red]\n")
