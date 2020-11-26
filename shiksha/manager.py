from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager):
    use_in_migrations=True
    def _create_user(self,email,password=None):
        if not email:
            raise ValueError("The email value must be set")
        user=self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user=self._create_user(email,password=password)
        user.is_superuser=True
        user.save(using=self._db)
        return user

