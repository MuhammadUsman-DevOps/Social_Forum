from django.contrib import admin

from Forum_User.models import UserProfile, Post, ContentPost, Comment, Votes

admin.site.index_title = "Social Forum Administration"
admin.site.site_title = "Social Forum Administration"
admin.site.site_header = "Social Forum Administration"


class PostAdminModel(admin.ModelAdmin):
    list_display = ['id', 'created']
    prepopulated_fields = {"slug": ("title",)}


class ContentPostAdminModel(admin.ModelAdmin):
    list_display = ['text_content', 'post_media', 'created']


class CommentAdminModel(admin.ModelAdmin):
    list_display = ['content', 'created', 'comment_by']


class VoteAdminModel(admin.ModelAdmin):
    list_display = ['upvote', 'downvote', 'created', 'vote_by']


admin.site.register(UserProfile)
admin.site.register(Post, PostAdminModel)
admin.site.register(ContentPost, ContentPostAdminModel)
admin.site.register(Comment, CommentAdminModel)
admin.site.register(Votes, VoteAdminModel)
