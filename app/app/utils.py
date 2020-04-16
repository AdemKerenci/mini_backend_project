from functools import wraps


def with_response(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        result, code, errors = [], 0, []
        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            code = 1
            errors.append(repr(e))
        return dict(result=result, code=code, errors=errors)

    return wrapped
