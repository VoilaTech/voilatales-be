from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class UserManager(BaseUserManager):
    def create(self, phone_number, display_name, username, password, display_image):
        if not phone_number:
            ValueError("You must enter valid a phone number.")
        if not display_name:
            ValueError("You must enter a display name.")
        if not username:
            ValueError("You must enter a valid username.")
        if not password:
            ValueError("You must enter a valid password.")

        user = self.model(
            phone_number  = phone_number,
            display_name  = display_name,
            username      = username,
            display_image = display_image
        )

        user.set_password(password)
        user.save(using = None)

        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    phone_number = PhoneNumberField(unique=True, editable=True)
    display_name = models.CharField(max_length=50)
    username      = models.CharField(max_length=50, unique=True)
    display_image = models.ImageField(null=True, upload_to = 'displayimg/')

    USERNAME_FIELD = 'username'
    objects        = UserManager()

