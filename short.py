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

days = st.number_input("Enter Days (1-30):", 1, 30, 5)

# ✅ SHORTS OPTION ADDED
only_shorts = st.checkbox("🎬 Show ONLY Shorts (≤ 60 sec)", value=True)

keywords = [
    "Affair Relationship Stories", "Reddit Update", "Reddit Relationship Advice",
    "Reddit Cheating", "AITA Update", "Open Marriage", "X GF Reddit",
    "Cheating Story Real", "True Cheating Story", "Reddit Marriage"
]

# =========================
# FETCH DATA
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

            # VIDEO STATS
            video_data = requests.get(
                YOUTUBE_VIDEO_URL,
                params={
                    "part": "statistics,contentDetails",
                    "id": ",".join(video_ids),
                    "key": API_KEY
                }
            ).json()

            # CHANNEL STATS
            channel_data = requests.get(
                YOUTUBE_CHANNEL_URL,
                params={
                    "part": "statistics",
                    "id": ",".join(channel_ids),
                    "key": API_KEY
                }
            ).json()

            if "items" not in video_data or "items" not in channel_data:
                continue

            video_map = {v["id"]: v for v in video_data["items"]}
            channel_map = {c["id"]: c for c in channel_data["items"]}

            # PROCESS
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

                    # =========================
                    # 🎬 SHORTS FILTER (NEW)
                    # =========================

                    duration = vdata["contentDetails"]["duration"]
                    seconds = int(isodate.parse_duration(duration).total_seconds())

                    if only_shorts and seconds > 60:
                        continue

                    all_results.append({
                        "Title": video["snippet"]["title"],
                        "URL": f"https://www.youtube.com/watch?v={vid}",
                        "Views": views,
                        "Subscribers": subs,
                        "Duration": seconds
                    })

                except:
                    continue

        # SORT
        all_results = sorted(all_results, key=lambda x: x["Views"], reverse=True)

        # OUTPUT
        if all_results:

            st.success(f"Found {len(all_results)} videos!")

            for r in all_results:

                st.markdown("---")
                st.markdown(f"""
**🎬 Title:** {r['Title']}  
**👀 Views:** {r['Views']}  
**👥 Subscribers:** {r['Subscribers']}  
**⏱️ Duration:** {r['Duration']} sec  
👉 [Watch Video]({r['URL']})
""")

        else:
            st.warning("No results found.")

    except Exception as e:
        st.error(f"Error: {e}")
