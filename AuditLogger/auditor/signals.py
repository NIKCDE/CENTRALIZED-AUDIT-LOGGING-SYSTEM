from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .services import AuditService


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditService.log(
        user=user,
        action="LOGIN",
        description="User logged in",
        ip_address=request.META.get('REMOTE_ADDR')
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    AuditService.log(
        user=user,
        action="LOGOUT",
        description="User logged out",
        ip_address=request.META.get('REMOTE_ADDR')
    )