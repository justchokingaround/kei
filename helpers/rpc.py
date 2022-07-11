#!/usr/bin/env python3
import time

import httpx
from pypresence import Presence

# ani-cli
# CLIENT_ID = "963136145691140097"
# anime
CLIENT_ID = "995856834558689410"
ENDPOINT = "https://kitsu.io/api/"

rpc_client = Presence(CLIENT_ID)
rpc_client.connect()

http_client = httpx.Client(base_url=ENDPOINT)

def get_anime(anime_name):
    return http_client.get(
        ENDPOINT + "edge/anime", params={"filter[text]": anime_name}
    ).json()["data"]

def get_episodes(anime_id, offset):

    params = {
        "filter[media_id]": anime_id,
        "sort": "number",
        "filter[mediaType]": "Anime",
        "page[limit]": 10,
    }
    if offset is not None and offset > 1:
        params["page[offset]"] = offset

    return http_client.get(ENDPOINT + "edge/episodes", params=params).json()["data"]


def set_streaming_episode(anime_name, episode):

    state = anime_name

    if episode:
        state += ": Episode {}".format(episode)

    content_list = get_anime(anime_name)

    if not content_list:
        return rpc_client.update(
            state=state,
            large_image="mascot",
            start=int(time.time()),
        )

    anime = content_list[0]

    anime_attributes = anime["attributes"]

    image = anime_attributes["posterImage"]["original"]
    count = anime_attributes["episodeCount"]

    if count is None or (episode > count):
        return rpc_client.update(
            state=state,
            large_image=image,
            small_image="mascot",
            large_text="deez nuts",
            start=int(time.time()),
        )

    around = episode - (episode % 10)

    current = get_episodes(anime["id"], around)[episode % 10 - 1]

    episode_thumbnail = (current.get("attributes", {}).get("thumbnail", {}) or {}).get(
        "original", "mascot"
    )

    if episode_thumbnail == "mascot":
        image, episode_thumbnail = episode_thumbnail, image

    return rpc_client.update(
        state=state + ("/{}".format(count)) if count else "~",
        large_image=episode_thumbnail,
        small_image=image,
        details=current.get("attributes", {}).get("canonicalTitle"),
        start=int(time.time()),
    )

