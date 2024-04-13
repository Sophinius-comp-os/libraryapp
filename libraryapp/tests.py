from django.test import TestCase
from .models import Members, Book, Transactions


class MembersTestCase(TestCase):
    def setUp(self):
        Members.objects.create(
            name="John Doe", email="john@example.com", phone="1234567890"
        )

    def test_member_creation(self):
        member = Members.objects.get(name="John Doe")
        self.assertEqual(member.name, "John Doe")
        self.assertEqual(member.email, "john@example.com")
        self.assertEqual(member.phone, "1234567890")


class BookTestCase(TestCase):
    def setUp(self):
        Members.objects.create(
            name="John Doe", email="john@example.com", phone="1234567890"
        )
        member = Members.objects.get(name="John Doe")
        Book.objects.create(
            title="Book Title",
            author="Author Name",
            stock=1,
            price=10,
            year=2022,
            issued_to=member,
        )

    def test_book_creation(self):
        book = Book.objects.get(title="Book Title")
        self.assertEqual(book.title, "Book Title")
        self.assertEqual(book.author, "Author Name")
        self.assertEqual(book.stock, 1)
        self.assertEqual(book.price, 10)
        self.assertEqual(book.year, 2022)

    def test_issue_book(self):
        book = Book.objects.get(title="Book Title")
        self.assertTrue(book.issue_book())
        self.assertEqual(book.stock, 0)
        self.assertFalse(book.issue_book())  # Trying to issue when stock is 0


class TransactionsTestCase(TestCase):
    def setUp(self):
        Members.objects.create(
            name="John Doe", email="john@example.com", phone="1234567890"
        )
        member = Members.objects.get(name="John Doe")
        Book.objects.create(
            title="Book Title",
            author="Author Name",
            stock=1,
            price=10,
            year=2022,
            issued_to=member,
        )
        book = Book.objects.get(title="Book Title")
        Transactions.objects.create(book=book, member=member, rent_fee=5)

    def test_transaction_creation(self):
        transaction = Transactions.objects.get(rent_fee=5)
        self.assertIsNotNone(transaction.issue_date)

    def test_update_balance(self):
        member = Members.objects.get(name="John Doe")
        self.assertEqual(member.balance, 100)
        Transactions.objects.create(
            book=Book.objects.get(title="Book Title"), member=member, rent_fee=5
        )
        member.refresh_from_db()
        self.assertEqual(member.balance, 95)
