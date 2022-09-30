from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import re
from django.shortcuts import render, redirect

from Forum_User.models import Post, ContentPost, Comment, Votes, UserProfile, HashTags


@login_required
def account_overview(request, username):
    print(username)
    _user = UserProfile.objects.get(user__username=username)
    _posts = Post.objects.filter(user=_user)
    posts = []
    upvotes = 0
    downvotes = 0
    for post in _posts:
        posts.append(post.contentpost_set.first())
        upvotes += post.get_upvotes()
        downvotes += post.get_downvotes()

    context = {'user': _user, 'posts': posts, 'upvotes': upvotes, 'downvotes': downvotes}
    return render(request, template_name="account/overview.html", context=context)


@login_required
def account_details(request, username):
    _user = UserProfile.objects.get(user__username=username)
    _posts = Post.objects.filter(user=_user)

    upvotes = 0
    downvotes = 0
    for post in _posts:
        upvotes += post.get_upvotes()
        downvotes += post.get_downvotes()
    context = {'user': _user, 'upvotes': upvotes, 'downvotes': downvotes}
    return render(request, template_name="account/user_details.html", context=context)


@login_required
def account_settings(request, username):
    _user = UserProfile.objects.get(user__username=username)
    _posts = Post.objects.filter(user=_user)

    upvotes = 0
    downvotes = 0
    for post in _posts:
        upvotes += post.get_upvotes()
        downvotes += post.get_downvotes()
    context = {'user': _user, 'upvotes': upvotes, 'downvotes': downvotes}
    return render(request, template_name="account/settings.html", context=context)


@login_required
def edit_profile(request):
    avatar = None
    _user = UserProfile.objects.get(user=request.user)
    print(_user.avatar)

    if request.method == "POST":
        print('inside post ')
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        country = request.POST['country']

        _user.user.first_name = first_name
        _user.user.last_name = last_name
        _user.country = country

        try:
            avatar = request.FILES['avatar']
        except:
            avatar = None
        # avatar = request.POST.get('avatar', None)
        if avatar is not None:
            _user.avatar = avatar

        _user.save()
        _user.user.save()

    print(_user.avatar)

    context = {'user': _user}
    # return render(request, template_name="account/settings.html", context=context)
    return redirect(request.META['HTTP_REFERER'])


@login_required
def upload_post(request):
    user = UserProfile.objects.get(user=request.user)
    post_media = None
    print(user)

    if request.method == "POST":
        text_content = request.POST.get('text_content', None)

        hast_tags = ''
        tag_list = extract_hash_tags(text_content)
        try:
            if tag_list:
                hast_tags = ','.join(tag_list)
        except:
            hast_tags = ''

        post_media = request.FILES.get('post_media')
        save_hash_tags(tag_list)

        post = Post.objects.create(user=user, hashtags=hast_tags)
        content_post = None
        post.save()
        if post_media is not None:
            content_post = ContentPost.objects.create(post=post, text_content=text_content, post_media=post_media)
            content_post.save()
        else:
            content_post = ContentPost.objects.create(post=post, text_content=text_content)
            content_post.save()

    context = {'post': content_post}
    return render(request, template_name="forum/post_section.html", context=context)


def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))


def save_hash_tags(tags):
    for t in tags:
        if not HashTags.objects.filter(tag=t).exists():
            HashTags.objects.create(tag=t)

@login_required
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


@login_required
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


def search_by_tag(request):
    tag = request.GET.get('tag')
    _posts = ContentPost.objects.all()
    posts = []
    for post in _posts:
        if post.post.hashtags is not None:
            if re.search(tag, post.post.hashtags, re.IGNORECASE):
                posts.append(post)

    context = {'posts': posts}
    # return posts
    return render(request, template_name="forum/search_post.html", context=context)
