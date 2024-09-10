"""
Scraping Data from real Website + Pd
se to pass the HTML code and find the elements inside it
"""

import random
import re
import string
import time
import requests
from bs4 import BeautifulSoup


class GetProducts:

  def products_amazon(self, url_p, start_page, end_page) -> dict:
    """
    :param url_p:
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

      next_page = get_next_url(url)
      if not next_page:
        break
      url = "https://www.amazon.com" + next_page

    return data

  @staticmethod
  def get_title(soup) -> string:
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
  def get_price(soup) -> string:
    """
    :param soup: new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
    :return: price
    """
    try:
      price = soup.find("span", attrs={"class": "a-price-whole"})
      price_str = price.text
      price_str = price_str.strip()
    except AttributeError:
      price_str = ""
    return price_str

  @staticmethod
  def get_rate(soup) -> string:
    """
    :param soup: new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
    :return:
    """
    try:
      rate = soup.find("span", attrs={"class": "a-icon-alt"})
      rate_value = rate.text
      rate_str = rate_value.strip()
    except AttributeError:
      rate_str = ""
    return rate_str

  @staticmethod
  def filter_links(links, prefix="/Samsung") -> list:
    """
    :param links:  links = soup.find_all("a", attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
    :param prefix:  prefix="/Samsung"
    :return: Una nueva lista con los links filtrados.
    """
    """Filtra una lista de links por un prefijo específico.

      Args:
        links: Una lista de strings representando links.
        prefix: El prefijo a buscar|.

      Returns:
        Una nueva lista con los links filtrados.

        re.match(f"^{prefix}", link, re.IGNORECASE):
        Busca si el prefijo prefix (en este caso, "samsung") aparece al inicio del link, ignorando mayúsculas y minúsculas.
        #La list comprehension crea una nueva lista con los links que cumplen la condición.
      """

    filtered_links = [link for link in links if re.match(f"^{prefix}", link, re.IGNORECASE)]
    return filtered_links


def start_requests():
  delay_request()
  session = requests.Session()
  session.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
  })
  USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    # Añade más User-Agents aquí
  ]
  HEADERS = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept-Language': 'en-US,en;q=0.5'
  }
  PROXIES = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
    # Añade más proxies aquí
  }
  return HEADERS, PROXIES, session


def get_next_url(url_actual):
  HEADERS, PROXIES, session = start_requests()

  try:
    response = requests.get(url_actual, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    next_url = soup.find('a', {'class': 's-pagination-next'})

    if next_url and 'href' in next_url.attrs:
      return next_url['href']
    else:
      return None

  except requests.exceptions.RequestException as e:
    print(f"Error al obtener la página: {e}")
  return None

def delay_request():
  """
  Creamos un delay para evitar ser detectados como un bot
  :return:
  """
  time.sleep(random.uniform(1, 3))  # Espera entre 1 y 3 segundos
