# -*- coding: utf-8 -*-
    
import requests
import hashlib

check_password = 'password1' #put your password here
hash_object = hashlib.sha1(check_password.encode())
hex_digest = hash_object.hexdigest().upper()

five_prefix = hex_digest[:5]


api_url = f"https://api.pwnedpasswords.com/range/{five_prefix}"

try:
    response = requests.get(api_url)
    response.raise_for_status()  # exception for bad status codes

    # Process the response (hashes)
    hashes = response.text.splitlines()
    # Check if any suffix matches
    found = False
    for hash_suffix in hashes:
        full_hash, count = hash_suffix.split(":")
        if full_hash.upper() == hex_digest[5:].upper():
            print(f"Password found! Appears {count} times.")
            found = True
            break
    if not found:
      print("Password not found.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")