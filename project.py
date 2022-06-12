import json
import csv
import pyfiglet
from tabulate import tabulate
from sys import exit
import os


os.system("")
FIELDNAMES = [
    "name",  "house", "patronus", "wand",
    "species", "ancestry", "gender", "eye_color",
    "hair_color", "date_of_birth",
]
CLEAR = "cls" if os.name == "nt" else "clear"


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

    wizards = []
    for d in data:
        wizard = {
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
        wizards.append(wizard)
        if len(wizards) >= 20:
            break

    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(wizards)

    return wizards


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


def display():
    ...


def view_controller(wizards, page):
    index = page * 5
    return wizards[index:index + 5]


def view(wizards):
    table = []
    # iterate all wizard dicts in the list
    # get its value and transform into a list.
    # tabulate() function needs [[], []] not [{}, {}]
    for wizard in wizards:
        row = []
        for values in wizard.values():
            row.append(values)
        table.append(row)


    current_page = 0
    max_page = int(len(wizards) / 5)
    
    print("PAGE: " + Style.RED + str(current_page + 1) + Style.RESET + " of " + \
            Style.RED + str(max_page) + Style.RESET)
    print(tabulate(table[current_page:current_page + 5], FIELDNAMES, tablefmt="grid"))
    
    # increment to 1 since we displayed wizards prior to this line
    current_page += 1
    while True:
        try:
            key = input("Press " + Style.YELLOW + "Enter " + Style.RESET + \
            "to show more (if there is any)... ")    
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        
        if key != "":
            continue       
    
        os.system(CLEAR)
        if current_page >= max_page:
            break
        
        render = view_controller(table, page=current_page)
        current_page += 1
        display_header()
        display_options()
        print("PAGE: " + Style.RED + str(current_page) + Style.RESET + \
                " of " + Style.RED + str(max_page) + Style.RESET)
        print(tabulate(render, FIELDNAMES, tablefmt="grid"))
    


def get_wizards():

    filename = "students.csv"
    try:           
        file = open(filename)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename} cannot be found.")
    except OSError:
        raise OSError(f"OS Error happened while accessing {filename}")
    except Exception as err:
        raise Exception(f"Unexpected error happened while accessing {filename}")

    with file:
        reader = csv.DictReader(file)
        wizards = [row for row in reader]

    return wizards


def main():

    # Try to Open the student database file
    # Otherwise, try to populate the database
    # If all else fails, exit the program
    try:
        wizards = get_wizards()
    except FileNotFoundError:
        try:
            wizards = populate_csv()
        except FileNotFoundError:
            exit(Style.RED + "Sorry. Student file cannot be found."  + Style.RESET)

    while True:
        choice = prompt()
        if choice == 0:
            exit(Style.RED + "Program Terminated." + Style.RESET)
        elif choice == 1:
            view(wizards)


    
if __name__ == "__main__":
    main()