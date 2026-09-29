# Uses argon2 password hasher to SECURELY store and verify passwords.
# creates an object PasswordHasher object (ph) with methods _ph.hash and _ph.verify both for hashing and salting a new password as well as for verifying a hash.

#Imports
import gc

from argon2 import PasswordHasher, Type
from argon2.exceptions import InvalidHashError, VerifyMismatchError

# Configures the hasher
#(Internal use only) hash_password and verify_password are wrapped functions
_ph = PasswordHasher(
    memory_cost=19456,
    time_cost=2,
    parallelism=1,
    type=Type.ID,
)

# Takes in the password converted to bytes and returns a unique, randomly salted hash as a string.
def hash_password(password_bytes: bytes) -> str:
    try:
        return _ph.hash(password_bytes)
    finally:
        del password_bytes
        gc.collect()

# Takes in the inputed password and checks it against the stored_hash to see if they coincide and user is verified.
def verify_password(stored_hash: str, password_input_bytes: bytes) -> bool:
    if not stored_hash:
        return False

    try:
        return _ph.verify(stored_hash, password_input_bytes)
    except (VerifyMismatchError, InvalidHashError, TypeError, ValueError):
        return False
    finally:
        del password_input_bytes
        gc.collect()

        

# Object Oriented programming my beloved.
