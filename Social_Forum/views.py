from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import re
from Forum_User.models import Post, ContentPost, UserProfile, HashTags


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
    hash_tags = HashTags.objects.all()
    hash_tags = trending_hashtags(hashtags=hash_tags, posts=posts)
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except:
            user_profile = None
    context = {'posts': reversed(posts), 'hash_tags': hash_tags, 'user_profile': user_profile}
    return render(request, template_name="forum/news_feed.html", context=context)


def trending_hashtags(hashtags, posts):
    # ----------------------------- FINDING THE TRENDING HASHTAGS BASED ON THEIR USAGE IN POST-----------------------
    trending_tags = {}
    for tag in hashtags:
        trending_tags[tag] = 0
        for post in posts:
            if post.post.hashtags is not None:
                if re.search(tag.tag, post.post.hashtags, re.IGNORECASE):
                    trending_tags[tag] = trending_tags[tag] + 1
    # SORTING THE LIST BY DECENDING ORDER
    trending_tags = dict(sorted(trending_tags.items(), key=lambda item: item[1], reverse=True))
    trending_tags = trending_tags.keys()
    # IF FINAL LIST IS GREATER THEN 10 THEN SELECT ONLY TOP 10 TAGS ELSE COMPLETE LIST
    if len(trending_tags) > 10:
        trending_tags = trending_tags[0:10]

    return trending_tags
