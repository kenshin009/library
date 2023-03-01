from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('search',views.search,name='search'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('delete/<int:book_id>',views.delete,name='delete'),
    path('add-book',views.add_book,name='add_book'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('register',views.register,name='register'),
]