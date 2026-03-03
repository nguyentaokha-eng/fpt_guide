# ============================================================
# TẠO FILE MỚI: fpt_guide/middleware.py
# ============================================================

class BlockIPMiddleware:
    """
    Middleware tự động chặn request từ IP bị block.
    Thêm vào settings.py:
        MIDDLEWARE = [
            ...
            'frontend.middleware.BlockIPMiddleware',
            ...
        ]
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy IP thực (hỗ trợ proxy/Railway)
        ip = self._get_client_ip(request)
        request.client_ip = ip  # gắn vào request để dùng ở view

        # Kiểm tra IP có bị block không
        # Import ở đây để tránh circular import
        try:
            from .models import BlockedIP
            if BlockedIP.objects.filter(ip_address=ip).exists():
                from django.http import JsonResponse, HttpResponse
                # Nếu là API call → trả JSON
                if request.path.startswith('/comment/') or \
                   request.path.startswith('/living-comment/') or \
                   request.path.startswith('/api/'):
                    return JsonResponse(
                        {"error": "Bạn đã bị chặn khỏi hệ thống do vi phạm nội quy."},
                        status=403
                    )
                # Nếu là POST form bình thường → redirect về trang trước
                if request.method == 'POST':
                    from django.shortcuts import redirect
                    return HttpResponse(
                        "<script>alert('Bạn đã bị chặn do vi phạm nội quy!'); history.back();</script>",
                        status=403
                    )
        except Exception:
            pass  # DB chưa migrate → bỏ qua

        response = self.get_response(request)
        return response

    @staticmethod
    def _get_client_ip(request):
        """Lấy IP thật của client, hỗ trợ proxy/Railway."""
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')