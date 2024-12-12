import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# cinema billboard URL
billboard_url = "https://entradas.todoshowcase.com/showcase/" 

# paths
csv_file_path = r"C:\\Users\\fedev\\OneDrive\\Documentos\\Letterboxd Showcase\\movies.csv"

# user credentials
username = "fvoltes"  # replaced with my letterboxd username
password = "mortalkombat9"  # replaced with my letterboxd password

# Existing Letterboxd list URL
list_url = "https://letterboxd.com/fvoltes/list/cartelera-cine-showcase-buenos-aires-1/edit/"

def update_csv_from_web():
    """Fetch the live HTML and update the CSV."""
    print("Fetching live cinema billboard data...")
    response = requests.get(billboard_url)
    response.raise_for_status()  

    # parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # extract movies 
    movies = []
    for slide in soup.select('.swiper-slide'):
        try:
            english_title = slide.select_one('.description').text.strip()  # Extracting English title
            genre = slide.select_one('.tagline').text.strip()
            rating = slide.select_one('.hd').text.strip() if slide.select_one('.hd') else "N/A"
            purchase_link = slide.select_one('.play-btn')['href']
            movies.append({
                'Title': english_title,  # Using English title as 'Title'
                'Genre': genre,
                'Rating': rating,
                'Purchase Link': purchase_link,
            })
        except AttributeError:
            continue

    # write to csv
    movies_df = pd.DataFrame(movies)
    movies_df.to_csv(csv_file_path, index=False)
    print(f"CSV updated successfully: {csv_file_path}")

def clear_list(driver):
    """
    Clear all items from the list by iterating through each 'Remove' link.
    """
    try:
        # wait until list items are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.film-list-entry"))
        )
        print("List items loaded.")

        # find all 'Remove' links
        remove_buttons = driver.find_elements(By.CSS_SELECTOR, "a.list-item-remove")
        print(f"Found {len(remove_buttons)} items to remove.")

        # click each 'Remove' link
        for button in remove_buttons:
            button.click()
            time.sleep(1)  # wait a second between clicks to ensure the UI updates
        print("All items removed.")

    except Exception as e:
        print(f"Error clearing the list: {e}")

def update_letterboxd_list():
    """Update an existing Letterboxd list using Selenium."""
    driver = webdriver.Chrome()

    try:
        # open Letterboxd login page
        driver.get("https://letterboxd.com/sign-in/")
        time.sleep(2)

        # log in
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        print("Login submitted.")
        time.sleep(3)

        # navigate to the list edit page
        driver.get(list_url)
        time.sleep(2)

        # clear the list
        clear_list(driver)

        # read updated CSV file
        movies_df = pd.read_csv(csv_file_path)
        movie_titles = movies_df["Title"]

        # add new movies to the list
        for title in movie_titles:
            search_box = driver.find_element(By.ID, "frm-list-film-name")
            search_box.click()  # ensure the box is clicked
            time.sleep(1)  # wait for the input box to be active
            search_box.send_keys(title)
            time.sleep(2)  # wait for suggestions to appear
            search_box.send_keys(Keys.RETURN)  # press Enter to add the movie
            time.sleep(2)  # ensure the movie is added

            # check if the movie was added
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//li[contains(@data-film-name, '{title}')]")
                ))
                print(f"Successfully added: {title}")
            except Exception as e:
                print(f"Failed to add: {title}, skipping.")

            search_box.clear()

        # save the list
        driver.find_element(By.ID, "list-edit-save").click()
        print("List updated successfully!")
        time.sleep(3)

    finally:
        # close the webdriver...
        driver.quit()

# combine the process
def main():
    update_csv_from_web()  # update csv with live data
    update_letterboxd_list()  # update the letterboxd list

if __name__ == "__main__":
    main()