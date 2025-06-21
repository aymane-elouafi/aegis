import getpass
import os
import time
from ui import header , clear_screen , print_info , print_error , print_success , print_warning 
from crypto_manager import save_vault , load_vault , initialize_vault
from actions import add_credential , list_services  , modify_credential , delete_credential , autotype_credential  


def main() :
    # clear the screen and print the header of the program
    clear_screen()
    header()
    if os.path.exists("vault.salt") :
        # "Sign In"
        # getpass: To securely prompt for the master password without it being visible.
        password = getpass.getpass("Enter the Master Password: ")
        # In your main() function
        data = load_vault(password)

        if data is not None:
            # Login was successful! Start the main menu with the data.
            show_main_menu_loop(data,password)
        else:
            # Login failed.
            print_error("Incorrect master password.")
    else:
        # "Sign Up"
        print_info("Welcome to Aegis! Let's set up your secure vault.")
        
        # Ask for the password
        password_1 = getpass.getpass("Create a Master Password: ")
        
        # Ask for it again to confirm
        password_2 = getpass.getpass("Confirm Master Password: ")

        # Check if they match
        if password_1 == password_2:
            # They match, so we can initialize the vault
            data = initialize_vault(password_1)
            if data is not None:
                # Login was successful! Start the main menu with the data.
                show_main_menu_loop(data,password_1)
            else:
                # If data is still None, it means login/setup failed.
                print_info("Exiting Aegis.")
                time.sleep(1)
                # The program will now naturally end because there's nothing else to do.
        else:
            # They don't match, show an error and exit
            print_error("Passwords do not match. Please try again.")
            time.sleep(2)
            # We would exit or handle this error here


def show_main_menu_loop(passwords_dictionary,password):
    while True :
        clear_screen()
        header()
        print(
            """ 
    [1] Add New Credentials
    [2] List All Services
    [3] Get & Autotype Password
    [4] Modify an Entry
    [5] Delete an Entry

    [q] Quit and Lock Vault

            """
        )
    
        user_choice = input("> ").lower().strip()

        if user_choice == "1" :
            add_credential(passwords_dictionary,password)
        elif user_choice == "2" :
            list_services(passwords_dictionary)
        elif user_choice == "3" :
            autotype_credential(passwords_dictionary)
        elif user_choice == "4" :
            modify_credential(passwords_dictionary,password)
        elif user_choice == "5" :
            delete_credential(passwords_dictionary,password)
        elif user_choice == "q" :
            clear_screen()
            print_info("Goodbye ! :) ")
            time.sleep(2)
            break
        else :
            print_error("Please enter a valid choice !")
            time.sleep(2)


if __name__ == "__main__" :
    main()


    