
# Hacker News Scraper

![Contributors](https://img.shields.io/github/contributors/medalha01/Hacker-News-Scrapper.svg?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/medalha01/Hacker-News-Scrapper.svg?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/medalha01/Hacker-News-Scrapper.svg?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/medalha01/Hacker-News-Scrapper.svg?style=for-the-badge)
![MIT License](https://img.shields.io/github/license/medalha01/Hacker-News-Scrapper.svg?style=for-the-badge)

<div align="center">
  <a href="https://github.com/medalha01/Hacker-News-Scrapper">
  </a>

  <h3 align="center">Hacker News Scraper</h3>

  <p align="center">
    A Python script for scraping and analyzing top stories from Hacker News.
    <br />
    <a href="https://github.com/medalha01/Hacker-News-Scrapper"><strong>Explore the Docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/medalha01/Hacker-News-Scrapper">View Demo</a>
    ·
    <a href="https://github.com/medalha01/Hacker-News-Scrapper/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/medalha01/Hacker-News-Scrapper/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

This project provides a tool to scrape the top stories from Hacker News using Python, BeautifulSoup, and aiohttp for asynchronous requests. It allows users to fetch daily news data, store it in a local SQLite database, and output the results in either JSON or HTML format.

### Built With

- Python
- BeautifulSoup
- Aiohttp
- SQLite3

## Getting Started

Follow the instructions below to set up the project on your local machine.

### Prerequisites

Ensure you have Python 3 installed. Install the necessary dependencies using `pip`:

```sh
pip install beautifulsoup4 requests lxml aiohttp
```

### Installation

1. Clone the repo:
    ```sh
    git clone https://github.com/medalha01/Hacker-News-Scrapper.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Hacker-News-Scrapper
    ```

3. Install the required Python libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To start scraping, run the script with the desired number of days to fetch data and specify the type of output (JSON, HTML, or both).

Example command:

```sh
python scraper.py 7  # Fetch top stories from the past 7 days
```

During the execution, you will be prompted to choose the report format:
- `1`: JSON
- `2`: HTML
- `3`: Both

### Example Usage:
```sh
python scraper.py 7  # Fetches data for the last 7 days
```

## Roadmap

- [ ] Add support for scraping other sections of Hacker News.
- [ ] Enhance data visualization in the output reports.
- [ ] Improve error handling and retry mechanism for failed requests.

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or improvements, feel free to fork the repo and submit a pull request.

### Steps to contribute:

1. Fork the Project.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Contact

Isac Martins - isacmartins.1224@gmail.com

Project Link: [https://github.com/medalha01/Hacker-News-Scrapper](https://github.com/medalha01/Hacker-News-Scrapper)

## Acknowledgments

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests: HTTP for Humans](https://requests.readthedocs.io/en/master/)
- [Aiohttp Documentation](https://docs.aiohttp.org/en/stable/)
  
---

This version clarifies usage, installation, and dependencies, aligns the code functionality with the instructions, and ensures consistency throughout.