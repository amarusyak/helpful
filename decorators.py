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


def singleton(class_):
    """
    Singleton Decorator.
    Example of use:
    >>> @singleton
    >>> class MyClass(object):
    >>>     pass
    NOTE: better use Metaclass...
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


class Singleton(type):
    """
    Singleton Metaclass.
    Example of use:
    >>> class MyClass(metaclass=Singleton):
    >>>     pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            # run __init__ every time the class is called
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
