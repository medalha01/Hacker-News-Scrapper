import requests
from bs4 import BeautifulSoup


def scrape_hacker_news(url):
    """Scrapes the Hacker News website for top stories."""
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    stories = soup.find_all("tr", class_="athing", limit=20)

    news_stories = []

    for story in stories:
        title_tag = story.find("span", class_="titleline").find("a")
        title = title_tag.text
        link = title_tag["href"]

        subtext = story.find_next_sibling("tr").find("td", class_="subtext")
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

        news_stories.append(
            {
                "rank": rank.strip(),
                "title": title,
                "url": link,
                "likes": int(points),
                "n_comments": comments,
            }
        )

    return news_stories
