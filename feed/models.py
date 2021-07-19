from django.db import models
from ..user_profile.models import User
import uuid

class Post(models.Model):
    id           = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_id      = models.ForeignKey(User, on_delete=models.CASCADE)
    description  = models.CharField(max_length=150, null=True)
    cover_image  = models.ImageField(upload_to='coverimg/')
    audio_field  = models.FileField(upload_to='audio/')

