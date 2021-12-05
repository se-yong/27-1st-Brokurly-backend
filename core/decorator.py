import jwt, bcrypt

from my_settings import SECRET_KEY, ALGORITHM



def signin(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            decode_password = jwt.encode('utf-8')(hashed_password, SECRET_KEY, algorithm=ALGORITHM)



        except 
        