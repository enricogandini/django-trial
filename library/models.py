from django.db import models


class Publisher(models.Model):
    """
    A publisher whose books are available in the library
    """

    business_name = models.CharField(
        max_length=200, help_text="The business name of the publisher",
    )
    address = models.TextField(
        null=True, blank=True, help_text="The address of the publisher",
    )
    phone_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="The main phone number of the publisher",
    )

    def __str__(self):
        return self.business_name


class Author(models.Model):
    """
    An author whose books are available in the library
    """

    first_name = models.CharField(max_length=100, help_text="The author's first name",)
    last_name = models.CharField(max_length=100, help_text="The author's last name",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    """
    A book available in the library
    """

    title = models.TextField(help_text="The title of the book",)
    authors = models.ManyToManyField(Author, help_text="The author(s) of the book",)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, help_text="The publisher of the book"
    )
    date_publication = models.DateField(
        null=True,
        blank=True,
        help_text=(
            "The publication date of a book. "
            "If only the year is available, by default use the 1st of January of that year."
        ),
    )

    price = models.FloatField(null=True, blank=True, help_text=("Price of the book"),)

    @property
    def year_publication(self):
        return getattr(self.date_publication, "year", None)

    def __str__(self):
        if self.date_publication is not None:
            return f"{self.title} ({self.year_publication})"
        else:
            return self.title
