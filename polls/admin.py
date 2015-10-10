from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Problem, Submission, Tag, News

admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Tag)
admin.site.register(News)
