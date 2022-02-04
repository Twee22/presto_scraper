def output_play_by_play_data(play_by_play_data, formatted_school_name, year):
    
    file_destination = ("data/" + formatted_school_name + "/" + 
            year + "/" + formatted_school_name + 
            "_batting_" + year + ".txt")
    
    with open(file_destination, "w") as f:
        for data_point in play_by_play_data:
            f.write(data_point + "\n")