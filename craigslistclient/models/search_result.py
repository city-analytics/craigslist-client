class SearchResult:
    def __init__(self, listings: set):
        self.listings = listings

    @property
    def get_listings(self):
        return self.listings

    def __str__(self):
        return str(self.listings)
