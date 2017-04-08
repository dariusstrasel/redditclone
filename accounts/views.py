from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def signup(request):
    if request.method == 'POST':
        user = {
            'username': request.POST['username'],
            'password': request.POST['password'],
            'password_verification': request.POST['password_verification'],
            'email': "user@example.com",
        }
        if user['password'] == user['password_verification']:
            try:
                User.objects.get(username=user['username'])
                return render(request, 'accounts/signup.html', {'error': 'User already exists.'})
            except User.DoesNotExist:
                user = User.objects.create_user(user['username'], user['email'], user['password'])
                login(request, user)
                return render(request, 'accounts/signup.html')
        else:
            return render(request, 'accounts/signup.html', {'error': "Passwords do not match."})

    else:
        return render(request, 'accounts/signup.html')


def login_user(request):
    if request.method == 'POST':
        user = {
            'username': request.POST['username'],
            'password': request.POST['password'],
        }

        authenticated_user = authenticate(username=user['username'], password=user['password'])

        if authenticated_user is not None:
            login(request, authenticated_user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid login.'})

    else:
        return render(request, 'accounts/login.html')


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
