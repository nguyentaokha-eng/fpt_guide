# ============================================================
# TẠO FILE MỚI: fpt_guide/ip_filter.py
# Các hàm tiện ích để lọc từ và quản lý IP
# ============================================================

import re
from home.models import BlockedIP, IPViolationLog, BAD_WORDS  # ĐÚNG

# Ngưỡng vi phạm trước khi tự động block
AUTO_BLOCK_THRESHOLD = 3


def get_client_ip(request):
    """Lấy IP từ request (đã được middleware gắn vào request.client_ip)."""
    return getattr(request, 'client_ip', None) or _extract_ip(request)


def _extract_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def check_and_filter_text(text, ip_address, page='unknown'):
    """
    Kiểm tra và lọc từ khiếm nhã trong text.

    Returns:
        dict:
            - filtered_text: text đã thay thế từ xấu bằng ***
            - has_violation: True nếu có vi phạm
            - bad_words_found: danh sách từ xấu tìm thấy
            - auto_blocked: True nếu IP bị auto-block
            - violation_count: tổng số lần vi phạm của IP này
    """
    if not text:
        return {
            'filtered_text': text,
            'has_violation': False,
            'bad_words_found': [],
            'auto_blocked': False,
            'violation_count': 0,
        }

    filtered = text
    found = []

    for word in BAD_WORDS:
        # Escape ký tự đặc biệt trong regex
        escaped = re.escape(word)
        pattern = re.compile(escaped, re.IGNORECASE)
        if pattern.search(filtered):
            found.append(word)
            # Thay bằng *** (giữ nguyên độ dài)
            filtered = pattern.sub(lambda m: '⬛' * len(m.group()), filtered)

    has_violation = len(found) > 0
    auto_blocked = False
    violation_count = 0

    if has_violation:
        # Ghi log vi phạm
        log = IPViolationLog.objects.create(
            ip_address=ip_address,
            page=page,
            original_text=text[:1000],   # giới hạn 1000 ký tự
            filtered_text=filtered[:1000],
            bad_words_found=found,
        )

        # Đếm tổng vi phạm của IP này
        violation_count = IPViolationLog.objects.filter(
            ip_address=ip_address
        ).count()

        # Kiểm tra ngưỡng auto-block
        if violation_count >= AUTO_BLOCK_THRESHOLD:
            blocked, created = BlockedIP.objects.get_or_create(
                ip_address=ip_address,
                defaults={
                    'reason': f'Tự động block: {violation_count} lần vi phạm. '
                              f'Từ vi phạm: {", ".join(found[:5])}',
                    'blocked_by': 'auto',
                    'violation_count': violation_count,
                }
            )
            if not created:
                # Cập nhật violation_count nếu đã bị block trước đó
                blocked.violation_count = violation_count
                blocked.reason = (f'Tự động block: {violation_count} lần vi phạm. '
                                  f'Từ vi phạm gần nhất: {", ".join(found[:5])}')
                blocked.save()

            auto_blocked = True
            log.auto_blocked = True
            log.save()

    return {
        'filtered_text': filtered,
        'has_violation': has_violation,
        'bad_words_found': found,
        'auto_blocked': auto_blocked,
        'violation_count': violation_count,
    }


def is_ip_blocked(ip_address):
    """Kiểm tra nhanh IP có bị block không."""
    return BlockedIP.objects.filter(ip_address=ip_address).exists()


def block_ip_manually(ip_address, reason='Admin block thủ công'):
    """Block IP thủ công bởi admin."""
    blocked, created = BlockedIP.objects.get_or_create(
        ip_address=ip_address,
        defaults={
            'reason': reason,
            'blocked_by': 'admin',
        }
    )
    if not created:
        blocked.reason = reason
        blocked.blocked_by = 'admin'
        blocked.save()
    return blocked, created


def unblock_ip(ip_address):
    """Bỏ block một IP."""
    deleted, _ = BlockedIP.objects.filter(ip_address=ip_address).delete()
    return deleted > 0