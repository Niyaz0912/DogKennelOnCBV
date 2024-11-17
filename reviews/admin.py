from django.contrib import admin
from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'dog', 'autor', 'created', 'sign_of_review',)
    ordering = ('created',)
    list_filter = ('dog', 'autor',)
