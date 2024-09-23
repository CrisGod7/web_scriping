import re
import random
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

class GetProducts:
    def products_amazon(self, url_p, start_page, end_page) -> dict:
        """
    :param url_p:2
    :param start_page:
    :param end_page:
    :return: dict('title', 'price', 'rating')
    """
        data = {"title": [], "price": [], "rate": []}
        HEADERS, PROXIES, session = start_requests()
        """
    Crear un metodo para crear el header, proxies and session. para evitar el bloque de amzaon.
    """
        url = url_p
        for i in range(start_page, end_page):
            print(f'page {i}')
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                print(f"Error: Unable to fetch page {i}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all("a", attrs={
                "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
            links_filters = self.filter_links([link.get('href') for link in links])

            for link in links_filters:
                print(f"link: {link}")
                new_webpage = requests.get("https://amazon.com" + link, headers=HEADERS)
                new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

                data['title'].append(self.get_title(new_soup))
                data['price'].append(self.get_price(new_soup))
                data['rate'].append(self.get_rate(new_soup))
                print(data)
            next_page = get_next_url(url)
            if not next_page:
                break
            url = "https://www.amazon.com" + next_page

        return data
    @staticmethod
    def get_title(soup) -> str:
        """
    :param soup: new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
    :return:Title
    """
        try:
            # <span id="productTitle" class="a-size-large product-title-word-break">        Samsung Galaxy A15 (
            # SM-155M/DSN), 128GB 6GB RAM, Dual SIM, Factory Unlocked GSM, International

            title = soup.find("span", attrs={"id": "productTitle"})
            title_value = title.text
            title_string = title_value.strip()
        except AttributeError:
            title_string = ""
        return title_string

    @staticmethod
    def get_price(soup: BeautifulSoup) -> str:
        try:
            price = soup.find("span", attrs={"class": "a-price-whole"})
            return price.text.strip() if price else ""
        except AttributeError:
            return ""

    @staticmethod
    def get_rate(soup: BeautifulSoup) -> str:
        try:
            rate = soup.find("span", attrs={"class": "a-icon-alt"})
            return rate.text.strip() if rate else ""
        except AttributeError:
            return ""

    @staticmethod
    def filter_links(links: List[str], prefix: str = "/Samsung") -> List[str]:
        return [link for link in links if re.match(f"^{prefix}", link, re.IGNORECASE)]

PROXIES = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
    # Add more proxies here
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    # Add more User-Agents here
]

def get_random_proxy() -> Dict[str, str]:
    return {'http': random.choice(PROXIES), 'https': random.choice(PROXIES)}

def start_requests() -> (Dict[str, str], Dict[str, str], requests.Session):
    delay_request()
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    })
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.5'
    }
    return headers, PROXIES, session

def get_next_url(current_url: str) -> Optional[str]:
    delay_request()
    headers, proxies, session = start_requests()
    try:
        response = session.get(current_url, headers=headers, proxies=proxies)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        next_url = soup.find('a', {'class': 's-pagination-next'})
        return next_url['href'] if next_url and 'href' in next_url.attrs else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def delay_request():
    time.sleep(random.uniform(1, 3))  # Wait between 1 and 3 seconds