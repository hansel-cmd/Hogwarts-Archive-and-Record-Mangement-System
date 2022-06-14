# Hogwarts Archive and Record Management System
Video Demo:  [https://youtu.be/azgNvJ3Kn6Y](https://youtu.be/azgNvJ3Kn6Y)

#### Description:
![main menu](/screenshots/main_menu.png)
The project is a console-based archive and record management system for *Hogwarts School of Witchcraft and Wizardry.*
The system contains five(5) functionalities namely - ***View, Find, About, Reproduce, Exit***, where:

***View*** 
![main menu](/screenshots/view.png)
- shows the records of all wizards present in the system. 
- contains pagination feature where it shows 5 wizards per page.
- For displaying the information in a tabular format, `tabulate` module is used.

***Find***
![main menu](/screenshots/find_1.png)
![main menu](/screenshots/find_2.png)
- allows the user to look for specific wizard/s based on the following lookup options:
    - *name* - the full name of the wizard
    - *house* - the house where the wizard belongs
    - *patronus* - the charm the wizard uses to protect him/herself from Dementors 
    - *wand* - the combination of the *wood* and *core* of the wizard's wand, i.e., [*vine, dragon heartstring*]
    - *species* - the type of species/being the wizard is part of
    - *ancestry* - the line of descent of the wizard 
    - *gender* - the gender of the wizard
    - *eye_color* - the color of the wizard's eyes
    - *hair_color* - the color of the wizard's hair
    - *date_of_birth (mm-dd-yyyy)* - the birthdate of the wizard
- uses `regular expression` at that specific lookup option column to find specific wizard/s
- contains the option to save or create a copy of the record the lookup returns

***About***
![main menu](/screenshots/about.png)
- shows the supposed information of the program. To be exact, it is a *lorem ipsum* paragraph.

***Reproduce***
![main menu](/screenshots/reproduce.png)
- contains the option to save and create a copy of the whole record the system has OR save and create a copy of the record of certain wizard/s.
- Calls ***find*** function if the user chooses to save a copy of specific wizards.

***Exit***
![main menu](/screenshots/exit.png)
- exits/closes the program
