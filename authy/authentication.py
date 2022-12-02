from django.contrib.auth import get_user_model


User = get_user_model()
class EmailAuthBackend:
    @staticmethod
    def authenticated(request , email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user 
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
    @staticmethod
    def get_user(user_id ):
        try:
            return User.objects.get(id= user_id)
        except User.DoesNotExist:
            return None