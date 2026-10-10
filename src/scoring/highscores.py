import json

file_path = open('./highscores.json', "r")
def load_highscores():
    if not file_path.exists():
        return []
    with open(file_path, "r") as file:
        return json.load(file)

def save_highscores():
    