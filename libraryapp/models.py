from django.db import models
from django.template.defaultfilters import slugify

# from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.


class Members(models.Model):
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=100)
    member_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    slug = models.SlugField(unique=True, null=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.transactions = None

    def save(self, *args, **kwargs):
        # Generate member ID based on the last three digits of the phone number
        if not self.member_id and self.phone:
            self.member_id = self.phone[-3:]
        self.slug = slugify(self.name)
        super(Members, self).save(*args, **kwargs)

    # def update_balance(self):
    #     # Calculate the current balance based on the sum of all rent fees
    #     total_rent_fees = self.transactions.aggregate(total=models.Sum('rent_fee'))['total']
    #     self.balance = total_rent_fees if total_rent_fees else 0
    #     self.save()
    #
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    book = models.FileField(upload_to="books/", null=False, blank=True, unique=True)
    # cover_preview = models.ImageField(upload_to="book_covers/", null=True, blank=True)
    slug = models.SlugField(unique=True, null=False)
    is_available = models.BooleanField(default=True)
    issued_to = models.ForeignKey(
        Members, null=True, blank=True, on_delete=models.SET_NULL
    )

    @property
    def book_url(self):
        if self.book and hasattr(self.book, "url"):
            return self.book.url

    @classmethod
    def search_books(cls, query):
        # Case-insensitive search by title and author
        results = cls.objects.filter(
            models.Q(title__icontains=query) | models.Q(author__icontains=query)
        )
        return results

    # def save(self, *args, **kwargs):
    #     if self.stock == 0:
    #         self.is_available = False
    #     else:
    #         self.is_available = True
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    #     if self.book and not self.cover_preview:
    #         self.create_cover_preview()

    # def create_cover_preview(self):
    #     if not self.book:
    #         return  # No need to proceed if there's no book associated

    #     image_path = self.book.path

    #     try:
    #         img = Image.open(image_path)
    #        img.thumbnail((100, 100))

    #         cover_preview_path = f"book_covers/cover_preview_{self.id}.png"
    #         img.save(cover_preview_path)

    #         self.cover_preview.name = cover_preview_path
    #         self.save()
    #     except Exception as e:
    #         # Handle the case when an exception occurs (e.g., image not found)
    #         print(f"Error creating cover preview: {e}")

    # def get_cover_preview_url(self):
    #     return self.cover_preview.url if self.cover_preview else None

    def issue_book(self):
        if self.stock > 0:
            self.stock -= 1
            self.save()
            return True
        else:
            return False

    def __str__(self):
        return self.title


class Transactions(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    rent_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.book.title + " - " + self.member.name

    def save(self, *args, **kwargs):
        # Call the superclass save method first
        super(Transactions, self).save(*args, **kwargs)

        # Update the member's balance after saving the transaction
        self.member.update_balance()


class BookTransaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    issued_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
