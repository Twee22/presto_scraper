from os import getcwd, mkdir
from os.path import isdir
import urllib3

def check_data_file_exists():
    path = getcwd() + "/data"

    if not isdir(path):
        mkdir(path)
        
def disable_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
def check_school_file_exists(formatted_school_name, year):
    path = getcwd() + "/data/" + formatted_school_name

    if not isdir(path):
        mkdir(path)

    path = getcwd() + "/data/" + formatted_school_name + "/" + year

    if not isdir(path):
        mkdir(path)