import json
import csv
import pyfiglet
from tabulate import tabulate
from sys import exit
import os


os.system("")

class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


# wizard_id
# name
# species = human, half-human, goblin
# house
# gender
# dateOfBirth
# ancestry
## eyeColour
## hairColour
# patronus
# hogwartsStudent
### hogwartsStaff
def populate_csv():
    filename =  "students.csv"
    dummy_data = "./data/characters.json"

    try:
        with open(dummy_data) as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Sorry. Student file cannot be found.")

    students = []
    for d in data:
        student = {
            "name":             d["name"] or "None",
            "house":            d["house"] or "None",
            "patronus":         d["patronus"] or "None",
            "wand":             f"{d['wand']['wood'] or 'None'}, {d['wand']['core'] or 'None'}",
            "species":          d["species"] or "None",
            "ancestry":         d["ancestry"] or "None",
            "gender":           d["gender"] or "None",
            "eye_color":        d["eyeColour"] or "None",
            "hair_color":       d["hairColour"] or "None",
            "date_of_birth":    d["dateOfBirth"] or "None"
        }
        students.append(student)

    with open(filename, "a", newline="") as file:
        fieldnames = [
            "name",  "house", "patronus", "wand",
            "species", "ancestry", "gender", "eye_color",
             "hair_color", "date_of_birth",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

    return True


def display_header():
    figlet = pyfiglet.Figlet()
    figlet.setFont(font="slant")
    print(Style.CYAN + figlet.renderText("Hogwarts"))


def display_options():
    header = ["Option", "Function", "Description"]
    table = [
        ["1", "View", "View Wizard Information"],
        ["2", "Find", "Look for a specific Wizard"],
        ["0", "Exit", "Exit/Quit the Program"],
    ]
    print(Style.WHITE + tabulate(table, header, tablefmt="simple"), "\n")

def prompt():
    
    display_header()
    display_options()
    
    while True:
        try:
            choice = input(Style.YELLOW + "What do you want to do? " + Style.RESET)
        except EOFError:
            exit("Program Terminated." + Style.RESET)
        except KeyboardInterrupt:
            exit("Program Terminated." + Style.RESET)
            

        if choice not in ['1', '2', '0']:
            continue
        break

    return int(choice)


def main():

    # Try to Open the student database file
    # Otherwise, try to populate the database
    # If all else fails, exit the program
    try:
        with open("students.csv") as file:
            reader = csv.DictReader(file)
    except FileNotFoundError:
        try:
            populate_csv()
        except FileNotFoundError:
            exit(Style.RED + "Sorry. Student file cannot be found."  + Style.RESET)

    if prompt() == 0:
        exit(Style.RED + "Program Terminated." + Style.RESET)


    


if __name__ == "__main__":
    main()