from auditor.services import AuditService


class AuditMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        try:
            if request.path.startswith('/admin'):
                return response

            user = request.user if request.user.is_authenticated else None

            model_name, object_id = self.extract_object_info(request)

            AuditService.log(
                user=user,
                action=self.get_action(request, response),
                model_name=model_name,
                object_id=object_id,
                description=f"{request.method} {request.path}",
                ip_address=self.get_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT'),
                status="SUCCESS" if response.status_code < 400 else "FAILED",
                metadata=self.get_safe_body(request)
            )

        except Exception as e:
            print("Audit Logging Error:", e)

        return response

    def extract_object_info(self, request):
        """
        Try to extract object_id from URL kwargs
        Example: /api/orders/5/
        """
        try:
            resolver = request.resolver_match
            if resolver and 'pk' in resolver.kwargs:
                return resolver.view_name, resolver.kwargs.get('pk')
        except:
            pass
        return None, None

    def get_safe_body(self, request):
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                data = request.body.decode('utf-8')
                return {"body": data[:500]}  # limit size
            except:
                return None
        return None

    def get_action(self, request, response):
        if response.status_code >= 400:
            return "FAILED"

        return {
            "POST": "CREATE",
            "PUT": "UPDATE",
            "PATCH": "UPDATE",
            "DELETE": "DELETE",
        }.get(request.method, "READ")

    def get_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')