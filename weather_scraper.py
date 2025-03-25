import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
import os

# Month name mapping (Slovak to English and numeric)
MONTH_MAPPING = {
    "Január": {"en": "January", "num": 1},
    "Február": {"en": "February", "num": 2},
    "Marec": {"en": "March", "num": 3},
    "Apríl": {"en": "April", "num": 4},
    "Máj": {"en": "May", "num": 5},
    "Jún": {"en": "June", "num": 6},
    "Júl": {"en": "July", "num": 7},
    "August": {"en": "August", "num": 8},
    "September": {"en": "September", "num": 9},
    "Október": {"en": "October", "num": 10},
    "November": {"en": "November", "num": 11},
    "December": {"en": "December", "num": 12}
}

def scrape_html(url):
    """Scrape weather data from the given URL"""
    response = requests.get(url)
    if response.status_code == 200:
        # Extract year from URL
        year_match = re.search(r'year=(\d{4})', url)
        if not year_match:
            print(f"Could not extract year from URL: {url}")
            return None
        year = year_match.group(1)
        
        # Extract data type from URL
        data_type_match = re.search(r'data=(\w+)', url)
        data_type = data_type_match.group(1) if data_type_match else "unknown"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find("table")
        
        if not table:
            print(f"No table found in {url}")
            return None
        
        # Extract month headers
        month_headers = []
        header_row = table.find("tr")
        if header_row:
            for th in header_row.find_all("th"):
                if th.get('id') and th.get('id').startswith('tc'):
                    month_headers.append(th.text.strip())
        
        # Extract data rows
        entries = []
        for row in table.find_all("tr")[1:]:  # Skip header row
            day_cell = row.find("th")
            if not day_cell or not day_cell.get('id') or not day_cell.get('id').startswith('tr'):
                continue
                
            day = day_cell.text.strip()
            if not day.isdigit():
                continue
                
            # Process each month cell in the row
            for i, month_name in enumerate(month_headers):
                month_num = MONTH_MAPPING.get(month_name, {}).get("num")
                if not month_num:
                    continue
                    
                # Find the corresponding cell (using index+1 because we're skipping the day cell)
                cells = row.find_all(["td", "th"])
                if len(cells) <= i+1:
                    continue
                    
                cell = cells[i+1]
                if not cell.get('class') or 'datacell' not in cell.get('class'):
                    continue
                    
                value_text = cell.text.strip()
                if not value_text:  # Skip empty cells
                    continue
                    
                # Replace comma with dot for decimal values if needed
                value_text = value_text.replace(',', '.')
                
                # Try to convert to float
                try:
                    value = float(value_text)
                except ValueError:
                    continue
                    
                # Create date string in format DD.MM.YYYY
                date_str = f"{int(day):02d}.{month_num:02d}.{year}"
                
                entry = {
                    "date": date_str,
                    "value": value,
                    "data_type": data_type
                }
                entries.append(entry)
        
        if entries:
            print(f"Extracted {len(entries)} entries from {url}")
            return entries
        else:
            print(f"No data entries found in {url}")
            return None
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def generate_urls(base_url, data_types, start_year, end_year):
    """Generate URLs for the given range of years and data types"""
    urls = []
    for year in range(start_year, end_year + 1):
        for data_type in data_types:
            urls.append(f"{base_url}data.php?year={year}&data={data_type}")
    return urls

if __name__ == "__main__":
    base_url = "https://www.pocasiebrezno.sk/"
    data_types = [
        "maxtemp", "mintemp", "avgtemp", "heatdex", "highapp", "lowapp", 
        "highdew", "lowdew", "rainfall", "rainhour", "rainrate", "maxpres", 
        "minpres", "windchill", "windgust", "windspeed", "windrun", 
        "maxhum", "minhum"
    ]
    start_year = 2014
    end_year = 2025
    
    # Create output directory if it doesn't exist
    output_dir = "weather_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Group URLs by data type
    data_type_urls = {}
    for data_type in data_types:
        data_type_urls[data_type] = []
    
    urls = generate_urls(base_url, data_types, start_year, end_year)
    for url in urls:
        data_type_match = re.search(r'data=(\w+)', url)
        if data_type_match:
            data_type = data_type_match.group(1)
            data_type_urls[data_type].append(url)
    
    # Process each data type separately
    for data_type, type_urls in data_type_urls.items():
        print(f"\nProcessing data type: {data_type}")
        data_type_entries = []
        
        for url in type_urls:
            entries = scrape_html(url)
            if entries:
                data_type_entries.extend(entries)
                print(f"Scraped {len(entries)} entries from {url}")
            else:
                print(f"No entries found for {url}")
        
        if data_type_entries:
            # Sort entries by date
            data_type_entries.sort(key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y"))
            
            output_file = os.path.join(output_dir, f"weather_scraped_{data_type}.csv")
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["date", "value", "data_type"])
                writer.writeheader()
                writer.writerows(data_type_entries)
                print(f"Saved {len(data_type_entries)} entries to {output_file}")
        else:
            print(f"No data was scraped for {data_type}.")
