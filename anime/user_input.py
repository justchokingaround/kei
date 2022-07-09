import pyfzf
from pyfzf.pyfzf import FzfPrompt
from anime import constants

fzf = FzfPrompt()

def prompt_user_for_input(dict):
    title = fzf.prompt(dict, '--prompt="Select an anime " --height=10')
    return title, constants.BASE + dict.get(title[0])

def select_episode(dict):
    # if len(dict) == 1:
    #     return dict.get(episode), "https:" + dict.get(episode)
    print("Select an episode from 1 to {}".format(len(dict)))
    episode = int(input("=> "))
    if episode in dict:
        return episode, "https:" + dict.get(episode)
    else:
        print("Invalid episode number")
        return select_episode(dict)
