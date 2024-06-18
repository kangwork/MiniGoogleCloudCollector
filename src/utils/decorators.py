import functools
import inspect
from fastapi.responses import JSONResponse


def method_error_handler_decorator(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            caller_class_name = type(self).__name__
            caller_info = f"{caller_class_name}.{method.__name__}"

            signature = inspect.signature(method)
            bound_arguments = signature.bind(self, *args, **kwargs)
            bound_arguments.apply_defaults()
            self.logger.add_error(
                f"{caller_info}({bound_arguments.arguments}): {str(e)}"
            )
            raise e

    return wrapper


def func_error_handler_decorator(logger, is_api=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                caller_info = f"{func.__name__}"

                signature = inspect.signature(func)
                bound_arguments = signature.bind(*args, **kwargs)
                bound_arguments.apply_defaults()
                logger.add_error(
                    f"{caller_info}({bound_arguments.arguments}): {str(e)}"
                )
                if not is_api:
                    raise e
                else:
                    api_response = {
                        "data": "",
                        "message": f"Failed to retrieve data: {str(e)}",
                    }
                    return JSONResponse(
                        content=api_response, status_code=getattr(e, "code", 500)
                    )

        return wrapper

    return decorator
