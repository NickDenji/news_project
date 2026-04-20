from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("approve/<int:article_id>/", views.approve_article, name="approve_article"),
    path("register/", views.register, name="register"),
    path("create-article/", views.create_article, name="create_article"),
    path("subscribe/<int:user_id>/", views.subscribe, name="subscribe"),
    path("unsubscribe/<int:user_id>/", views.unsubscribe, name="unsubscribe"),
    path("subscribed/", views.subscribed_articles, name="subscribed_articles"),
]
