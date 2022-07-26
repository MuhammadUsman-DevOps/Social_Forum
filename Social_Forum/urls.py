"""Social_Forum URL Configuration"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from Social_Forum import settings, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('u/', include("Forum_User.urls")),
    path('news-feed/', views.news_feed, name="news_feed"),
    path('accounts/login/', views.auth_login, name="auth_login"),
    path('accounts/signup/', views.auth_singup, name="auth_singup"),
    path('accounts/logout/', views.auth_logout, name="auth_logout"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)