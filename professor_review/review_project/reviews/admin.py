# reviews/admin.py

from django.contrib import admin
from .models import Teacher, Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher', 'rating', 'created_at')
    list_filter = ('teacher',)
    search_fields = ('user__username', 'teacher__name', 'comment')

admin.site.register(Teacher)
admin.site.register(Review, ReviewAdmin)
