from bs4 import BeautifulSoup
import requests
import json

__author__ = "Josh Garbi"
__sources__ = ["Hytale Wiki", "https://hytalewiki.org/", "GPT-4"]
__Date__ = "2026-01-29"

url = 'https://hytalewiki.org/'

def find_website_navigation_links(url, hclass=None):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        nav_links = []
        for item in soup.find_all(class_=hclass):
            link = item.find('a')
            if link and link.has_attr('href'):
                nav_links.append(link['href'])
        return nav_links
    

def gen_links(links):
    _links = []
    for link in links:
        if link.startswith('/'):
            link = url + link[1:]
            _links.append(link)

    return _links

layer1 = gen_links(find_website_navigation_links(url, 'mw-list-item'))
print('Layer 1 Links Found:', len(layer1))

with open('sandbox/scraper_output.json', 'w') as f:
    json.dump(layer1, f, indent=4)

layer2 = []
i = 0
for link in layer1:
    print(f'Processing Layer 2 Link {i+1}/{len(layer1)}: {link}', end='\r', flush=True)
    layer2_d = gen_links(find_website_navigation_links(link)) if find_website_navigation_links(link) else []
    for layer2_d_link in layer2_d:
        layer2.append(layer2_d_link)
    i += 1

layer2 = list(set(layer2))  # Remove duplicates

with open('sandbox/scraper_output_layer2.json', 'w') as f:
    json.dump(layer2, f, indent=4)

layer3 = []
total = 0

for link in layer2:
    print(f'Links Processed: {total} | Processing Layer 3 Link: {link}', end='\r', flush=True)
    layer3_d = gen_links(find_website_navigation_links(link)) if find_website_navigation_links(link) else []
    for layer3_d_link in layer3_d:
        layer3.append(layer3_d_link)
        total += 1

layer3 = list(set(layer3))  # Remove duplicates

with open('sandbox/scraper_output_layer3.json', 'w') as f:
    json.dump(layer3, f, indent=4)