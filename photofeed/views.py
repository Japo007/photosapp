from django.shortcuts import (HttpResponse, render, redirect,
                        get_object_or_404, reverse, get_list_or_404, Http404)
from . models import Image
from .forms import ImageForm
import sys


def profile(request):
    #user = get_object_or_404(User, username=username)
    images = Image.objects.all()
    print(sys.getsizeof(images))
    user = request.user
    print(user)
    print("HelloWorld")
    if request.method == "POST":
        print("POST IMAGE")
        form = ImageForm(request.POST, request.FILES)
        print(form.errors)        
        if form.is_valid():
            print("form is valid and saving")
            print(form)
            form.save()
            return redirect('/photofeed/profile')
        else:
            print("form is not valid")
    else:
        form = ImageForm()
    """
    # if the profile is private and logged in user is not same as the user being viewed,
    # show 404 error
    if user.profile.private and request.user.username != user.username:
        raise Http404
 
    # if the profile is not private and logged in user is not same as the user being viewed,
    # then only show public snippets of the user
    elif not user.profile.private and request.user.username != user.username:
        snippet_list = user.snippet_set.filter(exposure='public')
        user.profile.views += 1
        user.profile.save()
 
    # logged in user is same as the user being viewed
    # show everything
    else:
        snippet_list = user.snippet_set.all()
 
    snippets = paginate_result(request, snippet_list, 5)
    """
    return render(request, 'userdata/profile.html',
                  {'user' : user, 'form' : form, 'images': images} )
"""
def image_list(request):
    images = Image.objects.all()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = ImageForm()
    return render(request, 'album/photo_list.html', {'form': form, 'photos': photos})
"""