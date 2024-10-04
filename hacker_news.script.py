import sys
import json
import random
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from aiohttp import ClientError
import argparse
import sqlite3


connection = sqlite3.connect("hacker_scrapper.db")

cursor = connection.cursor()


async def batcher(tasks, size=10):
    """
    Batch async tasks to limit concurrency.
    """
    results = []
    for i in range(0, len(tasks), size):
        batch = tasks[i : i + size]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
    return results


async def fetch_url(session, url, retries=8, backoff_factor=2):
    """
    Asynchronously fetch a URL with specified retries and exponential backoff.

    Args:
        session (aiohttp.ClientSession): The session used to make requests.
        url (str): The URL to be fetched.
        retries (int): Number of times to retry on failure.
        backoff_factor (int): Multiplier for exponential backoff.

    Returns:
        str: The text of the response, or None if all retries fail.
    """
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except ClientError:
            if attempt < retries - 1:
                random_factor = random.uniform(0.5, 1.5)
                sleep_time = backoff_factor**attempt * random_factor
                print(
                    f"Attempt {attempt + 1} failed, retrying in {min(sleep_time, 60)} seconds..."
                )
                await asyncio.sleep(min(sleep_time, 60))  # Cap sleep time at 60 seconds
            else:
                print(f"Failed to fetch {url} after {retries} attempts.")
                return None


async def scrape_hacker_news(url):
    """
    Scrapes the Hacker News website for top stories.

    Args:
        url (str): The URL of the Hacker News page.

    Returns:
        list: A list of dictionaries, each containing information about a story.
    """

    news_stories = []

    db_entry = cursor.execute(f"SELECT * FROM hacker WHERE link = '{url}'").fetchall()

    if db_entry:
        for item in db_entry:
            news_stories.append(
                {
                    "rank": item[2],
                    "title": item[1],
                    "link": item[3],
                    "points": item[4],
                    "comments": item[5],
                }
            )
        return news_stories
    async with aiohttp.ClientSession(
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers",
        }
    ) as session:
        response = await fetch_url(session, url)

    if response is None:
        return news_stories

    soup = BeautifulSoup(response, "lxml")

    # Find all story containers (assuming each story is in a 'tr' tag with class 'athing')
    stories = soup.find_all("tr", class_="athing", limit=30)

    for story in stories:
        title_tag = story.find("span", class_="titleline").find("a")
        title = title_tag.text
        link = title_tag["href"]

        domain_tag = story.find("span", class_="sitebit")
        domain = domain_tag.text.strip() if domain_tag else "No domain"

        subtext = story.find_next_sibling("tr").find("td", class_="subtext")
        author = subtext.find("a", class_="hnuser")

        points = (
            subtext.find("span", class_="score").text.split(" ")[0]
            if subtext and subtext.find("span", class_="score")
            else "No points"
        )
        comments = (
            subtext.find("a", text=lambda x: "comment" in x.lower()).text
            if subtext and subtext.find("a", text=lambda x: "comment" in x.lower())
            else "No comments"
        )

        rank_tag = story.find("span", class_="rank")
        rank = rank_tag.text if rank_tag else "No rank"

        # Add the story to the list
        news_stories.append(
            {
                "rank": rank.strip(),
                "title": title,
                "link": link,
                "points": int(points),
                "comments": comments,
            }
        )
        cursor.execute(
            """ INSERT INTO hacker (title, rank, link, points, comments) VALUES (?, ?, ?, ?, ?)""",
            (title, rank, link, points, comments),
        )

    return news_stories


async def process_day(day):
    """
    Processes a specific day to scrape Hacker News.

    Args:
        day (int): The number of days before today to process.

    Returns:
        list: A list of dictionaries containing information about top stories for the day.
    """
    target_date = datetime.now() - timedelta(days=day)

    day_str = target_date.strftime("%d")
    month_str = target_date.strftime("%m")
    year_str = target_date.strftime("%Y")

    url = f"https://news.ycombinator.com/front?day={year_str}-{month_str}-{day_str}"

    return await scrape_hacker_news(url)


def generate_html_report(stories):
    """Generates an HTML report from the list of stories."""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"HackerReport_{now}.html"
    with open(file_name, "w", encoding="utf8") as file:
        file.write("<html><head><title>Hacker News Report</title></head><body>")
        file.write("<h1>Hacker News Report</h1><ul>")
        for story in stories:
            file.write(
                f"<li><a href='{story['link']}'>{story['title']}</a> - {story['points']} points, {story['comments']} comments</li>"
            )
        file.write("</ul></body></html>")
    print(f"HTML report generated: {file_name}")


def generate_json_report(stories):
    """Generates a JSON report from the list of stories."""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"HackerReport_{now}.json"
    with open(file_name, "w", encoding="utf8") as file:
        json.dump(stories, file, indent=4)
    print(f"JSON report generated: {file_name}")


async def main():
    parser = argparse.ArgumentParser(description="Scrape Hacker News for top stories.")
    parser.add_argument(
        "days", type=int, help="Number of days to generate reports for."
    )
    args = parser.parse_args()

    try:
        entry_value = int(
            input(
                "Choose the type of Output for the news report:\n1: JSON\n2: HTML\n3: Both\n"
            )
        )
    except ValueError:
        print("Invalid input. Please enter 1, 2, or 3.")
        sys.exit(1)

    if entry_value < 1 or entry_value > 3:
        print("Invalid input. Please enter 1, 2, or 3.")
        sys.exit(1)

    tasks = [process_day(i) for i in range(args.days)]
    results = await batcher(tasks)

    stories = [story for result in results for story in result]

    sorted_stories = sorted(
        stories, key=lambda x: int(x.get("points", 0)), reverse=True
    )

    if entry_value == 1 or entry_value == 3:
        generate_json_report(sorted_stories)
    if entry_value == 2 or entry_value == 3:
        generate_html_report(sorted_stories)

    connection.commit()
    cursor.close()


if __name__ == "__main__":

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS hacker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        rank TEXT NOT NULL,
        link TEXT NOT NULL,
        points INTEGER NOT NULL,
        comments TEXT NOT NULL
    )
    """
    )

    connection.commit()
    asyncio.run(main())
