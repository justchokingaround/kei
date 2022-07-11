import subprocess
from helpers.rpc import get_anime, get_episodes, set_streaming_episode


def open_video(url, title, episode_number):
    process = subprocess.Popen(
        args=[
            "mpv",
            url,
            f"--force-media-title={title[0]} Episode {episode_number}",
        ]
    )
    set_streaming_episode(title[0], episode_number)
    process.wait()
    # kill the process if it's still running
    if process.poll() is None:
        process.kill()
    return
