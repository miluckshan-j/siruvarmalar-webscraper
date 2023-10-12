import os
import time
import requests
from bs4 import BeautifulSoup
import json
import traceback

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

stories = []


def load_json(file):
    with open(os.getcwd() + f"/{file}", "r") as infile:
        file_contents = json.load(infile)
        return file_contents


def run_scrapper(stories: list):
    for index, story in enumerate(stories):
        print(f"Scraping story_id: {index+1}...")
        try:
            req = requests.get(story["url"], headers)
            soup = BeautifulSoup(req.content, "html.parser")
            append_story_content(soup, story)
            save_as_json(stories)
        except Exception:
            dump_error(f"{story['story_title']} {index+1}")
        time.sleep(10)


def append_story_content(soup: BeautifulSoup, story: dict):
    post_container = soup.find("div", "entry").children
    text_elements = []
    for element in post_container:
        # Rating, advertisements and Google ads elements inside container have class attribute which we skip
        # Reference: https://stackoverflow.com/questions/40760441/exclude-unwanted-tag-on-beautifulsoup-python
        if "class" not in element.attrs:
            text_elements.append(element.text)
    story["story"] = " ".join(text_elements)
    return story


def save_as_json(dictionary_list):
    with open("siruvarmalar.json", "w") as outfile:
        # ensure_ascii=False to support Tamil string
        json.dump(dictionary_list, outfile, ensure_ascii=False, indent=2)


def dump_error(story):
    with open("error.log", "a") as log:
        log.write(f"{time.ctime()} - {story}\n")
        log.write(traceback.format_exc())


stories = load_json("stories.json")
run_scrapper(stories)
