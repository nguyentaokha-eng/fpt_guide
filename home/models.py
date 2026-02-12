from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lecturer(models.Model):
    """Giảng viên - code dùng trong URL (vd: tring2)."""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    campus = models.CharField(max_length=50, default='ĐÀ NẴNG')
    # Các môn giảng dạy (mã môn), VD: ["CSD201", "CSI101"]
    subjects_json = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Chỉ tiêu đánh giá (hình 2, 3)
COMPATIBILITY_CHOICES = [(5, 'Tuyệt vời'), (4, 'Rất hợp'), (3, 'Hợp'), (2, 'Bình thường'), (1, 'Không hợp')]
PRESSURE_CHOICES = [(1, 'Rất dễ tính'), (2, 'Dễ tính'), (3, 'Bình thường'), (4, 'Khó tính'), (5, 'Rất khó tính')]
SUITABLE_FOR_CHOICES = [
    ('team_qua_mon', 'Team Qua Môn'),
    ('san_coc_vang', 'Săn Cóc Vàng'),
    ('cay_cuoc_nhieu', 'Cày Cuốc Nhiều'),
    ('tinh_than_thep', 'Tinh Thần Thép'),
]
OUTSTANDING_TRAITS = [
    ('giang_cuon_de_hieu', 'Giảng cuốn, dễ hiểu'),
    ('chi_doc_slide', 'Chỉ đọc slide'),
    ('tu_boi_la_chinh', 'Tự bơi là chính'),
    ('support_nhiet_tinh', 'Support nhiệt tình'),
    ('vui_tinh_hai_huoc', 'Vui tính, hài hước'),
    ('nghiem_khac_kho_tinh', 'Nghiêm khắc/Khó tính'),
    ('hoi_buon_ngu', 'Hơi buồn ngủ'),
    ('diem_danh_cuc_gat', 'Điểm danh cực gắt'),
    ('nhieu_bai_tap_deadline', 'Nhiều bài tập/Deadline'),
    ('cham_diem_thoang', 'Chấm điểm thoáng'),
    ('cham_diem_kho', 'Chấm điểm khó'),
    ('review_thi_sat_de', 'Review thi sát đề'),
    ('thoai_mai', 'Thoải mái'),
]


class Review(models.Model):
    """Đánh giá của user cho một giảng viên."""
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='reviews')
    # Mức độ hợp với giảng viên (1-5)
    rating_fit = models.IntegerField()
    # Cảm nhận áp lực & độ khó (1-5)
    rating_pressure = models.IntegerField()
    # Điểm số nhận được trên lớp (0-10)
    score = models.IntegerField()
    # Nhận xét chi tiết
    comment = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=True)
    reviewer_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Môn bạn đã học (nhập tự do, VD: CSI101, PRO192)
    subject_studied = models.CharField(max_length=200, blank=True)
    # Ai hợp với giảng viên này
    suitable_for = models.CharField(max_length=50, blank=True)
    # Đặc điểm nổi bật (tối đa 3) - lưu list key trong JSON
    tags = models.JSONField(default=list, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return f"Review {self.id} - {self.lecturer.name}"



# cmt và upload ảnh cho Afford food

class Restaurant(models.Model):
    """Restaurant model for Afford Food with rating statistics."""
    name = models.CharField(max_length=200)
    # Rating statistics (auto-calculated)
    price_avg = models.FloatField(default=0)
    quality_avg = models.FloatField(default=0)
    service_avg = models.FloatField(default=0)
    space_avg = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


# Place model for backward compatibility (links to Restaurant)
class Place(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Comment with ratings for a place."""
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    is_anonymous = models.BooleanField(default=False)
    content = models.TextField()
    
    price = models.IntegerField()
    quality = models.IntegerField()
    service = models.IntegerField()
    space = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('place', 'user')
    
    def __str__(self):
        return f"Comment by {self.display_name or 'Anonymous'} on {self.place.name}"


class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="comment_images/")


# Models for Afford Living (nơi ở)

class LivingPlace(models.Model):
    """Living place model for Afford Living with rating statistics."""
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True)
    distance = models.CharField(max_length=100, blank=True)
    # Rating statistics (auto-calculated)
    price_avg = models.FloatField(default=0)
    location_avg = models.FloatField(default=0)
    amenity_avg = models.FloatField(default=0)
    security_avg = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


class LivingComment(models.Model):
    """Comment with ratings for a living place."""
    living_place = models.ForeignKey(LivingPlace, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    is_anonymous = models.BooleanField(default=False)
    content = models.TextField()
    
    # Ratings for living places
    price = models.IntegerField()
    location = models.IntegerField()
    amenity = models.IntegerField()
    security = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('living_place', 'user')
    
    def __str__(self):
        return f"Comment by {self.display_name or 'Anonymous'} on {self.living_place.name}"


class LivingCommentImage(models.Model):
    comment = models.ForeignKey(LivingComment, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="living_comment_images/")
