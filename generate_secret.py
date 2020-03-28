from secrets import token_hex
from random import randint, choice

possibilities = []
for i in range(randint(1, 20)):
  possibility = token_hex()
  possibilities.append(possibility)
  outcome = choice(possibilities)
  
inp = input("Press Any Key to Generate a Secret...\n>").lower()
if inp or not inp:
  print("""\nYou don't have to use this script to generate a secret. 
But you do have to set two environment variables to run the flask app.
The secret does not matter in development, but you need one for the app to function.""")

print("""In case it needs to be said, 
this script will generate a secret key for testing of this app in development environments. 
Do not use a shitty, passed around secret generated from this script in production. 
Please be advised of this.\n""")

print(f"export FLASK_ENV=development\nexport FLASK_SECRET_KEY={outcome}\n\nAfter setting these environment variables you can start the server with 'flask run'\n")
  

