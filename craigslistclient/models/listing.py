from datetime import datetime


class Listing:
    def __init__(self, id: str, listing_url: str, title: str, price: str, date_posted: datetime, thumbnail_urls: [str], description: str, map_coordinates: [str], badges: [str]):
        self.id = id
        self.listing_url = listing_url
        self.title = title
        self.price = price
        self.date_posted = date_posted
        self.thumbnail_urls = thumbnail_urls
        self.description = description
        self.map_coordinates = map_coordinates
        self.badges = badges

    @property
    def get_id(self) -> str:
        return self.id

    @property
    def get_listing_url(self) -> str:
        return self.listing_url

    @property
    def get_title(self) -> str:
        return self.title

    @property
    def get_thumbnail_urls(self) -> [str]:
        return self.thumbnail_urls

    @property
    def get_description(self) -> str:
        return self.description

    @property
    def get_map_coordinates(self) -> [str]:
        return self.map_coordinates

    @property
    def get_badges(self) -> [str]:
        return self.badges

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "listing_url": self.listing_url,
            "title": self.title,
            "price": self.price,
            "date_posted": self.date_posted,
            "thumbnail_urls": self.thumbnail_urls,
            "badges": self.badges,
            "description": self.description,
            "map_coordinates": self.map_coordinates
        }

