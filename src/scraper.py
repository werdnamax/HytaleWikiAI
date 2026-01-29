from bs4 import BeautifulSoup
import requests

def scrape_website(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    print(soup.prettify())

def main():
    test_url = "http://google.com"
    scrape_website(test_url)

if __name__ == "__main__":
    main()