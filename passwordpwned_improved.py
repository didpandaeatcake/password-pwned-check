# -*- coding: utf-8 -*-
import hashlib
import requests
from getpass import getpass
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_password_compromised(password):
    try:
        # Hash the password
        hash_object = hashlib.sha1(password.encode())
        hex_digest = hash_object.hexdigest().upper()
        five_prefix = hex_digest[:5]

        # Query api
        api_url = f"https://api.pwnedpasswords.com/range/{five_prefix}"
        logging.info("Querying Have I Been Pwned API...")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        # response
        hashes = response.text.splitlines()
        found = False
        for hash_suffix in hashes:
            try:
                full_hash, count = hash_suffix.split(":")
                if full_hash.upper() == hex_digest[5:].upper():
                    print(f"Password found! Appears {count} times.")
                    found = True
                    break
            except ValueError:
                logging.error("Unexpected response format from api.")
                continue

        if not found:
            print("Password not found.")

    except requests.exceptions.Timeout:
        logging.error("The request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    
    check_password = getpass("Enter your password: ").strip()
    if not check_password:
        logging.error("Error: Password cannot be empty.")
        exit(1)

   
    check_password_compromised(check_password)