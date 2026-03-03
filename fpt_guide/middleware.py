class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self._get_client_ip(request)
        request.client_ip = ip

        try:
            from home.models import BlockedIP  # ← đã sửa đúng
            if BlockedIP.objects.filter(ip_address=ip).exists():
                from django.http import JsonResponse, HttpResponse
                if request.path.startswith('/comment/') or \
                   request.path.startswith('/living-comment/') or \
                   request.path.startswith('/api/'):
                    return JsonResponse(
                        {"error": "Bạn đã bị chặn khỏi hệ thống do vi phạm nội quy."},
                        status=403
                    )
                if request.method == 'POST':
                    return HttpResponse(
                        "<script>alert('Bạn đã bị chặn do vi phạm nội quy!'); history.back();</script>",
                        status=403
                    )
        except Exception:
            pass

        response = self.get_response(request)
        return response

    @staticmethod
    def _get_client_ip(request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')