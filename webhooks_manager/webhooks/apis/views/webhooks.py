from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from webhooks_manager.webhooks.apis.serializers import WebhookSerializer
from webhooks_manager.webhooks.models import Webhook
from webhooks_manager.webhooks.tasks import process_webhook


class WebhooksViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create a webhook"""
        data = request.data
        webhook_source_name = request.headers["Host"]

        # Call the asynchronous task to handle the webhook creation and processing
        process_webhook.delay(data, webhook_source_name)

        response_data = {
            "message": "Webhook on queue",
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
