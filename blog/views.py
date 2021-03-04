from django.shortcuts import render
from django.http import HttpResponse
from.models import Blogpost

# Create your views here.
def index(request):
    allpost = Blogpost.objects.all()
    print(allpost)

    return render(request, "blog/index.html", {"allpost": allpost})

def blogpost(request, bid):
    post = Blogpost.objects.filter(post_id=bid)[0]
    print(post)

    return render(request, "blog/blogpost.html", {"post": post})

