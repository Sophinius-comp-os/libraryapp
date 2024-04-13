from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .book_api import (
    AllDataAPIView,
    IssueBookAPIView,
    BooksIssuedPerMemberAPIView,
)  # BookSearchAPIView, MemberSearchAPIView

urlpatterns = [
    # Pages
    path(r"", views.books, name="index"),
    path(r"members", views.members, name="members"),
    path(r"books", views.books, name="books"),
    # CRUD
    path(r"add_books", views.add_books, name="add_books"),
    path(r"add_members", views.add_members, name="add_members"),
    path(r"update_member/<int:pk>", views.update_member, name="update_member"),
    path(r"delete_member/<int:pk>", views.delete_member, name="delete_member"),
    path(r"update_book/<int:pk>", views.update_book, name="update_book"),
    path(r"delete_book/<int:pk>/", views.delete_book, name="delete_book"),
    path(r"search_books/", views.search_books, name="search_books"),
    # API
    # path(r"get_books/", BookSearchAPIView.as_view(), name="get_books"),
    # path(r"get_members/", MemberSearchAPIView.as_view(), name="get_members"),
    path(r"get_all/", AllDataAPIView.as_view(), name="get_all"),
    # Issuance and return of books
    path(r"issue_books/", IssueBookAPIView.as_view(), name="issue_books"),
    # path(
    #     "books_issued_per_member/<int:member_id>/",
    #     BooksIssuedPerMemberAPIView.as_view(),
    #     name="books-issued-per-member",
    # ),
    path(
        "view_member/<int:member_id>/",
        views.members_info,
        name="view_member",
    ),
    path("issue_book/", views.issue_book, name="issue_book"),
    path(r"return/<int:issue_id>/", views.return_book, name="return_book"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
