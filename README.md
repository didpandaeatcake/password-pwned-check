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
**Always remove the check\_passord value after running the code for security**  

It will check first five prefix of your password hash against api pwnedpasswords and let you know  
if the password is weak or not, otherwise show "Password not found."

Possible Outputs:

*   currently for _password1_

> Password found! Appears 3383511 times.

*   for unknown password or difficult one

> Password not found.