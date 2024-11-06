from django.urls import path
from . import views

# http://127.0.0.1:8000/
urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('categories/<int:pk>', views.category_posts_page, name='category'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post_view, name='create'),
    path('posts/<int:pk>/delete/', views.delete_article, name='delete'),
    path('posts/<int:pk>/edit/', views.PostUpdate.as_view(), name='edit'),
    path('search/', views.search, name='search'),
    path('vote/<int:post_id>/<str:action>/', views.add_vote, name='add_vote')
]


# 1.  Разработать простое веб-приложение на фреймворке
# Django, которое позволит пользователям регистрироваться, авторизовываться
# и вести список личных задач (to-do list). Приложение должно предоставлять
# возможности для создания, просмотра, редактирования и удаления задач.
# Также необходима функциональность поиска среди своих задач.
# Технические требования
# 1.  Бэкенд
# •  Язык программирования: Python 3.8+
# •  Веб-фреймворк: Django 3.2+
# •  База данных: SQLite в разработке
# •  Аутентификация и авторизация: использовать стандартные механизмы Django
# 2.  Фронтенд
# •  HTML, CSS (Bootstrap или любой другой CSS фреймворк)
# 3.  Функциональные требования
# •  Регистрация/авторизация пользователей
# •  Создание, просмотр, редактирование и удаление задач
# •  Возможность отмечать задачи выполненными
# •  Поиск по задачам