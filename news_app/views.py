from django.shortcuts import render
from .models import Article, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .serializers import ArticleSerializer
from rest_framework import status
from .permissions import IsJournalist
from .permissions import IsEditorOrJournalist
from .permissions import IsEditor
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
import requests
from django.contrib.auth import login
from .permissions import IsReader

# Create your views here.


def register(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = User.objects.create_user(username=username, password=password, role=role)

        login(request, user)
        return redirect("home")

    return render(request, "news_app/register.html")


def home(request):
    """
    Displays articles based on user role.
    """

    if not request.user.is_authenticated:
        return render(request, "news_app/home.html")

    if request.user.role == "editor":
        articles = Article.objects.all()

    elif request.user.role == "reader":
        articles = Article.objects.filter(
            approved=True, author__in=request.user.subscribed_journalists.all()
        )

    else:
        # journalist
        articles = Article.objects.filter(approved=True)

    return render(request, "news_app/home.html", {"articles": articles})


def is_editor(user):
    """
    Check whether a given user has the 'editor' role.

    This function is typically used with decorators such as
    `user_passes_test` to restrict access to views that require
    editor-level permissions.

    Args:
        user (User): The user instance to be checked.

    Returns:
        bool: True if the user has the role 'editor', otherwise False.
    """
    return user.role == "editor"


@user_passes_test(is_editor)
def approve_article(request, article_id):
    """
    Allows only editors to approve articles and triggers API notification.
    """

    article = get_object_or_404(Article, id=article_id)

    if not article.approved:
        article.approved = True
        article.save()

        requests.post(
            "http://127.0.0.1:8000/api/approved/", json={"article_id": article.id}
        )

    return redirect("home")


class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns all approved articles.
        """
        articles = Article.objects.filter(approved=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class SubscribedArticlesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsReader]

    def get(self, request):
        """
        Returns articles from subscribed publishers and journalists.
        Accessible only to readers.
        """
        user = request.user

        articles = Article.objects.filter(approved=True).filter(
            Q(author__in=user.subscribed_journalists.all())
            | Q(publisher__in=user.subscribed_publishers.all())
        )

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve a single article by its primary key.

        This endpoint returns the details of a specific article.
        The user must be authenticated to access this view.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the article to retrieve.

        Returns:
            Response: A JSON response containing the serialized article data.

        Raises:
            Article.DoesNotExist: If no article exists with the given primary key.
        """
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


class ArticleCreateAPIView(CreateAPIView):
    """
    Allows journalists to create articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsJournalist]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleUpdateAPIView(UpdateAPIView):
    """
    Allows editors and journalists to update articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsEditorOrJournalist]

    def perform_update(self, serializer):
        article = self.get_object()

        # Journalists can only edit their own articles
        if (
            self.request.user.role == "journalist"
            and article.author != self.request.user
        ):
            raise PermissionDenied("You can only edit your own articles.")

        serializer.save()


class ArticleDeleteAPIView(DestroyAPIView):
    """
    Allows editors to delete articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsEditor]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approved_article_log(request):
    """
    Logs approved articles (simulating external API).
    """

    article_id = request.data.get("article_id")

    return Response({"message": f"Article {article_id} received by external API"})
