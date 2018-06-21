from django.contrib import admin

from web import models

admin.site.register(models.Book)
admin.site.register(models.BookChapter)
admin.site.register(models.BookSection)
