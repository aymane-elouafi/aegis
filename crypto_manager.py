from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import json
from ui import print_error 

def initialize_vault(password) :

    '''
    What is a Salt? A salt is a random piece of data. Its purpose is to make your encryption unique. Even if two users chose the exact same master password ("password123"), their salts would be different, which means their final encryption keys will also be completely different. This prevents attackers from using pre-computed "rainbow tables" to crack common passwords.

    '''

    '''
    get_random_bytes(16): This is a function from the pycryptodome library. It generates cryptographically secure random data. We use this instead of Python's standard random module because the random module is predictable and not safe for security use. 16 means we are generating 16 bytes (a common and secure length for a salt).

    '''

    # generate the salt using get_random_bytes(16)
    salt = get_random_bytes(16)

    # open a file and write the salt bytes on it 
    # The 'wb' is crucial – it means Write Bytes.
    with open("vault.salt", "wb") as f:
        f.write(salt)

    # encode the master password to bytes : password.encode('utf-8')
    password = password.encode('utf-8')

    '''
    
    This is the most important security step. We are turning the user's (potentially weak) password into a powerful, machine-strength encryption key.

    PBKDF2(...): This is the Password-Based Key Derivation Function 2. It's a special algorithm designed to be deliberately slow to protect against brute-force attacks.

    password.encode('utf-8'): Cryptographic functions don't work on Python strings; they work on bytes. This line converts the user's password string (e.g., "MyPassword123") into its byte representation.

    salt: We provide the salt we just generated. This ensures the derived key is unique.

    dkLen=32: This stands for Derived Key Length. We are telling PBKDF2 to produce a key that is 32 bytes long, which is the required length for the very strong AES-256 encryption standard.

    count=1000000: This is the iteration count. PBKDF2 will perform an internal hashing operation one million times. This is what makes it slow for an attacker. For you, it might take a fraction of a second, but for an attacker trying billions of passwords, it's a massive roadblock.

    '''
    # use the password and the salt you just created to generate the strong encryption key.
    key = PBKDF2(password, salt, dkLen=32, count=1000000)

    # create an empty dictionnary 
    empty_vault_data = {}

    # W3schools : If you have a Python object, you can convert it into a JSON string by using the json.dumps() method.
    # convert the dictionnary to a JSON string using json.dumps()
    # the result is a JSON string:
    json_data = json.dumps(empty_vault_data)

    # Encode that JSON string into bytes, because the encryption function needs bytes: 
    byte_data = json_data.encode('utf-8')

    '''
    AES.new(...): This creates a new encryption "cipher" object. We give it the powerful key we derived . We also tell it to use AES.MODE_GCM. 
        GCM mode is a modern and highly secure mode that provides both encryption (scrambling the data) and authentication (ensuring the data isn't tampered with).

    cipher.encrypt_and_digest(...): This is the method that does the actual work. It takes our byte data (b'{}') and produces two outputs:

        ciphertext: The scrambled, unreadable version of our data.

        tag: A small, unique "authentication tag" or signature. When we decrypt, we check this tag to prove the data is authentic and hasn't been changed.

    nonce = cipher.nonce: The GCM cipher automatically generates another random value called a "nonce" (number used once). This nonce is essential for decryption. It is not a secret and must be saved.

    '''

    # Create an AES cipher object: 
    cipher = AES.new(key, AES.MODE_GCM)

    # Use the cipher to encrypt the data. This will give you two results:
    ciphertext, tag = cipher.encrypt_and_digest(byte_data)

    # You also need the nonce from the cipher, which was created automatically: nonce = cipher.nonce 
    nonce = cipher.nonce

    # save all three pieces of encrypted information (nonce, tag, and ciphertext) to the vault.db file.

    with open("vault.db","wb") as f :
        # We write the three pieces of data to the file, one after the other. The order is important, as we must read them back in the same order.
        f.write(nonce)
        f.write(tag)
        f.write(ciphertext)

    return empty_vault_data


def load_vault(password) :
    # To derive the key, we first need the salt that we saved earlier.
    # 'rb' mode is crucial – it means Read Bytes.
    # open the salt file :
    with open('vault.salt','rb') as f :
        # read the contents into a variable
        salt = f.read()

    password = password.encode("utf-8")

    key = PBKDF2(password, salt, dkLen=32, count=1000000)

    '''
     the function f.readlines() is designed to read lines of text from a text file. Our vault.db file is a binary file; it doesn't have separate lines. It's just one continuous stream of bytes.

     The correct function to use here is ' f.read(size) ' , which reads a specific number of bytes.

    '''

    try:
        with open('vault.db','rb') as f :
            nonce = f.read(16)
            tag =  f.read(16)
            ciphertext = f.read()
    except FileNotFoundError:
        print_error("Vault database not found! It may be corrupted or deleted.")
        return None
    
    try :
        # Create the AES cipher object. 
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        # Attempt to decrypt
        decrypted_data_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        # convert the decrypted bytes back into a dictionary
        # Decode the bytes into a JSON string
        json_data = decrypted_data_bytes.decode('utf-8')
        # Parse the JSON string into a Python dictionary
        passwords_dictionary = json.loads(json_data)

        return passwords_dictionary
    
    except ValueError :
        return None


def save_vault(passwords_dictionary,password):
    with open("vault.salt","rb") as f :
        salt = f.read()
    
    password = password.encode("utf-8")

    key = PBKDF2(password ,salt , dkLen=32 , count=1000000 )

    json_data = json.dumps(passwords_dictionary)
    byte_data = json_data.encode("utf-8")

    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(byte_data)

    nonce = cipher.nonce

    with open("vault.db","wb") as f :
        f.write(nonce)
        f.write(tag)
        f.write(ciphertext)

    return True