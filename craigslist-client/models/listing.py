from datetime import datetime


class Listing:
    def __init__(self, title: str, price: str, date_posted: datetime, thumbnail_urls: [str], description: str, map_coordinates: [str], badges: [str]):
        self.title = title
        self.price = price
        self.date_posted = date_posted
        self.thumbnail_urls = thumbnail_urls
        self.description = description
        self.map_coordinates = map_coordinates
        self.badges = badges

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

    def __str__(self):
        return str({
            "title": self.title,
            "price": self.price,
            "date_posted": str(self.date_posted),
            "thumbnail_urls": str(self.thumbnail_urls),
            "badges": str(self.badges),
            "description": self.description,
            "map_coordinates": str(self.map_coordinates)
        })
