import json
import csv
import re
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


def wait():
    while True:
        try:
            key = input("Press " + Style.YELLOW + "Enter " + \
            Style.RESET + "to return...")
        except EOFError:
            break
        except KeyboardInterrupt:
            break

        if key == "":
            break
    os.system(CLEAR)


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


def display_options(header, table):
    print(Style.WHITE + tabulate(table, header, tablefmt="simple"), "\n")


def prompt():
    display_header()
    display_options(["Option", "Function", "Description"], [
        ["1", "View", "View Wizard Information"],
        ["2", "Find", "Look for a specific Wizard"],
        ["3", "About", "About the program"],
        ["4", "Reproduce", "Create a CSV copy"],
        ["0", "Exit", "Exit/Quit the Program"],
    ])
    
    while True:
        try:
            choice = input(Style.YELLOW + "What do you want to do? " + Style.RESET)
        except EOFError:
            exit("Program Terminated." + Style.RESET)
        except KeyboardInterrupt:
            exit("Program Terminated." + Style.RESET)
            

        if choice not in ['1', '2', '3', '4', '0']:
            continue
        break

    return int(choice)


def pagination(wizards, page):
    index = page * 5
    return wizards[index:index + 5]


def to_table_wizards(wizards):
    table = []
    # iterate all wizard dicts in the list,
    # get its value and transform into a different list.
    # tabulate() function needs [[], []] not [{}, {}]
    for wizard in wizards:
        row = []
        for values in wizard.values():
            row.append(values)
        table.append(row)

    return table


def view(wizards):
    
    table = to_table_wizards(wizards)

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
            "to show more (if there is any) while " + Style.YELLOW + "Space " + \
                Style.RESET + "to return...")    
        except EOFError:
            break
        except KeyboardInterrupt:
            break

        if key == " ":
            break

        if key != "":
            continue

        os.system(CLEAR)
        if current_page >= max_page:
            break
        
        render = pagination(table, page=current_page)
        current_page += 1
        display_header()
        display_options(["Option", "Function", "Description"], [
        ["1", "View", "View Wizard Information"],
        ["2", "Find", "Look for a specific Wizard"],
        ["0", "Exit", "Exit/Quit the Program"],
    ])
        print("PAGE: " + Style.RED + str(current_page) + Style.RESET + \
                " of " + Style.RED + str(max_page) + Style.RESET)
        print(tabulate(render, FIELDNAMES, tablefmt="grid"))

    os.system(CLEAR)
    

def find(wizards):
    header = ["Lookup Option", "Lookup Description"]
    table = [
        ["1.",  "name"],
        ["2.",  "house"],
        ["3.",  "patronus"],
        ["4.",  "wand"],
        ["5.",  "species"],
        ["6.",  "ancestry"],
        ["7.",  "gender"],
        ["8.",  "eye_color"],
        ["9.",  "hair_color"],
        ["10.", "date_of_birth (dd-mm-yyyy)"],
        ["0.",  "Back"]
    ]
    
    display_options(header, table)
    render = []
    while True:
        try:
            choice = input(Style.YELLOW + "Find wizard/s using option: " + Style.RESET)
        except EOFError:
            break
        except KeyboardInterrupt:
            break

        if choice not in list(map(str, list(range(len(table))))):
            continue

        if choice == "0":
            break

        kw = input(Style.YELLOW + f"Enter wizard's {FIELDNAMES[int(choice) - 1]}: " + Style.RESET)
        render = search_wizard(wizards, FIELDNAMES[int(choice) - 1], kw)
        render = to_table_wizards(render)
        os.system(CLEAR)
        display_options(header, table)
        print(tabulate(render, FIELDNAMES, tablefmt="grid"))
        
        while True:
            try:
                answer = input(Style.YELLOW + \
                    "Do you want to create a copy of this lookup (yes/no)? " + \
                    Style.RESET)
            except EOFError:
                break
            except KeyboardInterrupt:
                break

            if re.search("^([y]+.*)$", answer, re.IGNORECASE):
                try:
                    filename = input(Style.YELLOW + \
                        "Enter filename for this copy (archives.csv is the default name): " + \
                            Style.RESET)
                except Exception:
                    filename = "archives.csv"
                
                if filename == "" or not re.search(r"^([\w\d_ -])+$", filename):
                    filename = "archives.csv"

                try:
                    create_csv(filename, render, fr="find")
                except OSError:
                    raise OSError(f"OS Error happened while creating {filename}")
                except Exception:
                    raise Exception(f"Unexpected error happened while creating {filename}")

                display_options(header, table)
                break
            
            if re.search("^([n]+.*)$", answer, re.IGNORECASE):
                break

    os.system(CLEAR)
    return render


def search_wizard(wizards, col, kw):
    if col == "gender":
        # so that if kw = male, it will only look up [^fe]male wizards
        pattern = f"^({kw}).*$"
    else:
        pattern = f"^.*({kw}).*$"
    filtered_wizards = filter(
        lambda wizard: re.search(pattern, wizard[col], re.IGNORECASE),  
        wizards
    )

    return list(filtered_wizards)


def get_wizards():
    filename = "students.csv"
    try:           
        file = open(filename)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename} cannot be found.")
    except OSError:
        raise OSError(f"OS Error happened while accessing {filename}")
    except Exception:
        raise Exception(f"Unexpected error happened while accessing {filename}")

    with file:
        reader = csv.DictReader(file)
        wizards = [row for row in reader]

    return wizards


def about_program():
    display_header()
    print("""
    Welcome to Hogwarts' Archives and Record Management. 

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi 
    ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum 
    dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
    deserunt mollit anim id est laborum. 

    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, 
    totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta 
    sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia 
    consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui 
    dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora 
    incidunt ut labore et dolore magnam aliquam quaerat voluptatem.

    - Hogwarts, circa 9th-10th Century
    """ + Style.RESET)

    wait()


def create_csv(filename, wizards, fr="reproduce"):
    if fr == "find":
        row = []
        for wizard in wizards:
            w = {
                "name":             wizard[0],
                "house":            wizard[1],
                "patronus":         wizard[2],
                "wand":             wizard[3],
                "species":          wizard[4],
                "ancestry":         wizard[5],
                "gender":           wizard[6],
                "eye_color":        wizard[7],
                "hair_color":       wizard[8],
                "date_of_birth":    wizard[9]
            }
            row.append(w)
        wizards = row

    if ".csv" not in filename:
        filename += ".csv"
    try:
        file = open(filename, "w", newline="")
    except OSError:
        raise OSError(f"OS Error happened while creating {filename}")
    except Exception:
        raise Exception(f"Unexpected error happened while creating {filename}")
    
    with file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(wizards)
    print(Style.GREEN + f"{filename} created successfully!")

    wait()
    return True


def reproduce(wizards):

    while True:
        try:
            choice = input(Style.YELLOW + "Reproduce the whole CSV file (yes/no)? " + \
                Style.RESET).strip()
        except EOFError:
            return None
        except KeyboardInterrupt:
            return None

        if re.search("^([y]+.*)$", choice, re.IGNORECASE):
            filename = "archives.csv"
            try:
                create_csv(filename, wizards)
            except OSError:
                raise OSError(f"OS Error happened while creating {filename}")
            except Exception:
                raise Exception(f"Unexpected error happened while creating {filename}")
            return True
        
        if re.search("^([n]+.*)$", choice, re.IGNORECASE):
            break
    
    print("\nCreate .csv with specific wizards using lookup.\n")
    find(wizards)
    wait()
    

def main():
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
        elif choice == 2:
            os.system(CLEAR)
            find(wizards)
        elif choice == 3:
            os.system(CLEAR)
            about_program()
        elif choice == 4:
            reproduce(wizards)


if __name__ == "__main__":
    main()