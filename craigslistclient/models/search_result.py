class SearchResult:
    def __init__(self, results: [str]):
        self.results = results

    @property
    def get_results(self):
        return self.results

    def __str__(self):
        return str(self.results)
