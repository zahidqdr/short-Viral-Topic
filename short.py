```python
import streamlit as st
import requests
from datetime import datetime, timedelta
import isodate

# ==============================
# YOUTUBE API KEY
# ==============================

API_KEY = "AIzaSyBmowEzxvxsZtBFFc-R14uym8CAS5BwFRY"

# ==============================
# YOUTUBE API URLS
# ==============================

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# ==============================
# PAGE SETTINGS
# ==============================

st.set_page_config(
    page_title="Viral Shorts Finder",
    layout="wide"
)

st.title("🔥 Viral Shorts Finder")

st.write(
    "Find newly created low subscriber channels "
    "getting massive Shorts views."
)

# ==============================
# USER INPUTS
# ==============================

days = st.slider(
    "Search Videos Uploaded Within Days",
    1,
    30,
    7
)

max_subscribers = st.number_input(
    "Maximum Subscribers",
    min_value=100,
    max_value=100000,
    value=3000
)

minimum_views = st.number_input(
    "Minimum Views",
    min_value=1000,
    max_value=100000000,
    value=50000
)

max_results = st.slider(
    "Videos Per Keyword",
    1,
    20,
    5
)

# ==============================
# KEYWORDS
# ==============================

keywords = [

    "reddit stories shorts",
    "relationship stories shorts",
    "aita shorts",
    "reddit cheating shorts",
    "open marriage shorts",
    "surviving infidelity shorts",
    "cheating stories shorts",
    "true story shorts",
    "reddit update shorts"

]

# ==============================
# FETCH BUTTON
# ==============================

if st.button("🚀 Find Viral Shorts"):

    all_results = []
    seen_videos = set()

    published_after = (
        datetime.utcnow() - timedelta(days=days)
    ).isoformat("T") + "Z"

    for keyword in keywords:

        st.write(f"Searching: {keyword}")

        try:

            # ==============================
            # SEARCH VIDEOS
            # ==============================

            search_params = {

                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": published_after,
                "maxResults": max_results,
                "key": API_KEY

            }

            response = requests.get(
                YOUTUBE_SEARCH_URL,
                params=search_params
            )

            data = response.json()

            if "items" not in data:
                continue

            videos = data["items"]

            video_ids = []
            channel_ids = []

            for video in videos:

                try:

                    video_id = video["id"]["videoId"]
                    channel_id = video["snippet"]["channelId"]

                    if video_id not in seen_videos:

                        seen_videos.add(video_id)

                        video_ids.append(video_id)
                        channel_ids.append(channel_id)

                except:
                    pass

            if not video_ids:
                continue

            # ==============================
            # VIDEO DETAILS
            # ==============================

            video_params = {

                "part": "statistics,contentDetails",
                "id": ",".join(video_ids),
                "key": API_KEY

            }

            video_response = requests.get(
                YOUTUBE_VIDEO_URL,
                params=video_params
            )

            video_data = video_response.json()

            if "items" not in video_data:
                continue

            # ==============================
            # CHANNEL DETAILS
            # ==============================

            channel_params = {

                "part": "statistics,snippet",
                "id": ",".join(channel_ids),
                "key": API_KEY

            }

            channel_response = requests.get(
                YOUTUBE_CHANNEL_URL,
                params=channel_params
            )

            channel_data = channel_response.json()

            if "items" not in channel_data:
                continue

            # ==============================
            # LOOKUP DICTIONARIES
            # ==============================

            video_lookup = {}

            for item in video_data["items"]:

                video_lookup[item["id"]] = item

            channel_lookup = {}

            for item in channel_data["items"]:

                channel_lookup[item["id"]] = item

            # ==============================
            # PROCESS VIDEOS
            # ==============================

            for video in videos:

                try:

                    video_id = video["id"]["videoId"]
                    channel_id = video["snippet"]["channelId"]

                    if video_id not in video_lookup:
                        continue

                    if channel_id not in channel_lookup:
                        continue

                    video_info = video_lookup[video_id]
                    channel_info = channel_lookup[channel_id]

                    # ==============================
                    # VIEWS
                    # ==============================

                    views = int(
                        video_info["statistics"].get(
                            "viewCount",
                            0
                        )
                    )

                    if views < minimum_views:
                        continue

                    # ==============================
                    # SHORTS FILTER
                    # ==============================

                    duration = video_info[
                        "contentDetails"
                    ]["duration"]

                    duration_seconds = int(
                        isodate.parse_duration(
                            duration
                        ).total_seconds()
                    )

                    if duration_seconds > 60:
                        continue

                    # ==============================
                    # SUBSCRIBERS
                    # ==============================

                    subscribers = int(
                        channel_info["statistics"].get(
                            "subscriberCount",
                            0
                        )
                    )

                    if subscribers > max_subscribers:
                        continue

                    # ==============================
                    # CHANNEL AGE
                    # ==============================

                    channel_created = channel_info[
                        "snippet"
                    ]["publishedAt"]

                    channel_created_date = datetime.strptime(
                        channel_created,
                        "%Y-%m-%dT%H:%M:%SZ"
                    )

                    age_days = (
                        datetime.utcnow() -
                        channel_created_date
                    ).days

                    # ==============================
                    # VIRAL SCORE
                    # ==============================

                    if subscribers == 0:
                        viral_score = views
                    else:
                        viral_score = round(
                            views / subscribers,
                            2
                        )

                    # ==============================
                    # VIDEO URL
                    # ==============================

                    video_url = (
                        f"https://www.youtube.com/watch?v={video_id}"
                    )

                    # ==============================
                    # SAVE RESULT
                    # ==============================

                    all_results.append({

                        "title":
                            video["snippet"]["title"],

                        "channel":
                            video["snippet"]["channelTitle"],

                        "views":
                            views,

                        "subscribers":
                            subscribers,

                        "viral_score":
                            viral_score,

                        "age_days":
                            age_days,

                        "url":
                            video_url,

                        "keyword":
                            keyword

                    })

                except:
                    pass

        except Exception as e:

            st.error(f"Error: {e}")

    # ==============================
    # SORT RESULTS
    # ==============================

    all_results = sorted(
        all_results,
        key=lambda x: x["views"],
        reverse=True
    )

    # ==============================
    # DISPLAY RESULTS
    # ==============================

    if all_results:

        st.success(
            f"Found {len(all_results)} Viral Shorts!"
        )

        for result in all_results:

            st.markdown("---")

            st.markdown(
                f"""
## 🎬 {result['title']}

### 📺 Channel:
{result['channel']}

### 👀 Views:
{result['views']:,}

### 👥 Subscribers:
{result['subscribers']:,}

### 🔥 Viral Score:
{result['viral_score']}

### 📅 Channel Age:
{result['age_days']} Days

### 🔍 Keyword:
{result['keyword']}

### ▶️ Watch Video:
{result['url']}
"""
            )

    else:

        st.warning(
            "No viral Shorts found."
        )
```
