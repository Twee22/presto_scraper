import requests 
import re

from src.config.config import headers
from src.config.config import url_part_1, url_part_2

def get_school_name(school):
    school_name = str()
    URL = school["url_part_1"] + school["url_part_2"]
    r = requests.get(URL, headers=headers, verify=False)
    text = r.text
    
    school_name = re.findall(r"<h1>.*NAIA Baseball Schedule :.*</h1>", text)[0]
    school_name = school_name.split(":")[1]
    school_name = school_name.split("<")[0]
    school_name = school_name.strip()
    
    return school_name

def get_year(school):
    year = str()
    URL = school["url_part_1"] + school["url_part_2"]
    r = requests.get(URL, headers=headers, verify=False)
    text = r.text
    
    year = re.findall(r"<h1>.*NAIA Baseball Schedule :.*</h1>", text)[0]

    year = year.split("NAIA")[0]
    year = year.split("<h1>")[1]
    year = year.strip()
    
    return year