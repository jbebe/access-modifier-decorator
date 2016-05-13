from inspect import currentframe

def __accessmod_error():
    raise AttributeError(
        "Private methods are only accessible from the owner class."
    )

def public(method):
    def wrapper(*args, **kwargs):
        return method(*args, **kwargs)
    return wrapper

def private(method):
    def wrapper(*args, **kwargs):
        caller_self = currentframe().f_back.f_locals.get("self")
        if caller_self is None:
            __accessmod_error()
            return method(*args, **kwargs)
        caller_full_name = caller_self.__class__.__qualname__
        func_name = method.__name__
        func_full_name = method.__qualname__
        caller_full_fn_name = caller_full_name + '.' + func_name
        if func_full_name != caller_full_fn_name:
            __accessmod_error()
        return method(*args, **kwargs)
    return wrapper

def protected(method):
    def wrapper(*args, **kwargs):
        def find_class(class_str, child_class):
            if child_class.__qualname__ == class_str:
                return True
            for base in child_class.__bases__:
                if base.__qualname__ == class_str:
                    return True
                if base.__bases__ != (object,):
                    find_class(class_str, base.__bases__)
            return False
        caller_self = currentframe().f_back.f_locals.get("self")
        if caller_self is None:
            __accessmod_error()
        caller_type = caller_self.__class__
        func_full_name = method.__qualname__
        func_class_name_end = func_full_name.rfind('.')
        func_class_full_name = func_full_name[0:func_class_name_end]
        if not find_class(func_class_full_name, caller_type):
            __accessmod_error()
        return method(*args, **kwargs)
    return wrapper
