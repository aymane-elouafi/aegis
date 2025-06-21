# Aegis - A secure, interactive command-line password manager

#### Description:

Aegis is a secure, interactive command-line password manager built with Python. It allows users to store, manage, and retrieve their sensitive credentials in a locally stored, fully encrypted vault. The application is protected by a single master password and features a user-friendly, menu-driven interface.

This project was created as a final project for CS50P.

#### Features

- **Secure Encrypted Vault:** All stored credentials are encrypted using AES in GCM mode, a modern and highly secure authenticated encryption standard.
    
- **Master Password Protection:** A single master password, strengthened using the PBKDF2 key derivation function, is used to encrypt and decrypt the entire vault.
    
- **Intuitive CLI Menu:** A simple, menu-driven interface that guides the user through all available actions.
    
- **Full CRUD Functionality:**
    
    - **Add:** Add new service credentials (service name, username, and password).
        
    - **Modify:** Interactively select and modify the username or password for any saved account.
        
    - **Delete:** Securely select and delete any saved account.
        
- **List and Select:** Easily list all saved services and select accounts from interactive, numbered menus to prevent typos.
    
- **Autotype Credentials:** A powerful feature that automatically types the selected username and password into any login field, eliminating the need for copy and paste.
    

#### Installation

To run Aegis, you first need to install the required Python libraries from the `requirements.txt` file.

1. **Clone or download the project** into a local directory.
    
2. **Navigate to the project directory** in your terminal.
    
    ```
    cd path/to/your/project/folder
    ```
    
3. **It is recommended to use a virtual environment.**
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    
4. **Install the dependencies.**
    
    ```
    pip install -r requirements.txt
    ```
    

#### Usage

Once the dependencies are installed, running the application is simple.

1. **Run the main script:**
    
    ```
    python project.py
    ```
    
2. **First-Time Setup:** If this is your first time running the application, it will guide you through the process of creating a secure master password.
    
3. **Login:** On subsequent runs, you will be prompted to enter your master password to unlock the vault.
    
4. **Main Menu:** After a successful login, you will be presented with the main menu. Simply enter the number corresponding to the action you wish to perform and follow the on-screen prompts.
    
    ```
       [1] Add New Credentials
       [2] List All Services
       [3] Get & Autotype Password
       [4] Modify an Entry
       [5] Delete an Entry
    
       [q] Quit and Lock Vault
    ```
    

### Autotype Warning

When using the Autotype feature, you will have a 5-second countdown. During this time, you must place your mouse cursor in the **username field** of the login form you wish to fill. The script will then automatically type the username, press the `Tab` key, and type the password. Be careful not to have another window or text field in focus, as the script will type wherever the cursor is placed.

## Technology Stack

- **Language:** Python 3
    
- **Cryptography:** `pycryptodome` for PBKDF2 key derivation and AES-GCM encryption.
    
- **Automation:** `pyautogui` for the keyboard automation in the autotype feature.
    
- **Standard Libraries:** `os`, `platform`, `json`, `getpass`, `time`.
    
- **Testing:** `pytest` for unit testing the application's core logic.
