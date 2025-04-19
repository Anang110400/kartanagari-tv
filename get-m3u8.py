import subprocess

with open("live.txt", "r") as f:
    lines = f.readlines()

playlist = []
for index, line in enumerate(lines, start=1):
    if "|" not in line:
        continue
    title, yt_url = [part.strip() for part in line.split("|", 1)]

    if "youtube.com/live/" in yt_url:
        video_id = yt_url.split("/live/")[1].split("?")[0]
        yt_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        result = subprocess.run(
            ["yt-dlp", "-g", yt_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        m3u8_url = result.stdout.strip().splitlines()[0]
        playlist.append(f"{title} | {m3u8_url}")
    except subprocess.CalledProcessError as e:
        print(f"Gagal fetch M3U8 untuk {title}: {e.stderr}")

with open("playlist.txt", "w") as f:
    f.write("\n".join(playlist) + "\n")

print("playlist.txt berhasil diupdate.")
