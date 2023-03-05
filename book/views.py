from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,date,timedelta
from django.db import IntegrityError
from django.urls import reverse
from django.db.models import Q
import json
from .models import *
# Create your views here.

@login_required(login_url='login')
def index (request):
    # Get all books
    books = Book.objects.all()
    # Get all user's wishlists
    wishlists = WishList.objects.filter(username=request.user.username)
    # GEt all user's hirebooks
    hirebooks = HireBook.objects.filter(username=request.user.username)
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/index.html',{
        'books': books,
        'wishlists': wishlists,
        'hirebooks': hirebooks,
        'categories': categories
    })

def pdf_view(request):
    with open('media/files/goblet.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
        return response

def search(request):

    if request.method == 'POST':
        # Get the searched words
        q = request.POST['search']
        # Filter the books 
        book_filter = Book.objects.filter(
                        Q(name__icontains=q) | Q(author__icontains=q))
        print(book_filter)
        wishlists = WishList.objects.filter(username=request.user.username)

    # GEt all user's hirebooks
    hirebooks = HireBook.objects.filter(username=request.user.username)
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/index.html',{
        'books': book_filter,
        'wishlists': wishlists,
        'hirebooks': hirebooks,
        'categories': categories,
        'searched': True,    
    })

def delete(request,book_id):
    # Get the book and delete it
    book = Book.objects.get(id=book_id)
    book.delete()
    return HttpResponseRedirect(reverse('index'))


def hirebook(request,book_id):
    # Get the book
    book = Book.objects.get(id=book_id)
    # Get all categories
    categories = Category.objects.all()
    # Check whether the user has already hired the book or not
    hired = HireBook.objects.filter(username=request.user.username,book_id=book.id).first()
    # if the user has already hired
    if hired is not None:
   
        # Show a message to contact librarian to delete hire
        message = 'Please contact your librarian to cancel'
         # Get all books
        books = Book.objects.all()
        # Get all user's wishlists
        wishlists = WishList.objects.filter(username=request.user.username)
        # GEt all user's hirebooks
        hirebooks = HireBook.objects.filter(username=request.user.username)
        
        # Redirect to home with context
        return render(request,'book/index.html',{
            'books': books,
            'wishlists': wishlists,
            'hirebooks': hirebooks,
            'message': message,
            'categories': categories
        })
    # if not hired yet
    else:
        # Create new hired book
        hirebook = HireBook.objects.create(username=request.user.username,book_id=book.id,book_name=book.name,
                                                book_image=book.image,return_date=date.today() + timedelta(days=14))
        hirebook.save()
        return render(request,'book/hirebook_detail.html',{
            'hirebook':hirebook,
            'categories': categories
            }) 
    
def hirebook_cancel(request,id):
    if request.user.username == 'admin':
        # if the user is admin
        # Get the hirebook and delete it
        hirebook = HireBook.objects.get(id=id)
        hirebook.delete()
    else:
        # if user is not admin
        message = 'You need to inform your librarian to cancel'
        # Get all categories
        categories = Category.objects.all()

        return render(request,'book/hirebook_detail.html',{
            'message': message,
            'categories': categories
        })
    return redirect('hirebook_list')

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

def hirebook_detail(request,book_id):
    # Get the hired book
    try:
        hirebook = HireBook.objects.get(id=book_id)
    except HireBook.DoesNotExist:
        raise Http404
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/hirebook_detail.html',{'hirebook':hirebook,'categories':categories})


def category_books(request,cat_id):
    # Get the specific category
    category = Category.objects.get(id=cat_id)
    # Get all books with the same category
    category_books = Book.objects.filter(category=category)
    # Get all categories
    categories = Category.objects.all()
    # Get all user's wishlists
    wishlists = WishList.objects.filter(username=request.user.username)
    # GEt all user's hirebooks
    hirebooks = HireBook.objects.filter(username=request.user.username)

    return render(request,'book/index.html',{
        'categories': categories,
        'books': category_books,
        'wishlists': wishlists,
        'hirebooks': hirebooks
    })

@csrf_exempt
def wishlist(request):

    if request.method == 'GET':
        # Get all the books in user's wishlist
        all_wishlist = []
        wishlists = WishList.objects.filter(username=request.user.username)
        if wishlists is not None:
            for wishlist in wishlists:
                book = Book.objects.get(id=wishlist.book_id)
                all_wishlist.append(book)
        else:
            pass
        # Get all categories
        categories = Category.objects.all()

        return render(request,'book/wishlist.html',{
            'wishlists': all_wishlist,
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

def contact (request):
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/contact.html',{'categories':categories})

@login_required(login_url='login')
def add_book(request):

    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        category = request.POST['category']
        image = request.FILES.get('image')
        buy_date = request.POST['buy_date']

        # Check category is already present or not
        try:
            category_obj = Category.objects.get(title=category.upper())
        except:
            category_obj = Category.objects.create(title=category.upper())
        # Create new book
        new_book = Book.objects.create(name=name,author=author,category=category_obj,image=image,buy_date=buy_date)
        new_book.save()
        return redirect('index')
    
    # Get all categories
    categories = Category.objects.all()

    return render(request,'book/add_book.html',{'categories':categories})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        # Check user is present or not
        user_filter = User.objects.filter(username=username,password=password).first()
        # Check if authentication successful
        if user_filter is not None:
            user = User.objects.get(username=username,password=password)
            # user = authenticate(request, username=username,password=password,email=get_user.email,phone=get_user.phone,address=get_user.address)
      
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
            # if user is not None:
            #     login(request, user)
                
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
            user = User.objects.create(username=username, email=email, password=password, phone=phone, address=address)
            user.save()

        except IntegrityError:
            return render(request, "book/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "book/register.html")