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
        return redirect('/')

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
        return redirect('/')