from .models import Post
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchPost(request):
    

    skills = Skill.objects.filter(name__icontains = text)
    posts = Post.objects.distinct().filter(Q(name__icontains = text) | 
                                    Q(short_intro__icontains = text)
                                    |Q(skill__in=skills))
    return profiles, text

def paginationProfile(request,profiles,results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 1)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) +  2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)


    return custom_range,profiles