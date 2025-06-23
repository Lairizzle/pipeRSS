import feedparser
import requests
from readability import Document
import html2text
from rich.console import Console
from rich.prompt import Prompt
import pipeFormat
import pipeList
import pipeDisplay


console = Console()


def fetch_rss(url):
    feed = feedparser.parse(url)
    if feed.bozo:
        console.print("[red][X] Failed to parse RSS feed.[/red]")
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
        return f"[⚠️ Error fetching article: {e}]"


def select_feed_and_read():
    pipeList.show_feeds()
    feeds = pipeList.load_feeds()

    while True:

        try:
            feedChoice = Prompt.ask(
                "[yellow]Select feed number to read, 'b' to go back, 'q' to quit[/yellow]"
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
                        ##Replace with a table
                        # article_lines = [
                        #     f"Feed: {feed.feed.get('title', 'No title')}",
                        #     "",
                        # ]
                        # for i, entry in enumerate(feed.entries[:10]):
                        #     article_lines.append(f"{i + 1}. {entry.title}")

                        # pipeFormat.print_centered_block(article_lines)

                        choice = Prompt.ask(
                            "[yellow]Enter article number to read, 'b' to go back, 'm' for main menu, 'q' to quit[/yellow]"
                        )
                        if choice.lower() == "b":
                            pipeList.show_feeds()
                            break
                        if choice.lower() == "m":
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
                                console.print("[red]Invalid article number.[/red]")
                        else:
                            console.print(
                                "[red]Please enter a valid number, 'b', 'm', or 'q'.[/red]"
                            )
            else:
                console.print("[red]Invalid selection.[/red]\n")
        except ValueError:
            console.print("[red]Please enter a valid number or option.[/red]\n")
