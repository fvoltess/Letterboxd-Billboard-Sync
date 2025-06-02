from __future__ import annotations

import time
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "user"              
PASSWORD = "password"        
LIST_URL = "https://letterboxd.com/fvoltes/list/cartelera-cine-showcase-buenos-aires-1/edit/"
BILLBOARD_URL = "https://entradas.todoshowcase.com/showcase/"
CSV_PATH: Path = Path(__file__).resolve().parent / "movies.csv"
HEADLESS = False   
VERBOSE = True      
SKIP_SCRAPE = False 

logging.basicConfig(
    level=logging.DEBUG if VERBOSE else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

def parse_movies_from_html(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    movies: list[dict[str, str]] = []
    for slide in soup.select(".swiper-slide"):
        try:
            title = slide.select_one(".description").text.strip()
            genre = slide.select_one(".tagline").text.strip()
            rating_tag = slide.select_one(".hd")
            rating = rating_tag.text.strip() if rating_tag else "N/A"
            link_tag = slide.select_one(".play-btn")
            link = link_tag["href"] if link_tag else ""
            movies.append({
                "Title": title,
                "Genre": genre,
                "Rating": rating,
                "Purchase Link": link,
            })
        except AttributeError:
            continue
    return movies

def update_csv_from_web(url: str, csv_path: Path) -> None:
    log.info("Fetching cinema billboard data …")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    movies = parse_movies_from_html(resp.text)
    pd.DataFrame(movies).to_csv(csv_path, index=False)
    log.info("CSV written → %s", csv_path)

def clear_list(driver: webdriver.Chrome) -> None:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.film-list-entry"))
    )
    while (buttons := driver.find_elements(By.CSS_SELECTOR, "a.list-item-remove")):
        buttons[0].click()
        time.sleep(1)
    log.info("List cleared")


def update_list_description(driver: webdriver.Chrome) -> None:
    textarea = driver.find_element(By.NAME, "notes")
    current = textarea.get_attribute("value")
    timestamp = datetime.now().strftime("Ultima actualizacion: %Y-%m-%d %H:%M:%S")
    if "Ultima actualizacion:" in current:
        updated = "\n".join(
            timestamp if line.startswith("Ultima actualizacion:") else line
            for line in current.splitlines()
        )
    else:
        updated = f"{current}\n{timestamp}"
    textarea.clear()
    textarea.send_keys(updated)

# ---------------------------------------------------------------------------
# Main Selenium workflow
# ---------------------------------------------------------------------------

def update_letterboxd_list(csv_path: Path) -> None:
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://letterboxd.com/sign-in/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(2)

        driver.get(LIST_URL)
        time.sleep(2)
        clear_list(driver)

        for title in pd.read_csv(csv_path)["Title"]:
            box = driver.find_element(By.ID, "frm-list-film-name")
            box.click(); time.sleep(0.4)
            box.send_keys(title); time.sleep(1.2)
            box.send_keys(Keys.RETURN); time.sleep(0.8)
            log.info("Added: %s", title)
            box.clear()

        update_list_description(driver)
        driver.find_element(By.ID, "list-edit-save").click()
        log.info("Letterboxd list saved ✓")
        time.sleep(2)

    finally:
        driver.quit()

# ---------------------------------------------------------------------------
# Entry‑point
# ---------------------------------------------------------------------------

def main() -> None:
    if not SKIP_SCRAPE:
        update_csv_from_web(BILLBOARD_URL, CSV_PATH)
    update_letterboxd_list(CSV_PATH)

if __name__ == "__main__":
    main()
