from django.contrib import admin
from .models import Book, Members, Transactions
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'stock', 'display_cover_preview')

    def display_cover_preview(self, obj):
        if obj.cover_preview:
            return f'<img src="{obj.cover_preview.url}" width="50" height="50" />'
        return 'No Preview'

    display_cover_preview.allow_tags = True

admin.site.register(Book, BookAdmin)
admin.site.register(Members)
admin.site.register(Transactions)