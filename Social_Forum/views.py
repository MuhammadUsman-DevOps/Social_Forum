from django.shortcuts import render


def news_feed(request):
    return render(request, template_name="forum/news_feed.html")


def auth_login(request):
    return render(request, template_name="authentication/signin.html")

def auth_singup(request):
    return render(request, template_name="authentication/signup.html")