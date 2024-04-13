from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, response
from .models import Book, Members, Transactions, BookTransaction
from django.db.models import Max
from .forms import (
    MemberForm,
    BookForm,
    UpdateBookForm,
    UpdateMemberForm,
    IssueBookForm,
    ReturnBookForm,
)
from django.core.files.storage import default_storage as storage

# Create your views here.
format = "%Y-%m-%dT%H:%M:%S.%f"


# Start
def index(request):
    return render(request, "base.html")


# CRUD operations on Members #
def members(request):
    members = Members.objects.all()
    context = {"members": members}
    return render(request, "members.html", context=context)


def add_members(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Member created successfully.")
            return redirect("members")
        else:
            error_message = ", ".join(
                [f"{field}: {error}" for field, error in form.errors.items()]
            )
            messages.error(
                request, f"There was an error in the form submission: {error_message}"
            )
    else:
        form = MemberForm()
    context = {"form": form}
    return render(request, "add_member.html", context=context)


def update_member(request, pk):
    member = Members.objects.get(id=pk)
    if request.method == "POST":
        form = UpdateMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Member "{member.member_id}" updated successfully.'
            )
            return redirect("members")
    else:
        # Corrected the form class to UpdateMemberForm
        form = UpdateMemberForm(instance=member)

    context = {
        "form": form,
    }
    return render(request, "update_member.html", context=context)


def members_info(request, member_id):
    try:
        member = Members.objects.get(id=member_id)
    except Members.DoesNotExist:
        messages.error(request, "Member not found")
        return redirect("members")

    books_issued = Book.objects.filter(issued_to=member)

    context = {
        "member": member,
        "books_issued": books_issued,
    }

    return render(request, "view_member.html", context=context)


def delete_member(request, pk):
    member = Members.objects.get(id=pk)

    if request.method == "POST":
        messages.error(request, f'Member "{member.member_id}" deleted successfully.')
        member.delete()

    return redirect("members")


# CRUD operation for books
def books(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "books.html", context=context)


def search_books(request):
    query = request.GET.get("q", "")
    if query:
        results = Book.search_books(query)
    else:
        results = Book.objects.all()

    context = {"books": results, "query": query}
    return render(request, "search.html", context)


# def search_books(request):
#     query = request.GET.get("q", "")
#     if query:
#         results = Book.search_books(query)
#     else:
#         results = Book.objects.all()

#     book_list = [{"title": book.title, "author": book.author} for book in results]

#     return JsonResponse({"books": book_list, "query": query})


def add_books(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, prefix="books")
        if form.is_valid():
            books = form.save()
            for book in request.FILES.getlist("book"):
                books.book.save()

            messages.success(request, f"Book created successfully.")
            return redirect("books")
    else:
        form = BookForm(prefix="books")
    context = {"form": form}
    return render(request, "add_book.html", context=context)


def update_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == "POST":
        form = UpdateBookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully.')
            return redirect("books")  # Redirect after successful form submission
        # else:
        #     messages.error(request, "Error updating the book. Please check the form.")
    else:
        form = UpdateBookForm(instance=book)
    context = {
        "form": form,
    }
    return render(request, "update_book.html", context=context)


def delete_book(request, pk):
    book = Book.objects.get(id=pk)

    if request.method == "POST":
        deleted_id = book.pk
        messages.error(request, f'Book "{book.title}" deleted successfully.')
        book.delete()

        # Find the maximum ID in the Book table
        max_id = Book.objects.all().aggregate(Max("id"))["id__max"]

        # Set the next ID to the deleted ID + 1 or 1 if there was no previous ID
        next_id = deleted_id + 1 if max_id is not None else 1

        # You can create a new book with the next ID if needed
        # new_book = Book.objects.create(id=next_id, other_fields=...)

    return redirect("books")


def issue_book(request):
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data["book_id"]
            book = Book.objects.get(id=book_id)

            if book.is_available:
                book.is_available = False
                book.save()
                transaction = BookTransaction.objects.create(
                    book=book, member=request.Members, issued_date=datetime.now()
                )
                return messages.success(request, "Book issued successfully")
            else:
                return messages.error(request, "Book is not available")
    else:
        form = IssueBookForm()

    context = {"form": form}

    return render(request, "issue_book.html", context=context)


def return_book(request):
    if request.method == "POST":
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            transaction_id = form.cleaned_data["transaction_id"]
            transaction = BookTransaction.objects.get(
                id=transaction_id, user=request.user, returned_date=None
            )

            transaction.book.is_available = True
            transaction.book.save()

            transaction.returned_date = datetime.now()
            transaction.save()

            return messages.success(request, "Book returned successfully")
    else:
        form = ReturnBookForm()
    context = {"form": form}

    return render(request, "return_book.html", context=context)
