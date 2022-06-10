
#Generate a key to use as your flask secret key

import secrets
key = secrets.token_urlsafe(secrets.randbelow(10) + 30)
print(key)