import functools
import inspect

def error_handler_decorator(method):
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
            self.logger.add_error(f"{caller_info}({bound_arguments.arguments}): {str(e)}")
            raise e
    return wrapper