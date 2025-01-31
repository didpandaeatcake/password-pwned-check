import hashlib
import requests
from diceware import get_passphrase
import re
import logging
import time


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
    # Query the api
    api_url = f"https://api.pwnedpasswords.com/range/{five_prefix}"
    try:
        logging.info("Querying Have I Been Pwned API...")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        # response
        hashes = response.text.splitlines()
        for hash_suffix in hashes:
            try:
                full_hash, count = hash_suffix.split(":")
                if full_hash.upper() == hex_digest[5:].upper():
                    print(f"Password found! Appears {count} times.")
                    return True
            except ValueError:
                logging.error("Unexpected response format from API.")
                continue

        print("Password not found.")
        return False

    except requests.exceptions.Timeout:
        logging.error("The request timed out. Please try again later.")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False

def main():
    # Generate a secure passphrase using Diceware
    passphrase = get_passphrase()
    modify = input("Do you want to add hyphens to the passphrase? (y/n): ").strip().lower()
    while modify not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'.")
        modify = input("Do you want to add hyphens to the passphrase? (y/n): ").strip().lower()

    modified_string = add_hyphens(passphrase) if modify == 'y' else passphrase
    print(f"Generated passphrase: {modified_string}")

    # Check if the passphrase has been compromised
    print("Checking passphrase against api.pwnedpasswords...")
    if check_password_pwned(modified_string):
        print("Warning: This passphrase has been compromised!")
    else:
        print("This passphrase is secure!")

if __name__ == "__main__":
    main()