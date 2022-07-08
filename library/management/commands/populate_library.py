import json
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand

from library.models import Author, Book, Publisher


class Command(BaseCommand):
    DIR_INITIAL_DATA = Path("initial_data")
    FILE_INITIAL_LIBRARY = Path(DIR_INITIAL_DATA, "db2.json")

    help = f"Populate the library tables with data from {FILE_INITIAL_LIBRARY}"

    def load_initial_library(self) -> dict:
        with open(self.FILE_INITIAL_LIBRARY, "r") as f:
            library = json.load(f)
        return library

    def get_authors_from_library_data(self, library: dict) -> dict[int, dict]:
        authors = library["autori"]
        authors = {
            author["id"]: {"first_name": author["nome"], "last_name": author["cognome"]}
            for author in authors
        }
        return authors

    def get_publishers_from_library_data(self, library: dict) -> dict[int, dict]:
        publishers = library["editori"]
        publishers = {
            publisher["id"]: {
                "business_name": publisher["ragione sociale"],
                "address": publisher.get("indirizzo", None),
                "phone_number": publisher.get("telefono", None),
            }
            for publisher in publishers
        }
        return publishers

    def _get_date_from_book(self, book: dict) -> datetime:
        default_month = 1
        default_day = 1
        date = book.get("anno edizione", None)
        if date is not None:
            date = int(date)
            date = datetime(year=date, month=default_month, day=default_day)
        return date

    def get_books_from_library_data(self, library: dict) -> list[dict]:
        books = library["libri"]
        books = [
            {
                "title": book["titolo"],
                "authors_ids": book["autore"],
                "publisher_id": book["editore"],
                "date_publication": self._get_date_from_book(book),
            }
            for book in books
        ]
        return books

    def populate_authors(self, authors: dict) -> dict[int, Author]:
        authors = {
            author_id: Author.objects.create(**author_fields)
            for author_id, author_fields in authors.items()
        }
        return authors

    def populate_publishers(self, publishers: dict) -> dict[int, Publisher]:
        publishers = {
            publisher_id: Publisher.objects.create(**publisher_fields)
            for publisher_id, publisher_fields in publishers.items()
        }
        return publishers

    def populate_books(
        self, books: list[dict], authors: dict, publishers: dict
    ) -> list[Book]:
        books_objs = []
        for book in books:
            authors = [authors[author_id] for author_id in book["authors_ids"]]
            publisher = publishers[book["publisher_id"]]
            book_obj = Book.objects.create(
                title=book["title"],
                date_publication=book["date_publication"],
                publisher=publisher,
            )
            book_obj.authors.set(authors)
            self.stdout.write(f"Added {book_obj} by {authors} published by {publisher}")
            books_objs.append(book_obj)
        return books_objs

    def handle(self, *args, **options):
        library = self.load_initial_library()

        authors = self.get_authors_from_library_data(library)
        publishers = self.get_publishers_from_library_data(library)
        books = self.get_books_from_library_data(library)

        authors = self.populate_authors(authors)
        publishers = self.populate_publishers(publishers)
        books = self.populate_books(books=books, authors=authors, publishers=publishers)

        self.stdout.write(
            self.style.SUCCESS(
                f"Library populated with data from {self.FILE_INITIAL_LIBRARY}!"
            )
        )
