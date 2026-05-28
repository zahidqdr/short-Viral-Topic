import streamlit as st
import requests
from datetime import datetime, timedelta

# =========================
# YOUTUBE API KEY
# =========================

API_KEY = "ENTER_YOUR_API_KEY"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# =========================
# UI
# =========================

st.title("🔥 YouTube Viral Topics Tool")

days = st.number_input(
    "Enter Days to Search (1-30):",
    min_value=1,
    max_value=30,
    value=5
)

# =========================
# KEYWORDS
# =========================

keywords = [
    "Affair Relationship Stories", "Reddit Update", "Reddit Relationship Advice", "Reddit Relationship",
    "Reddit Cheating", "AITA Update", "Open Marriage", "Open Relationship", "X BF Caught",
    "Stories Cheat", "X GF Reddit", "AskReddit Surviving Infidelity", "GurlCan Reddit",
    "Cheating Story Actually Happened", "Cheating Story Real", "True Cheating Story",
    "Reddit Cheating Story", "R/Surviving Infidelity", "Surviving Infidelity",
    "Reddit Marriage", "Wife Cheated I Can't Forgive", "Reddit AP", "Exposed Wife", "Cheat Exposed"
]

# =========================
# BUTTON
# =========================

if st.button("🚀 Fetch Data"):

    try:

        start_date = (
            datetime.utcnow() - timedelta(days=int(days))
        ).isoformat("T") + "Z"

        all_results = []
        seen_videos = set()

        for keyword in keywords:

            st.write(f"Searching: {keyword}")

            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY
            }

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            if "items" not in data:
                continue

            videos = data["items"]

            video_ids = []
            channel_ids = []

            for video in videos:
                try:
                    vid = video["id"]["videoId"]
                    cid = video["snippet"]["channelId"]

                    if vid not in seen_videos:
                        seen_videos.add(vid)
                        video_ids.append(vid)
                        channel_ids.append(cid)

                except:
                    continue

            if not video_ids:
                continue

            # =========================
            # VIDEO STATS
            # =========================

            stats_params = {
                "part": "statistics",
                "id": ",".join(video_ids),
                "key": API_KEY
            }

            stats_data = requests.get(YOUTUBE_VIDEO_URL, params=stats_params).json()

            # =========================
            # CHANNEL STATS
            # =========================

            channel_params = {
                "part": "statistics",
                "id": ",".join(channel_ids),
                "key": API_KEY
            }

            channel_data = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params).json()

            if "items" not in stats_data or "items" not in channel_data:
                continue

            # LOOKUP MAP
            video_map = {v["id"]: v for v in stats_data["items"]}
            channel_map = {c["id"]: c for c in channel_data["items"]}

            # =========================
            # PROCESS
            # =========================

            for video in videos:

                try:
                    vid = video["id"]["videoId"]
                    cid = video["snippet"]["channelId"]

                    if vid not in video_map or cid not in channel_map:
                        continue

                    vdata = video_map[vid]
                    cdata = channel_map[cid]

                    views = int(vdata["statistics"].get("viewCount", 0))
                    subs = int(cdata["statistics"].get("subscriberCount", 0))

                    if subs >= 3000:
                        continue

                    all_results.append({
                        "Title": video["snippet"].get("title", ""),
                        "Description": video["snippet"].get("description", "")[:200],
                        "URL": f"https://www.youtube.com/watch?v={vid}",
                        "Views": views,
                        "Subscribers": subs
                    })

                except:
                    continue

        # =========================
        # OUTPUT
        # =========================

        if all_results:

            st.success(f"Found {len(all_results)} results!")

            for r in all_results:
                st.markdown(
                    f"""
**Title:** {r['Title']}  
**Description:** {r['Description']}  
**URL:** [Watch Video]({r['URL']})  
**Views:** {r['Views']}  
**Subscribers:** {r['Subscribers']}  
---
"""
                )

        else:
            st.warning("No results found.")

    except Exception as e:
        st.error(f"Error: {e}")
