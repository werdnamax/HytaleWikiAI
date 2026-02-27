from get_endpoints import url, find_website_navigation_links
from bs4 import BeautifulSoup
import requests
import json
import re
import html2text
from concurrent.futures import ThreadPoolExecutor, as_completed
# Assisted by gemini for cleaner troubleshooting and junk selector identification
# 2/24/26 - new process by gemini to make the process much faster with some parrallel processing

session = requests.Session()

junk_selectors = [
    '#mw-navigation', '#footer', '#p-personal', '#p-cactions', 
    '.printfooter', '.catlinks', '#p-search', '.mw-editsection',
    '#toc' # Table of Contents usually isn't needed for RAG
]

def getSampleContent():
    with open('data/endpoints/scraper_output_layer3.json', 'r') as f:
        layer1 = json.load(f)
    return layer1  

def clean_html_to_text(html_content):
    """Refined cleaning: Uses BS4 for pruning and html2text for formatting."""
    soup = BeautifulSoup(html_content, 'lxml') # 'lxml' is faster than 'html.parser'
    
    for selector in junk_selectors:
        for elem in soup.select(selector):
            elem.decompose()
            
    # Convert the cleaned soup back to string for html2text
    clean_html = str(soup)
    
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    converter.body_width = 0
    return converter.handle(clean_html)

def process_link(link):
    """Worker function for a single URL."""
    # Fast-fail for non-content links
    if any(x in link for x in ["Special:", "Talk:", "User:", "File:", "Category:"]):
        return None

    try:
        # Reduced timeout so one hung site doesn't stall the whole script
        response = session.get(link, timeout=10)
        if response.status_code == 200:
            content = clean_html_to_text(response.text)
            return {'url': link, 'content': content}
    except Exception as e:
        print(f"\nError processing {link}: {e}")
    
    return None

def genSemantics():
    links = getSampleContent() # Assuming this returns your 15k links
    data = []
    
    print(f"Starting crawl of {len(links)} links...")
    
    # max_workers=20 is a safe start; move to 50 if the server allows it
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Map the process_link function to all links
        future_to_url = {executor.submit(process_link, link): link for link in links}
        
        completed = 0
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                data.append(result)
            
            completed += 1
            if completed % 10 == 0:
                print(f"Progress: {completed}/{len(links)} links processed", end='\r')

    with open('data/semantics/cleaned_content.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    print("\nScraping complete.")