from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_order_confirmation(self, email, order_id):
    """
    Sends an order confirmation email asynchronously via Celery.

    Retries up to 3 times if sending fails, with a 1-minute delay between retries.
    """
    subject = "Order Confirmation"
    message = f"Your order {order_id} has been received and is being processed."
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False  # Raise exception if email fails
        )
        # Return structured info
        return {"email": email, "order_id": order_id, "status": "sent"}

    except Exception as exc:
        # Retry the task in 60 seconds if email sending fails
        raise self.retry(exc=exc, countdown=60)
