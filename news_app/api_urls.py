from django.urls import path
from .views import (
    ArticleListAPIView,
    SubscribedArticlesAPIView,
    ArticleDetailAPIView,
    ArticleCreateAPIView,
    ArticleUpdateAPIView,
    ArticleDeleteAPIView,
)
from .views import approved_article_log

urlpatterns = [
    path("articles/", ArticleListAPIView.as_view()),
    path("articles/subscribed/", SubscribedArticlesAPIView.as_view()),
    path("articles/<int:pk>/", ArticleDetailAPIView.as_view()),
    path("articles/create/", ArticleCreateAPIView.as_view()),
    path("articles/<int:pk>/update/", ArticleUpdateAPIView.as_view()),
    path("articles/<int:pk>/delete/", ArticleDeleteAPIView.as_view()),
    path("approved/", approved_article_log),
]
