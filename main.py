import sys
from datetime import datetime
from multiprocessing import Pool

from database import connect_db, get_from_db_by_date, insert_stories
from scraper import scrape_hacker_news
from report import generate_html_report, generate_json_report


def process_day_db(day):
    """Processes a specific day to scrape Hacker News."""
    conn = connect_db()

    now = datetime.now()
    month = now.month
    year = now.year
    actualDay = int(now.day) - day
    while actualDay <= 0:
        month -= 1

        if month == 0:
            month = 12
            year -= 1

        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                actualDay = 29 + actualDay
            else:
                actualDay = 28 + actualDay
        elif month in [4, 6, 9, 11]:
            actualDay = 30 + actualDay
        else:
            actualDay = 31 + actualDay

    day_str = f"0{actualDay}" if actualDay < 10 else str(actualDay)
    month_str = f"0{month}" if month < 10 else str(month)

    url = f"https://news.ycombinator.com/front?day={year}-{month_str}-{day_str}"

    temp_stories = get_from_db_by_date(conn, f"{year}-{month_str}-{day_str}")
    if temp_stories:
        conn.close()
        return temp_stories

    stories = scrape_hacker_news(url)
    insert_stories(conn, f"{year}-{month_str}-{day_str}", stories)
    conn.close()
    return stories


def process_day(day):
    """Processes a specific day to scrape Hacker News."""

    now = datetime.now()
    month = now.month
    year = now.year
    actualDay = int(now.day) - day
    while actualDay <= 0:
        month -= 1

        if month == 0:
            month = 12
            year -= 1

        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                actualDay = 29 + actualDay
            else:
                actualDay = 28 + actualDay
        elif month in [4, 6, 9, 11]:
            actualDay = 30 + actualDay
        else:
            actualDay = 31 + actualDay

    day_str = f"0{actualDay}" if actualDay < 10 else str(actualDay)
    month_str = f"0{month}" if month < 10 else str(month)

    url = f"https://news.ycombinator.com/front?day={year}-{month_str}-{day_str}"

    stories = scrape_hacker_news(url)
    return stories


if __name__ == "__main__":
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

    do_you_want_to_use_db = input("Do you want to use DB? (Y/N): ")
    if do_you_want_to_use_db.lower() == "y":
        process_day = process_day_db

    number_of_days = int(sys.argv[1])

    pool_workers = 1
    if len(sys.argv) == 3:
        pool_workers = int(sys.argv[2])

    with Pool(processes=pool_workers) as pool:
        results = pool.map(process_day, range(number_of_days))

    weekly_stories = [story for sublist in results for story in sublist]
    sorted_news_stories = sorted(weekly_stories, key=lambda x: x["likes"], reverse=True)

    if entry_value != 2:
        generate_json_report(sorted_news_stories)

    if entry_value != 1:
        generate_html_report(sorted_news_stories)

    print("Done!")
