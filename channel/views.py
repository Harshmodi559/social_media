# from pickle import NONE
# from turtle import pos
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
# from sklearn.cluster import linkage_tree
# from pyrsistent import l
# from matplotlib.backend_bases import LocationEvent
# from pyrsistent import l
from .models import Post, Profile,FollowersCount,LikePost
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from itertools import chain

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required(login_url='signin')
def index(request):
    # print(request.user.username)
    obj=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=obj)
    # user_profile=Profile.objects.all()
    
    user_following_list = []
    feed = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    # print(type(user_following))  queryset
    for users in user_following:
        user_following_list.append(users.user)
    user_following_list.append(request.user)


    for user in user_following_list:
        feed_lists=Post.objects.filter(user=user)
        feed.append(feed_lists)
    
    feed_list=list(chain(*feed))    ### import chain

    ########## now for user suggestion
    all_users = Profile.objects.all()
    # print(all_users)
    followers=FollowersCount.objects.filter(follower=request.user.username)
    # print(followers)
    list_all_users=[]
    list_all_followers=[]
    for i in all_users:
        list_all_users.append(i.user.username)
    # print(list_all_users)

    for j in followers:
        list_all_followers.append(j.user)
    # print(list_all_followers)

    user_suggestion_list=[]   ## which are not followed will be displayed
    for i in list_all_users:
        if i not in list_all_followers:
            user_suggestion_list.append(i)

   ## removing self user
    user_self=request.user.username   
    user_suggestion_list.remove(user_self)

    print(user_suggestion_list)
    import random
    random.shuffle(user_suggestion_list)
   ### now to find all user_sugg_list profiles

    username_profile_list=[]
    for i in user_suggestion_list:
        ids=User.objects.get(username=i)
        profile=Profile.objects.filter(id_user=ids.id).first()
        username_profile_list.append(profile)
    print(username_profile_list)

    # suggestions_username_profile_list = list(chain(*username_profile_list))
    suggestions_username_profile_list = list(username_profile_list)
    return render(request,'index.html',{'user_profile':user_profile,'posts':feed_list,'suggestions_username_profile_list': suggestions_username_profile_list})

def signup(request):
    if(request.method=='POST'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email Already Exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login=auth.authenticate(username=username, password=password) ## imp.
                auth.login(request,user_login)  ## imp.

                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,"Password not matched")
            return redirect('signup')


    else:
        return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request,'signin.html')

@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    if(request.method=='POST'):
        image = user_profile.profileimg
        bio = request.POST['bio']
        location = request.POST['location']
        if request.FILES.get('image')==None:
            user_profile.profileimg=image
        else:
            image=request.FILES.get('image')
            user_profile.profileimg=image
        user_profile.bio=bio
        user_profile.location=location
        user_profile.save()
        
        return redirect('settings')
    # else:
    return render(request,'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def follow(request):
    if(request.method=='POST'):
        follower=request.POST['follower']
        user=request.POST['user']  ### username
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
    
        else:
            # print("followed")
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save() 

    return redirect('/')


@login_required(login_url='signin')
def like_post(request,id):
    post_id=id
    post_like_user=request.user.username
    post=Post.objects.get(id=post_id)

    already_liked=LikePost.objects.filter(post_id=post_id,username=post_like_user).first()
  
    if(already_liked != None):
        already_liked.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')
    else:
        new_user_liked=LikePost.objects.create(post_id=post_id,username=post_like_user,owner=post.user)
        new_user_liked.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        
        return redirect('/')

# @login_required(login_url='signin')
def profile(request,id):
    user_object=User.objects.get(username=id)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=id) ## total posts of user
    user_post_length = len(user_posts)
    follower=request.user.username


    follower = request.user.username
    user = id

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=id)) ## imp.
    user_following = len(FollowersCount.objects.filter(follower=id))  ## imp.

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request,'profile.html',context)

@login_required(login_url='signin')
def delete_post(request,id):
    currently_loggedin_user=request.user.username
    # print(currently_loggedin_user)
    post_obj=Post.objects.get(id=id)
    if(post_obj.user==currently_loggedin_user):
        # print('deleted successfully ')
        post_obj.delete()
        # post_obj.save()   not to used this when deleting
    return redirect('/')


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if(request.method=='POST'):
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        
        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

