import jwt

from django.http       import JsonResponse

from json.decoder      import JSONDecodeError

from jwt.exceptions    import DecodeError

from users.models      import User
from brokurly.settings import SECRET_KEY, ALGORITHM

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.value('token') # FE에서 보내준 token
            decode_token = jwt.decode('utf-8')(access_token, SECRET_KEY, algorithm=ALGORITHM)
            request.user = User.objects.get(id=decode_token['id'])

            if 'token' not in request.headers:
                return JsonResponse({'message':'Token not Exist'}, status=404)

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message':'Invalid User'}, status=400)

        except DecodeError:
            return JsonResponse({'message':'Invalid Token'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)
        
    return wrapper