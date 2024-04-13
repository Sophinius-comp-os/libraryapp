from django.test import TestCase, Client
from django.urls import reverse
from .models import Members, Book, Transactions


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = Members.objects.create(
            name="John Doe", email="john@example.com", phone="1234567890"
        )
        self.book = Book.objects.create(
            title="Book Title",
            author="Author Name",
            stock=1,
            price=10,
            year=2022,
            issued_to=self.member,
        )

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")

    def test_members_view(self):
        response = self.client.get(reverse("members"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members.html")

    # Add more view tests as needed

    def test_add_member_view(self):
        response = self.client.post(
            reverse("add_members"),
            {"name": "Jane Doe", "email": "jane@example.com", "phone": "9876543210"},
        )
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after successful form submission
        self.assertTrue(Members.objects.filter(name="Jane Doe").exists())

    def test_update_member_view(self):
        response = self.client.post(
            reverse("update_member", kwargs={"pk": self.member.pk}),
            {"name": "Updated Name"},
        )
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after successful form submission
        self.member.refresh_from_db()
        self.assertEqual(self.member.name, "Updated Name")

    # Add more tests for other views

    def test_issue_book_view(self):
        response = self.client.post(reverse("issue_book"), {"book_id": self.book.id})
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after successful form submission
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_available)

    def test_return_book_view(self):
        transaction = BookTransaction.objects.create(
            book=self.book, user=self.member, issued_date=datetime.now()
        )
        response = self.client.post(
            reverse("return_book"), {"transaction_id": transaction.id}
        )
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after successful form submission
        transaction.refresh_from_db()
        self.assertIsNotNone(transaction.returned_date)
        self.assertTrue(self.book.is_available)
