import subprocess

def open_video(url, title, episode_number):
    process = subprocess.Popen(
        args=[
            "mpv",
            url,
            f"--force-media-title={title[0]} Episode {episode_number}",
        ]
    )
    process.wait()
    return
