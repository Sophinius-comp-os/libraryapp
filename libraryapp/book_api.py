# views.py
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Members, Transactions, BookTransaction
from .serializers import BookSerializer, MemberSerializer, TransactionSerializer


class AllDataAPIView(APIView):
    def get(self, request):
        books_queryset = Book.objects.all()
        viewmembers_queryset = Members.objects.all()
        members_queryset = Members.objects.filter(
            balance__lt=0
        )  # Filter members with negative balance so as not to rent books

        books_serializer = BookSerializer(books_queryset, many=True)
        all_members_serializer = MemberSerializer(viewmembers_queryset, many=True)
        members_serializer = MemberSerializer(members_queryset, many=True)

        data = {
            "books": books_serializer.data,
            "members": all_members_serializer.data,
            "members_with_negative_balance": members_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)


class BooksIssuedPerMemberAPIView(APIView):
    def get(self, request, member_id):
        try:
            member = Members.objects.get(id=member_id)
        except Members.DoesNotExist:
            return Response(
                {"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND
            )

        books_issued = Book.objects.filter(issued_to=member)
        serializer = BookSerializer(books_issued, many=True)
        member_serializer = MemberSerializer(member)

        data = {
            "member": member_serializer.data,
            "books_issued": serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)


class IssueBookAPIView(APIView):
    def post(self, request):
        book_id = request.data.get("book_id", None)

        if book_id is not None:
            try:
                book = Book.objects.get(id=book_id)

                if book.is_available:
                    book.is_available = False
                    book.save()

                    transaction = BookTransaction.objects.create(
                        book=book,
                        member=request.user.members,
                        issued_date=timezone.now(),
                    )

                    serializer = BookSerializer(book)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Book is not available"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            except Book.DoesNotExist:
                return Response(
                    {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )
