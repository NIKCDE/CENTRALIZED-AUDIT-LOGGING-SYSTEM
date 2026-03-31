from functools import wraps
from .services import AuditService


def audit_log(action="CUSTOM", model_name=None):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):

            response = view_func(self, request, *args, **kwargs)

            user = request.user if request.user.is_authenticated else None

            AuditService.log(
                user=user,
                action=action,
                model_name=model_name,
                object_id=kwargs.get("pk"),
                description=f"Custom action in {view_func.__name__}",
                status="SUCCESS" if response.status_code < 400 else "FAILED"
            )

            return response

        return wrapper

    return decorator