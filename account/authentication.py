from django.conf import settings
from .models import CustomUserModel


class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {'email' : username}
        else:
            kwargs = {'username' : username}
        try:
            user = CustomUserModel.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return CustomUserModel.objects.get(pk=user_id)
        except CustomUserModel.DoesNotExist:
            return None
