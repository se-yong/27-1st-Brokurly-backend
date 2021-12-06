import json, bcrypt

from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from django.db              import DataError

from users.models   import User
from core.validator import validates_email, validates_password, validates_username

def check_existing_username(request):
    try:
        data     = request.body 

        username = data['username']
    
        if User.objects.filter(username = username).exists():
            return JsonResponse({'message' : 'USERNAME_ALREADY_EXISTS'}, status = 400)
    
    except KeyError:
        return JsonResponse({'messages' : 'KEY_ERROR'}, status = 400)

def check_existing_email(request):
    try:
        data  = request.body 

        email = data['email']
    
        if User.objects.filter(email = email).exists():
            return JsonResponse({'message' : 'EMAIL_ALREADY_EXISTS'}, status = 400)
    
    except KeyError:
        return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            validates_email(data['email'])
            validates_password(data['password'])
            validates_username(data['username'])

            username = data['username']
            email    = data['email']
            password = data['password']
            address  = data['address']
            name     = data['name']
            contact  = data['contact']

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
            username = username,
            email    = email,
            password = hashed_password,
            address  = address,
            name     = name,
            contact  = contact
            )
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except DataError:
            return JsonResponse({'message' : 'DATA_ERROR'}, status = 400)
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 400)

