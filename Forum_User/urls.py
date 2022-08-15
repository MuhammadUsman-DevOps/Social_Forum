"""Social_Forum URL Configuration"""
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from Forum_User import views
from Social_Forum import settings

urlpatterns = [

    path('<str:username>/profile', views.account_overview, name="account_overview"),
    path('<str:username>/details/', views.account_details, name="account_details"),
    path('<str:username>/settings/', views.account_settings, name="account_settings"),

    # path('', views.account_overview, name="account_overview"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),

    path('upload-post/', views.upload_post, name="upload_post"),
    path('add-comment/', views.add_comment, name="add_comment"),
    path('add-vote/', views.add_vote, name="add_vote"),



]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
