"""Gunicorn settings module.
"""
import uptrace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor



def post_fork(server, worker):
    """Config Opentelemetry monitoring tools.
    """
    server.log.info("Worker spawned (pid: %s)", worker.pid)

    # uptrace.configure_opentelemetry(
    #     # Set dsn or use UPTRACE_DSN env var.
    #     #dsn="",
    #     service_name="",
    #     service_version="1.0.0",
    # )
    # DjangoInstrumentor().instrument()
    # Psycopg2Instrumentor().instrument()
