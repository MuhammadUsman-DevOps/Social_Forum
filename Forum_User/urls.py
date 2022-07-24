
"""Social_Forum URL Configuration"""
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from Forum_User import views
from Social_Forum import settings

urlpatterns = [
   path('', views.account_overview, name="account_overview"),
   path('details/', views.account_details, name="account_details"),
   path('settings/', views.account_settings, name="account_settings"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)