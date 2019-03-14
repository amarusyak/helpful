def content_type(method):
    """
    Decorator that adds {'content-type': 'application/json'} 
        to HTTP methods headers.
    """
    def wrapper(*args, **kwargs):
        headers = kwargs.pop('headers', dict())
        if 'content-type' not in headers:
            headers['content-type'] = 'application/json'
        return method(headers=headers, *args, **kwargs)
    return wrapper
