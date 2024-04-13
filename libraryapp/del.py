from models import Book, Members, Transactions

Book.objects.all().delete()
Members.objects.all().delete()
Transactions.objects.all().delete()
