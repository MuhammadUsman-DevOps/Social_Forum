from django.contrib import admin

from Forum_User.models import UserProfile, Post, ContentPost, Comment

admin.site.index_title = "Social Forum Administration"
admin.site.site_title = "Social Forum Administration"
admin.site.site_header = "Social Forum Administration"


class PostAdminModel(admin.ModelAdmin):
    list_display = ['title', 'likes', 'dislikes', 'created', 'user']
    prepopulated_fields = {"slug": ("title",)}


class ContentPostAdminModel(admin.ModelAdmin):
    list_display = ['text_content', 'post_media', 'created', 'post']


class CommentAdminModel(admin.ModelAdmin):
    list_display = ['content', 'created', 'comment_by', 'post']


admin.site.register(UserProfile)
admin.site.register(Post, PostAdminModel)
admin.site.register(ContentPost, ContentPostAdminModel)
admin.site.register(Comment, CommentAdminModel)
