from rest_framework import serializers
import uuid
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    id           = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    user_id      = serializers.PrimaryKeyRelatedField(read_only=True)
    description  = serializers.CharField(max_length=150)
    cover_image  = serializers.ImageField()
    audio_field  = serializers.FileField()
    created_at   = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Post
        fields = ['id','user_id', 'description', 'cover_image', 'audio_field', 'created_at']
