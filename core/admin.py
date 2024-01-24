from django.contrib import admin
from . import models
# Register your models here.
admin.site.register([
    models.User, models.category, models.Article,
    models.PostImage, models.Comment, models.Replies,
    models.securityQuestion
])