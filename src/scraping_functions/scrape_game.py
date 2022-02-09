import requests
import re

from bs4 import BeautifulSoup

from src.config.config import headers

def scrape_game(link, school_name):
    
    try:
        URL = link
        r = requests.get(URL, headers=headers, verify=False)
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        results = soup.find_all("tr")
        
        new_results = []
        for r in results:
            new_results.append(r.find_all(["td", "h3"]))
        results = new_results
        
        results =  results + get_starting_pitchers(link, school_name)
        
        return results
    except:
        # This triggers if the game can't be scraped
        return []

def get_starting_pitchers(link, school_name):
    try:
        URL = link
        r = requests.get(URL, headers=headers, verify=False)
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        results = soup.find_all("div", {"class": "lineup-table"})
        
        team_pitchers = []
        opposition_pitchers = []
        for r in results:
            text = r.text.lower()
            if "pitch" in text:
                if school_name.lower() in text:
                    team_pitchers.append(r.find_all("a", {"class": "player-name"}))
                else:
                    opposition_pitchers.append(r.find_all("a", {"class": "player-name"}))
                
        
        team_starting_pitcher = team_pitchers[0][0]
        team_starting_pitcher = re.sub("<[^>]*>", "", str(team_starting_pitcher))
        team_starting_pitcher = team_starting_pitcher.strip()
        
        opposition_starting_pitcher = opposition_pitchers[0][0]
        opposition_starting_pitcher = re.sub("<[^>]*>", "", str(opposition_starting_pitcher))
        opposition_starting_pitcher = opposition_starting_pitcher.strip()
        
        starting_pitchers = [school_name + " starting pitcher: " + team_starting_pitcher,
                            "OPPOSITION starting pitcher: " + opposition_starting_pitcher]
        
        return starting_pitchers
    except:
        return []