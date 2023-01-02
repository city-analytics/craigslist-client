import requests
from datetime import datetime
from bs4 import BeautifulSoup
from craigslistclient.models.search_result import SearchResult
from craigslistclient.models.listing import Listing


class Craigslist:
    def get_search_results(self, url: str) -> SearchResult:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return SearchResult(results=self.__get_results_urls(soup))

    def get_listing_details(self, url: str) -> Listing:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return Listing(
            title=self.__get_title(soup),
            price=self.__get_price(soup),
            date_posted=self.__get_date_posted(soup),
            thumbnail_urls=self.__get_thumbnail_urls(soup),
            description=self.__get_description(soup),
            map_coordinates=self.__get_map_coordinates(soup),
            badges=self.__get_badges(soup)
        )

    def __get_title(self, soup: BeautifulSoup) -> str:
        title_span = soup.find("span", {"id": "titletextonly"})
        return title_span.text

    def __get_price(self, soup: BeautifulSoup) -> str:
        price_span = soup.find("span", {"class": "price"})
        return price_span.text

    def __get_date_posted(self, soup: BeautifulSoup) -> datetime:
        date_dom = soup.find("time", {"class": "date timeago"})
        return datetime.strptime(date_dom["datetime"], "%Y-%m-%dT%H:%M:%S%z")

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
        return [map_div["data-latitude"], map_div["data-longitude"]]

    def __get_description(self, soup: BeautifulSoup) -> [str]:
        description = soup.find(id='postingbody')
        return description.text.strip('QR Code Link to This Post')

    def __get_results_urls(self, soup: BeautifulSoup) -> [str]:
        raw_rows = soup.find_all(class_='result-row')
        ad_link_raw = [item.find('a') for item in raw_rows]
        return [items.get('href') for items in ad_link_raw]
