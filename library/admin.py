from django.contrib import admin

from .models import Author, Book, Publisher


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date_publication",
        "publisher",
        "price",
    )
    sortable_by = ("title", "date_publication", "price")


admin.site.register(Author)
admin.site.register(Publisher)
