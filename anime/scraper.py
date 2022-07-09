import httpx
import lxml.html
import json
import regex
import base64
from base64 import b64decode, b64encode
from anime import constants

ID_MATCHER = regex.compile(r"\?id=([^&]+)")
M3U8_MATCHER = regex.compile(r".+?#(.+?)#")

client = httpx.Client(base_url=constants.BASE)
headers = {"user-agent": "mozilla/5.0"}

def get_episodes_list(url):
    data = json.loads(
        lxml.html.fromstring(client.get(url, headers=constants.HEADERS).content)
        .cssselect("#epslistplace")[0]
        .text
    )
    dict = {}
    for value in range(int(data.get("eptotal"))):
        dict.update({value + 1: (data[str(value)])})
    return dict

def scrape_embed(url):
    html = client.get(url, headers=constants.HEADERS).text
    id = ID_MATCHER.search(html).group(1)
    embed = (
        "https://animixplay.to/api/live"
        + base64.b64encode(
            "{}LTXs3GrU8we9O{}".format(
                id, base64.b64encode(id.encode()).decode()
            ).encode()
        ).decode()
    )
    location = client.get(embed, headers=constants.HEADERS).headers["location"]
    m3u8 = base64.b64decode(M3U8_MATCHER.search(location).group(1))
    return f"{m3u8.decode()}"
