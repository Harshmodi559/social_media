# from pickle import NONE
# from turtle import pos
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
# from matplotlib.backend_bases import LocationEvent
# from pyrsistent import l
from .models import Post, Profile,FollowersCount,LikePost
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def index(request):
    # print(request.user.username)
    obj=User.objects.get(username=request.user.username)
    # user_profile=Profile.objects.filter(user=obj)
    user_profile=Profile.objects.all()
    posts=Post.objects.all()


    return render(request,'index.html',{'user_profile':user_profile,'posts':posts})

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
    user_profile=Profile.objects.filter(id_user=request.user.id)
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
            print("followed")
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
    if(already_liked is not None):
        already_liked.delete()
        already_liked.save()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')
    else:
        new_user_liked=LikePost.objects.create(post_id=post_id,username=post_like_user)
        new_user_liked.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
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


