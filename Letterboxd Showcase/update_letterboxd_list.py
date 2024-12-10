import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Cinema billboard URL
billboard_url = "https://entradas.todoshowcase.com/showcase/"  # Replace with the actual URL

# Paths
csv_file_path = r"C:\Users\fedev\OneDrive\Documentos\Letterboxd Showcase\movies.csv"

# User credentials
username = "fvoltes"  # Replace with your Letterboxd username
password = "mortalkombat9"  # Replace with your Letterboxd password

# Existing Letterboxd list URL
list_url = "https://letterboxd.com/fvoltes/list/cartelera-cine-showcase-buenos-aires-1/edit/"  # Update with the actual edit URL


def update_csv_from_web():
    """Fetch the live HTML and update the CSV."""
    print("Fetching live cinema billboard data...")
    response = requests.get(billboard_url)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract movies (this logic depends on the billboard HTML structure)
    movies = []
    for slide in soup.select('.swiper-slide'):
        try:
            title = slide.select_one('.name').text.strip()
            genre = slide.select_one('.tagline').text.strip()
            rating = slide.select_one('.hd').text.strip() if slide.select_one('.hd') else "N/A"
            description = slide.select_one('.description').text.strip()
            purchase_link = slide.select_one('.play-btn')['href']
            movies.append({
                'Title': title,
                'Genre': genre,
                'Rating': rating,
                'Description': description,
                'Purchase Link': purchase_link,
            })
        except AttributeError:
            continue

    # Write to CSV
    movies_df = pd.DataFrame(movies)
    movies_df.to_csv(csv_file_path, index=False)
    print(f"CSV updated successfully: {csv_file_path}")


def update_letterboxd_list():
    """Update an existing Letterboxd list using Selenium."""
    driver = webdriver.Chrome()

    try:
        # Open Letterboxd login page
        driver.get("https://letterboxd.com/sign-in/")
        time.sleep(2)

        # Log in
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        print("Login submitted.")
        time.sleep(3)

        # Navigate to the existing list edit page
        driver.get(list_url)
        time.sleep(2)

        # Clear all existing entries (optional)
        try:
            clear_button = driver.find_element(By.CLASS_NAME, "js-clear-list")  # Update class name if necessary
            clear_button.click()
            print("Cleared existing list entries.")
            time.sleep(2)
        except Exception as e:
            print(f"Could not clear existing list entries: {e}")

        # Read updated CSV file
        movies_df = pd.read_csv(csv_file_path)
        movie_titles = movies_df["Title"]

        # Add new movies to the list
        for title in movie_titles:
            search_box = driver.find_element(By.ID, "frm-list-film-name")
            search_box.send_keys(title)
            time.sleep(2)  # Wait for suggestions to appear
            search_box.send_keys(Keys.RETURN)  # Press Enter to add the movie
            time.sleep(1)
            search_box.clear()

        # Save the list
        driver.find_element(By.ID, "list-edit-save").click()
        print("List updated successfully!")
        time.sleep(3)

    finally:
        # Close the WebDriver
        driver.quit()


# Combine the process
def main():
    update_csv_from_web()  # Update CSV with live data
    update_letterboxd_list()  # Update the Letterboxd list

if __name__ == "__main__":
    main()
