# password-pwned-check

**How to edit python code to add your password**

put your password here in the code

```
check_password = 'password1'
```

then run the code 

```
python passwordpwned.py
```
**Always remove the check\_password value after running the code for security**  

It will check first five prefix of your password hash against api pwnedpasswords and let you know  
if the password is weak or not, otherwise show "Password not found."

Possible Outputs:

*   currently for _password1_

> Password found! Appears 3383511 times.

*   for unknown password or difficult one

> Password not found.

# generate and check password

use diceware to generate random passpharse and also at same time check the password-pwned

```
pip install diceware
```

just run 
```
python generate_and_check.py
```
