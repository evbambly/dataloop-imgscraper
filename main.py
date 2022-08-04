import json
from sys import argv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from re import search, match

regex_find_base_url = r"^[a-z]+:\/\/[^\s\/]+"


class ImageResponse:
    def __init__(self, image_url: str, source_url: str, depth: int):
        self.image_url = image_url
        self.source_url = source_url
        self.depth = depth

    def __dict__(self):
        return {
            "imageUrl": self.image_url,
            "sourceUrl": self.source_url,
            "depth": self.depth
        }

    def __hash__(self):
        return hash(self.image_url + self.source_url)


def normalize_urls(anchors, origin_url):
    urls = []
    for a in anchors:
        href = a["href"]
        if len(href) > 0 and href[0] == "/":
            base_url = search(regex_find_base_url, origin_url).group()
            href = base_url + href
        cut_url = href.split("#", 1)
        if len(cut_url[0]) > 0:
            urls.append(cut_url[0])
    return set(urls)


def get_html_elements(url):
    html = None
    try:
        html = urlopen(url)
    except Exception as e:
        print(url, e)
    if html is None:
        return None, None
    bs = BeautifulSoup(html, 'html.parser')
    found_imgs = bs.find_all('img', src=True)
    images = {img['src'] for img in found_imgs}
    found_anchors = bs.find_all('a', href=True)
    cut_urls = normalize_urls(found_anchors, url)
    return images, cut_urls


def iterate_urls(visited_urls, unvisited_urls, current_depth):
    next_images = []
    next_unvisited_urls = set()
    for url in unvisited_urls:
        print(f'Depth: {current_depth}, URL: {url}')
        images, next_urls = get_html_elements(url)
        if images is None:
            continue
        visited_urls.add(url)
        next_unvisited_urls = next_unvisited_urls.union(next_urls)
        image_responses = [ImageResponse(img, url, current_depth) for img in images]
        next_images.extend(image_responses)
    next_unvisited_urls = next_unvisited_urls - visited_urls
    return next_unvisited_urls, next_images


def scrape(start_url, depth):
    visited_urls = set()
    unvisited_urls = {start_url}
    response = []
    for i in range(depth + 1):
        unvisited_urls, next_images = iterate_urls(visited_urls, unvisited_urls, i)
        response.extend(next_images)
    with open("./image_results.json", "w") as file:
        json.dump([img.__dict__() for img in response], file)

    # Prove no duplicate images are returned
    # print(len(set(response)))
    # print(len(response))


if __name__ == '__main__':
    if len(argv) != 3:
        raise Exception("Expected 2 arguments")
    start_url = argv[1]
    if not match(regex_find_base_url, start_url):
        raise ValueError("Invalid URL")
    try:
        depth = int(argv[2])
    except ValueError:
        raise ValueError("Invalid depth parameter")
    scrape(start_url, depth)
