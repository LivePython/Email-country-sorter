import random
import requests
from bs4 import BeautifulSoup
import re
import time

def scrape_emails_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
        return emails
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

def email_country_sorter(country_code, key_word):
    headers_list = [
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
        {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"},
    ]
    headers = random.choice(headers_list)

    for start in range(0, 50, 10):  
        # Scraping the first 5 pages
        search_urls = [
            f"https://www.google.com/search?q={key_word}+email+site:.{country_code}&start={start}",
            f"https://search.yahoo.com/search?p={key_word}+email+site:.{country_code}"
        ]

        for search_url in search_urls:
            try:
                response = requests.get(search_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a'):
                    print('Scanning...')
                    url = link.get('href')
                    data = set()  

                    if search_url.startswith("https://www.google.com"):
                        if url and url.startswith('/url?q='):
                            actual_url = url.split('/url?q=')[1].split('&')[0]
                            data = scrape_emails_from_url(actual_url)
                            print('Saving emails...', data)
                    
                    elif search_url.startswith("https://yandex.com") or search_url.startswith("https://www.ask.com"):
                        if url and url.startswith('/'):
                            actual_url = url
                            data = scrape_emails_from_url(actual_url)
                            print('Saving emails...', data)

                    if data:
                        # Save collected emails
                        with open(f'{country_code}-{key_word}.txt', 'a') as file:
                            file.write(f'{data}\n')

                        # Pause between requests
                        time.sleep(4)  

            except Exception as e:
                print(f"Error fetching search page: {e}")

def main():
    country_code_v = input("Enter country code ('uk', 'pt', 'ng'): ")
    key_word = input("Enter search keyword: ")
    email_country_sorter(country_code_v, key_word)

if __name__ == '__main__':
    advert = '''
            MAILIONDEV APP
        ======================
         EMAIL COUNTRY SORTER
        ======================
        telegram: @MailionDev
        '''
    print(advert)
    main()
    print('\n')
    print('Complete............')
