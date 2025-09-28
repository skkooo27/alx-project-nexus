import os
from celery import Celery
from decouple import config

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Redis URL (Upstash) – provide default to avoid errors
REDIS_URL = config(
    "REDIS_URL",
    default="rediss://default:ATWqAAIncDIwMTA4NWFkMDY5MTk0MmUzODMyOTY5ZDNkMzc4OWVmM3AyMTM3Mzg@robust-kangaroo-13738.upstash.io:6379"
)

# Initialize Celery app
app = Celery(
    "config",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["core.tasks"]
)

# Load Django settings with CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# SSL configuration for Upstash Redis
app.conf.broker_use_ssl = {"ssl_cert_reqs": None}
app.conf.result_backend_transport_options = {"ssl_cert_reqs": None}

# Optional: route specific tasks to a queue
app.conf.task_routes = {
    "core.tasks.send_order_confirmation": {"queue": "celery"}
}
