from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Article
from unittest.mock import patch


class ArticleAPITests(APITestCase):
    """
    Test suite for Article API endpoints.

    This class verifies correct behaviour of the API, including:
    - Role-based permissions (reader, journalist, editor)
    - Article creation and deletion
    - Visibility of approved articles
    - Subscription-based filtering
    - External API trigger on approval
    """

    def setUp(self):
        """
        Set up test data for all test cases.

        Creates three users with different roles (journalist, editor, reader)
        and an initial unapproved article authored by the journalist.
        """

        self.journalist = User.objects.create_user(
            username="journalist", password="pass123", role="journalist"
        )

        self.editor = User.objects.create_user(
            username="editor", password="pass123", role="editor"
        )

        self.reader = User.objects.create_user(
            username="reader", password="pass123", role="reader"
        )

        self.article = Article.objects.create(
            title="Test", content="Test content", author=self.journalist, approved=False
        )

    def test_journalist_can_create_article(self):
        """
        Verify that a journalist can successfully create an article.

        Expected result:
            - HTTP 201 Created
        """
        self.client.login(username="journalist", password="pass123")

        response = self.client.post(
            "/api/articles/create/", {"title": "New Article", "content": "Some content"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reader_cannot_create_article(self):
        """
        Verify that a reader is forbidden from creating an article.

        Expected result:
            - HTTP 403 Forbidden
        """
        self.client.login(username="reader", password="pass123")

        response = self.client.post(
            "/api/articles/create/", {"title": "Fail", "content": "Should not work"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_delete_article(self):
        """
        Verify that an editor can delete an article.

        Expected result:
            - HTTP 204 No Content
        """
        self.client.login(username="editor", password="pass123")

        response = self.client.delete(f"/api/articles/{self.article.id}/delete/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_journalist_cannot_delete_article(self):
        """
        Verify that a journalist cannot delete an article.

        Expected result:
            - HTTP 403 Forbidden
        """
        self.client.login(username="journalist", password="pass123")

        response = self.client.delete(f"/api/articles/{self.article.id}/delete/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_approved_articles_visible(self):
        """
        Verify that only approved articles are returned in the API.

        Expected behaviour:
            - Unapproved articles are hidden
            - Approved articles are visible
        """
        self.client.login(username="reader", password="pass123")

        response = self.client.get("/api/articles/")
        self.assertEqual(len(response.data), 0)

        # Approve article
        self.article.approved = True
        self.article.save()

        response = self.client.get("/api/articles/")
        self.assertEqual(len(response.data), 1)

    def test_reader_gets_only_subscribed_articles(self):
        """
        Verify that a reader only receives articles from subscribed journalists.

        Expected behaviour:
            - Only articles from subscribed users are returned
        """
        self.client.login(username="reader", password="pass123")

        # Subscribe reader to journalist
        self.reader.subscribed_journalists.add(self.journalist)

        # Approve article
        self.article.approved = True
        self.article.save()

        response = self.client.get("/api/articles/subscribed/")

        self.assertEqual(len(response.data), 1)

    @patch("news_app.views.requests.post")
    def test_approval_triggers_api_call(self, mock_post):
        """
        Verify that approving an article triggers an external API call.

        Expected behaviour:
            - requests.post is called once when an article is approved
        """
        self.client.login(username="editor", password="pass123")

        self.client.get(f"/approve/{self.article.id}/")

        mock_post.assert_called_once()
