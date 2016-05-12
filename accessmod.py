import inspect

def private(function):
    def oop_violation_error():
        raise AttributeError(
            "Private attributes and methods are only " +
            "accessible from the owner class."
        )
    def wrapper(*args, **kwargs):
        class_instance = inspect.currentframe().f_back.f_locals.get("self", None)
        if class_instance is None:
            oop_violation_error()
        caller_class = class_instance.__class__.__qualname__
        fn_name = function.__name__
        qualified_fn_name = function.__qualname__
        if qualified_fn_name != "{0}.{1}".format(caller_class, fn_name):
            oop_violation_error()
        return function(*args, **kwargs)
    return wrapper

def public(function):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper
