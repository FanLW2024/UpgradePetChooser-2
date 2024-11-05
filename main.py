# Lir-Wan Fan
# Purpose: Upgrade your Pet Chooser
########## Original Pet Chooser: Creating a Pets Class using different inputs and values
                      # 1. Start
                      # 2. Connect to your personal (pets) database
                      # 3. Read data
                      # 4. Create one (object) instance of a Pets class for each pet listed in your database.
                      #     Keep your Pets class in a separate file
                      # 5. Display a list of pet names, from the pet object instances
                      # 6. Ask the user to choose a pet
                      # 7. Once a pet is chosen, print that pet's info from the (object) instance.
# Upgrade Pet Chooser ###############################################################
# (a) Clone your Pet Chooser program to a new PyCharm project.
#     At every menu, allow the user to use Q or q to quit your program nicely.
# (b) Initial View: When the program begins, list all of the pets like before, and ask the user to choose a pet.
#     Once a pet is chosen, print out the same information as before.
# (c) Options: When the pet's information has been displayed, ask the user if they would like to continue or edit the pet's information.
#     Display the chosen pet’s information and ask whether like to [C]ontinue, [Q]uit, or [E]dit this pet?
#     Choosing to quit (by typing Q + [ENTER]), quit the program nicely.
#     Choosing to continue (by typing C + [ENTER]), display the list of pets again from the Initial View.
#     Choosing to edit (by typing E + [ENTER]), display the Edit Process below.
# (d) Edit Process: Ask the user which pet to edit (a number from the Initial View list), step through the pet's name and age to ask the user to provide an update.
#     Updating that pet's name in the database.  Display a message indicating the pet's name has
#     Updating that pet's age in the database.  Display a message indicating the pet's age has been updated.
# When the updates are complete, display the list of pets again from the Initial View.
#########################################################################################

# (a) Clone your Pet Chooser program to a new PyCharm project.
# 1. Start
#### pip install pymysql
# Importing pymysql.cursors
import pymysql.cursors

# Contain your database credentials
from creds import *

# 4. Creating another python file named pet_class.py.  Importing PetsClass from this separate file.
from pets_class import PetsClass

# 3. Read data.  Creating a list of Pets Class instances based on the data fetched from the database.
pets_list = []

# 2. Creating a connection to the MySQL database
try:
    myConnection = pymysql.connect(
        host=hostname,
        user=username,
        password=password,
        db=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Database connection established.")

# If any error occurs, it will stored as e, and print the error message and exit the program.
except Exception as e:
    print(f"Error connecting to the database.  Exiting: {e}")
    exit()

try:
    with myConnection.cursor() as cursor:
        # Modify the SQL query to perform a LEFT JOIN to include pets without matching owners
        sqlSelect = """
            SELECT pets.name, types.animal_type as types_animal_type, pets.age, owners.name as owner_name
            FROM pets
            LEFT JOIN owners ON pets.owner_id = owners.id
            LEFT JOIN types ON pets.animal_type_id = types.id;
        """
        cursor.execute(sqlSelect)

        # Fetch all results at once
        rows = cursor.fetchall()

        if not rows:
            print("No pets found in the database.")

        else:
            # Clear the list to avoid duplicates
            pets_list.clear()

            # Create Pets instances
            for row in rows:
                owner_name = row['owner_name'] if row['owner_name'] else "Unknown Owner"  # Handle NULL owner
                types_animal_type = row['types_animal_type'] if row['types_animal_type'] else "Unknown Type"  # Handle NULL Type
                pet = PetsClass(row['name'], types_animal_type, owner_name, row['age'])
                pets_list.append(pet)  # Add to the pets list

except Exception as e:
    print(f"An error occurred while fetching pet data: {e}")

################################################################################
# 5. Display a list of pet names, from the pet object instances
# 6. Ask the user to choose a pet
def display_pet_choices():
    print("\n################################# Pet Chooser #################################")
    print("Welcome to Upgrade Pet Chooser!")
    print("Please choose a pet by serial number from the list below or enter 'q' to quit:")
    print("###############################################################################")

    for index, pet in enumerate(pets_list, start=1):
        print(f"[{index}] {pet.name}")

# (d) Edit Process: Function to edit a pet's name and age
def edit_pet(pet):
    print()
    print(f"You have chosen to edit {pet.name}.\n")
    new_name = input("New name: [ENTER == no change]: ")
    if new_name:
        pet.name = new_name
        print(f"The pet's name has been updated to {pet.name}.\n")

    new_age = input("New age: [ENTER == no change]: ")
    if new_age:
        try:
            pet.age = int(new_age)
            print(f"The pet's age has been updated to {pet.age}.\n")
        except ValueError:
            print("Invalid input. Age must be a number.\n")

while True:
# (b) Initial view: Display pet choices
    display_pet_choices()
    print("[Q] Quit")
    user_input = input("Input your choice from the list or enter 'q' to quit:").strip()

    if user_input.lower() == 'q':
        print()
        print(f"Thank you very much for using pet chooser.  Exiting the program.  Goodbye!")
        break

    try:
        choice = int(user_input) - 1  # Convert to index

        if 0 <= choice < len(pets_list):
            chosen_pet = pets_list[choice]

            # 7. Print the chosen pet's info from the (object) instance.
            print(f"\nYou have chosen {chosen_pet.name}, the {chosen_pet.type}. {chosen_pet.name} is {chosen_pet.age} years old. {chosen_pet.name}'s owner is {chosen_pet.owner}.")

# (c) Option: Check the user's chosen action
            action = input("Would you like to [C]ontinue, [Q]uit, or [E]dit this pet? ").strip().lower()
            if action == "c":
                continue

            elif action == "q":
                print()
                print(f"Thank you very much for using pet chooser.  Exiting the program.  Goodbye!")
                break

            elif action == "e":
                edit_pet(chosen_pet)
                continue

            else:
                print("Invalid choice. Please select a valid option.")

        else:
            print("Invalid choice.  Please select a valid number.")

    except ValueError:
        print("Invalid input. Please input a number corresponding to your choice or 'q' to quit.")

# Close the database connection after data is fetched
myConnection.close()
print("Database connection closed.")

