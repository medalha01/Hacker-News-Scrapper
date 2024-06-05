import psycopg2
from psycopg2.extras import execute_values


def connect_db():
    """Connects to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname="HackerNews",
        user="postgres",
        password="mypass",
        host="localhost",
        port="7654",
    )
    return conn


def get_from_db_by_date(dn_connection, date):
    """Gets stories from the PostgreSQL database and returns them as a list of dictionaries."""
    with dn_connection.cursor() as cur:
        cur.execute(
            """
            SELECT title, url, likes, n_comments
            FROM news
            WHERE emission_date = %s
            """,
            (date,),
        )
        rows = cur.fetchall()

        stories = [
            {
                "title": row[0],
                "url": row[1],
                "likes": row[2],
                "n_comments": row[3],
            }
            for row in rows
        ]

        return stories


def get_from_db_by_title(dn_connection, title):
    """Gets stories from the PostgreSQL database."""
    with dn_connection.cursor() as cur:
        cur.execute(
            """
            SELECT title, url, likes, n_comments
            FROM news
            WHERE title = %s
            """,
            (title,),
        )
        return cur.fetchall()


def insert_stories(dn_connection, date, stories):
    """Inserts stories into the PostgreSQL database."""
    with dn_connection.cursor() as cur:
        unique_stories = {story["title"]: story for story in stories}.values()

        execute_values(
            cur,
            """
            INSERT INTO news (title, url, emission_date, likes, n_comments)
            VALUES %s
            ON CONFLICT (title) DO UPDATE SET
                url = EXCLUDED.url,
                emission_date = EXCLUDED.emission_date,
                likes = EXCLUDED.likes,
                n_comments = EXCLUDED.n_comments
            """,
            [
                (
                    story["title"],
                    story["url"],
                    date,
                    story["likes"],
                    story["n_comments"],
                )
                for story in unique_stories
            ],
        )
    dn_connection.commit()
