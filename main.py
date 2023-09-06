import requests
from bs4 import BeautifulSoup
import json

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

url = f"https://www.siruvarmalar.com"

stories_list = []

req = requests.get(url, headers)

soup = BeautifulSoup(req.content, "html.parser")


def get_story_list(soup: BeautifulSoup):
    list_items = soup.find_all("li")
    for index, item in enumerate(list_items):
        stories_list.append(
            {"story_id": index + 1, "story_title": item.a.string, "url": item.a["href"]}
        )


def save_as_json(dictionary_list):
    with open("stories.json", "w") as outfile:
        # ensure_ascii=False to support Tamil string
        json.dump(dictionary_list, outfile, ensure_ascii=False, indent=2)


# Uncomment to save story list as JSON
# get_story_list(soup.main)
# save_as_json(stories_list)
