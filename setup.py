import pathlib
from setuptools import setup, find_packages

cwd = pathlib.Path(__file__).parent.resolve()
long_description = (cwd / 'README.md').read_text(encoding='utf-8')
setup(
    name='craigslistclient',
    version='1.2',
    description='Client for Craigslist listings',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/city-analytics/craigslist-client',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['beautifulsoup4', 'requests', 'requests-html'],
    include_package_data=True
)
