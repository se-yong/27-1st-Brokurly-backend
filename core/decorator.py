import jwt

from django.http       import JsonResponse

from jwt.exceptions    import DecodeError

from users.models      import User
from brokurly.settings import SECRET_KEY, ALGORITHM

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers['Authorization']
            decode_token = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            request.user = User.objects.get(id=decode_token['id'])
           
            return func(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message':'Invalid User'}, status=400)

        except DecodeError:
            return JsonResponse({'message':'Invalid Token'}, status=400)

    return wrapper