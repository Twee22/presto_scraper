from src.scraping_functions.scrape_links import get_all_school_links
from src.setup.setup_helper_functions import check_data_file_exists, disable_warnings
from src.scraping_functions.scrape_school import scrape_school
from src.scraping_functions.scrape_links import get_all_school_links

from src.config.config import url_part_1, url_part_2

def main():
    
    disable_warnings()
    check_data_file_exists()
    
    school_list = get_all_school_links()
    
    for school in school_list:
        scrape_school(school)
    
    print("Program terminates")
    return