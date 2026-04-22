from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),

    path("create-article/", views.create_article, name="create_article"),
    path("update/<int:article_id>/", views.update_article, name="update_article"),
    path("delete/<int:article_id>/", views.delete_article, name="delete_article"),

    path("approve/<int:article_id>/", views.approve_article, name="approve_article"),

    path("subscribe/<int:user_id>/", views.subscribe, name="subscribe"),
    path("unsubscribe/<int:user_id>/", views.unsubscribe, name="unsubscribe"),

    path("subscribed/", views.subscribed_articles, name="subscribed_articles"),

    # NEWSLETTERS
    path("newsletters/", views.list_newsletters, name="newsletters"),
    path("create-newsletter/", views.create_newsletter, name="create_newsletter"),
    path("subscribe-newsletter/<int:newsletter_id>/", views.subscribe_newsletter, name="subscribe_newsletter"),
    path("update-newsletter/<int:newsletter_id>/", views.update_newsletter, name="update_newsletter"),
    path("delete-newsletter/<int:newsletter_id>/", views.delete_newsletter, name="delete_newsletter"),
    path("article/<int:article_id>/", views.article_detail, name="article_detail"),
    path("create-publisher/", views.create_publisher, name="create_publisher"),
]
