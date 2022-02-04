from src.setup.setup_helper_functions import check_data_file_exists, disable_warnings
from src.scraping_functions.scrape_school import scrape_school
from src.config.config import url_part_1, url_part_2

def main():
    
    disable_warnings()
    check_data_file_exists()
    
    # Get school list would eventually replace this test stuff
    test_school = {"url_part_1": url_part_1,
                   "url_part_2": url_part_2}
    school_list = [test_school]
    
    for school in school_list:
        scrape_school(school)
    
    print("Program terminates")
    return