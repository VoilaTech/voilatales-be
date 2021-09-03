from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from django.contrib.auth.models import PermissionsMixin
from decouple import config


class UserManager(BaseUserManager):
    def create(self, phone_number, display_name, username, display_image, isVerified, otp):
        if not phone_number:
            ValueError("You must enter valid a phone number.")
        if not display_name:
            ValueError("You must enter a display name.")
        if not username:
            ValueError("You must enter a valid username.")

        user = self.model(
            phone_number  = phone_number,
            display_name  = display_name,
            username      = username,
            display_image = display_image,
            isVerified    = isVerified,
            otp           = otp,
        )
        user.set_unusable_password()
        user.save(using = self._db)

        return user

    def create_superuser(self,username,password=None, **extra_fields):
        if not username:
            raise ValueError("User must have an Username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            username=username
        )
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    phone_number = PhoneNumberField(unique=True, editable=True)
    display_name = models.CharField(max_length=50)
    username      = models.CharField(max_length=50, unique=True)
    display_image = models.ImageField(null=True, upload_to = 'displayimg/')
    isVerified = models.BooleanField(blank=False, default=False)
    otp = models.IntegerField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    objects        = UserManager()
    def get_profile_pic_url(self):
        if not self.display_image:
            return None
        return config("BASEURL") + self.display_image.url

class UserRelationship(models.Model):
    user_id = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'], name="unique_followers")
        ]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"