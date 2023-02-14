# utils/context_processor.py
"""Module to get the selected settings value."""
from django.conf import settings


def get_version(request) -> dict:
    """Return the version value as a dictionary you may add other values
    here as well.
    :return: Project version.
    :rtype: dict
    """
    return {"APP_VERSION_NUMBER": settings.APP_VERSION_NUMBER}
