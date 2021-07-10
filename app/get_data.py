import requests
import calendar
import os
from datetime import datetime as dt


def degToCompass(num):
    """Converts Wind (in degrees) to direction known to human"""
    val = int((num / 22.5) + 0.5)
    arr = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return arr[(val % 16)]


def get_weather_desc(code):
    """Accepts the Weather status code and returns the keywords for
    the type of music that can be listened in that weather"""

    weather_desc_list = {
        "2": "music acoustic electronic",
        "3": "soft soothing slow music",
        "5": "sad soulful emotional heartfelt music",
        "6": "instrumental music",
        "7": "atmosphere music",
        "8": "thrill upbeat uplifting music",
    }

    if str(code) == "800":
        weather_desc = "higher-energy  happy music fast"
    else:
        weather_desc = weather_desc_list.get(str(code)[0], "songs")

    return weather_desc


def get_videos(weather_code_desc):
    """Accepts the keywords for weather decription,
    to return youtube videos and their details """

    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_url = "https://www.googleapis.com/youtube/v3/videos"

    search_params = {
        "part": "snippet",
        "q": weather_code_desc,
        "key": os.environ.get('MY_YOUTUBE_API_KEY'),
        "maxResults": 12,
        "type": "video",
    }

    video_ids = []
    r = requests.get(search_url, params=search_params)
    results = r.json()["items"]

    for result in results:
        video_ids.append(result["id"]["videoId"])

    video_params = {
        "part": "snippet",
        "id": ",".join(video_ids),
        "maxResults": 12,
        "key": os.environ.get('MY_YOUTUBE_API_KEY'),
    }

    vr = requests.get(video_url, params=video_params)

    video_results = vr.json()["items"]

    video_data = {}
    videos = []
    for vresult in video_results:
        video_data = {
            "title": "{}{}".format(str(vresult["snippet"]["title"])[0:40], "..."),
            "id": vresult["id"],
            "url": f'https://youtube.com/watch?v={vresult["id"]}',
            "thumbnail": vresult["snippet"]["thumbnails"]["high"]["url"],
        }
        videos.append(video_data)
    return videos


icon_list = {  # 'd' is day and 'n' is night
    "01d": "images/icons/icon-2.svg",  # clear sky
    "01n": "images/icons/icon-2.svg",
    "02d": "images/icons/icon-3.svg",  # few clouds
    "02n": "images/icons/icon-3.svg",
    "03d": "images/icons/icon-4.svg",  # scattered clouds
    "03n": "images/icons/icon-4.svg",
    "04d": "images/icons/icon-6.svg",  # broken clouds
    "04n": "images/icons/icon-6.svg",
    "09d": "images/icons/icon-9.svg",  # shower rain
    "09n": "images/icons/icon-9.svg",
    "10d": "images/icons/icon-10.svg",  # rain
    "10n": "images/icons/icon-10.svg",
    "11d": "images/icons/icon-11.svg",  # thunder
    "11n": "images/icons/icon-11.svg",
    "13d": "images/icons/icon-13.svg",  # snow
    "13n": "images/icons/icon-13.svg",
    "50d": "images/icons/icon-16.svg",  # mist
    "50n": "images/icons/icon-16.svg",
}


def get_data(data):
    """Accepts the weather data in JSON which is further read/modified depending on needs"""

    todaydate = data["current"]["dt"]
    local_time = dt.fromtimestamp(todaydate)                #get today's date

    today_day_count = local_time.weekday()
    day_name = calendar.day_name[today_day_count]           #get today's dayname

    today_date_regular = local_time.strftime("%B %d")
                                                            # date variable outputs in format sunday,Nov 25

    weather_code = data["current"]["weather"][0]["id"]

    weather_code_desc = get_weather_desc(weather_code)

    icon = data["current"]["weather"][0]["icon"]
    icon_image = icon_list.get(icon)
    current_temp = int(data["current"]["temp"])
    wind_direction = degToCompass(float(data["current"]["wind_deg"]))
    crnt_temp_high = int(data["daily"][0]["temp"]["max"])
    crnt_temp_low = int(data["daily"][0]["temp"]["min"])
    wind_speed = "{:.2f} km/h ".format((data["daily"][0]["wind_speed"]) * 3.6)
    humidity = int(data["daily"][0]["humidity"])

    video_list = get_videos(weather_code_desc)

    # 7 days weather forecast

    daily_weather = []
    for i in range(1, 7):

        daily_high = int(data["daily"][i]["temp"]["max"])
        daily_low = int(data["daily"][i]["temp"]["min"])
        daily_icon = data["daily"][i]["weather"][0]["icon"]
        daily_icon_image = icon_list.get(daily_icon)
        daily_time = data["daily"][i]["dt"]
        daily_date = dt.fromtimestamp(daily_time).strftime("%B %d")

        daily_weather.append((daily_high, daily_low, daily_date, daily_icon_image,))

    context = {
        "today_date": today_date_regular,
        "weather_icon": icon_image,
        "wind_direction": wind_direction,
        "current_temp": current_temp,
        "today_day_name": day_name,
        "crnt_temp_high": crnt_temp_high,
        "crnt_temp_low": crnt_temp_low,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "daily_weather": daily_weather,
        "videos": video_list,
    }
    return context
