from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
from django.utils.crypto import get_random_string


def pg_records(request, list, num):
    paginator = Paginator(list, num)

    # get the page parameter from the query string
    # if page parameter is available get() method will return empty string ''
    page = request.GET.get('page')

    try:
        # create Page object for the given page
        page_object = paginator.page(page)
    except PageNotAnInteger:
        # if page parameter in the query string is not available, return the first page
        page_object = paginator.page(1)
    except EmptyPage:
        # if the value of the page parameter exceeds num_pages then return the last page
        page_object = paginator.page(paginator.num_pages)

    return page_object


def generate_activation_key(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()
