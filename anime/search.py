import sys
import httpx
import lxml.html
from anime import constants

SEARCH_URL = "https://cachecow.eu/api/search"

client = httpx.Client(base_url=constants.BASE)


def search_anime():
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = input("=> ")
    data = lxml.html.fromstring(
        client.post(SEARCH_URL, headers=constants.HEADERS, data={"qfast": query}).json()["result"]
    )
    dict = {}
    for results in data.cssselect("a[title]"):
        dict.update({results.get("title"): results.get("href")})
    return dict
