import requests
from markdownify import markdownify as md
from bs4 import BeautifulSoup
import re
import csv

def scrape_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find(id="main-content")

        pattern = re.compile(
            r"(Dňa \d{2}\.\d{2}\.\d{4}.*?)(?:\s+(\[.*?\]\(.*?\)))?\s+(\*\d{2}\.\s*\d{2}\.\s*\d{4}\*)",
        )

        # Extrahovanie všetkých záznamov
        entries = []
        preaty_md = md(main_content.prettify())
        for match in pattern.finditer(preaty_md):
            entry = {
                "obsah": match.group(1) + match.group(2),
                "datum": match.group(3).replace("*", "").strip(),
            }
            entries.append(entry)

        if entries:
            return entries

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    base_url = "https://www.minv.sk/?ros_monitoring_aktuality"
    urls = [f"{base_url}&stranka={i}" for i in range(1, 116)]
    entries = []
    for url in urls:
        new_entries = scrape_html(url)
        entries.append(new_entries)
        if new_entries:
            print(f"Scraped content from {url}")
        else:
            break
    with open('scraped_entries.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["obsah", "datum"])
        writer.writeheader()
        for entry in entries:
            if entry:
                writer.writerows(entry)
    # print(entries)
