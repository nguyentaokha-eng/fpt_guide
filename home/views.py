from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction, models
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import (
    Member, Experience, Lecturer, Review,
    COMPATIBILITY_CHOICES, PRESSURE_CHOICES, SUITABLE_FOR_CHOICES, OUTSTANDING_TRAITS,
    Place, Restaurant, Comment, CommentImage,
    LivingPlace, LivingComment, LivingCommentImage,
)

# Seed giảng viên (gọi khi cần)
LECTURERS_SEED = [
    {'code': 'xuatnt', 'name': 'XUATNT', 'department': 'CÔNG NGHỆ THÔNG TIN', 'subjects': ['SSA101']},
    {'code': 'tring2', 'name': 'TRING2', 'department': 'CÔNG NGHỆ THÔNG TIN', 'subjects': ['CSD201', 'CSI101', 'IAP301', 'REL301M']},
    {'code': 'annv35', 'name': 'ANNV35', 'department': 'CÔNG NGHỆ THÔNG TIN', 'subjects': ['ANM322', 'ANR401']},
    {'code': 'thott', 'name': 'ThoTT', 'department': 'NGOẠI NGỮ', 'subjects': ['ECR301']},
    {'code': 'trangnt', 'name': 'TrangNT', 'department': 'NGOẠI NGỮ', 'subjects': ['ENG303']},
    {'code': 'nhungdt', 'name': 'NhungDT', 'department': 'TIẾNG TRUNG', 'subjects': ['CHN113']},
    {'code': 'thuannt12', 'name': 'ThuanNT12', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'hunghn10', 'name': 'HungHN10', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'nghiabv5', 'name': 'NghiaBV5', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'ngapt', 'name': 'NgaPT', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'truongdq', 'name': 'TruongDQ', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'dungdtt23', 'name': 'DungDTT23', 'department': 'Nhạc cụ truyền thống', 'subjects': ['DTR103']},
    {'code': 'quynhtnp', 'name': 'QuynhTNP', 'department': 'Nhạc cụ truyền thống', 'subjects': ['DTB103']},
    {'code': 'maycc', 'name': 'MayCC', 'department': 'TIẾNG ANH', 'subjects': ['ENT403', 'ENT503']},
    {'code': 'juosea.mm.delmundo', 'name': 'Juosea.MM.DelMundo', 'department': 'TIẾNG ANH', 'subjects': ['ENT403', 'ENT503']},
    {'code': 'lilibeth', 'name': 'Lilibeth', 'department': 'TIẾNG ANH', 'subjects': ['ENT403', 'ENT503']},
    {'code': 'hera ballbero', 'name': 'Hera Ballbero', 'department': 'TIẾNG ANH', 'subjects': ['ENT403', 'ENT503', 'Top Notch']},
    {'code': 'trammc', 'name': 'trammc', 'department': 'TIẾNG TRUNG', 'subjects': ['CHN113']},
    {'code': 'taihx', 'name': 'TAIHX', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'namtp3', 'name': 'namtp3', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'donglb', 'name': 'DongLB', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'thainp', 'name': 'THAINP', 'department': 'THỂ DỤC THỂ THAO', 'subjects': ['VOV114', 'VOV124', 'VOV134']},
    {'code': 'marrygalebo', 'name': 'MarryGaleBO', 'department': 'TIẾNG ANH', 'subjects': ['ENT403', 'ENT503']},
    {'code': 'tramdt7', 'name': 'TramDT7', 'department': 'MARKETING', 'subjects': ['BRA301']},
    {'code': 'hangdtt57', 'name': 'HangDTT57', 'department': 'MARKETING', 'subjects': ['MKT309m']},
    {'code': 'lienbtb2', 'name': 'LienBTB2', 'department': 'MARKETING', 'subjects': ['LAW102']},

]


def ensure_lecturers():
    for item in LECTURERS_SEED:
        Lecturer.objects.get_or_create(
            code=item['code'],
            defaults={
                'name': item['name'],
                'department': item['department'],
                'campus': 'ĐÀ NẴNG',
                'subjects_json': item['subjects'],
            },
        )


def get_lecturer_stats(reviews):
    """Tính thống kê tổng hợp từ danh sách review (dùng cho phần trên trang giảng viên)."""
    from collections import Counter
    n = len(reviews)
    if n == 0:
        return {
            'review_count': 0,
            'avg_score': 0,
            'distribution_fit': {i: 0 for i in range(1, 6)},
            'distribution_pressure': {i: 0 for i in range(1, 6)},
            'top_traits': [],
            'suitable_for_most': None,
            'pressure_most': None,
        }
    # Phân phối mức độ hợp (1-5)
    fit_counts = Counter(r.rating_fit for r in reviews)
    distribution_fit = {i: fit_counts.get(i, 0) for i in range(1, 6)}
    # Phân phối áp lực (1-5)
    pressure_counts = Counter(r.rating_pressure for r in reviews)
    distribution_pressure = {i: pressure_counts.get(i, 0) for i in range(1, 6)}
    # Top 3 đặc điểm nổi bật (từ tags)
    all_tags = []
    for r in reviews:
        if isinstance(r.tags, list):
            all_tags.extend(r.tags)
    trait_counts = Counter(all_tags)
    top_traits = [{'key': k, 'label': next((lb for kb, lb in OUTSTANDING_TRAITS if kb == k), k), 'count': c}
                  for k, c in trait_counts.most_common(10)]
    # Phù hợp nhất với (suitable_for)
    suitable_counts = Counter(r.suitable_for for r in reviews if r.suitable_for)
    suitable_most = suitable_counts.most_common(1)
    suitable_for_most = suitable_most[0] if suitable_most else None
    # Áp lực nhiều nhất (mode của rating_pressure)
    pressure_most_value = pressure_counts.most_common(1)[0][0] if pressure_counts else None
    pressure_most_label = next((lb for v, lb in PRESSURE_CHOICES if v == pressure_most_value), '') if pressure_most_value else ''
    avg_score = sum(r.score for r in reviews) / n
    return {
        'review_count': n,
        'avg_score': round(avg_score, 1),
        'distribution_fit': distribution_fit,
        'distribution_pressure': distribution_pressure,
        'top_traits': top_traits,
        'suitable_for_most': suitable_for_most,
        'suitable_for_percent': round(100 * suitable_most[0][1] / n, 0) if suitable_most else 0,
        'pressure_most': pressure_most_label,
        'compatibility_labels': dict(COMPATIBILITY_CHOICES),
        'pressure_labels': dict(PRESSURE_CHOICES),
        'suitable_labels': dict(SUITABLE_FOR_CHOICES),
    }


def home(request):
    members = Member.objects.all()
    return render(request, 'home.html', {'members': members})


def experience_detail(request, slug):
    member = get_object_or_404(Member, slug=slug)
    experiences = Experience.objects.filter(member=member)
    return render(request, 'experience.html', {
        'member': member,
        'experiences': experiences,
    })


def explore(request):
    return render(request, 'explore.html')


def afford(request):
    return render(request, 'afford.html')


def families(request):
    return render(request, 'families.html')


# SAU (mới)
def rate_lecture(request):
    ensure_lecturers()
    from django.db.models import Count
    lecturers = Lecturer.objects.annotate(review_count=Count('reviews')).order_by('name')
    # Tạo dict: code -> review_count để truyền vào template
    review_counts = {l.code: l.review_count for l in lecturers}
    return render(request, 'rate_lecture.html', {
        'lecturers': lecturers,
        'review_counts': review_counts,
    })


def lecturer_detail(request, lecturer_id):
    ensure_lecturers()
    lecturer = Lecturer.objects.filter(code=lecturer_id).first()
    if not lecturer:
        return redirect('rate_lecture')

    if request.method == 'POST':
        # Lưu đánh giá mới
        try:
            rating_fit = int(request.POST.get('rating_fit', 3))
            rating_pressure = int(request.POST.get('rating_pressure', 3))
            score = int(request.POST.get('score', 5))
            if score < 0:
                score = 0
            if score > 10:
                score = 10
            subject_studied = (request.POST.get('subject_studied') or '').strip()
            suitable_for = (request.POST.get('suitable_for') or '').strip()
            tags = request.POST.getlist('outstanding_traits')
            if len(tags) > 3:
                tags = tags[:3]
            comment = (request.POST.get('comment') or '').strip()
            is_anonymous = request.POST.get('is_anonymous') == '1'
            reviewer_name = (request.POST.get('reviewer_name') or '').strip() if not is_anonymous else ''
            Review.objects.create(
                lecturer=lecturer,
                rating_fit=rating_fit,
                rating_pressure=rating_pressure,
                score=score,
                subject_studied=subject_studied,
                suitable_for=suitable_for,
                tags=tags,
                comment=comment,
                is_anonymous=is_anonymous,
                reviewer_name=reviewer_name or None,
            )
        except (ValueError, TypeError):
            pass
        return redirect('lecturer_detail', lecturer_id=lecturer_id)

    reviews = list(lecturer.reviews.all().order_by('-created_at'))
    stats = get_lecturer_stats(reviews)
    n = stats['review_count']
    fit_bars = [(v, lbl, stats['distribution_fit'].get(v, 0)) for v, lbl in COMPATIBILITY_CHOICES]
    suitable_label = None
    if stats.get('suitable_for_most'):
        skey = stats['suitable_for_most'][0]
        suitable_label = dict(SUITABLE_FOR_CHOICES).get(skey, skey)

    lecturer_data = {
        'id': lecturer.id,
        'code': lecturer.code,
        'name': lecturer.name,
        'department': lecturer.department,
        'status': lecturer.campus,
        'subjects': lecturer.subjects_json or [],
    }
    return render(request, 'lecturer_detail.html', {
        'lecturer': lecturer_data,
        'lecturer_id': lecturer_id,
        'reviews': reviews,
        'stats': stats,
        'fit_bars': fit_bars,
        'suitable_label': suitable_label,
        'compatibility_choices': COMPATIBILITY_CHOICES,
        'pressure_choices': PRESSURE_CHOICES,
        'suitable_for_choices': SUITABLE_FOR_CHOICES,
        'outstanding_traits': OUTSTANDING_TRAITS,
    })

#trang mo rong cua afford


def Afford_living(request):
    return render(request, 'Afford_living.html')

def Afford_job(request):
    return render(request, 'Afford_job.html')
def Afford_food(request):
    query = request.GET.get('q', '')  # nội dung user gõ

    foods = []

    if query:
        q = query.lower()

        if 'rẻ' in q or '30k' in q:
            foods.append('Bánh mì – ~20k')
            foods.append('Cơm sinh viên – ~25k')

        if 'cay' in q:
            foods.append('Mì cay – ~30k')

        if not foods:
            foods.append('Chưa có gợi ý phù hợp 😢')

    return render(request, 'Afford_food.html', {
        'query': query,
        'foods': foods
    })

#Afford_food cmt và rating
####

def recalculate_place_ratings(place):
    """Recalculate rating averages for a place based on all its comments."""
    comments = place.comments.all()
    total = comments.count()
    
    if total == 0:
        place.price_avg = 0
        place.quality_avg = 0
        place.service_avg = 0
        place.space_avg = 0
        place.overall_score = 0
        place.total_reviews = 0
    else:
        price_sum = sum(c.price for c in comments)
        quality_sum = sum(c.quality for c in comments)
        service_sum = sum(c.service for c in comments)
        space_sum = sum(c.space for c in comments)
        
        place.price_avg = round(price_sum / total, 1)
        place.quality_avg = round(quality_sum / total, 1)
        place.service_avg = round(service_sum / total, 1)
        place.space_avg = round(space_sum / total, 1)
        place.total_reviews = total
        
        # Overall score is average of the 4 category averages
        place.overall_score = round(
            (place.price_avg + place.quality_avg + place.service_avg + place.space_avg) / 4, 1
        )
    
    place.save()


def post_comment(request, place_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    # Validate rating values (must be 0-10)
    try:
        price = int(request.POST.get("price", 0))
        quality = int(request.POST.get("quality", 0))
        service = int(request.POST.get("service", 0))
        space = int(request.POST.get("space", 0))
        
        if not (0 <= price <= 10 and 0 <= quality <= 10 and 0 <= service <= 10 and 0 <= space <= 10):
            return JsonResponse({"error": "Ratings must be between 0-10"}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid rating values"}, status=400)
    
    content = request.POST.get("content", "").strip()
    display_name = request.POST.get("display_name", "").strip() or "Ẩn danh"
    is_anonymous = request.POST.get("is_anonymous") == "true"
    
    # Get or create place
    place, created = Place.objects.get_or_create(
        id=place_id, 
        defaults={'name': f'Place {place_id}'}
    )
    
    # Get user if authenticated
    user = request.user if request.user.is_authenticated else None
    
    with transaction.atomic():
        # Check if user already has a comment for this place
        existing_comment = None
        if user:
            existing_comment = Comment.objects.filter(place=place, user=user).first()
        
        if existing_comment:
            # Update existing comment
            existing_comment.price = price
            existing_comment.quality = quality
            existing_comment.service = service
            existing_comment.space = space
            existing_comment.content = content
            existing_comment.display_name = display_name
            existing_comment.is_anonymous = is_anonymous
            existing_comment.save()
            comment = existing_comment
        else:
            # Create new comment
            comment = Comment.objects.create(
                place=place,
                user=user,
                display_name=display_name,
                is_anonymous=is_anonymous,
                content=content,
                price=price,
                quality=quality,
                service=service,
                space=space,
            )
        
        # Handle image uploads
        for img in request.FILES.getlist("images"):
            CommentImage.objects.create(comment=comment, image=img)
        
        # Recalculate ratings
        recalculate_place_ratings(place)
    
    return JsonResponse({"success": True, "comment_id": comment.id})


def get_comments(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        return JsonResponse([], safe=False)
    
    data = []

    for c in place.comments.all().order_by("-created_at"):
        data.append({
            "id": c.id,
            "user_id": c.user_id if c.user else None,
            "user": "Ẩn danh" if c.is_anonymous else c.display_name,
            "content": c.content,
            "ratings": {
                "price": c.price,
                "quality": c.quality,
                "service": c.service,
                "space": c.space,
            },
            "images": [img.image.url for img in c.images.all()],
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        })

    return JsonResponse(data, safe=False)


def get_restaurants(request):
    """API endpoint to get all restaurants with their ratings."""
    restaurants = Restaurant.objects.all()
    
    data = []
    for r in restaurants:
        data.append({
            "id": r.id,
            "name": r.name,
            "price_avg": r.price_avg,
            "quality_avg": r.quality_avg,
            "service_avg": r.service_avg,
            "space_avg": r.space_avg,
            "overall_score": r.overall_score,
            "total_reviews": r.total_reviews,
        })
    
    return JsonResponse(data, safe=False)


def get_places(request):
    """API endpoint to get all places with their ratings and comments count."""
    places = Place.objects.all()
    
    data = []
    for p in places:
        data.append({
            "id": p.id,
            "name": p.name,
            "price_avg": p.price_avg,
            "quality_avg": p.quality_avg,
            "service_avg": p.service_avg,
            "space_avg": p.space_avg,
            "overall_score": p.overall_score,
            "total_reviews": p.total_reviews,
            "comments_count": p.comments.count(),
            "restaurant_id": p.restaurant_id if p.restaurant else None,
        })
    
    return JsonResponse(data, safe=False)


def student_life(request):
    return render(request, 'student_life.html')


def curriculum(request):
    return render(request, 'curriculum.html')


# ========== AFFORD LIVING COMMENT SYSTEM ==========

def recalculate_living_place_ratings(living_place):
    """Recalculate rating averages for a living place based on all its comments."""
    comments = living_place.comments.all()
    total = comments.count()
    
    if total == 0:
        living_place.price_avg = 0
        living_place.location_avg = 0
        living_place.amenity_avg = 0
        living_place.security_avg = 0
        living_place.overall_score = 0
        living_place.total_reviews = 0
    else:
        price_sum = sum(c.price for c in comments)
        location_sum = sum(c.location for c in comments)
        amenity_sum = sum(c.amenity for c in comments)
        security_sum = sum(c.security for c in comments)
        
        living_place.price_avg = round(price_sum / total, 1)
        living_place.location_avg = round(location_sum / total, 1)
        living_place.amenity_avg = round(amenity_sum / total, 1)
        living_place.security_avg = round(security_sum / total, 1)
        living_place.total_reviews = total
        
        # Overall score is average of the 4 category averages
        living_place.overall_score = round(
            (living_place.price_avg + living_place.location_avg + 
             living_place.amenity_avg + living_place.security_avg) / 4, 1
        )
    
    living_place.save()


def post_living_comment(request, living_place_id):
    """Post a comment for a living place."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    # Validate rating values (must be 0-10)
    try:
        price = int(request.POST.get("price", 0))
        location = int(request.POST.get("location", 0))
        amenity = int(request.POST.get("amenity", 0))
        security = int(request.POST.get("security", 0))
        
        if not (0 <= price <= 10 and 0 <= location <= 10 and 0 <= amenity <= 10 and 0 <= security <= 10):
            return JsonResponse({"error": "Ratings must be between 0-10"}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid rating values"}, status=400)
    
    content = request.POST.get("content", "").strip()
    display_name = request.POST.get("display_name", "").strip() or "Ẩn danh"
    is_anonymous = request.POST.get("is_anonymous") == "true"
    
    # Get or create living place
    living_place, created = LivingPlace.objects.get_or_create(
        id=living_place_id, 
        defaults={'name': f'Living Place {living_place_id}'}
    )
    
    # Get user if authenticated
    user = request.user if request.user.is_authenticated else None
    
    with transaction.atomic():
        # Check if user already has a comment for this place
        existing_comment = None
        if user:
            existing_comment = LivingComment.objects.filter(living_place=living_place, user=user).first()
        
        if existing_comment:
            # Update existing comment
            existing_comment.price = price
            existing_comment.location = location
            existing_comment.amenity = amenity
            existing_comment.security = security
            existing_comment.content = content
            existing_comment.display_name = display_name
            existing_comment.is_anonymous = is_anonymous
            existing_comment.save()
            comment = existing_comment
        else:
            # Create new comment
            comment = LivingComment.objects.create(
                living_place=living_place,
                user=user,
                display_name=display_name,
                is_anonymous=is_anonymous,
                content=content,
                price=price,
                location=location,
                amenity=amenity,
                security=security,
            )
        
        # Handle image uploads
        for img in request.FILES.getlist("images"):
            LivingCommentImage.objects.create(comment=comment, image=img)
        
        # Recalculate ratings
        recalculate_living_place_ratings(living_place)
    
    return JsonResponse({"success": True, "comment_id": comment.id})


def get_living_comments(request, living_place_id):
    """Get all comments for a living place."""
    try:
        living_place = LivingPlace.objects.get(id=living_place_id)
    except LivingPlace.DoesNotExist:
        return JsonResponse([], safe=False)
    
    data = []

    for c in living_place.comments.all().order_by("-created_at"):
        data.append({
            "id": c.id,
            "user_id": c.user_id if c.user else None,
            "user": "Ẩn danh" if c.is_anonymous else c.display_name,
            "content": c.content,
            "ratings": {
                "price": c.price,
                "location": c.location,
                "amenity": c.amenity,
                "security": c.security,
            },
            "images": [img.image.url for img in c.images.all()],
            "created_at": c.created_at.isoformat(),
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        })

    return JsonResponse(data, safe=False)


def get_living_places(request):
    """API endpoint to get all living places with their ratings."""
    living_places = LivingPlace.objects.all()
    
    data = []
    for lp in living_places:
        data.append({
            "id": lp.id,
            "name": lp.name,
            "address": lp.address,
            "distance": lp.distance,
            "price_avg": lp.price_avg,
            "location_avg": lp.location_avg,
            "amenity_avg": lp.amenity_avg,
            "security_avg": lp.security_avg,
            "overall_score": lp.overall_score,
            "total_reviews": lp.total_reviews,
        })
    
    return JsonResponse(data, safe=False)