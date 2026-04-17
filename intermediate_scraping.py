import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" 
    )
}

def fetching_content(url):
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_book_data(article):
    book_title = article.find("h3").text
    product_element = article.find('div', class_='product_price')
    price = product_element.find('p', class_='price_color').text
    availability_element = product_element.find('p', class_='instock availability')
    available = "Available" if availability_element else "Not Available"

    rating_element = article.find('p', class_='star-rating')
    rating = rating_element['class'][1] if rating_element else "No Rating Found"

    books = {
        "Title": book_title,
        "Price": price,
        "Availability": available,
        "Rating": rating
    }

    return books

def scrape_book(base_url, start_page=1, delay=5):
    data = []
    page_number = start_page

    while True:
        url = base_url.format(page_number)
        print(f"Scraping page: {url}")

        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            articles_elements = soup.find_all("article", class_="product_pod")

            for article in articles_elements:
                book_data = extract_book_data(article)
                data.append(book_data)

            next_button = soup.find("li", class_="next")
            if next_button:
                page_number += 1
                time.sleep(delay)
            else:
                break
        else:
            break
    return data

def main():
    BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = scrape_book(BASE_URL)
    df = pd.DataFrame(all_books)
    print(df.head())
    df.to_csv("books_data.csv", index=False)

if __name__ == "__main__":
    main()