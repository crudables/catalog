from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)')
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Book(models.Model):

    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',on_delete=models.SET_NULL, null = True)


    # Foreign Key used because book can only have one author, but authors can have multiple books
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """

        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_discription = 'Genre'

class BookInstance(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text="unique id for a particular book instance")
    book = models.ForeignKey('Book', on_delete =models.SET_NULL, null = True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null = True,blank=True)
    borrower = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)


    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
        )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back :
            return True
        return False
    status = models.CharField(max_length=1,choices = LOAN_STATUS, blank= True, default='m', help_text="Book availability")
    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '%s (%s)' %(self.id, self.book.title)


class Author(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField("died",null = True, blank = True)

    def get_absolute_url(self):
        return reverse('authordetail', args=[str(self.id)])

    def __str__(self):
        return "{}, {}".format(self.first_name,self.last_name)
    class Meta:
        permissions = (("can create_update_delete author","create update delete author"),)