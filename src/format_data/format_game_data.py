import re

from src.format_data.format_helper_functions import similar, remove_adjacent

def format_game_data(game_data, school_name):
    
    if not game_data:
        return []
    
    game_data = [re.sub("<[^>]*>", "", str(gd)) for gd in game_data]
    game_data = [re.sub("\s+", " ", r) for r in game_data]
    game_data = [re.sub("[\[\]]", "", r) for r in game_data]
    game_data = [r for res in game_data for r in re.split("[;,]", res)]
    game_data = [r.strip() for r in game_data]
    game_data = remove_adjacent(game_data)
    
    game_data = [g.lower() for g in game_data]

    game_data = find_game_data(game_data)
    game_data = format_team_names(game_data, school_name)

    game_data = game_data[-2:] + game_data[:-2]

    game_data.insert(0, "GAME_START_POINT")
    game_data.append("GAME_END_POINT")
    
    return game_data
    
def format_team_names(game_data, school_name):
    top_names = []
    bottom_names = []
    for g in game_data:
        if "top of" in g:
            top_names.append(re.sub("top of [0-9a-z]+ inning", "", (g + '.')[:-1]))
        elif "bottom of" in g:
            bottom_names.append(re.sub("bottom of [0-9a-z]+ inning", "", (g + '.')[:-1]))
    
    top_similarity = 0
    for t in top_names:
        top_similarity += similar(school_name, t)
    top_similarity = top_similarity / len(top_names)
    
    bottom_similarity = 0
    for b in bottom_names:
        bottom_similarity += similar(school_name, b)
    bottom_similarity = bottom_similarity / len(bottom_names)
    
    #removes duplicates
    top_names = list(set(top_names))
    bottom_names = list(set(bottom_names))
    
    if top_similarity > bottom_similarity:
        for t in top_names:
            game_data = [g.replace(t, school_name + " ") for g in game_data]
        for b in bottom_names:
            game_data = [g.replace(b, "OPPOSITION ") for g in game_data]
    else:
        for t in top_names:
            game_data = [g.replace(t, "OPPOSITION ") for g in game_data]
        for b in bottom_names:
            game_data = [g.replace(b, school_name + " ") for g in game_data]
            
    return game_data

def find_game_data(game_data):
    index = 0
    cont = True
    while cont:
        if "inning" in game_data[index]:
            cont = False
        else:
            index += 1
    
    return game_data[index:]