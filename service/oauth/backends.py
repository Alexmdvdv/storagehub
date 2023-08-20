from django.contrib.auth.backends import ModelBackend

from oauth.models import User


class UserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if username is not None:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        elif email is not None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return None
        else:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
