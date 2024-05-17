# Dictionary to store game library with their quantities and rental costs
import os

game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2.0},
    "Super Mario Bros": {"quantity": 5, "cost": 3.0},
    "Tetris": {"quantity": 2, "cost": 1.0},
    "Tekken": {"quantity": 1, "cost": 6.0}
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Main menu
def main():
    os.system('cls')
    print("\nVIDEO GAME RENTAL SYSTEM")
    
    try:
        while True:
            print("\nWhat action would you like to do?\n1. User Login\n2. User Registration\n3. Admin Login\n4. Exit")

            choice = int(input("Choose a number: "))

            if choice == 1:
                os.system('cls')
                login()
            elif choice == 2:
                os.system('cls')
                register_user()
            elif choice == 3:
                os.system('cls')
                admin_login()
            elif choice == 4:
                os.system('cls')
                print("You have exited the program!")
                break
            else:
                print("Choose a valid number!")

    except ValueError as e:
        print("You have to choose a number!")
        main()
        return

    return

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("\nAvailable Games: ")
    for game_id, (game, game_details) in enumerate(game_library.items(), start = 1):
        print(f"{game_id}. {game}:")
        for quantity, cost in game_details.items():
            print(f"\t\t\t{quantity}: {cost}")

    return    

# Function to register a new user
def register_user(): 
    print("\nUSER REGISTRATION")
    
    while True:
        username = input("Enter username: ")
        
        if username in user_accounts:
            print("Username is already taken.")
        break
    
    password = input("Enter password: ")

    user_accounts[username] = {
        "password": password, 
        "balance": 0.0, 
        "points": 0, 
        "inventory": [],
    }
    print("\nYou have succesfully registered!")

    return

# Function to rent a game
def rent_game(username):
    display_available_games()
    
    print("\nRENT GAME")

    while True:
        chosen_game = input("\nWhat game would you like to rent? (Press Enter to go back)\n")

        if not chosen_game:
            os.system('cls')
            return
        
        if chosen_game not in game_library:
            print(f"{chosen_game} doesn't exist!")
            continue
        
        if game_library[chosen_game]["quantity"] == 0:
            print(f"{chosen_game} is out of stock.")
            continue
        
        if game_library[chosen_game]["cost"] > user_accounts[username]["balance"]:
            print(f"You don't have enough money to rent {chosen_game}! Please top-up.")
            input("Press Enter to continue")
            top_up_account(username)
            return

        game_library[chosen_game]["quantity"] -= 1
        user_accounts[username]["balance"] -= game_library[chosen_game]["cost"]
        user_accounts[username]["inventory"].append(chosen_game)
        user_accounts[username]["points"] += game_library[chosen_game]["cost"] / 2
        
        print(f"You have rented {chosen_game}!")
        print(f"You have earned {game_library[chosen_game]['cost'] / 2} points! Total points: {user_accounts[username]['points']}")
        print(f'Your remaining balance is ${user_accounts[username]["balance"]}')
        
        return

# Function to return a game
def return_game(username):
    print("\nRETURN GAME")
    while True:
        display_game_inventory(username)
        game = input("What game would you like to return? (Press Enter to go back) \n")

        if not game: 
            os.system('cls')
            return

        if game not in user_accounts[username]["inventory"]:
            print(f"{game} doesn't exist!")
            continue
        break   

    game_library[game]["quantity"] += 1
    user_accounts[username]["inventory"].remove(game)
    print(f"You have returned {game}.")

    display_game_inventory(username)
    return

# Function to top-up user account
def top_up_account(username):
    print("\nTOP-UP")

    while True: 
        try:
            amount = float(input("How much would you like to top-up? "))
            if amount <= 0:
                raise Exception()
            break

        except:
            print("Enter a valid amount!")

    user_accounts[username]["balance"] += amount
    print(f"Current Balance: ${user_accounts[username]['balance']}")
    return

# Function to display user's inventory
def display_inventory(username):
    print("\nINVENTORY")

    print(f"Balance: ${user_accounts[username]['balance']}")
    print(f"Points: {user_accounts[username]['points']}")
    
    display_game_inventory(username)
    return

# Function for admin to update game details
def admin_update_game():
    print("\nADMIN GAME UPDATE MENU")
    
    while True:
        display_available_games()
        game = input("Which game would you like to update? (Press Enter to go back) \n")

        if not game: 
            os.system('cls')
            return

        if game not in game_library:
            print(f"{game} does not exist!")
            continue
        
        try:
            detail_update = int(input("What game detail will you update? \n\t1. Quantity\n\t2. Cost \n"))

            if detail_update == 1:
                quantity = int(input(f"Change game quanity from {game_library[game]['quantity']} to: "))
                game_library[game]["quantity"] = quantity
            elif detail_update == 2:
                cost = float(input(f"Change game quanity from {game_library[game]['cost']} to: "))
                game_library[game]["cost"] = cost
                break
            else:
                print("Choose a valid number!")

        except ValueError as e:
            print("You have to choose a number!", e)
            return
        
    display_available_games()
    return

# Function for admin login
def admin_login():
    print("\nADMIN LOGIN")
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    if check_credentials(username, password, True):
        admin_menu()
        return
    else:
        print("Returning to menu...")
        os.system('cls')
        return

# Admin menu
def admin_menu():
    try:
        while True:
            print("\nWhat action would you like to do?\n1. Update Game Details\n2. Log-out")

            choice = int(input("Choose a number: "))

            if choice == 1:
                os.system('cls')
                admin_update_game()
            elif choice == 2:
                print("Logging out...")
                os.system('cls')
                break
            else:
                print("Choose a valid number!")

    except ValueError as e:
        print("You have to choose a number!")
    return

# Function for users to redeem points for a free game rental
def redeem_free_rental(username):
    print("\nREDEEM FREE RENTAL (at least 3 points to redeem a game)")

    needed_points = 3

    while True:
        display_available_games()
        chosen_game = input("What game would you like to rent using points? (enter to return) \n")

        if not chosen_game: 
            os.system('cls')
            return

        if chosen_game not in game_library:
            print("Game does not exist.")
            continue
        
        if game_library[chosen_game]["quantity"] <= 0:
            print(f"Sorry, {chosen_game} is out of stock!")
            break
        
        if user_accounts[username]["points"] < needed_points:
            print(f"You don't have enough points to rent {chosen_game}.")
            return

        game_library[chosen_game]["quantity"] -= 1
        user_accounts[username]["points"] -= needed_points
        user_accounts[username]["inventory"].append(chosen_game)

        print(f"You have rented {chosen_game} using your points!")
        print(f"Current Points: {user_accounts[username]['points']}")
        return

# Function to display game inventory
def display_game_inventory(username):
    print("\nGAME INVENTORY")

    print("Inventory contains: ")
    for i in user_accounts[username]['inventory']:
        print(f"> {i}")

    return

# Function to handle user's logged-in menu
def logged_in_menu(username):
    try:
        while True:
            print("\nUSER MENU")
            print("\nWhat action would you like to do?\n1. Top-up\n2. Show Available Games\n3. Rent a Game\n4. Use Points to Redeem a Game\n5. Return a Game\n6. Check Profile\n7. Log-out")

            choice = int(input("Choose a number: "))

            if choice == 1:
                os.system('cls')
                top_up_account(username)
            elif choice == 2:
                os.system('cls')
                display_available_games()
            elif choice == 3:
                os.system('cls')
                rent_game(username)
            elif choice == 4:
                os.system('cls')
                redeem_free_rental(username)
            elif choice == 5:
                os.system('cls')
                return_game(username)
            elif choice == 6:
                os.system('cls')
                display_inventory(username)
            elif choice == 7:
                print("Logging out...")
                os.system('cls')
                break
            else:
                print("\nChoose a valid number!")

    except ValueError as e:
        print("You have to choose a number!")
        logged_in_menu(username)
        return
    
# Function to handle login
def login():
    print("\nUSER LOGIN")
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    if check_credentials(username, password, False):
        logged_in_menu(username)
        return
    else:
        print("Returning to menu...")
        os.system('cls')
        return

# Function to check user credentials
def check_credentials(username, password, admin):
    if admin:
        if username == admin_username and password == admin_password:
            print("Admin logged in.")
            os.system('cls')
            return True
        else: 
            print("Incorrect credentials.")
            return False
    
    if not admin:
        if username in user_accounts:
            if user_accounts[username]["password"] == password:
                print("\nLogged in.")
                os.system('cls')
                return True
            else:
                print("Incorrect credentials")
                return False
        else:
            print("\nUser does not exist. You have to register first!")
            return False

if __name__ == "__main__":
    main()