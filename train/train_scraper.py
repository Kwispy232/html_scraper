import requests
from markdownify import markdownify as md
from bs4 import BeautifulSoup
import re
import csv

def scrape_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find("table")

        pattern = re.compile(
            r"(\d{2}\.\d{2}\.\d{4})[\s\S]*?(\d+\.\d+)\s*min\.",
        )

        # Extrahovanie všetkých záznamov
        entries = []
        for match in pattern.finditer(main_content.prettify()):
            entry = {
                "date": match.group(1),
                "time": match.group(2),
            }
            entries.append(entry)

        if entries:
            return entries

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    
def generate_urls(start_year, start_month, end_year, end_month):
        urls = []
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == start_year and month < start_month:
                    continue
                if year == end_year and month > end_month:
                    break
                urls.append(f"https://meskanievlakov.info/informacie/denna-statistika-pohybu-vlakov.cfm?rok={year}&mesiac={month}")
        return urls

if __name__ == "__main__":
    urls = generate_urls(2020, 4, 2025, 3)
    entries = []
    for url in urls:
        new_entries = scrape_html(url)
        entries.append(new_entries)
        if new_entries:
            print(f"Scraped content from {url}")
        else:
            break
        
    with open('train_scraped_entries.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["date", "time"])
        writer.writeheader()
        for entry in entries:
            if entry:
                writer.writerows(entry)



