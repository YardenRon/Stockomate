from .config import YAHOO_FINANCE
from . import session
from utils import ApiError
import logging
from bs4 import BeautifulSoup

class YahooScraper:

    def __init__(self):
        self.base_url = YAHOO_FINANCE["base_url"]
        self.logger = logging.getLogger('app.scraper')

    def get_company_expected_growth_rate(self, ticker):
        url = self.base_url + YAHOO_FINANCE["analysis"] % ticker
        self.__add_param_to_url("p", ticker)

        self.logger.debug("Scraping expected growth rate of company [%s] from Yahoo Finance, url=%s", ticker, url)

        response = session.get(url)

        self.__remove_param_from_url("p")

        if response.status_code != 200:
            raise ApiError(url, response.status_code)

        egr = self.__extract_EGR_from_html(response.content)

        self.logger.debug("Successfully scraped expected growth rate of company [%s] from Yahoo Finance, url=%s",
                          ticker, url)
        return egr


    def __extract_EGR_from_html(self, html):
        parser = BeautifulSoup(html, 'html.parser')
        # Not so good practice - may be fragile
        egr_string = parser.find_all("td", class_="Ta(end) Py(10px)")[16].get_text()
        return float(egr_string.strip('%'))/100

    def __add_param_to_url(self, param, value):
        if param is not None:
            session.params[param] = value


    def __remove_param_from_url(self, param):
        if param is not None:
            del session.params[param]