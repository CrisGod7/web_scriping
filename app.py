"""
Scraping Data from real Website + Pd
se to pass the HTML code and find the elements inside it
"""
import csv
import string
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from io import StringIO


class get_products:

    def products_amazon(self, url_p, start_page, end_page) -> dict:
        """
        :param HEADERS: user
        :param end_page: page number end
        :param start_page: page number start
        :param url_p: url principal
        :return: dic with product name , price and rate
        """
        data = {"title": [], "price": [], "rate": []}
        l = []
        HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/127.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.5'})
        url = url_p
        # Headers for request
        for i in range(start_page, end_page):
            url = self.get_urls(url, start_page, end_page)
            print(url)
            response = requests.get(url, headers=HEADERS)
            # Soup object containing all data
            soup = BeautifulSoup(response.content, 'html.parser')
            # find all is find all the tags available inside our page that we joust extracted where the class name is "
            # class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" "

            links = soup.find_all("a", attrs={
                "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
            links_list = []
            # class=""
            # Loop for extracting links from tag objects
            for link in links:
                links_list.append(link.get('href'))
                print(f'url: {url} loop{i}')
                # Loop for extracting details from each link
                # loop add arl amz + link to find product
                # Create a new soup and extracting details from each link

                # filter links
                links_filters = self.filter_links(links_list)

            for link in links_filters:
                # Headers for request
                print(f'url: {url} loop:{i}')

                new_webpage = requests.get("https://amazon.com/" + link, headers=HEADERS)
                new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

                # Function calls to display all necessary product information

                data['title'].append(self.get_title(new_soup))
                data['price'].append(self.get_price(new_soup))
                data['rate'].append(self.get_rate(new_soup))

        return data

    @staticmethod
    def get_title(soup) -> string:
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
        try:
            # <span class="a-price a-text-normal aok-align-center reinventPriceAccordionT2" data-a-size="l"
            # data-a-color="base"><span class="a-offscreen">$142.99</span><span aria-hidden="true"><span
            # class="a-price-symbol">$</span><span class="a-price-whole">142<span
            # class="a-price-decimal">.</span></span><span class="a-price-fraction">99</span></span></span>
            # <span class="a-price-whole">1,059<span class="a-price-decimal">.</span></span>

            price = soup.find("span", attrs={"class": "a-price-whole"})
            price_str = price.text
            price_str = price_str.strip()
        except AttributeError:
            price_str = ""
        return price_str

    @staticmethod
    def get_rate(soup) -> string:
        try:
            # <span class="a-icon-alt">4.1 out of 5 stars</span>

            rate = soup.find("span", attrs={"class": "a-icon-alt"})
            rate_value = rate.text
            rate_str = rate_value.strip()
        except AttributeError:
            rate_str = ""
        return rate_str

    @staticmethod
    def filter_links(links, prefix="/Samsung") -> list:
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

    @staticmethod
    def obtener_siguiente_enlace_amazon(url_actual):
        """
        Obtiene el enlace a la siguiente página de resultados de Amazon, si existe.

        Args:
            url_actual: La URL de la página actual de Amazon.

        Returns:
            El enlace a la siguiente página, o None si no hay siguiente página.
            :param url_actual: url del enlace.
            :param HEADERS: user
        """
        HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/127.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.5'})
        try:
            response = requests.get(url_actual, headers=HEADERS)
            response.raise_for_status()  # Lanzar una excepción si hay un error HTTP

            soup = BeautifulSoup(response.content, 'html.parser')

            # Buscar el elemento que contiene el enlace a la siguiente página
            siguiente_enlace = soup.find('a', {'class': 's-pagination-next'})

            if siguiente_enlace:
                return siguiente_enlace['href']
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la página: {e}")
            return None

    def get_urls(self, url_actual, start_page, end_page):
        url_p = "https://www.amazon.com/s?k=samsung&ref=nb_sb_noss"
        while start_page <= end_page:
            return url_p + self.obtener_siguiente_enlace_amazon(url_actual)

# Ejemplo de uso:
