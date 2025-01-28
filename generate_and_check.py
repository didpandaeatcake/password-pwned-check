import requests
import hashlib
from diceware import get_passphrase

def add_hyphens(input_string):
    """Adds hyphens before capital letters (except the first one)."""
    return re.sub(r'(?<!^)([A-Z])', r'-\1', input_string)

def check_password_pwned(password):
    """
    Check if a password has been compromised using the HIBP API.

    Args:
        password (str): The password to check.
    """
    # Compute SHA-1 hash of the password
    hash_object = hashlib.sha1(password.encode())
    hex_digest = hash_object.hexdigest().upper()

    # Extract the first 5 characters of the hash
    five_prefix = hex_digest[:5]

    # Query the HIBP API
    api_url = f"https://api.pwnedpasswords.com/range/{five_prefix}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Check if the password hash suffix is in the response
        hashes = response.text.splitlines()
        for hash_suffix in hashes:
            full_hash, count = hash_suffix.split(":")
            if full_hash.upper() == hex_digest[5:].upper():
                print(f"Password found! Appears {count} times.")
                return True

        # If the password is not found
        print("Password not found.")
        return False

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return False

def main():
    # Generate a secure passphrase using Diceware
    passphrase = get_passphrase()
    modified_string = add_hyphens(passphrase)
    print(f"Generated passphrase: {modified_string}")

    # Check if the passphrase has been compromised
    print("Checking passphrase against api.pwnedpasswords...")
    if check_password_pwned(modified_string):
        print("Warning: This passphrase has been compromised!")
    else:
        print("This passphrase is secure!")

if __name__ == "__main__":
    main()