# libraryapp


[![JcaJJln.png](https://iili.io/JcaJJln.png)](https://freeimage.host/)
[![JcaJdSs.png](https://iili.io/JcaJdSs.png)](https://freeimage.host/)
[![JcaJHKX.png](https://iili.io/JcaJHKX.png)](https://freeimage.host/)
[![JcaJ3HG.png](https://iili.io/JcaJ3HG.png)](https://freeimage.host/)
[![JcaJFRf.png](https://iili.io/JcaJFRf.png)](https://freeimage.host/)
![Screenshot from 2024-03-18 21-24-43](https://github.com/wathika-eng/libraryapp/assets/71040609/7af9fff8-b697-42c0-8ff4-968d41ae8576)


Base Library System
Overview
The Base Library System is designed to help librarians manage books, members, and transactions efficiently. It provides functionalities for performing general CRUD operations on books and members, issuing and returning books, searching for books by name and author, and managing rent fees for book returns.

Features

1. Books Management
   Create, Read, Update, Delete (CRUD): Librarians can perform basic CRUD operations on books, including adding new books, updating book information, and removing books from the system.

Stock Management: The system maintains the stock of each book, allowing librarians to track the availability of books in the library.

2. Members Management
   Create, Read, Update, Delete (CRUD): Librarians can manage the member database, adding new members, updating member information, and removing members from the system.
3. Transactions
   Issue Book to Member: Librarians can issue a book to a member, updating the book's availability and recording the transaction details.

Return Book from Member: Librarians can process book returns, calculate rent fees, and update the member's outstanding debt.

4. Search
   Search for a Book by Name and Author: Librarians can search for books based on their name and author, making it easy to locate specific books in the library.
5. Rent Fee Management
   Charge Rent Fee on Book Returns: The system calculates and charges rent fees when a member returns a book.

Debt Limit: The system ensures that a member's outstanding debt does not exceed KES.500, helping in debt management.

Usage

To use the Base Library System, follow these steps:

- Clone the repository: `git clone <repository-url>`
- Make a virtual environment: `python -m virtualenv venv`
- Activate the venv: `source venv/scripts/activate`
- or on Linux: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Navigate to settings.py and make sqlite the default db, uncomment any line with cloudinary config
- Set up the database and run migrations: `python manage.py makemigrations` `python manage.py migrate --run-syncdb`
- Run the development server: `python manage.py runserver`
- Navigate to the homepage: http://127.0.0.1:8000

Books Management:

Navigate to the "Books" section to add, update, or remove books.
Monitor the stock of each book to ensure accurate availability.
Members Management:

Access the "Members" section to add, update, or remove members from the system.
Transactions:

Issue books to members by recording transactions.
Process book returns, calculate rent fees, and update member debts accordingly.
Search:

Use the search functionality to find books based on their name and author.
Rent Fee Management:

Charge rent fees on book returns and ensure that a member's outstanding debt stays below KES.500.
