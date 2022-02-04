from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def remove_adjacent(list):
  i = 1
  while i < len(list):    
    if list[i] == list[i-1]:
      list.pop(i)
      i -= 1  
    i += 1
  return list