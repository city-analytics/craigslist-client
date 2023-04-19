class SearchResult:
    def __init__(self, listing_urls: set):
        self.listing_urls = listing_urls

    @property
    def get_listing_urls(self):
        return self.listing_urls

    def __str__(self):
        return str(self.listing_urls)
