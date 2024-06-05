import json


def generate_html_report(stories):
    """Generates an HTML report from the list of stories."""
    with open("HackerReport.html", "w", encoding="utf8") as file:
        file.write("<html><head><title>Hacker News Report</title></head><body>")
        file.write("<h1>Hacker News Report</h1><ul>")
        for story in stories:
            file.write(
                f"<li><a href='{story['url']}'>{story['title']}</a> - {story['likes']} points, {story['n_comments']} comments</li>"
            )
        file.write("</ul></body></html>")


def generate_json_report(stories):
    """Generates a JSON report from the list of stories."""
    with open("HackerReport.json", "w", encoding="utf8") as file:
        json.dump(stories, file, indent=4)
