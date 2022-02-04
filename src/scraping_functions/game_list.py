import requests 
import re

from src.config.config import headers
from src.config.config import url_part_1, url_part_2

def get_game_list(school):
    
    URL = school["url_part_1"] + school["url_part_2"]
        
    r = requests.get(URL, headers=headers)

    text = r.text
        
    links = re.findall(r"href=\".*xml.*\"", text)

    links = get_all_links(links)
    
    links = [i for n, i in enumerate(links) if i not in links[:n]]

    return links

def get_all_links(links):
    
    new_links = []
    
    for l in links:
        if "https" not in l:
            line = l.split("\"")[1]
            new_links.append(url_part_1 + line)
    
    return new_links