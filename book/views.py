from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse,Http404,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from datetime import datetime,date,timedelta
from django.db import IntegrityError
from django.urls import reverse
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator
import json
from .models import *
# Create your views here.

# Book views
@login_required(login_url='login')
def index (request):
    # Get all books
    books = Book.objects.all()
    # Add pagination 
    paginator = Paginator(books,20) # 20 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/index.html',{
        'books': page_obj,
        'categories': categories
    })

@login_required(login_url='login')
def add_book(request):

    if request.method == "POST":
        isbn = request.POST['isbn']
        name = request.POST['name']
        author = request.POST['author']
        category = request.POST['category']
        image = request.FILES.get('image')
        book_file = request.FILES.get('book_file')
        publisher = request.POST['publisher']
        pub_date = request.POST['pub_date']
        print(book_file)
        # Check category is already present or not
        try:
            category_obj = Category.objects.get(title=category.upper())
        except:
            category_obj = Category.objects.create(title=category.upper())
        # Create new book
        new_book = Book.objects.create(isbn=isbn,name=name,author=author,category=category_obj,
                                       book_file=book_file,image=image,
                                       publisher=publisher,publication_date=pub_date)
        new_book.save()
        return redirect('index')
    
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/add_book.html',{'categories':categories})

def book_detail(request,book_id):
    # Get the book
    book = Book.objects.get(id=book_id)
    # Check if the book is in user's whislist
    wishlist = WishList.objects.filter(username=request.user.username,book_id=book_id).first()
    # Check if the user has hired this book
    user_hired = HireBook.objects.filter(username=request.user.username,book_id=book_id).first()
    # Check if other user has hired this book
    other_hired = HireBook.objects.filter(book_id=book_id).first()
    # Get all categories
    categories = Category.objects.all()
    print(other_hired)
    return render(request,'book/book_detail.html',{
        'book':book,
        'wishlist': wishlist,
        'user_hired': user_hired,
        'other_hired': other_hired,
        'categories': categories
    })

@login_required(login_url='login')
def pdf_view(request,book_id):
    # Get the book
    book = Book.objects.get(id=book_id)
    # Open the file
    with open(f'media/{book.book_file.name}', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
        return response

@login_required(login_url='login')
def search(request):

    if request.method == 'POST':
        # Get the searched words
        q = request.POST['search']
        # Filter the books 
        book_filter = Book.objects.filter(
                        Q(name__icontains=q) | Q(author__icontains=q))
        # Add Pagination feature
        paginator = Paginator(book_filter,20) # show 20 books per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/index.html',{
        'books': page_obj,
        'categories': categories,
        'searched': True,  
        'search_words': q,  
    })

@login_required(login_url='login')
def delete(request,book_id):
    # Get the book and delete it
    book = Book.objects.get(id=book_id)
    book.delete()
    return HttpResponseRedirect(reverse('index'))


# Members views # Only for admin 
def members(request):
    # Make sure only admin has access to members list
    if request.user.username == 'admin':
        # Get all users except admin
        members = User.objects.all().exclude(is_superuser=True)
    else:
        return HttpResponseForbidden()
    
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/members.html',{
        'members': members,
        'categories': categories
    })

def delete_member(request,member_id):
    # Get the member and delete it
    member = User.objects.get(id=member_id)
    member.delete()
    return redirect('members')


# hirebook views
@login_required(login_url='login')
def hirebook(request,book_id):
    # Get the book
    book = Book.objects.get(id=book_id)
    # Get all categories
    categories = Category.objects.all()
   
    # Create new hired book
    hirebook = HireBook.objects.create(username=request.user.username,book_id=book.id,book_name=book.name,
                                            book_image=book.image,return_date=date.today() + timedelta(days=14))
    hirebook.save()
    return render(request,'book/hirebook_detail.html',{
        'hirebook':hirebook,
        'categories': categories
        }) 

# This feature is only for admin
def search_hirebooks(request):
    if request.method == "POST":
        # Get the searched words
        search = request.POST['search']
        # Filter all hirebooks by username and book name
        hirebooks = HireBook.objects.filter(Q(username__icontains=search) | 
                                            Q(book_name__icontains=search))
    # Get all categories
    categories = Category.objects.all()   

    return render(request,'book/hirebook_list.html',{
        'hirebooks': hirebooks,
        'categories': categories
    })

@login_required(login_url='login')
def hirebook_list(request):
    if request.user.username == 'admin':
        # Get all hired books
        hirebooks = HireBook.objects.all()
        # Get all categories
        categories = Category.objects.all()
    else:
        # Get user's hired books
        hirebooks = HireBook.objects.filter(username=request.user.username)
        # Get all categories
        categories = Category.objects.all()
        return render(request,'book/hirebook_list.html',{'hirebooks': hirebooks,'categories':categories})
    
    return render(request,'book/hirebook_list.html',{'hirebooks': hirebooks,'categories':categories})

@login_required(login_url='login')
def hirebook_detail(request,book_id):
    # Get the hired book
    try:
        hirebook = HireBook.objects.get(id=book_id)
    except HireBook.DoesNotExist:
        raise Http404
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/hirebook_detail.html',{'hirebook':hirebook,'categories':categories})

@login_required(login_url='login')
def hirebook_cancel(request,id):

    # Get the hirebook
    hirebook = HireBook.objects.get(id=id)
    if request.user.username == 'admin':
        # if the user is admin, delete it   
        hirebook.delete()
    else:
        # if user is not admin
        message = 'Please contact your librarian to cancel'
        # Get all categories
        categories = Category.objects.all()

        return render(request,'book/hirebook_detail.html',{
            'hirebook': hirebook,
            'message': message,
            'categories': categories
        })
    return redirect('hirebook_list')

# Category and wishlist views
@login_required(login_url='login')
def category_books(request,cat_id):
    # Get the specific category
    category = Category.objects.get(id=cat_id)
    # Get all books with the same category
    category_books = Book.objects.filter(category=category)
    # Add Pagination feature
    paginator = Paginator(category_books,20) # 20 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/index.html',{
        'categories': categories,
        'books': page_obj
    })

@login_required(login_url='login')
@csrf_exempt
def wishlist(request):

    if request.method == 'GET':
        # Get all the books in user's wishlist
        all_wishlist = []
        wishlists = WishList.objects.filter(username=request.user.username)
        if wishlists is not None:
            for wishlist in wishlists:
                try:
                    book = Book.objects.get(id=wishlist.book_id)
                except Book.DoesNotExist:
                    book = None
                all_wishlist.append(book)
            # Add pagination 
            paginator = Paginator(all_wishlist,20) # 20 books per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            pass
        # Get all categories
        categories = Category.objects.all()

        return render(request,'book/wishlist.html',{
            'books': page_obj,
            'categories': categories
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        
        # Get the book
        book = Book.objects.get(id=data['book_id'])
        # Check whether this book is in user's wishlist or not
        wishlist_obj = WishList.objects.filter(username=request.user.username,book_id=book.id).first()
        if wishlist_obj is not None:
            # Get the wishlist and Delete it
            wishlist = WishList.objects.get(username=request.user.username,book_id=book.id)
            wishlist.delete()
            new_data = {
                'wishlist_already': True
            }
        else:
            # Create new wishlist
            wishlist = WishList.objects.create(username=request.user.username,book_id=book.id)
            wishlist.save()
            new_data = {
                'username': wishlist.username,
                'book_id': wishlist.book_id,
                'wishlist_already': False
            }

            return JsonResponse(new_data,status=200)
        return JsonResponse(new_data,status=200)
    else:
        return JsonResponse({"Error":"POST or GET request method required"},status=404)

# Contact views
@login_required(login_url='login')
def contact (request):
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/contact.html',{'categories':categories})

def send_email(request):
    if request.method == 'POST':
        username = request.POST['username']
        email_from = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Format the message
        message = '''
        From: {}

        Username: {}

        Subject: {}

        New message: {}
        '''.format(email_from,username,subject,message)

        recipient_list = [settings.EMAIL_HOST_USER,]
        send_mail( subject, message,'', recipient_list )

     # Get all categories
    categories = Category.objects.all()

    return render(request,'book/contact.html',{
        'message':'Email was sent successfully',
        'categories': categories
        })


# login,logout,register views
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
                
        else:
            return render(request, "book/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "book/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "book/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create(username=username, email=email, password=make_password(password), phone=phone, address=address)
            user.save()

        except IntegrityError:
            return render(request, "book/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "book/register.html")