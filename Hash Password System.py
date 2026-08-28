import hashlib
import os

debug = False
if debug == True:  # Random Password Salter
    # 1. Generate a random 16 bit  salt
    salt = os.urandom(16)
    print("Random hash", salt)
    # If debug = false, used stored hash instead.


# Username and password checker.

username = "AzureDiamond"
# Placeholder Username: AzureDiamond
# Placeholder Password: hunter2

stored_hash = b"\n\x9b\x9b\x07\x05qd3\x9b9\x88\xb1^\xb8[\xbe\xdd\xab\x0c\xd7\xe5\xdd\x86\xbc\x13=\x95.\xf1\xe1\xa6<\x11\xf9l\\\x9fHK\xdb{h\xb6\x93K=m\xd6\xfe\xb8i\xb9F\x98\x1dO\xd7\xb4\x85 \xe4\xde0\x1f"
stored_salt = b"#\x91\x1f\x96\x92-nl\x87\xf2\x8c7~\xea|\x84"
print("hello")
#hello evernyan
not_identified = True
while True:
    username_input = input("What's your Username? > :")
    if username_input == "AzureDiamond":
        # 1. If username is correct go ahead and ask for password, then compare to stored hash and salt:
        password_input = input("What is your password? > ")
        password = password_input.encode("utf-8")

        # 2. Hash using library hashlib.scrypt, using default values.
        hashed_password = hashlib.scrypt(
            password,
            salt=stored_salt,
            n=16384,  # CPU/Memory cost factor
            r=8,  # Block size
            p=1,  # Parallelization factor
        )
        if debug != True:
            salt = "No new Salt generated."

        print()
        print("Random Salt:", salt)
        print(f"{password_input} if hashed:", hashed_password)
        print("Verification hash:", stored_hash)
        print()
        print("Using salt:", stored_salt)
        print()

        if hashed_password == stored_hash:
            print("Welcome aboard, captain. Verification confirmed.")
            identified = False
            break
        else:
            print("Password Incorrect. Try Again.\n")
            continue
    else:
        print("Username Incorrect. Try Again.\n")
        continue

# Rest of program:
print()
print("Rest of program here:")
print()
# Done:
# Learn password hashing: https://pbs.twimg.com/media/DXsv0sKVwAA_RrZ.jpg
# To-do
# Prevent SQL Injections. Bobby Tables, my beloved: https://xkcd.com/327/
