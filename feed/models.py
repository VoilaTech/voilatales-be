from django.db import models
from user_profile.models import User
import uuid
from django_comments_xtd.signals import should_request_be_authorized
from django.dispatch import receiver

class Post(models.Model):
    id           = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    description  = models.CharField(max_length=150, null=True)
    cover_image  = models.ImageField(upload_to='coverimg/')
    audio_field  = models.FileField(upload_to='audio/')
    created_at   = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        if len(self.description) > 15:
            return f"{self.user} posted a tale with description as {self.description[0:15]}..."
        return f"{self.user} posted a tale with description as {self.description}"

@receiver(should_request_be_authorized)
def my_callback(sender, comment, request, **kwargs):
    if (request.user and request.user.is_authenticated):
        return True