from os import stat
import requests
import re

from bs4 import BeautifulSoup

from src.config.config import url_part_1, lineup_url, headers
from src.scraping_functions.scraping_helper_functions import format_school_name
from src.setup.setup_helper_functions import check_school_file_exists

def get_lineup_and_stats():
    
    team_lineup_pages = get_team_lineup_pages()
    
    for page in team_lineup_pages:
        scrape_lineup_and_stats(page)
    return
    
    
def scrape_lineup_and_stats(page):
    
    try:
        school_name = scrape_lineup_name(page)
        year = scrape_lineup_year(page)
        
        formatted_school_name = format_school_name(school_name)
        
        check = check_school_file_exists(formatted_school_name, year)
        
        print("Scraping Lineup and Official Statistics for {} in {}".format(school_name, year))
        
        scrape_lineup(page, formatted_school_name, year)
        
        scrape_stats(page, formatted_school_name, year)
    except:
        return
    
def scrape_stats(page, formatted_school_name, year):
    URL = page
    r = requests.get(URL, headers=headers, verify=False)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    
    file_destination = ("data/" + formatted_school_name + "/" + 
        year + "/" + formatted_school_name + 
        "_official_statistics_" + year + ".txt")
    
    with open(file_destination, "w") as f:
        f.write("")
    
    with open(file_destination, "a") as f:
        counter = 0
        for r in soup.find_all("div", {"class": "stats-box stats-box-alternate full clearfix"}):
            if counter == 0:
                f.write("HITTING\n")
            elif counter == 1:
                f.write("EXTENDED HITTING\n")
            elif counter == 2:
                f.write("PITCHING\n")
            elif counter == 3:
                f.write("FIELDING\n")
            counter += 1
            
            for tr in r.find_all('tr')[2:]:
                tds = tr.find_all('td')
                try:
                    stat_line = []
                    for td in tds:
                        stat_line.append(td.text.strip())
                    stat_line = "\t".join(stat_line)
                    stat_line = stat_line.replace("\t\t", "\t-\t")
                    f.write(stat_line + "\n")
                except:
                    continue
        
    return
    
def scrape_lineup(page, formatted_school_name, year):
    URL = page
    r = requests.get(URL, headers=headers, verify=False)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    
    file_destination = ("data/" + formatted_school_name + "/" + 
        year + "/" + formatted_school_name + 
        "_team_" + year + ".txt")
    
    with open(file_destination, "w") as f:
        f.write("number f_name name class position\n")
    
    players = []
    for r in soup.find_all("div", {"class": "stats-box stats-box-alternate full clearfix"}):
        for tr in r.find_all('tr')[2:]:
            tds = tr.find_all('td')
            try:
                information = [tds[0].text, tds[1].text, tds[2].text, tds[3].text]
                information = [i.strip() for i in information]
                information[1] = re.sub(" +", " ", information[1])
                if len(information[1]) > 2:
                    information[1] = information[1].replace(" ", "_", (information[1].count(" ")-1))
                if information[0]:
                    players.append(" ".join(information))
            except:
                continue
                
    players = list(set(players))
                
    with open(file_destination, "a") as f:
        for player in players: 
            f.write(player + "\n")
        
    return
    
def scrape_lineup_name(page):
    URL = page
    r = requests.get(URL, headers=headers, verify=False)
    
    name = re.findall("<h1>.*Baseball Statistics.*</h1>", r.text)[0]
    name = name.split("-")[-1]
    name = name.split("<")[0]
    name = name.strip()
    
    return name
    
def scrape_lineup_year(page):
    URL = page
    r = requests.get(URL, headers=headers, verify=False)
    
    year = re.findall("<h1>.*Baseball Statistics.*</h1>", r.text)[0]
    year = year.split(">")[1]
    year = year.split(" ")[0]
    year = year[:2] + year[-2:]
    
    return year

def get_team_lineup_pages():    
    URL = lineup_url
    r = requests.get(URL, headers=headers, verify=False)

    links = re.findall(r"href=\".*/teams/.*\"", r.text)
    
    new_links = []
    [new_links.append(x) for x in links if x not in new_links]  
    links = new_links
    
    links = [l[6:-1] for l in links]
    links = [url_part_1 + l for l in links]
    
    return links
        
    