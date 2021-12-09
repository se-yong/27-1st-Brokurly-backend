import json, bcrypt, jwt

from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from django.db              import DataError

from brokurly.settings      import ALGORITHM, SECRET_KEY
from users.models           import User
from core.validator         import validates_email, validates_password, validates_username

def check_existing_username(request):
    try:
        data     = json.loads(request.body)
        username = data['username']

        if User.objects.filter(username = username).exists():
            return JsonResponse({'message' : 'USERNAME_ALREADY_EXISTS'}, status = 400)

        return JsonResponse({"message": 'USERNAME_NOT_EXISTS'}, status=200)
    
    except KeyError:
        return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

def check_existing_email(request):
    try:
        data  = json.loads(request.body)
        email = data['email']
    
        if User.objects.filter(email = email).exists():
            return JsonResponse({'message' : 'EMAIL_ALREADY_EXISTS'}, status = 400)
        
        return JsonResponse({"message": 'EMAIL_NOT_EXISTS'}, status=200)
    
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

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = User.objects.get(username = data['username'])
            password = data['password']

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 401)
            
            Authorization = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
            return JsonResponse({'ACCESS_TOKEN' : Authorization}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status = 404)


