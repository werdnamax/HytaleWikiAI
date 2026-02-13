from get_endpoints import url, find_website_navigation_links
from bs4 import BeautifulSoup
import requests
import json
import re
import html2text

junk_selectors = [
    '#mw-navigation', '#footer', '#p-personal', '#p-cactions', 
    '.printfooter', '.catlinks', '#p-search', '.mw-editsection',
    '#toc' # Table of Contents usually isn't needed for RAG
]

def getSampleContent():
    with open('sandbox/scraper_output.json', 'r') as f:
        layer1 = json.load(f)
    return layer1  # Return the first 10 links for sample content

def genContent(links):
    data = []
    for link in links:
        page = requests.get(link)
        if "Special:" in link or "Talk:" in link or "User:" in link or "File:" in link or "Category:" in link:
            continue  # Skip non-content pages
        elif page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            for selector in junk_selectors:
                for elem in soup.select(selector):
                    elem.decompose()  # Remove junk elements from the soup
            content = soup.get_text()
            data.append({
                'url': link,
                'content': content
            })
    return data
        
def clean_text(text):
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    converter.body_width = 0
    return converter.handle(text)


def genSemantics():
    links = getSampleContent()
    content = genContent(links)
    for item in content:
        item['content'] = clean_text(item['content'])
    
    with open('data/semantics/cleaned_content.json', 'w') as f:
        json.dump(content, f, indent=4)
