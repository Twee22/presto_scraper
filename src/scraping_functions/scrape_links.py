import requests
import re

from bs4 import BeautifulSoup

from src.config.config import headers, url_part_1, url_part_2

def get_all_school_links():
    URL = url_part_1 + url_part_2
    r = requests.get(URL, headers=headers, verify=False)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    
    results = soup.find("select", id="select-box-team-filter")
    
    teams = results.find_all("option")
    
    team_links = []
    for team in teams:
        string_team = str(team)
        if "All Teams" in string_team:
            continue
        else:
            string_team = string_team[string_team.index("\"") + 1:string_team.index(">") - 1]
            team_links.append({"url_part_1": url_part_1,
                                "url_part_2": string_team})
        
    
    return team_links