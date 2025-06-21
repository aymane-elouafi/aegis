import os
import platform



def clear_screen() :
    ''' os.system(...): This is a function from the os module that lets our Python script run a command directly in the computer's command prompt or terminal, just as if we had typed it in ourselves. '''
    # Check if the Operating System is Windows
    if platform.system() == "Windows" :
        os.system("cls")
    # Otherwise, it's probably Mac or Linux
    else :
        os.system("clear")


def header() :
    print("""

   █████████   ██████████   █████████  █████  █████████ 
  ███░░░░░███ ░░███░░░░░█  ███░░░░░███░░███  ███░░░░░███
 ░███    ░███  ░███  █ ░  ███     ░░░  ░███ ░███    ░░░ 
 ░███████████  ░██████   ░███          ░███ ░░█████████ 
 ░███░░░░░███  ░███░░█   ░███    █████ ░███  ░░░░░░░░███
 ░███    ░███  ░███ ░   █░░███  ░░███  ░███  ███    ░███
 █████   █████ ██████████ ░░█████████  █████░░█████████ 
░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░░░░░  ░░░░░  ░░░░░░░░░  
    
    +------------------------------------------+
            Your Secure Password Manager              
    +------------------------------------------+          

""")


class Colors:
    ''' A class to hold ANSI color codes. '''
    # Class attribute : These belong to the class itself. They are shared by all objects of the class, and they exist as soon as the class is defined, even before any objects are created.
    # Ex : \033[92m: This command tells the terminal, "From now on, make all text bright green."
    # The terminal follows that rule until it gets a new command. Without a "reset" command, all the text you print afterwards would continue to be green.
    # RESET : \033[00m: This is the command that says, "Stop all special styling. Go back to the terminal's default color and style."
    SUCCESS = "\033[92m"
    ERROR = "\033[91m"
    INFO = "\033[96m"
    WARNING = "\033[93m"
    RESET = "\033[0m"


# Print Color Text using ANSI escape sequences
def print_success(message) :
    print(f"{Colors.SUCCESS}{message}{Colors.RESET}")
def print_error(message):
    print(f"{Colors.ERROR}{message}{Colors.RESET}")
def print_info(message):
    print(f"{Colors.INFO}{message}{Colors.RESET}")
def print_warning(message):
    print(f"{Colors.WARNING}{message}{Colors.RESET}")

