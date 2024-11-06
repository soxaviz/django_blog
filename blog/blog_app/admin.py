from django.contrib import admin
from .models import Category, HomeSlider, FAQ, Post, PostGallery


class PostGalleryInline(admin.StackedInline):
    model = PostGallery
    min_num = 1
    max_num = 3


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_gallery_images']
    inlines = [PostGalleryInline]


admin.site.register([Category, HomeSlider, FAQ])
admin.site.register(Post, PostAdmin)
