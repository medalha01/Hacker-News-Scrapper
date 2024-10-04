import requests
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool
import json
import sys
import asyncio
import aiohttp
from aiohttp import ClientError
import random
from datetime import datetime, timedelta

async def batcher(tasks, size = 10):
    return_list = []
    for i in range(0, len(tasks), size):
        batch = tasks[i: i + size]
        results = await asyncio.gather(*batch)
        return_list.append(results)
    return return_list
    


async def fetch_url(session, url, retries=8, backoff_factor=2):
    """
    Asynchronously fetch a URL with specified retries and exponential backoff.

    Args:
        session (aiohttp.ClientSession): The session used to make requests.
        url (str): The URL to be fetched.
        retries (int): Number of times to retry on failure.
        backoff_factor (int): Multiplier for exponential backoff.

    Returns:
        str: The text of the response.

    Raises:
        Exception: Raises an exception if all retries fail.
    """
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                response.raise_for_status()  
                return await response.text()
        except aiohttp.ClientError as e:
            if attempt < retries - 1:
                random_factor = random.uniform(0.5, 1.5) 
                sleep_time = backoff_factor ** attempt * random_factor
                print(f"Attempt {attempt + 1} failed, retrying in {min(sleep_time, 60)} seconds...")
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

    async with aiohttp.ClientSession(
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers"
        }
    ) as session:
        response = await fetch_url(session, url)
    
    if response is None:
        return news_stories
    soup = BeautifulSoup(response, "lxml")
    # Parsing the HTML

    # Find all story containers (assuming each story is in a 'tr' tag with class 'athing')
    stories = soup.find_all("tr", class_="athing", limit=30)


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


"""def process_day(day):

    Processes a specific day to scrape Hacker News.

    Args:
        day (int): The number of days before today to process.

    Returns:
        list: A list of dictionaries containing information about top stories for the day.

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
"""

def process_day(day):
    """
    Processes a specific day to scrape Hacker News.

    Args:
        day (int): The number of days before today to process.

    Returns:
        list: A list of dictionaries containing information about top stories for the day.
    """
    # Calculate the date 'day' days before today
    target_date = datetime.now() - timedelta(days=day)
    
    # Format the day and month to always have two digits
    day_str = target_date.strftime("%d")
    month_str = target_date.strftime("%m")
    year_str = target_date.strftime("%Y")

    # Construct the URL
    url = f"https://news.ycombinator.com/front?day={year_str}-{month_str}-{day_str}"
    
    # Call the scraping function (assuming scrape_hacker_news is already defined)
    return scrape_hacker_news(url)



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
    if len(sys.argv) != 2:
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


    results = []

    tasks = [process_day(i) for i in range(int(number_of_days))]

    results = await batcher(tasks)

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
