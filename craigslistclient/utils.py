def build_primary_urls(search_query: str, category: str, cities: [str], filters: [str]) -> [str]:
    """

    :return: list of urls
    """
    urls = []
    url_template = "https://{city}.craigslist.org/search/{category}{filters}"
    filters = "&".join(filters)
    for city in cities:
        if search_query is not None:
            filters = "query=" + search_query + "&" + filters
        filters = "?" + filters
        url = url_template.format(city=city, category=category, filters=filters)
        urls.append(url)
    return urls
