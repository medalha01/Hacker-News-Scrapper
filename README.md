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

This project provides a tool to scrape the top stories from Hacker News using Python, BeautifulSoup, and requests. It allows users to fetch daily news data, aggregate it, and output the results in either JSON or HTML format.

### Built With

- Python
- BeautifulSoup
- Requests

## Getting Started

To set up this project locally, follow these simple steps.

### Prerequisites

- Python 3
- pip
  ```sh
  pip install beautifulsoup4 requests lxml
  ```
## Usage

To start scraping, run the script with the desired number of days to fetch data and optionally specify the number of worker threads.

  ```sh
  python scraper.py 7 4  # Example: Fetch data for 7 days using 4 threads
  ```

## Roadmap

- [ ] Add support for scraping other sections of Hacker News.
- [ ] Enhance data visualization in the output reports.

## Contributing

We welcome contributions to this project. If you have improvements or bug fixes, feel free to fork the repo and submit a pull request.

## Contact

Isac Martins - isacmartins.1224@gmail.com

Project Link: [https://github.com/medalha01/Hacker-News-Scrapper](https://github.com/medalha01/Hacker-News-Scrapper)

## Acknowledgments

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests: HTTP for Humans](https://requests.readthedocs.io/en/master/)
