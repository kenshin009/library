from django.urls import path 
from . import views

urlpatterns = [
    # book routes
    path('',views.index,name='index'),
    path('book-detail/<int:book_id>',views.book_detail,name='book_detail'),
    path('view-pdf/<int:book_id>', views.pdf_view,name='pdf_view'),
    path('search',views.search,name='search'),
    path('delete/<int:book_id>',views.delete,name='delete'),
    path('add-book',views.add_book,name='add_book'),

    # member routes
    path('members',views.members,name='members'),
    path('delete-member/<int:member_id>',views.delete_member,name='delete_member'),

    # hirebook routes
    path('hirebook/<int:book_id>',views.hirebook,name='hirebook'),
    path('hirebook-list',views.hirebook_list,name='hirebook_list'),
    path('hirebook-detail/<int:book_id>',views.hirebook_detail,name='hirebook_detail'),
    path('hirebook-cancel/<int:id>',views.hirebook_cancel,name='hirebook_cancel'),
    path('search-hirebooks',views.search_hirebooks,name='search_hirebooks'),

    #category and wishlist routes
    path('category-books/<int:cat_id>',views.category_books,name='category_books'),
    path('wishlist',views.wishlist,name='wishlist'),

    # contact routes
    path('contact',views.contact,name='contact'),
    path('send-email',views.send_email,name='send_email'),

    # login,logout,register routes
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('register',views.register,name='register'),
]