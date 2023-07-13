from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
