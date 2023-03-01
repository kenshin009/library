from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.urls import reverse
import json
from .models import *
# Create your views here.

def index (request):

    books = Book.objects.all()
    wishlists = WishList.objects.filter(username=request.user.username)
    return render(request,'book/index.html',{
        'books': books,
        'wishlists': wishlists
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

        return render(request,'book/wishlist.html',{
            'wishlists': all_wishlist
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
    return render(request,'book/add_book.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
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