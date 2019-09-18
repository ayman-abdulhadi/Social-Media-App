from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from .forms import ImageCreateForm, CommentForm
from .models import Image, Comment
from actions.utils import create_action
from django.conf import settings
import redis

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "Bookmarked Image", new_image)
            messages.success(request, "Image Added Successfully")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm()
    context = {
        'form'    :   form,
        'section' :   'images',
    }
    return render(request, "images/create.html", context)

# @login_required
# def image_detail(request, id, slug):
#         image = get_object_or_404(Image, id=id, slug=slug)
#         total_views = r.incr('image:{}:view'.format(image.id))
#         # increment image ranking by 1
#         r.zincrby('image_ranking', image.id, 1)
#         context = {
#             'image'       :  image,
#             'section'     :  'images',
#             'total_views' : total_views,
#         }
#         return render(request, "images/detail.html", context)

@login_required
def image_list(request):
    comment = CommentForm()
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        form    = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "Bookmarked Image", new_image)
            messages.success(request, "Image Added Successfully")
            return redirect('images:list')
        else:
            print("Form Not Valid")
        if comment.is_valid():
            id = request.POST.get('image')
            body = request.POST.get('body')
            image = Image.objects.get(id=id)
            image.comments.create(user=request.user, body=body)
            return redirect('images:list')

    else:
        form    = ImageCreateForm()
    images    = Image.objects.all()
    comments  = Comment.objects.all()
    paginator = Paginator(images, 4)
    page      = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, "images/list_ajax.html", {"images":images, "section":"images", "form":form, "CommentForm" : comment,"comments": comments,})
    context = {
        "section"     : "images",
        "images"      : images,
        "comments"    : comments,
        "form"        : form,
        "CommentForm" : comment,
    }
    return render(request, "images/list.html", context)

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action   = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
        except:
            pass
    return JsonResponse({'status':'ok'})

# @ajax_required
# @login_required
# @require_POST
# def image_comment(request):
#     image_id = request.POST.get('id')
#     action   = request.POST.get('action')
#     body     = request.POST.get('body')
#     response = None
#     if image_id and action:
#         try:
#             image = Image.objects.get(id=image_id)
#             if action == 'comment':
#                 image.users_comment.add(request.user)
#                 response = image.comments.create(user=request.user, body=body)
#                 create_action(request.user, "commented on", image)
#         except Exception as e:
#             print(e)
#     return JsonResponse(response)

# @login_required
# def image_ranking(request):
#     image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
#     image_ranking_ids = [int(id) for id in image_ranking]
#     # get most viewed images
#     most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
#     most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
#     return render(request,'images/ranking.html',{'section': 'images','most_viewed': most_viewed})
