from .models import AuditLog


class AuditService:

    @staticmethod
    def log(
        user=None,
        action="READ",
        model_name=None,
        object_id=None,
        description="",
        ip_address=None,
        user_agent=None,
        status="SUCCESS",
        metadata=None
    ):
        try:
            AuditLog.objects.create(
                user=user,
                action=action,
                model_name=model_name,
                object_id=object_id,
                description=description,
                ip_address=ip_address,
                user_agent=user_agent,
                status=status,
                metadata=metadata
            )
        except Exception as e:
            print("Audit Service Error:", e)