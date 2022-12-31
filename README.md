# craigslist-client

**This package is only meant to be used for personal use only.**

## Table of Contents
* [Description](#description)
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)

### Description
craigslist-client is that can be used to fetch listings from a given search query, but also obtain listing details.

### Installation
```
pip install git+shttps://github.com/city-analytics/craigslist-client.git
```

### Usage
```python
from utils import build_primary_urls
from client import Craigslist

# Build the urls for a given search query, city, filters, and category.
search_query = "condo"
filters = ['postedToday=1']
cities = ["toronto"]
category = "apa" # This category represents housing
urls = build_primary_urls(search_query, category, cities, filters)

# Create the Craigslist client object
client = Craigslist()

# Use the result from the build_primary_urls() function to fetch all the listing urls
results = client.get_search_results(urls)

# To obtain the listing details, use the Client.get_listing_details() URL
listing_details = client.get_listing_details(results.get_results()[0])
```

### License
Distributed under the MIT License. See `LICENSE` for more information.


