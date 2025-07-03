# this script executes on an interval to check new articles in a set of RSS feeds
# and sends the recent articles to a Kindle device via email

from opml import OpmlDocument
from datetime import datetime
from time import mktime
from settings import opml_file_path, output_directory, published_after
import feedparser
import os


def load_opml_file(file_path):
    """
    Load an OPML file and return the parsed document.
    """
    try:
        document = OpmlDocument.load(file_path)
        return document
    except Exception as e:
        print(f"Error loading OPML file: {e}")
        return None


def get_feeds_from_opml(document):
    """
    Extract feeds from the OPML document.
    Returns a list of dictionaries with 'title' and 'xml_url'.
    """
    feeds = []
    for outline in document.outlines:
        if outline.type == "rss" and outline.xml_url:
            feeds.append({"title": outline.title, "xml_url": outline.xml_url})
        else:
            # If the outline has nested outlines, recursively check them
            if outline.outlines:
                nested_feeds = get_feeds_from_opml(outline)
                feeds.extend(nested_feeds)
    return feeds


def fetch_feed_articles(feed_url, published_after=None):
    """
    Fetch articles from a given RSS feed URL.
    Returns a list of articles with 'title' and 'link'.
    """
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries:
            if published_after:
                if (
                    "published_parsed" in entry
                    and datetime.fromtimestamp(mktime(entry.published_parsed))
                    > published_after
                ):
                    articles.append(
                        {
                            "title": entry.title,
                            "link": entry.link,
                            "summary": entry.summary if "summary" in entry else "",
                            "content": entry.content if "content" in entry else "",
                        }
                    )
            else:
                # If no date filter is applied, include all articles
                articles.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary if "summary" in entry else "",
                        "content": entry.content if "content" in entry else "",
                    }
                )
        return articles
    except Exception as e:
        print(f"Error fetching feed articles {feed_url}: {e}")
        return []


def main():
    # Load the OPML file
    document = load_opml_file(opml_file_path)

    if document:
        # Extract feeds from the OPML document
        feeds = get_feeds_from_opml(document)
        print(f"Total feeds found: {len(feeds)}")
        for feed in feeds:
            print(f"Feed Title: {feed['title']}, URL: {feed['xml_url']}")
        # Fetch articles from each feed
        for feed in feeds:
            articles = fetch_feed_articles(feed["xml_url"], published_after)
            if articles:
                print(f"Articles from {feed['title']}:")
                for article in articles:
                    print(f"- {article['title']} ({article['link']}))")
                # create an HTML file for each feed containing the articles content
                all_content = "\n".join(
                    f"<h2>{article['title']}</h2><br /><div>{article['content']}</div><br /><br /><hr />"
                    for article in articles
                )
                # Create output directory if it doesn't exist
                os.makedirs(output_directory, exist_ok=True)
                with open(
                    f"{output_directory}/{feed['title'].replace(' ', '_')}.html",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(all_content)

            else:
                print(f"No articles found for {feed['title']}.")
    else:
        print("No feeds found or error loading OPML file.")


if __name__ == "__main__":
    main()
