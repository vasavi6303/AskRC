import requests
from bs4 import BeautifulSoup

def scrape_and_save(urls, output_file="scraped_content.md"):
    """
    Scrape content from a list of URLs and save the content into a .md file with preserved formatting.
    
    Args:
        urls (list): List of URLs to scrape.
        output_file (str): File path to save the scraped content.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for url in urls:
                print(f"Scraping content from: {url}")
                try:
                    response = requests.get(url)
                    print(f"Response code: {response.status_code}")
                    response.raise_for_status()  # Check if the request was successful
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Write the URL as a header for clarity
                    f.write(f"# URL: {url}\n\n")

                    # Process text and script/code separately
                    for element in soup.descendants:
                        # Capture preformatted code blocks
                        if element.name in ["pre", "code"]:
                            code_content = element.get_text(separator="\n", strip=True)
                            f.write(f"```bash\n{code_content}\n```\n\n")
                        # Capture main text content
                        elif element.name == "p" and element.get_text(strip=True):
                            f.write(element.get_text(strip=True) + "\n\n")
                    
                    # Separator between pages
                    f.write("="*80 + "\n\n")
                
                except requests.exceptions.RequestException as e:
                    print(f"Failed to retrieve {url}: {e}")
                    f.write(f"Failed to retrieve content from: {url}\n\n")
                    f.write("="*80 + "\n\n")

        print(f"Scraped content saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred while saving to {output_file}: {e}")


