import math
import re
import time

import requests
from requests_html import HTMLSession, HTML
from datetime import datetime
from bs4 import BeautifulSoup
from craigslistclient.models.search_result import SearchResult
from craigslistclient.models.listing import Listing


class Craigslist:
    def __init__(self):
        self.session = HTMLSession()

    def get_search_results(self, url: str) -> SearchResult:
        headers = {
            'Host': 'vancouver.craigslist.org',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.7,fa;q=0.3',
        }

        initial_response = self.session.get(url, headers=headers)
        initial_response.html.render(timeout=10, sleep=3)
        pagination_urls = self.__generate_pagination_urls(initial_response.html)

        listing_urls = set()
        for pagination_url in pagination_urls:
            response = self.session.get(pagination_url, headers=headers)
            response.html.render(timeout=10, sleep=3)
            listing_urls.update(self.__get_listing_urls(response.html))

        return SearchResult(listing_urls=listing_urls)

    def get_listing_details(self, url: str) -> Listing:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return Listing(
            id=self.__get_id(url),
            listing_url=url,
            title=self.__get_title(soup),
            price=self.__get_price(soup),
            date_posted=self.__get_date_posted(soup),
            thumbnail_urls=self.__get_thumbnail_urls(soup),
            description=self.__get_description(soup),
            map_coordinates=self.__get_map_coordinates(soup),
            badges=self.__get_badges(soup)
        )

    def __get_id(self, url: str) -> str:
        id_ = re.findall("\\d+", url)
        return id_[-1]

    def __get_title(self, soup: BeautifulSoup) -> str:
        title_span = soup.find("span", {"id": "titletextonly"})
        return None if title_span is None else title_span.text

    def __get_price(self, soup: BeautifulSoup) -> int:
        price_span = soup.find("span", {"class": "price"})
        if price_span:
            price_int = int(re.sub("[^0-9]", "", price_span.text))
            return price_int
        return None

    def __get_date_posted(self, soup: BeautifulSoup) -> datetime:
        date_dom = soup.find("time", {"class": "date timeago"})
        return None if date_dom is None else datetime.strptime(date_dom["datetime"], "%Y-%m-%dT%H:%M:%S%z")

    def __get_badges(self, soup: BeautifulSoup) -> [str]:
        span_elements = soup.select("span")
        badges = []
        for span in span_elements:
            if not (span.has_attr('class') or span.has_attr('id')):
                badges.append(span.text)
            elif span.has_attr('class') and "shared-line-bubble" in span["class"]:
                if " / " in span.text:
                    multiple_badge_from_single_span = span.text.split(" / ")
                    badges += multiple_badge_from_single_span
                else:
                    badges.append(span.text)
        return badges

    def __get_thumbnail_urls(self, soup: BeautifulSoup) -> [str]:
        a_elements = soup.select("a")
        thumbnail_urls = []
        for a in a_elements:
            if a.has_attr("class") and "thumb" in a["class"]:
                thumbnail_urls.append(a["href"])
        return thumbnail_urls

    def __get_map_coordinates(self, soup: BeautifulSoup) -> [str]:
        map_div = soup.find("div", {"id": "map"})
        return None if map_div is None else [float(map_div["data-longitude"]), float(map_div["data-latitude"])]

    def __get_description(self, soup: BeautifulSoup) -> [str]:
        description = soup.find(id='postingbody')
        if description:
            if not description.text:
                return None
            else:
                return description.text.strip('\n\nQR Code Link to This Post\n\n\n')


    def __get_listing_urls(self, html: HTML) -> [str]:
        regex_pattern = r"^.*/d/"
        return [url for url in html.absolute_links if re.match(regex_pattern, url)]


    def __generate_pagination_urls(self, html: HTML) -> [str]:
        urls = []
        try:
            pagination_str = html.xpath('//span[@class="cl-page-number"]')[0]
            pagination_list = pagination_str.full_text.split(" ")  # Sample list ['1', '-', '120', 'of', '7,877']
            listings_per_page = int(pagination_list[2].replace(",", ""))
            number_of_listings = int(pagination_list[4].replace(",", ""))
            total_pages = math.ceil(number_of_listings / listings_per_page)
            for i in range(total_pages):
                url = "{base_url}#search=1~list~{page}~0".format(base_url=html.url, page=i)
                urls.append(url)
        except Exception as e:
            print("Error: " + e)
        return urls


if __name__ == "__main__":
    client = Craigslist(chromium_executable_path='/Users/eric/Downloads/headless-chromium')
    url = "https://vancouver.craigslist.org/search/apa?postedToday=1"
    result = client.get_search_results(url)
    for listing_url in result.get_listing_urls:
        time.sleep(1)  # Be kind to Craigslist servers
        details = client.get_listing_details(listing_url)
        print(details.to_dict())
