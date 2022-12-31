from setuptools import setup, find_packages
import pathlib

cwd = pathlib.Path(__file__).parent.resolve()
long_description = (cwd / 'README.md').read_text(encoding='utf-8')
setup(
    name='craigslist-scraper',
    version='1.0.0',
    description='Client for scrapping Craigslist listings',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/city-analytics/craigslist-client',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['beautifulsoup4', 'requests'],
    include_package_data=True
)
