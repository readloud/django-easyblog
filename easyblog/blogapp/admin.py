from django.contrib import admin

# Register your models here.
from .models import BlogModel, CommentModel
admin.site.register(BlogModel)
admin.site.register(CommentModel)