from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from multiupload.fields import MultiFileField
from .models import Book, Members, Transactions
from django import forms


class MemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ["name", "email", "phone", "balance"]
        labels = {
            "name": "Member Name",
            "email": "Email",
            "phone": "Phone Number",
            "balance": "Balance",
        }


class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ["name", "email", "phone", "balance"]
        labels = {
            "name": "Member Name",
            "email": "Email",
            "phone": "Phone Number",
            "balance": "Balance",
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "stock", "price", "year", "book"]
        books = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5)
        labels = {
            "title": "Book Title",
            "author": "Author",
            "stock": "Quantity",
            "price": "Price in Ksh.",
            "year": "Year of Publication",
            "book": "Book",
        }


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "stock", "price", "year", "book"]
        labels = {
            "title": "Book Title",
            "author": "Author",
            "stock": "Quantity",
            "price": "Price in Ksh.",
            "year": "Year of Publication",
            "book": "Book",
        }


class IssueBookForm(forms.Form):
    book_id = forms.IntegerField()


class ReturnBookForm(forms.Form):
    transaction_id = forms.IntegerField()
