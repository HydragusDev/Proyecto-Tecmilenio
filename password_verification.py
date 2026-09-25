import gc
import sys


import pwinput
import database as db
from password_hasher import verify_password


#User, mail, username, bytes_hashed_password, 


#Book

def verify_login_main_loop() -> dict | None:
    attempts = 0

    while True:
        try:
            print("=== USER LOGIN SYSTEM ===")
            input_mail = input("Email > ").strip().lower()

            if not input_mail:
                print("Email is required.")
                continue

            print("=== Username LOGIN ===")
            input_username = input("Username > ").strip().lower()

            if not input_username:
                print("Username is required.")
                continue

            
            user_temp = db.obtain_from_mail(input_mail)
            if user_temp is None:
                attempts += 1
                print(f"\nAccess Negado: Correo o contraseña invalidos. Le quedan {attempts} intentos.")
                if attempts >= 3:
                    print("Demasiados intentos, intente de nuevo")
                    sys.exit(1)
                continue

            password_input_bytes = pwinput.pwinput("Password > ", mask="*").encode("utf-8")

            stored_hash = user_temp["hashed_password"]

            if isinstance(stored_hash, (bytes, bytearray)):
                stored_hash = stored_hash.decode("utf-8", errors="ignore")

            verified = verify_password(stored_hash, password_input_bytes) #verify password with hash.

            if verified:
                print("\nAccess granted. Welcome aboard Captain.")
                return dict(user_temp)

            attempts += 1
            print("\nAccess Denied: Invalid email or password.")

            if attempts >= 3:
                print("Too many failed attempts. Exiting.")
                sys.exit(1)

        except KeyboardInterrupt:
            print("\nLogin cancelado.")
            sys.exit(0)

        #Cleans up
        finally:
            if "password_input_bytes" in locals():
                del password_input_bytes
            gc.collect()


if __name__ == "__main__":
    usuario = verify_login_main_loop()
    if usuario is not None:
        print(f"Logged in as: {usuario['role']} ({usuario['mail']})")