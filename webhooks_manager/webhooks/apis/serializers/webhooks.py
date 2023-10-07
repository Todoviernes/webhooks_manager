from rest_framework import serializers

from webhooks_manager.webhooks.models import Source, Webhook


class WebhookSerializer(serializers.ModelSerializer):
    """Serializer for Webhook model"""

    data = serializers.JSONField()

    class Meta:
        """Meta class"""

        model = Webhook
        fields = ["id", "source", "data"]

    def create(self, validated_data):
        """Create a webhook"""
        return Webhook.objects.create(**validated_data)


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("id", "name", "url")  # And other fields if you added any
