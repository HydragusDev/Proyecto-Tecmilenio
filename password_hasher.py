
#Uses argon2 password hasher to SECURELY store and verify passwords.
#creates an object PasswordHasher object (ph) with methods ph.hash and ph.verify both for hashing and salting a new password as well as for verifying a hash.


import sys
import gc
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError

# Configures the hasher 
_ph = PasswordHasher(
    memory_cost= 19456,
    time_cost= 2,
    parallelism= 1,
    type=Type.ID
    )


#Takes in the password converted to bytes and returns a unique, randomly salted hash.
def hash_password(password_bytes: bytes) -> str: #Requires the input to already be bytes, requires output to be string.
    #Used by password_registration.py to secure new passwords."""
    try:
        return _ph.hash(password_bytes)
    #Cleans up memory
    finally:
        del password_bytes
        gc.collect()


#Takes in the inputed password and checks it against the stored_hash to see if they coincide and user is verified
def verify_password(stored_hash: str, password_input_bytes: bytes) -> bool: #Requires the input to already be bytes, requires output to be a boolean.
    #Used by password_verification.py to check login attempts.
    try:
        return _ph.verify(stored_hash, password_input_bytes)
    except VerifyMismatchError:
        return False
    #Cleans up the memory
    finally:
        del password_input_bytes
        gc.collect()


#Object Oriented programming my beloved