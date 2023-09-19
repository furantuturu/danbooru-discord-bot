import os
from dotenv import load_dotenv
load_dotenv()

api_posts = "https://danbooru.donmai.us/posts.json?"
KEY = os.getenv("API_KEY")

import urllib.parse
import requests

tag = "kayoko_(blue_archive)"

url = api_posts + urllib.parse.urlencode({"tags": tag, "key": KEY})

print(url)
json_data = requests.get(url).json()
# print(json_data)
print(json_data[0]["id"])