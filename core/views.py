from itertools import chain
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from accounts.models import Profile
from .models import Post, LikePost, FollowersCount
from django.contrib.auth.models import User, auth

# Create your views here.
@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    # ------------followers-------------------
    # list following
    user_following_list = []
    # list feeds
    feed = []

    # جلب اليوزر المستخدم حاليا والمتابع للشخص
    user_following = FollowersCount.objects.filter(followers=request.user.username)

    for users in user_following:
        # اضافة اليوزر المستخدم حاليا والمتابع في قائمه
        user_following_list.append(users.user)

    for usernames in user_following_list:
        # فتلرة البوستات بالاسم اللذي جلبناه 
        fees_lists = Post.objects.filter(user=usernames)
        # اضافته في قائمه 
        feed.append(fees_lists)
    # عمل القائمه التي ستعرض بدل كل البوستات
    fees_list = list(chain(*feed))
    # ------------end followers-------------------

    # -----------users suggestions starts-------------
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        # جلب اليوزر المتابع حاليا
        user_list = User.objects.get(username=user.user)
        # اضافتهم في هذه الليسته
        user_following_all.append(user_list)
    # هاتلي اليوزر اللي مش متابع
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    # هاتلي اسم اليوز
    current_user = User.objects.filter(username=request.user.username)
    # هاتلي اليوزر اللي مش متابع ومش مسجل دلوقتي
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    # ابحث
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        # هاتلي الايدي بتاع اليوزر اللي مش مسجل ومش متابع وضيفه في الليست
        username_profile.append(users.id)

    for ids in username_profile:
        # هاتلي البروفيل اللي الايدي بتاعه يساوي الايدي بتاع اليوزر
        profile_lists = Profile.objects.filter(id=ids)
        # ضفلي البروفايل اللي جبناه في الليست
        username_profile_list.append(profile_lists)
    # اعرضلي البروفيلات دي    
    suggestions_username_profile_list = list(chain(*username_profile_list))
    # -----------end users suggestions starts-------------

    return render(request, 'index.html', {'profile' : profile, 'posts' : fees_list, 'suggestions_username_profile_list' : suggestions_username_profile_list[:4]})

@login_required
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        img = request.FILES.get('image')
        description = request.POST['description']

        new_post = Post.objects.create(user=user, img=img, description=description)
        new_post.save()
        return redirect('/')
    
    else:
        return redirect('/')

def search(request):
    # جلب اليوزر الحالي
    user_object = User.objects.get(username=request.user.username)
    # جلب اليوزر الموجود في البروفايل بنفس الاسم المسجل
    user_profile = Profile.objects.get(user=user_object)
    # لو كتب معلومات
    if request.method == 'POST':
        # جلب الاسم اللذي كتب في صفحة العرض
        username = request.POST['username']
        # هاتلي اليوزر نام اللذي يحتوي علي الاسم اللذ جلب من صفحة العرض
        username_object = User.objects.filter(username__icontains=username)

        # انشاء قائمتين فارغتين
        username_profile = []
        username_profile_list = []

        for users in username_object:
            # هات الايدي بتاع الاسم اللي بحثت عنه
            username_profile.append(users.id)

        for ids in username_profile:
            # ضفلي الليست دي واضف بداخلها الايدي اللي جبته
            username_profile_list.append(Profile.objects.filter(id=ids))
        # اعملي ده كله ليست
        username_profile_list = list(chain(*username_profile_list))


    return render(request, 'search.html', {'user_profile' : user_profile, 'username_profile_list' : username_profile_list})

@login_required
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_like = post.no_of_like+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_like = post.no_of_like-1
        post.save()
        return redirect('/')

@login_required
def follow(request):
    if request.method == 'POST':
        followers = request.POST['followers']
        user = request.POST['user']

        if FollowersCount.objects.filter(followers=followers, user=user).first():
            delete_follower = FollowersCount.objects.get(followers=followers, user=user)
            delete_follower.delete()
            return redirect('/accounts/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(followers=followers, user=user)
            new_follower.save()
            return redirect('/accounts/profile/'+user)
    else:
        return redirect('/')

# def profile(request, pk):
#     user_object = User.objects.get(username=pk)
#     user_profile = Profile.objects.get(user=user_object)
#     user_posts = Post.objects.filter(user=pk)
#     user_post_length = len(user_posts)
#     context = {
#         'user_object' : user_object,
#         'user_profile' : user_profile,
#         'user_posts' : user_posts,
#         'user_post_length' : user_post_length,
#     }
#     return render(request, 'profile.html', context)

@login_required
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('img') == None:
            img = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = img
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('img') != None:
            img = request.FILES.get('img')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = img
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect(reverse('core:settings'))


    return render(request, 'setting.html', {'user_profile' : user_profile})

