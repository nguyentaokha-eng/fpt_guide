from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experience/<slug:slug>/', views.experience_detail, name='experience'),
    path('explore/', views.explore, name='explore'),
    path('afford/', views.afford, name='afford'),
    path('families/', views.families, name='families'),
    path('rate-lecture/', views.rate_lecture, name='rate_lecture'),
    path('rate/', views.rate_lecture, name='rate_lecture_alias'),
    path('lecturer/<str:lecturer_id>/', views.lecturer_detail, name='lecturer_detail'),
    path('student_life/', views.student_life, name='student_life'),
    path('curriculum/', views.curriculum, name='curriculum'),
    #url mo rong cua afford
    path('Afford/food/', views.Afford_food, name='Afford_food'),
    path('Afford/living/', views.Afford_living, name='Afford_living'),
    path('afford/job/', views.Afford_job, name='Afford_job'),
    path('comment/<int:place_id>/', views.post_comment, name='post_comment'),
    path('comment/list/<int:place_id>/', views.get_comments, name='get_comments'),
    path('api/restaurants/', views.get_restaurants, name='get_restaurants'),
    path('api/places/', views.get_places, name='get_places'),
    # Afford Living API
    path('api/living-places/', views.get_living_places, name='get_living_places'),
    path('living-comment/<int:living_place_id>/', views.post_living_comment, name='post_living_comment'),
    path('living-comment/list/<int:living_place_id>/', views.get_living_comments, name='get_living_comments'),
]

# ============================================================
# THÊM VÀO urls.py HIỆN TẠI (thêm vào list urlpatterns)
# ============================================================

# Thêm 2 dòng này vào cuối urlpatterns:

#   path('admin/ip-manager/', views.admin_ip_manager, name='admin_ip_manager'),
#   path('admin/api/block-ip/', views.api_block_ip, name='api_block_ip'),


# ============================================================
# File urls.py hoàn chỉnh sau khi thêm:
# ============================================================

urlpatterns = [
    path('', views.home, name='home'),
    path('experience/<slug:slug>/', views.experience_detail, name='experience'),
    path('explore/', views.explore, name='explore'),
    path('afford/', views.afford, name='afford'),
    path('families/', views.families, name='families'),
    path('rate-lecture/', views.rate_lecture, name='rate_lecture'),
    path('rate/', views.rate_lecture, name='rate_lecture_alias'),
    path('lecturer/<str:lecturer_id>/', views.lecturer_detail, name='lecturer_detail'),
    path('student_life/', views.student_life, name='student_life'),
    path('curriculum/', views.curriculum, name='curriculum'),

    # Afford sub-pages
    path('Afford/food/', views.Afford_food, name='Afford_food'),
    path('Afford/living/', views.Afford_living, name='Afford_living'),
    path('afford/job/', views.Afford_job, name='Afford_job'),

    # Food comment API
    path('comment/<int:place_id>/', views.post_comment, name='post_comment'),
    path('comment/list/<int:place_id>/', views.get_comments, name='get_comments'),
    path('api/restaurants/', views.get_restaurants, name='get_restaurants'),
    path('api/places/', views.get_places, name='get_places'),

    # Living comment API
    path('api/living-places/', views.get_living_places, name='get_living_places'),
    path('living-comment/<int:living_place_id>/', views.post_living_comment, name='post_living_comment'),
    path('living-comment/list/<int:living_place_id>/', views.get_living_comments, name='get_living_comments'),

    # ── MỚI: Admin IP Manager ───────────────────────────────
    path('admin/ip-manager/', views.admin_ip_manager, name='admin_ip_manager'),
    path('admin/api/block-ip/', views.api_block_ip, name='api_block_ip'),
]