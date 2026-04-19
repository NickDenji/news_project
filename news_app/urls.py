from django.urls import path
from .views import home
from .views import approve_article
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("approve/<int:article_id>/", approve_article, name="approve_article"),
    path("register/", views.register, name="register"),
]
