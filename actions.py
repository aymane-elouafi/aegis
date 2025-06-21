import pyautogui
import time
from ui import header , clear_screen , print_info , print_error , print_success , print_warning 
from crypto_manager import save_vault 
import getpass


def add_credential(passwords_dictionary , password) :

    clear_screen()
    print_info("Add new credentials...")
    time.sleep(1)
    header()

    service = input("Enter the service name: ").strip().lower()
    username = input("Enter the username: ")
    new_password = getpass.getpass("Enter the password: ")

    new_account = {"username": username, "password": new_password} 

    if service in passwords_dictionary :
        # Service exists, append the new account to the list
        passwords_dictionary[service].append(new_account)
    else :
        # This is a new service, create a new list for it
        passwords_dictionary[service] = [new_account]

    save_vault(passwords_dictionary,password)

    print_success(f"Credentials for '{service}' saved successfully!")

    time.sleep(2)


def list_services(passwords_dictionary) :
    clear_screen()
    print_info("Loading your services...")
    time.sleep(1)
    clear_screen()
    header()
    print_info("--- Your Saved Services ---")

    '''

    This is a common and "Pythonic" way to check if a container is empty. In Python, an empty dictionary ({}) evaluates to False in a boolean context. So, not passwords_dictionary will be True only when the dictionary has no keys in it. It's a slightly shorter way of writing if passwords_dictionary == {}. If it's empty, we print a helpful message.
    
    '''

    if not passwords_dictionary :
        print_info("\nYour vault is currently empty.")
    else :

        '''

        passwords_dictionary.keys(): This gets all the keys (the service names like "Google", "Amazon", etc.) from our dictionary.

        enumerate(...): This is a brilliant built-in Python function. It takes an iterable (like our list of keys) and turns it into a series of pairs. Each pair contains a counter and the original item.

        , 1: By default, enumerate starts its counter at 0. For a user-facing list, we want to start at 1. This second argument tells enumerate to begin counting from 1.

        for i, service in ...: This loop iterates through the pairs provided by enumerate. In each loop, the variable i will hold the number (1, 2, 3, ...) and the variable service will hold the service name string.

        '''

        for i, service in enumerate(passwords_dictionary.keys() , 1):
            print(f"[{i}] {service}")
            
    input("\nPress Enter to return to the main menu...")


def select_account(passwords_dictionary):
    clear_screen()
    header()

    if not passwords_dictionary:
        print_info("Your vault is currently empty.")
        time.sleep(2)
        return None, None # Return nothing if the vault is empty
    
    # --- Part 1: Select the Service ---

    # Convert keys to a list so we can access by index
    services_list = list(passwords_dictionary.keys())

    print_info("--- Select a Service ---")
    for i, service in enumerate(services_list, 1):
        print(f"[{i}] {service}")
    
    try:
        service_choice_str = input("\nEnter the number of the service (or 'c' to cancel): ")
        if service_choice_str.lower() == 'c':
            return None, None

        # Convert input to a valid index
        service_choice_num = int(service_choice_str)
        # Check if that number is in the valid range (e.g., if there are 3 services, the number must be between 1 and 3).
        if not (1 <= service_choice_num <= len(services_list)):
            raise ValueError("Choice out of range.")
        
        selected_service_index = service_choice_num - 1
        selected_service_name = services_list[selected_service_index]

    except (ValueError, IndexError):
        print_error("Invalid selection. Returning to main menu.")
        time.sleep(2)
        return None, None

    # --- Part 2: Select the Account ---

    accounts_list = passwords_dictionary[selected_service_name]

    if len(accounts_list) == 1:
        # If there's only one account, we don't need to ask
        return selected_service_name, 0 # Return the service and the first (and only) index

    print_info(f"\n--- Select an Account for '{selected_service_name}' ---")

    for i, account in enumerate(accounts_list, 1):
        # Access the username from the dictionary inside the list
        print(f"[{i}] {account['username']}")

    try:
        account_choice_str = input("\nEnter the number of the account (or 'c' to cancel): ")
        if account_choice_str.lower() == 'c':
            return None, None
        
        account_choice_num = int(account_choice_str)
        if not (1 <= account_choice_num <= len(accounts_list)):
            raise ValueError("Choice out of range.")
            
        selected_account_index = account_choice_num - 1
        
        # We have everything we need!
        return selected_service_name, selected_account_index
    
    except (ValueError, IndexError):
        print_error("Invalid selection. Returning to main menu.")
        time.sleep(2)
        return None, None
    

def delete_credential(passwords_dictionary, password) :
    service_name, account_index = select_account(passwords_dictionary)
    if service_name is not None :
        username_to_delete = passwords_dictionary[service_name][account_index]['username']
        print_warning(f"Are you sure you want to delete the account '{username_to_delete}' for '{service_name}'? [y/n]:")
        answer = input("> ").strip().lower()
        if answer == 'y' :
            accounts_list = passwords_dictionary[service_name]
            accounts_list.pop(account_index)
            if not accounts_list :
                del passwords_dictionary[service_name]
            save_vault(passwords_dictionary, password)
            print_success(f"Credentials for '{service_name}' deleted successfully!")
        else : 
            # If user answers anything other than 'y', confirm cancellation
            print_info("Deletion cancelled.")
        # Pause so the user can see the result
        time.sleep(2)
    else :
        return None
        
def modify_credential(passwords_dictionary, password) :
    service_name, account_index = select_account(passwords_dictionary)
    if service_name is not None :
        print_info("""What would you like to modify?
                    [1] Username
                    [2] Password
                   """)        
        answer = input("> ").strip()

        modification_made = False

        if answer == "1" :
            new_username = input("Enter the new username: ")
            passwords_dictionary[service_name][account_index]['username'] = new_username
            modification_made = True
        elif answer == "2":
            new_password = getpass.getpass("Enter the new password: ")
            passwords_dictionary[service_name][account_index]['password']= new_password
            modification_made = True
        else :
            print_error("Modification cancelled.")
        if modification_made :
            save_vault(passwords_dictionary, password)
            print_success(f"Credentials for '{service_name}' modified successfully!")
        time.sleep(2)
    else :
        return None 
        

def autotype_credential(passwords_dictionary):
    service_name, account_index = select_account(passwords_dictionary)
    if service_name is not None :
        #  retrieve the username and password from the dictionary
        username = passwords_dictionary[service_name][account_index]['username']
        password = passwords_dictionary[service_name][account_index]['password']
        print_warning("""

[!] IMPORTANT: You have 5 seconds to place your cursor in the USERNAME field.
[!] The script will then type the username and password automatically.

                      """)
        #  visual countdown 
        for i in range(5,0,-1) :
            print(f"    Typing in {i}...", end='\r') # '\r' moves cursor to the start of the line
            time.sleep(1)
        print_info("Typing now...")
        pyautogui.typewrite(username, interval=0.05) # Add a small interval for reliability
        pyautogui.press('tab')
        time.sleep(0.1) # A tiny pause can help
        pyautogui.typewrite(password, interval=0.05)
        pyautogui.press('enter')

        print_success("Autotype complete!")
        time.sleep(2)

