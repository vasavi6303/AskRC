"""
scraper.py

This module manages the scraping logic for each section of the website. It handles the logic 
for scraping sections based on the current week and ensuring that a new section is added each week.
"""

# Import necessary functions from other modules
from .get_all_url import fetch_and_print_links
from .arrange import arrange_scraped_data
from .utils import get_current_week
import os


# Define the URLs for each section to scrape
section_urls = {}

def read_urls_from_file():
    urls = []
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(cur_dir, "baseURLs.txt")
    with open(file_path, "r" ) as file:
        urls = [line.rstrip() for line in file]
    return urls

def update_section_urls():
    urls = read_urls_from_file()
    for index, url in enumerate(urls):
        section_urls["section-" + str(index + 1)] = [url]


def scrape_sections_up_to_current_week():
    """
    Scrape sections up to and including the current week.

    This function dynamically determines which sections to scrape based on the current week. 
    It fetches links for all sections up to the current week and arranges the scraped content 
    into directories.

    Returns:
        dict: A dictionary of the sections that were scraped in the current run.
    """
    print("Starting the scraping process...")  # Indicate the start of the scraping process
    update_section_urls()
    current_week = get_current_week()  # Calculate the current week based on the start date
    
    # Ensure the current week does not exceed the number of available sections (11)
    max_sections = len(section_urls)  # Maximum number of sections is 11
    if current_week > max_sections:
        current_week = max_sections  # Limit the week to 11 if it exceeds the available sections
    
    # Determine which sections to scrape (based on the current week)
    sections_to_scrape = {f'section-{i}': section_urls[f'section-{i}'] for i in range(1, current_week + 1)}
    print(f"Sections to scrape: {sections_to_scrape}")  # Debug statement to show which sections will be scraped
    
    # Fetch links and arrange the scraped data for the sections
    fetched_links = fetch_and_print_links(sections_to_scrape)
    print(f"Fetched links: {fetched_links}")  # Debug statement to show fetched links
    arrange_scraped_data(fetched_links)
    
    return sections_to_scrape   # Return the sections that were scraped