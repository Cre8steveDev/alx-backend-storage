#!/usr/bin/env python3
"""
Implementing a Web Page Tracker to count the Number
of times a specific url is accessed
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """ Decorator that counts how many times a
    URL is accessed"""
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text
