from django.contrib import admin
from .models import Word, Text, Exercise, UserWord, UserProgress

admin.site.register(Word)
admin.site.register(Text)
admin.site.register(Exercise)
admin.site.register(UserWord)
admin.site.register(UserProgress)