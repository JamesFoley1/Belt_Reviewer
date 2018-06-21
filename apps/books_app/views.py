from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


def index(request):
    request.session.clear()
    return render(request, 'books/index.html')

def books(request):
    if request.session['isvalid'] == True:
        context = {
            'user': Users.objects.get(id = request.session['user_id']),
            'book': Books.objects.all(),
            'review': Review.objects.all(),
        }
        return render(request, 'books/books.html', context)
    else:
        redirect('/')

def add_books(request):
    if request.session['isvalid'] == True:
        return render(request, 'books/add_books.html')
    else: redirect('/')

def show_books(request, id):
    if request.session['isvalid'] == True:
        context = {
            'user': Users.objects.get(id = request.session['user_id']),
            'book': Books.objects.get(id = id),
            'review': Review.objects.all(),
        }
        request.session['show_id'] = id
        return render(request, 'books/show_books.html', context)
    else:
        return redirect('/')

def users(request, id):
    if request.session['isvalid'] == True:
        context = {
            'user': Users.objects.get(id = id),
            'book': Books.objects.all(),
            'review': Review.objects.filter(id = id),
            'user_book': Users.objects.get(id = id).reviewer.all()
        }
        request.session['count'] = len(context['user'].reviewer.all())
        return render(request, 'books/users.html', context)
    else:
        return redirect('/')

def register(request):
    request.session['name'] = request.POST['name']
    request.session['alias'] = request.POST['alias']
    request.session['email'] = request.POST['email']
    request.session['password'] = request.POST['password']
    request.session['pw_confirm'] = request.POST['pw_confirm']
    if request.method == "POST":
        result = Users.objects.basic_validator(request.POST)
        if isinstance(result, dict):
            for tags, value in result.items():
                messages.error(request, value, extra_tags=tags)
            return redirect('/')
        else:
            request.session['isvalid'] = True
            request.session['user_id'] = result
            request.session['name'] = Users.objects.get(id = result).name
        return redirect('/books')

def login(request):
    if request.method == "POST":
        user = Users.objects.basic_validator2(request.POST)
        if 'invalid_email' in user or 'empty' in user:
            for tags, value in user.items():
                messages.error(request, value, extra_tags=tags)
            return redirect('/')
        else:
            request.session['isvalid'] = True
            request.session['user_id'] = user[0].id
            request.session['name'] = user[0].name
            return redirect('/books')

def review(request):
    if request.method == "POST":
        my_id = request.session['user_id']
        review = Users.objects.basic_validator3(request.POST, my_id)
        return redirect('/books/show/'+request.session['show_id'])

def destroy(request):
    if request.method == "POST":
        if Review.objects.get(id = request.POST['review_id']).user.id == request.session['user_id']:
            Review.objects.get(id = request.POST['review_id']).delete()
            return redirect('/books/show/'+request.session['show_id'])

def addbook(request):
    if request.method == "POST":
        my_id = request.session['user_id']
        book = Users.objects.basic_validator4(request.POST, my_id)
        new_id = str(book.id)
        return redirect('/books/show/'+new_id)