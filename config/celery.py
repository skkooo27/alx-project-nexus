import os
from celery import Celery
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

REDIS_URL = config(
    "REDIS_URL",
    default="rediss://default:ATWqAAIncDIwMTA4NWFkMDY5MTk0MmUzODMyOTY5ZDNkMzc4OWVmM3AyMTM3Mzg@robust-kangaroo-13738.upstash.io:6379"
)

# Initialize Celery app
app = Celery(
    "config",
    broker=REDIS_URL,   # Use Upstash Redis as broker
    backend=None,       
    include=["core.tasks"]
)

# Load Django settings for Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

# Optional: route specific tasks to a queue
app.conf.task_routes = {
    "core.tasks.send_order_confirmation": {"queue": "celery"}
}
