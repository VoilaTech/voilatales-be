from django.contrib import admin
from .models import User, UserRelationship

admin.site.register([User, UserRelationship])