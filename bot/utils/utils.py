import logging
import os

import requests

log = logging.getLogger(__name__)


def retry(times):
    """
    @retry decorator to handle random 404s from the Spotify API
    https://github.com/spotify/web-api/issues/1160
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    attempt += 1
                    logging.warning(
                        f"{func.__name__}: attempt {attempt} of {times} failed"
                    )
                    logging.warning(err)
            return func(*args, **kwargs)

        return newfn

    return decorator


def internet():
    """Check for internet connectivity"""

    try:
        requests.get("https://www.kernel.org").status_code
        return True
    except requests.exceptions.RequestException:
        return False


def push(message):
    """Push a message to phone"""

    requests.post(
        os.environ["NTFY_URL"],
        data=message.encode(encoding="utf-8"),
        headers={"Title": "Sigurd", "Priority": "2"},
    )
