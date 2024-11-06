from django.apps import AppConfig

# main
# 1) main_category
# blog
# 2) blog_category
# cart
# 3) cart_category


class BlogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_app'
