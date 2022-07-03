from django.shortcuts import render
from rest_framework import viewsets

from library.models import Book
from library.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    View the available Books
    """
    serializer_class = BookSerializer

    queryset = Book.objects.all()
