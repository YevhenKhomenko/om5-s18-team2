from django import forms
from . models import Book
from author.models import Author

CHOICES_SORT = (
    ("1", "Name_asc"),
    ("2", "Name_desc"),
    ("3", "Count_asc"),
    ("4", "Count_desc"),
)

CHOICES_FILTER = (
    ("1", "Author_id="),
    ("2", "Count="),
    ("3", "Name_contains"),
    ("4", "Desc_contains"),
)


class QueryForm(forms.Form):
    author_id = forms.IntegerField(label='author_id')


class UserForm(forms.Form):
    user_id = forms.IntegerField(label='user_id')


class BookIDForm(forms.Form):
    book_id = forms.IntegerField(label='book_id')


# creating a form
class SortFilterForm(forms.Form):
    sort = forms.ChoiceField(choices=CHOICES_SORT, required=False)
    filter = forms.ChoiceField(choices=CHOICES_FILTER, required=False)
    find = forms.CharField(max_length=100, required=False)


class EditBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['name', 'description', 'count']

