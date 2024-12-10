from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Path to the CSV file
csv_file_path = r"C:\Users\fedev\OneDrive\Documentos\Letterboxd Showcase\movies.csv"

# User credentials
username = "fvoltes"  # Replace with your Letterboxd username
password = "mortalkombat9"  # Replace with your Letterboxd password

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

try:
    # Open Letterboxd login page
    driver.get("https://letterboxd.com/sign-in/")
    time.sleep(2)

    # Debug: Check page source to ensure login elements are present
    print("Page loaded. Checking for login elements...")

    # Find and interact with login fields
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    print("Login submitted.")
    time.sleep(3)

    # Navigate to "Create a List" page
    driver.get("https://letterboxd.com/list/new/")
    time.sleep(2)

    # Input list title and description
    list_title = "Cartelera Cine Showcase Buenos Aires"
    list_description = "Esta lista ha sido creada automáticamente con Selenium y un archivo CSV de la cartelera UwU"
    driver.find_element(By.NAME, "name").send_keys(list_title)
    driver.find_element(By.NAME, "notes").send_keys(list_description)

    # Read movie titles from the CSV file
    movies_df = pd.read_csv(csv_file_path)
    movie_titles = movies_df["Title"]

     # Add movies to the list
    for title in movie_titles:
        search_box = driver.find_element(By.ID, "frm-list-film-name")
        search_box.send_keys(title)
        time.sleep(1)  # Wait for suggestions to appear
        search_box.send_keys(Keys.RETURN)  # Press Enter to add the movie
        time.sleep(1)  # Ensure the movie is added

        # Clear the input field
        search_box.clear()
        time.sleep(0.5)  # Brief pause before moving to the next movie

    # Save the list
    driver.find_element(By.ID, "list-edit-save").click()
    time.sleep(3)

    print("List created successfully!")

finally:
    # Close the WebDriver
    driver.quit()
