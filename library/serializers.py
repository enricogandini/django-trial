from rest_framework import serializers

from library.models import Author, Book, Publisher


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "date_publication",
            "author",
            "publisher",
        )
