from rest_framework.authentication import get_authorization_header,BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings
from .models import User



class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_headers=get_authorization_header(request)
        auth_data=auth_headers.decode('utf-8')
        auth_token=auth_data.split(' ')

        if len(auth_token)!=2:
            raise exceptions.AuthenticationFailed('token not valid')
        token=auth_token[1]    

        try:
          payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')

          username=payload['username']

          user=User.objects.get(username=username)

          return (user,token)


        except jwt.ExpiredSignatureError as ex:
             raise exceptions.AuthenticationFailed('token is expired,login again')
        except jwt.DecodeError as ex:
             raise exceptions.AuthenticationFailed('token is invalid')    

        except User.DoesNotExist as no_user:
             raise exceptions.AuthenticationFailed('no such user')


        return super().authenticate(request)