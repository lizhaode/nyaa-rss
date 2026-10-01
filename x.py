import json, glob, csv
import subprocess

ALL_VIDEOS = []


def main(data: dict):
    instructions = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]

    for inst in instructions:
        if inst["type"] == "TimelinePinEntry":
            pin_legacy = inst["entry"]["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
            for media in filter(lambda m: m["type"] == "video", pin_legacy['entities'].get('media', {})):
                best = max(media["video_info"]["variants"], key=lambda v: v.get("bitrate", 0))
                ALL_VIDEOS.append(
                    {
                        "id": len(ALL_VIDEOS) + 1,
                        "文案": pin_legacy["full_text"],
                        "画质": best["url"].split("/")[-2],
                        "url": best["url"],
                    }
                )
        elif inst["type"] == "TimelineAddEntries":
            for entry in [
                entry for entry in inst["entries"] if entry["content"]["entryType"] == "TimelineTimelineItem"
            ]:
                if entry["content"]["itemContent"]["tweet_results"]["result"].get('legacy') is None:
                    add_legacy = entry["content"]["itemContent"]["tweet_results"]["result"]['tweet']
                else:
                    add_legacy = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
                for media in filter(lambda m: m["type"] == "video", add_legacy.get('entities', {}).get('media', {})):
                    best = max(media["video_info"]["variants"], key=lambda v: v.get("bitrate", 0))
                    ALL_VIDEOS.append(
                        {
                            "id": len(ALL_VIDEOS) + 1,
                            "文案": add_legacy["full_text"],
                            "画质": best["url"].split("/")[-2],
                            "url": best["url"],
                        }
                    )


def write_videos_to_csv(data: list[dict]):
    fieldnames = ["id", "文案", "画质", "url"]
    with open('output.csv', "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"已写入 {len(data)} 条视频信息到 output.csv")


def download_from_csv():

    with open('output.csv', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("url", "").strip()

            filename = f"{row.get('id','')}.mp4"
            cmd = [
                "aria2c",
                "--all-proxy=http://127.0.0.1:7890",
                "-x",
                "16",
                "--out",
                filename,
                url,
            ]

            print(f"下载：{filename}")
            subprocess.run(cmd, check=True)


def book_mark_parser(data: dict):
    instructions = data['data']['bookmark_timeline_v2']['timeline']['instructions']
    assert len(instructions) == 1

    for e in [entry for entry in instructions[0]['entries'] if entry["content"]["entryType"] == "TimelineTimelineItem"]:
        if e["content"]["itemContent"]["tweet_results"]["result"].get('legacy') is None:
            legacy = e["content"]["itemContent"]["tweet_results"]["result"]['tweet']["legacy"]
        else:
            legacy = e["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
        best = max(legacy['entities']['media'][0]["video_info"]["variants"], key=lambda v: v.get("bitrate", 0))
        ALL_VIDEOS.append(
            {
                "id": len(ALL_VIDEOS) + 1,
                "文案": legacy["full_text"],
                "画质": best["url"].split("/")[-2],
                "url": best["url"],
            }
        )


if __name__ == '__main__':
    for path in sorted(glob.glob("*.json")):
        print(f"处理: {path}")
        book_mark_parser(json.load(open(path)))
        print(f"当前已收集 {len(ALL_VIDEOS)} 条视频信息")
    if ALL_VIDEOS:
        write_videos_to_csv(ALL_VIDEOS)
    download_from_csv()
