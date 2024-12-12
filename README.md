# Letterboxd Billboard Sync

This repository automates the process of updating a Letterboxd list with the latest movies displayed on the billboard of a local cinema in Buenos Aires. It’s a personal project designed to save time by automating a task I previously handled manually: checking the cinema's billboard for new films and assessing their quality on Letterboxd. The script is specifically tailored for that cinema.

## Repository Structure

### Files and Folders:

- **`update_letterboxd_list.py`**
  - The main Python script that performs the following functions:
    - Scrapes the Showcase cinema billboard to fetch the latest movie data.
    - Updates a CSV file with the fetched data.
    - Logs into Letterboxd and updates a specific movie list using Selenium.

- **`movies.csv`**
  - A CSV file that stores the current list of movies fetched from the cinema billboard.
  - Updated every time the script is run.

- **`/testing`**
  - A folder containing sample HTML files of different sections of a Letterboxd page, useful for testing the script.

## Features

- **Automated Web Scraping:**
  - Extracts movie details such as title, genre, rating, and purchase link from the Showcase cinema billboard website.

- **CSV Management:**
  - Maintains an up-to-date CSV file with the fetched movie data.

- **Letterboxd List Synchronization:**
  - Logs into Letterboxd, clears the specific list, and repopulates it with movies from the updated CSV.
  - Updates the list description with a timestamp of the last update.

## Requirements

- **Python Libraries:**
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `pandas`

- **Web Driver:**
  - ChromeDriver

