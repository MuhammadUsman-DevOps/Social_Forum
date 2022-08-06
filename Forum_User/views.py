from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from Forum_User.models import Post, ContentPost, Comment, Votes, UserProfile


def account_overview(request, username):
    user = ""
    likes = 0
    dislikes = 0
    posts = ""
    try:
        user = UserProfile.objects.get(user__username=username)
        # ToDo: Get All Upvotes & Downvotes on user's posts
    except Exception as e:
        print("Exception in account overview: ",e)
        return HttpResponse("Something went wrong!")
    context = {
        "user": user,
    }
    return render(request, template_name="account/overview.html", context=context)


def account_details(request, username):
    try:
        user = UserProfile.objects.get(user__username=username)
        # ToDo: Get All Upvotes & Downvotes on user's posts
    except Exception as e:
        print("Exception in account overview: ",e)
        return HttpResponse("Something went wrong!")
    context = {
        "user": user,
    }
    return render(request, template_name="account/user_details.html", context=context)


def account_settings(request, username):
    try:
        user = UserProfile.objects.get(user__username=username)
        # ToDo: Get All Upvotes & Downvotes on user's posts
    except Exception as e:
        print("Exception in account overview: ",e)
        return HttpResponse("Something went wrong!")
    context = {
        "user": user,
    }
    return render(request, template_name="account/settings.html", context=context)


def upload_post(request):
    user = UserProfile.objects.get(user=request.user)
    post_media = None
    if request.method == "POST":
        text_content = request.POST.get('text_content', None)
        post_media = request.FILES.get('post_media')

        post = Post.objects.create(user=user)
        content_post = None;
        post.save()
        if post_media is not None:
            content_post = ContentPost.objects.create(post=post, text_content=text_content, post_media=post_media)
            content_post.save()
        else:
            content_post = ContentPost.objects.create(post=post, text_content=text_content)
            content_post.save()

    context = {'post': content_post}
    return render(request, template_name="forum/post_section.html", context=context)


def add_comment(request):
    user = UserProfile.objects.get(user=request.user)
    post = request.GET.get('post')
    content = request.GET.get('content')
    post_obj = Post.objects.get(id=post)

    comment = Comment.objects.create(post=post_obj, content=content, comment_by=user)
    comment.save()

    context = {'comment': comment}
    response = {'success': True, 'html': render(request, 'forum/comment_section.html', context=context)}
    return render(request, 'forum/comment_section.html', context=context)


def add_vote(request):
    user = UserProfile.objects.get(user=request.user)
    post = request.GET.get('post')
    vote_type = request.GET.get('vote')
    post_obj = Post.objects.get(id=post)

    try:
        vote = Votes.objects.get(post=post_obj, vote_by=user)
    except:
        vote = None

    if vote is not None:
        if vote_type == '0':
            vote.upvote = False
            vote.downvote = True
            vote.save()
        else:
            vote.upvote = True
            vote.downvote = False
            vote.save()
    else:
        if vote_type == "0":
            vote = Votes.objects.create(post=post_obj, vote_by=user, downvote=True, upvote=False)
            vote.save()
        else:
            vote = Votes.objects.create(post=post_obj, vote_by=user, downvote=False, upvote=True)
            vote.save()

    response = {'success': True, 'upvote': post_obj.get_upvotes(), 'downvote': post_obj.get_downvotes()}
    return JsonResponse(response)
