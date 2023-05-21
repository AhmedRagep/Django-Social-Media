from django.shortcuts import redirect, render
from django.urls import reverse

from core.models import FollowersCount, Post
from .forms import SignupForm, UserForm
from django.contrib.auth import authenticate, login
from .models import Profile
from django.contrib.auth.models import User
# Create your views here.

def signup(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # للتسجيل بالاسم والباسورد اللذي تم اضافتهم
            user = authenticate(username=username,password=password)
            login(request,user)
            ##############################
            return redirect('/accounts/profile')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form':form})

# -------------------

def profile(request, pk):
    # profile = Profile.objects.get(user=user)
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    followers = request.user.username
    user = pk

    if FollowersCount.objects.filter(followers=followers, user=user).first():
        button_text = 'UnFollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(followers=pk))

    context = {
         'user_object' : user_object,
         'user_profile' : user_profile,
         'user_posts' : user_posts,
         'user_post_length' : user_post_length,
         'button_text' : button_text,
         'user_followers' : user_followers,
         'user_following' : user_following,
    }
    return render(request, 'accounts/profile.html', context)

# ------------------
# def profile_edit(request):
#     profile = Profile.objects.get(user=request.user)

#     if request.method=='POST':
#         userform = UserForm(request.POST,instance=request.user)
#         profileform = ProfileForm(request.POST, request.FILES, instance=profile)
#         if userform.is_valid() and profileform.is_valid():
#             userform.save()
#             myprofile = profileform.save(commit=False)
#             myprofile.user = request.user
#             myprofile.save()
#             return redirect(reverse('accounts:profile'))
#     else:
#         userform = UserForm(instance=request.user)
#         profileform = ProfileForm(instance=profile)

#     return render(request, 'accounts/profile_edit.html', {'userform':userform, 'profileform':profileform})