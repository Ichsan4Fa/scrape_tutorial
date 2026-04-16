import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS ={
    "User-Agent":(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}

def extract_tourism_data(section):
    tourist_dest = section.find("h3").text
    dest_description = section.find("p").text.replace("\n", " ").strip()
    pict_url = section.find('img')['src']

    return {
        "Tourist Destination": tourist_dest,
        "Description": dest_description,
        "Picture URL": pict_url
    }

def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None 
    
def scrape_tourism_data(url):
    content = fetch_page_content(url)
    if not content:
        return []

    soup = BeautifulSoup(content, "html.parser")
    data = []
    articles = soup.find("article", id='wisata', class_='card')
    if articles:
        sections = [desc for desc in articles.descendants if desc.name == "section"]
        for section in sections:
            tourism_data = extract_tourism_data(section)
            data.append(tourism_data)
    return data

def main():
    url = "https://halaman-profil-bandung-grid.netlify.app/"
    tourism_data = scrape_tourism_data(url)
    if tourism_data:
        df = pd.DataFrame(tourism_data)
        print(df)
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
