from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from webhooks_manager.users.api.views import UserViewSet
from webhooks_manager.webhooks.apis.views.webhooks import WebhooksViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("webhooks", WebhooksViewSet)

app_name = "api"
urlpatterns = router.urls
