import json
from pathlib import Path

from django.core.management.base import BaseCommand

from library.models import Author, Book, Publisher

DIR_INITIAL_DATA = Path("initial_data")
FILE_INITIAL_LIBRARY = Path(DIR_INITIAL_DATA, "initial_library.json")


class Command(BaseCommand):
    help = f"Populate the library tables with data from {FILE_INITIAL_LIBRARY}"

    def handle(self, *args, **options):
        with open(FILE_INITIAL_LIBRARY, "r") as f:
            library = json.load(f)
        authors = {
            author["id"]: {"first_name": author["nome"], "last_name": author["cognome"]}
            for author in library["autori"]
        }
        self.stdout.write(
            self.style.SUCCESS(
                f"Library populated with data from {FILE_INITIAL_LIBRARY}!"
            )
        )
