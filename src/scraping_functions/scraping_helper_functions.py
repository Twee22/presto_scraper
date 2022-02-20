import re

def format_school_name(school_name):
    school_name = school_name.lower().replace(" ", "_").replace("&amp;", "and")
    school_name = re.sub(r"[^a-zA-Z0-9_]","", school_name)
    return school_name
