from django.shortcuts import render


def account_overview(request):
    return render(request, template_name="account/overview.html")


def account_details(request):
    return render(request, template_name="account/user_details.html")


def account_settings(request):
    return render(request, template_name="account/settings.html")
