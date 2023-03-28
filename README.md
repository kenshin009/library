# Library

## README
### Distinctiveness and Complexity

This library project is created for both librarian and library members.

Members can find books on this web app comfortably from their home, and can tell the librarian whether they will get their borrowed books by delivery or on their own 
This library project is totally distinct from other projects by its unique purpose.
It may resemble in some features, but the functionality of this project is different from others.

In this project, library members (users) can find books by their book names and authors, they can read the books online, and they can borrow the books they like without going to the library. If they accidentally clicked a button to borrow, they can cancel it only by contacting to the librarian.

In aspect of librarian (admin), he/she can easily manage the library system by using this project. He/she has to add new books, so that the members can borrow.
If members request to cancel borrow, he/she has to cancel it. The librarian also has access to all data of members, books and borrowed books.
The librarian can delete members and books. All these tasks can now be easily performed by librarian on this project.   

In contact feature, I implemented Send Email feature by using Django.


### Files contained in Library Project

A Django project called library contains a single app called book. Inside book/models.py, I created 5 models: User model, Category model, Book model, HireBook model, and Wishlist model.

Inside book/urls.py, there are 20 routes for this project. But, I grouped and labeled them with comments to make it more readable and understandable.
In book/views.py contains 20 views for this project. Like in book/urls.py, I grouped together some views as they share the same purpose, e.g: book views, hirebook views and members views, etc.

The book/templates/book contains all the html files for this project.

The main project also has media folder which consists of two folders, book_images and files. The former, book_images store images of book covers and the files folder store pdf files.


### How to run this project
To run this project on your local machine, follow these steps:

#### Prerequisites
Python 3 must be installed on your machine. You can download it from https://www.python.org/downloads/.

pip (Python package manager) must also be installed on your machine. You can check if it's installed by running pip --version in your terminal. If it's not installed, you can install it using the instructions at https://pip.pypa.io/en/stable/installing/.

#### Installation
1. Clone the repository from GitHub by running the following command in your terminal:
    `git clone https://github.com/kenshin009/library.git`
2. Then, in your terminal, cd into **library** directory.
3. Run `pip install -r requirements.txt` in your terminal.
4. Run `python manage.py runserver` in your terminal.
