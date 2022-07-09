from anime import search, user_input, constants, player, scraper

dict = search.search_anime()
title, anime_url = user_input.prompt_user_for_input(dict)
episodes = scraper.get_episodes_list(anime_url)
episode_number, embed_link = user_input.select_episode(episodes)
m3u8_link = scraper.scrape_embed(embed_link)
player.open_video(m3u8_link, title, episode_number)
