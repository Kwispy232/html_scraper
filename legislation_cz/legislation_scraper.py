import requests
from bs4 import BeautifulSoup
import csv
import re
import time

url = "https://www.aspi.cz/products/search"

payload = 'pageId=ppoaBXzGwptE1758953884852&ajaxType=paginator_pp&returnType=updateElem&csrfmiddlewaretoken=OZmPHTYVspgl5olmDvwmHMqZEI6E9JK3f3DHJaE1CdhgSQU8obFnDdYWrKuHVxTB&page=1&sorttype=S&aPa=&textsource=SB&searchModulesActiveTab=0&searchModules=&tabModules%5Bpp%5D=pp_uv_mu_vs_eu_cn_pl&tabModules%5Bjud%5D=ju_hi&tabModules%5Blit%5D=ko_li_nv_mo_me_vz_rk&tabModulesId%5Bpp%5D=1_2_9_3_5_19_8&tabModulesId%5Bjud%5D=4_18&tabModulesId%5Blit%5D=13_7_16_12_14_6_10&editFilterGroups%5B4%5D%5BfilterGroupsAttrs%5D%5B0%5D%5Bfilter_group_id%5D=5&editFilterGroups%5B4%5D%5BfilterGroupsAttrs%5D%5B0%5D%5Battrs%5D%5Bhas_license%5D=false&editFilterGroups%5B4%5D%5BfilterGroupsAttrs%5D%5B0%5D%5Battrs%5D%5Bis_new%5D=true&editFilterGroups%5B4%5D%5BfilterGroupsAttrs%5D%5B0%5D%5Battrs%5D%5BpramenGroupId%5D=1&editFilterGroups%5B4%5D%5BfilterGroupsAttrs%5D%5B0%5D%5Battrs%5D%5BpramenExpertJudFilterId%5D=486&editFilterGroups%5B4%5D%5BrenameFilterGroups%5D%5B0%5D%5Bfilter_group_id%5D=5&editFilterGroups%5B4%5D%5BrenameFilterGroups%5D%5B0%5D%5Brename_to%5D=Expertn%C3%AD+judikatura&editFilterGroups%5B4%5D%5BremoveFilterItem%5D%5B0%5D%5Bfilter_group_id%5D=5&editFilterGroups%5B4%5D%5BremoveFilterItem%5D%5B0%5D%5Bitems_ids%5D%5B%5D=0&editFilterGroups%5B4%5D%5BremoveFilterItem%5D%5B1%5D%5Bfilter_group_id%5D=1&editFilterGroups%5B4%5D%5BremoveFilterItem%5D%5B1%5D%5Bitems_ids%5D%5B%5D=486&editFilterGroups%5B4%5D%5BrenameFilterItem%5D%5B0%5D%5Bfilter_group_id%5D=1&editFilterGroups%5B4%5D%5BrenameFilterItem%5D%5B0%5D%5Bitems_ids%5D%5B0%5D%5B%5D=486&editFilterGroups%5B4%5D%5BrenameFilterItem%5D%5B0%5D%5Bitems_ids%5D%5B0%5D%5B%5D=Expertn%C3%AD+judikatura&sorttype_active=S&selMod=none&visibleModuleTitle=P%C5%99edpisy+%C4%8CR&activeModule=pp'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'sk-SK,sk;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Mode': 'cors',
    'Origin': 'https://www.aspi.cz',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15',
    'Content-Length': '1713',
    'Referer': 'https://www.aspi.cz/products/search',
    'Connection': 'keep-alive',
    'Cookie': 'sessionid=2yhh3yp4vkfokzo6yk6kn9mr597306l6; __cmpcccx89963=aCQYaxL-gA6WYB3w1qxlaWRMoE0ahTFGkCMEhgCJRBQ0jKQgwiSW; __cmpconsentx89963=CQYZoDAQYZoDAAferBCSB-FgAAAAAAAAAAigF5wAwAAgJtAXmBecAIBNoC8wAA; _ga=GA1.1.454286041.1758953958; _ga_2SMKZ102PY=GS2.1.s1758953958$o1$g0$t1758953958$j60$l0$h866196866; _gcl_au=1.1.948487665.1758953958; _hjSessionUser_3612559=eyJpZCI6IjgxMGQ2ZGZlLTlkMTYtNWY3ZC05NGQ3LWQ5YzM4NmQxMzEwYSIsImNyZWF0ZWQiOjE3NTg5NTM5NTg2NDgsImV4aXN0aW5nIjpmYWxzZX0=; csrftoken=OZmPHTYVspgl5olmDvwmHMqZEI6E9JK3f3DHJaE1CdhgSQU8obFnDdYWrKuHVxTB',
    'Sec-Fetch-Dest': 'empty',
    'X-CSRFToken': 'OZmPHTYVspgl5olmDvwmHMqZEI6E9JK3f3DHJaE1CdhgSQU8obFnDdYWrKuHVxTB',
    'X-Requested-With': 'XMLHttpRequest',
    'Priority': 'u=3, i'
}

# Initialize list to store all entries
all_entries = []

# Process pages from 1 to 1410
for page in range(1, 1410):
    print(f"\nProcessing page {page}...")
    
    # Update the page number in the payload
    page_payload = payload.replace('page=1', f'page={page}')
    
    # Make the request
    try:
        response = requests.request("POST", url, headers=headers, data=page_payload)
        response.raise_for_status()
        
        # Parse the JSON response
        response_data = response.json()
        
        # Extract the HTML content from the JSON
        html_content = response_data.get('elements', {}).get('#results-ppoaBXzGwptE1758953884852-pp', '')
        
        print(f"Status code: {response.status_code}")
        print(f"Response length: {len(html_content)} characters")
        
        # Save raw response for the first page for inspection
        if page == 1:
            with open('raw_response.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("Saved first page response to raw_response.html")

        if response.status_code == 200:
            # Parse the HTML content with explicit UTF-8 encoding
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all result boxes
            result_boxes = soup.find_all('div', class_='resultBox')
            entries = []
            
            for box in result_boxes:
                try:
                    # Get law number
                    law_number_elem = box.find('span', class_='lawNumber')
                    law_number = law_number_elem.get_text(strip=True) if law_number_elem else 'N/A'
                    
                    # Get title
                    title_elem = box.find('div', class_=lambda x: x and 'wk-lawtextdetails-row' in str(x or ''))
                    title = title_elem.get_text(' ', strip=True) if title_elem else 'N/A'
                    
                    # Get all details
                    details = box.find_all('div', class_=lambda x: x and 'wk-lawtextdetails-row-lawInfo' in str(x or ''))
                    effectivity = 'N/A'
                    
                    for detail in details:
                        detail_text = detail.get_text(' ', strip=True)
                        
                        # Look for 'Účinnosť:' in the text
                        if 'Účinnost:' in detail_text:
                            date_part = detail_text.split('Účinnost:', 1)[1].strip()
                            # Find the first date in the remaining text
                            date_match = re.search(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', date_part)
                            if date_match:
                                effectivity = date_match.group(0)
                                break
                        # Also check for 'účinnosť:' in case of different case
                        elif 'účinnost:' in detail_text:
                            date_part = detail_text.split('účinnost:', 1)[1].strip()
                            date_match = re.search(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', date_part)
                            if date_match:
                                effectivity = date_match.group(0)
                                break
                    
                    # Create entry with proper encoding
                    entry = {
                        'obsah': f"{law_number} - {title}",
                        'datum': effectivity
                    }
                    entries.append(entry)
                    print(f"Page {page}: Added entry: {entry}")
                    
                except Exception as e:
                    print(f"Error processing entry on page {page}: {e}")
                    continue
            
            # Add entries from this page to the main list
            all_entries.extend(entries)
            print(f"Page {page}: Processed {len(entries)} entries")
            
            # Save progress after each page
            with open('scraped_legislation.csv', 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(['obsah', 'datum'])  # Write header
                for entry in all_entries:
                    content = f"{entry['obsah']}".encode('utf-8', 'replace').decode('utf-8')
                    date = f"{entry['datum']}".encode('utf-8', 'replace').decode('utf-8')
                    writer.writerow([content, date])
            
            # Add a small delay to avoid overwhelming the server
            time.sleep(1)
            
        else:
            print(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
            # Continue with next page even if one fails
            continue
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed for page {page}: {e}")
        continue

# Final save with all entries after all pages are processed
if all_entries:
    with open('scraped_legislation.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['obsah', 'datum'])  # Write header
        for entry in all_entries:
            content = f"{entry['obsah']}".encode('utf-8', 'replace').decode('utf-8')
            date = f"{entry['datum']}".encode('utf-8', 'replace').decode('utf-8')
            writer.writerow([content, date])
    print(f"\nSuccessfully saved all {len(all_entries)} entries to scraped_legislation.csv")
else:
    print("No entries were found in any page.")
