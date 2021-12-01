from django.contrib import admin

from .models import Author, Scholarship, Fieldofstudies, Comment

# Register your models here.
admin.site.register(Author)
# admin.site.register(Category)
admin.site.register(Scholarship)
admin.site.register(Fieldofstudies)
admin.site.register(Comment)
