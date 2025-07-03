# Scan a set of RSS feeds defined in an OPML file,
# and sends the recent articles to a Kindle device via email

from opml import OpmlDocument
from datetime import datetime
from time import mktime
from settings import opml_file_path, output_directory, published_after
import feedparser
import os
import logging


def load_opml_file(file_path):
    """
    Load an OPML file and return the parsed document.
    """
    try:
        document = OpmlDocument.load(file_path)
        return document
    except Exception as e:
        logging.error(f"Error loading OPML file: {e}")
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
        logging.error(f"Error fetching feed articles {feed_url}: {e}")
        return []


def save_to_file(content, feed_title) -> str:
    """
    Save the content to an HTML file in the output directory.
    The file is named after the feed title.
    """
    file_name = f"{feed_title.replace(' ', '_')}.html"
    file_path = os.path.join(output_directory, file_name)
    logging.info(f"Saving content to {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def collect() -> [str]:
    # Load the OPML file
    document = load_opml_file(opml_file_path)
    generated_files = []

    if document:
        # Extract feeds from the OPML document
        feeds = get_feeds_from_opml(document)
        logging.info(f"Total feeds found: {len(feeds)}")
        for feed in feeds:
            logging.info(f"Feed Title: {feed['title']}, URL: {feed['xml_url']}")
        # Fetch articles from each feed
        for feed in feeds:
            articles = fetch_feed_articles(feed["xml_url"], published_after)
            if articles:
                logging.info(f"Articles from {feed['title']}:")
                for article in articles:
                    logging.info(f"- {article['title']} ({article['link']}))")
                # create an HTML file for each feed containing the articles content
                all_content = "\n".join(
                    f"<h2>{article['title']}</h2><br /><div>{article['content']}</div><br /><br /><hr />"
                    for article in articles
                )
                file_path = save_to_file(all_content, feed["title"])
                generated_files.append(file_path)
            else:
                logging.info(f"No articles found for {feed['title']}.")
    else:
        logging.info("No feeds found or error loading OPML file.")
    return generated_files
