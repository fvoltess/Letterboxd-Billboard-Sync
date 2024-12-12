# Letterboxd Showcase Updater

This repository automates the process of updating a Letterboxd list with the latest movies displayed on a local cinema's billboard. It’s a personal project aimed at saving time by automating a process I used to do manually: checking the billboard for new films and then assessing their quality on Letterboxd.

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

