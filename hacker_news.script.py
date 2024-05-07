import requests
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool
import json
import sys
import asyncio
import aiohttp
from aiohttp import ClientError


async def fetch_url(session, url, retries=6):
    """
    Asynchronously fetch a URL with specified retries on failure.

    Args:
        session (aiohttp.ClientSession): The session used to make requests.
        url (str): The URL to be fetched.
        retries (int): Number of times to retry on failure.

    Returns:
        str: The text of the response.

    Raises:
        Exception: Raises an exception if all retries fail.
    """
    for attempt in range(retries):
        try:
            response = await session.get(url)
            response.raise_for_status()  # Will raise an error for 4XX or 5XX status
            return await response.text()
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectionError) as e:
            if attempt < retries - 1:
                await asyncio.sleep(2 * attempt)  # Exponential backoff
            else:
                raise Exception(f"Failed to fetch {url} after {retries} attempts.")


async def scrape_hacker_news(url):
    """
    Scrapes the Hacker News website for top stories.

    Args:
        url (str): The URL of the Hacker News page.

    Returns:
        list: A list of dictionaries, each containing information about a story.
    """
    async with aiohttp.ClientSession(
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
        }
    ) as session:
        response = await fetch_url(session, url)

    soup = BeautifulSoup(response, "lxml")
    # Parsing the HTML

    # Find all story containers (assuming each story is in a 'tr' tag with class 'athing')
    stories = soup.find_all("tr", class_="athing", limit=30)

    # List to hold all stories
    news_stories = []

    # Extracting data from each story
    for story in stories:
        title_tag = story.find("span", class_="titleline").find("a")
        title = title_tag.text
        link = title_tag["href"]

        # Extracting the site domain (optional)
        domain_tag = story.find("span", class_="sitebit")
        domain = domain_tag.text.strip() if domain_tag else "No domain"

        # Extracting the author, points, and comments
        subtext = story.find_next_sibling("tr").find("td", class_="subtext")
        author = subtext.find("a", class_="hnuser")

        subtext = story.next_sibling.find("td", class_="subtext")
        points = (
            subtext.find("span", class_="score").text
            if subtext and subtext.find("span", class_="score")
            else "No points"
        ).split(" ")[0]
        comments = (
            subtext.find("a", text=lambda x: "comment" in x.lower()).text
            if subtext and subtext.find("a", text=lambda x: "comment" in x.lower())
            else "No comments"
        )

        rank_tag = story.find("span", class_="rank")
        rank = rank_tag.text if rank_tag else "No rank"

        # Adding story to the list
        news_stories.append(
            {
                "rank": rank.strip(),
                "title": title,
                "link": link,
                "points": int(points),
                "comments": comments,
            }
        )

    return news_stories


def process_day(day):
    """
    Processes a specific day to scrape Hacker News.

    Args:
        day (int): The number of days before today to process.

    Returns:
        list: A list of dictionaries containing information about top stories for the day.
    """
    print(day)
    now = datetime.now()
    month = now.month
    year = now.year
    actualDay = int(now.day) - day
    while actualDay <= 0:
        month -= 1

        if (
            month == 0
        ):  # If month becomes 0, wrap around to December of the previous year
            month = 12
            year -= 1

        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                actualDay = 29 + actualDay  # Leap year: February has 29 days
            else:
                actualDay = 28 + actualDay

        elif month in [4, 6, 9, 11]:
            actualDay = 30 + actualDay
        else:
            actualDay = 31 + actualDay

    day_str = f"0{actualDay}" if actualDay < 10 else str(actualDay)
    month_str = f"0{month}" if month < 10 else str(month)

    url = f"https://news.ycombinator.com/front?day={year}-{month_str}-{day_str}"
    print(url)
    return scrape_hacker_news(url)


def generate_html_report(stories):
    """Generates an HTML report from the list of stories."""
    with open("HackerReport.html", "w", encoding="utf8") as file:
        file.write("<html><head><title>Hacker News Report</title></head><body>")
        file.write("<h1>Hacker News Report</h1><ul>")
        for story in stories:
            file.write(
                f"<li><a href='{story['link']}'>{story['title']}</a> - {story['points']} points, {story['comments']} comments</li>"
            )
        file.write("</ul></body></html>")


def generate_json_report(stories):
    """Generates a JSON report from the list of stories."""
    with open("HackerReport.json", "w", encoding="utf8") as file:
        json.dump(stories, file, indent=4)


async def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(
            "Usage: python script.py arg1 arg2 \n Where Arg1 is the number of days in the report and Arg2 the number of thread workers (Default = 1)"
        )
        sys.exit(1)
    try:
        entry_value = int(
            input(
                "Choose the type of Output for the news report:\n1: Json\n2: HTML\n3: Both\n"
            )
        )
    except Exception:
        print("Wrong type of input")
        sys.exit(-1)

    if entry_value < 1 or entry_value > 3:
        print("Wrong type of input")

        sys.exit(-1)
    # Get the arguments
    number_of_days = sys.argv[1]

    pool_workers = 1
    if len(sys.argv) == 3:
        pool_workers = sys.argv[2]

    # Get the top 20 Hacker News stories
    ##with Pool(processes=int(pool_workers)) as pool:
    ##    # Map the process_day function to each day in the range
    ##  results = pool.map(process_day, range(int(number_of_days)))
    results = []

    tasks = [process_day(i) for i in range(int(number_of_days))]

    results = await asyncio.gather(*tasks)  # Await all tasks concurrently
    ##for i in range(int(number_of_days)):
    ##    results += process_day(i)

    # Flatten the list of lists into a single list
    weekly_stories = [story for sublist in results for story in sublist]

    sorted_news_stories = sorted(
        weekly_stories, key=lambda x: x["points"], reverse=True
    )

    if entry_value != 2:
        generate_json_report(sorted_news_stories)

    if entry_value != 1:
        generate_html_report(sorted_news_stories)


if __name__ == "__main__":
    asyncio.run(main())
