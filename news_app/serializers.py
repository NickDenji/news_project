from rest_framework import serializers
from .models import Article, Publisher, Newsletter, User


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Handles conversion between Article instances and JSON, and ensures
    that sensitive fields such as 'author' and 'approved' cannot be
    manually set by clients.

    The author is automatically assigned based on the authenticated user.
    Articles are created as unapproved by default and can only be approved
    by editors.
    """

    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Meta configuration for ArticleSerializer.

        Attributes:
            model (Model): The Article model.
            fields (str): Include all model fields.
            read_only_fields (list): Prevents modification of restricted fields.
            extra_kwargs (dict): Makes publisher optional.
        """

        model = Article
        fields = "__all__"
        read_only_fields = ["author", "approved"]
        extra_kwargs = {"publisher": {"required": False}}


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model.

    Converts Publisher instances to and from JSON representation.
    """

    class Meta:
        model = Publisher
        fields = "__all__"


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Newsletter model.

    Used to validate and serialize newsletter data.
    """

    class Meta:
        model = Newsletter
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Exposes only essential user information required by the API.
    """

    class Meta:
        model = User
        fields = ["id", "username", "role"]
