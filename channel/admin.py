from django.contrib import admin
from .models import Profile, Post,FollowersCount,LikePost,Comment
# Register your models here.


# @admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','id_user','bio','profileimg','location')
admin.site.register(Profile,ProfileAdmin)

# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('user','id','image','no_of_likes','created_at','caption')
admin.site.register(Post,PostAdmin)

# @admin.register(FollowersCount)
class FollowerAdmin(admin.ModelAdmin):
    list_display=('follower','user')
admin.site.register(FollowersCount,FollowerAdmin)

# @admin.register(LikePost)
class LikeAdmin(admin.ModelAdmin):
    list_display=('post_id','owner','username','liked_at')
admin.site.register(LikePost,LikeAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display=('user','body','post_idd','profile_image','date_added')
admin.site.register(Comment,CommentsAdmin)