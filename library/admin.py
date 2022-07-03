from django.contrib import admin

from .models import Author, Book, Publisher


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "date_publication",
        "publisher",
    )
    sortable_by = ("title", "date_publication")


admin.site.register(Author)
admin.site.register(Publisher)
