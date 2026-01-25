from django.shortcuts import render, get_object_or_404
from .models import Member, Experience

def home(request):
    members = Member.objects.all()
    return render(request, 'home.html', {
        'members': members
    })

def experience_detail(request, slug):
    member = get_object_or_404(Member, slug=slug)
    experiences = Experience.objects.filter(member=member)
    return render(request, 'experience.html', {
        'member': member,
        'experiences': experiences
    })
def explore(request):
    return render(request, 'explore.html')

def afford(request):
    return render(request, 'afford.html')

def families(request):
    return render(request, 'families.html')



