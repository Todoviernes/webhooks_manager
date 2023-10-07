import logging

from celery import Task, shared_task
from celery.exceptions import MaxRetriesExceededError

from webhooks_manager.webhooks.models import Source, Webhook

# Set up logging for the webhooks app
logger = logging.getLogger("webhooks")


class RetryTask(Task):
    """Custom task class to handle retries"""

    autoretry_for = (MaxRetriesExceededError,)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = True


# Define a shared task for processing webhooks


@shared_task(bind=True, base=RetryTask)
def process_webhook(self, data, webhook_source_name):
    """Process a webhook"""
    try:
        # Get or create the webhook source
        webhook_source, created = Source.objects.get_or_create(name=webhook_source_name)

        # Create a new webhook instance
        webhook = Webhook(source=webhook_source, data=data)

        # Save the webhook instance to the database
        webhook.save()

        # Process the webhook as needed
        webhook.processed = True
        webhook.save()

        # Log a success message
        logger.info(f"Webhook {webhook.id} saved successfully")

        # Return the webhook ID
        return webhook.id
    except MaxRetriesExceededError as exc:
        # Log an error message and re-raise the exception
        logger.error(f"Max retries exceeded for webhook: {exc}")
        raise
    except Exception as exc:
        # Log an error message and retry the task
        logger.error(f"Error processing webhook: {exc}")
        self.retry(exc=exc)
