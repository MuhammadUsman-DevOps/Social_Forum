from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from Forum_User.models import Post, ContentPost, UserProfile


def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("news_feed")
        else:
            messages.error(request, "Invalid Email address Or Password!")
    return render(request, template_name="authentication/signin.html")


def auth_singup(request):
    if request.method == "POST":
        email_address = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        user = User.objects.create(
            username=email_address,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            email=email_address,
            is_active=True
        )
        user.save()

        userProfile = UserProfile.objects.create(user=user)
        # TODO: Sent Account Confirmation Email
        auth_user = authenticate(request, username=email_address, password=password)
        if auth_user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("news_feed")
    return render(request, template_name="authentication/signup.html")


def auth_logout(request):
    logout(request)
    return redirect("news_feed")


def news_feed(request):
    posts = ContentPost.objects.all()
    user_profile = None
    if (request.user.is_authenticated):
        user_profile = UserProfile.objects.get(user=request.user)
    context = {'posts': reversed(posts), 'user_profile': user_profile}
    return render(request, template_name="forum/news_feed.html", context=context)
