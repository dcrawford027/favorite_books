from django.shortcuts import render, redirect
from .models import User, Book
import bcrypt
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(first_name=firstName, last_name=lastName, email=email, password=pw_hash)
        request.session['user_id'] = user.id
        return redirect('/books')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email)
        request.session['user_id'] = user.id
        return redirect('/books')

def books(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'books': Book.objects.all(),
        }
        return render(request, 'books.html', context)

def addBook(request):
    errors = Book.objects.add_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        title = request.POST['title']
        desc = request.POST['desc']
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(title=title, desc=desc)
        book.uploaded_by_id.add(user)
        book.users_who_like.add(user)
        return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')