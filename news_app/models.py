from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    This model introduces role-based access control and subscription features.
    Users can have one of three roles: reader, editor, or journalist.

    Additional Features:
    - Users can subscribe to publishers and journalists.
    - Users are automatically assigned to a Django Group based on their role.
    """

    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("editor", "Editor"),
        ("journalist", "Journalist"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    subscribed_publishers = models.ManyToManyField(
        "Publisher", blank=True, related_name="subscribers"
    )

    subscribed_journalists = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="followers"
    )

    def save(self, *args, **kwargs):
        """
        Override save method to assign the user to a Django group
        based on their role.

        This ensures role-based permissions can be managed using Django's
        built-in authentication system.
        """
        super().save(*args, **kwargs)

        if self.role:
            group, created = Group.objects.get_or_create(name=self.role)
            self.groups.add(group)

    def __str__(self):
        """
        Return a readable string representation of the user.
        """
        return f"{self.username} ({self.role})"


class Publisher(models.Model):
    """
    Represents a news publisher.

    A publisher can have multiple editors and journalists associated with it.
    """

    name = models.CharField(max_length=255)

    editors = models.ManyToManyField(
        "news_app.User", related_name="publisher_editor_roles", blank=True
    )

    journalists = models.ManyToManyField(
        "news_app.User", related_name="publisher_journalist_roles", blank=True
    )

    def __str__(self):
        """
        Return the publisher name.
        """
        return self.name


class Article(models.Model):
    """
    Represents a news article created by a journalist.

    Articles can optionally belong to a publisher and must be approved
    before becoming visible to readers.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def clean(self):
        """
        Validate that the article has a valid author.

        Raises:
            ValueError: If the article does not have an associated author.
        """
        if not self.author:
            raise ValueError("Article must have an author.")

    def __str__(self):
        """
        Return the article title.
        """
        return self.title


class Newsletter(models.Model):
    """
    Represents a newsletter containing a collection of articles.

    A newsletter is authored by a user and can include multiple articles.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="newsletters"
    )

    articles = models.ManyToManyField(Article)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return the newsletter title.
        """
        return self.title
