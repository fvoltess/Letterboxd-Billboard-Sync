import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

# cinema billboard URL
billboard_url = "https://entradas.todoshowcase.com/showcase/" 

# paths
csv_file_path = r"C:\\Users\\fedev\\OneDrive\\Documentos\\Letterboxd Showcase\\movies.csv"

# user credentials
username = "letterboxd_username"  # replaced with my letterboxd username
password = "letterboxd_password"  # replaced with my letterboxd password

# letterboxd list url
list_url = "https://letterboxd.com/fvoltes/list/cartelera-cine-showcase-buenos-aires-1/edit/"

def update_csv_from_web():
    """fetch the live HTML and update the CSV."""
    print("Fetching live cinema billboard data...")
    response = requests.get(billboard_url)
    response.raise_for_status()  

    # parse the html
    soup = BeautifulSoup(response.text, 'html.parser')

    # extract movies 
    movies = []
    for slide in soup.select('.swiper-slide'):
        try:
            english_title = slide.select_one('.description').text.strip()  # extracting english title
            genre = slide.select_one('.tagline').text.strip()
            rating = slide.select_one('.hd').text.strip() if slide.select_one('.hd') else "N/A"
            purchase_link = slide.select_one('.play-btn')['href']
            movies.append({
                'Title': english_title,  # using english title as 'Title'
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
    clear all items from the list by iterating through each 'remove' link.
    """
    try:
        # wait until list items are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.film-list-entry"))
        )
        print("List items loaded.")

        # find all 'remove' links
        remove_buttons = driver.find_elements(By.CSS_SELECTOR, "a.list-item-remove")
        print(f"Found {len(remove_buttons)} items to remove.")

        # click each 'remove' link
        for button in remove_buttons:
            button.click()
            time.sleep(1)  # wait a second between clicks to ensure the ui updates
        print("All items removed.")

    except Exception as e:
        print(f"Error clearing the list: {e}")

def update_list_description(driver):
    """
    update the list description with the last update timestamp.
    """
    try:
        # locate the description textarea using the 'name' attribute
        description_textarea = driver.find_element(By.NAME, "notes")
        
        # read the current description
        current_description = description_textarea.get_attribute("value")
        
        # replace the existing "última actualizacion" line or add it if it doesn't exist
        last_update = datetime.now().strftime("Ultima actualizacion: %Y-%m-%d %H:%M:%S")
        if "Ultima actualizacion:" in current_description:
            updated_description = "\n".join(
                line if not line.startswith("Ultima actualizacion:") else last_update
                for line in current_description.splitlines()
            )
        else:
            updated_description = f"{current_description}\n{last_update}"
        
        # update the textarea with the new description
        description_textarea.clear()
        description_textarea.send_keys(updated_description)
        
        print("Description updated successfully.")
    except Exception as e:
        print(f"Error updating the description: {e}")

def update_letterboxd_list():
    """update an existing Letterboxd list using selenium."""
    driver = webdriver.Chrome()

    try:
        # open Letterboxd login page
        driver.get("https://letterboxd.com/sign-in/")
        time.sleep(1)

        # log in
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        print("Login submitted.")
        time.sleep(2)

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
            time.sleep(1)  # ensure the movie is added

            # check if the movie was added
            if title.lower() in driver.page_source.lower():
                print(f"Successfully added: {title}")
            else:
                print(f"Failed to verify addition of: {title}, skipping.")

            search_box.clear()

        # update the list description with the last update timestamp
        update_list_description(driver)

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
