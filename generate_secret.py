import secrets
import string

length = secrets.choice(range(64, 256))
alphabet = string.ascii_letters + string.digits + string.punctuation
secret = ''.join(secrets.choice(alphabet) for i in range(length))
print(secret)
