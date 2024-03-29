from src.scraping_functions.game_list import get_game_list
from src.scraping_functions.extract_school_information import get_school_name, get_year
from src.scraping_functions.scrape_game import scrape_game
from src.scraping_functions.scraping_helper_functions import format_school_name
from src.setup.setup_helper_functions import check_school_file_exists
from src.format_data.format_game_data import format_game_data
from src.output_data.output_data import output_play_by_play_data

def scrape_school(school):

    try:
        school_name = get_school_name(school)
        print("Beginning to scrape: ", school_name)
        year = get_year(school)
    except:
        # This triggers if the school doesn't exist
        print(str(school["url_part_1"]+school["url_part_2"]), "failed")
        return
    
    formatted_school_name = format_school_name(school_name)
    
    check = check_school_file_exists(formatted_school_name, year)
    
    game_links = get_game_list(school)
    play_by_play_data = []
    
    len_game_links = len(game_links)  
    half_game_links = len_game_links / 2  

    for count, link in enumerate(game_links):
        if count == half_game_links or count == (half_game_links - 0.5):
            print(school_name, "50% complete")
        try:
            game_data = scrape_game(link, school_name)
            play_by_play_data += format_game_data(game_data, school_name)
        except:
            # This triggers if the game can't be scraped
            continue
        
    output_play_by_play_data(play_by_play_data, formatted_school_name, year)
    
    print(school_name, "completed")