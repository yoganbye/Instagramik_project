from django.conf.urls import url
from django.urls import path, reverse_lazy
from . import views, auth_views
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)#вьхи аутентификации

"""
Вспомогательный Юрл? Передаём в основной url
"""

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),#url можно добавлять с помощью url или path; IndexView.as_view() - для связи с классом вьюхи

    path('feed/', views.FeedView.as_view(), name='feed'),#as_view - использовать класс как метод

    path('posts/create/', views.CreatePostView.as_view(), name='post_create'),

    path('posts/<int:post_id>/', views.PostView.as_view(), name='post_detail'),#Чтобы передать данные указываем в ссылке через регулярку, что нужно

    path('posts/<int:post_id>/edit/', views.EditePostView.as_view(), name='post_edit'),#добавляем к адресу поста edit, тогда есть возможность редактировать

    path('posts/<int:post_id>/delete/', views.DeletePostView.as_view(), name='post_delete'),#<int:post_id> - аналог предыдущей регулярки
    
    path('posts/<int:post_id>/delete_success/', TemplateView.as_view(
        template_name = 'core/delete_success.html'), name='delete-post-success'),#url вьюхи успешного удаления

    path('posts/<int:post_id>/like/', views.LikePostView.as_view(), name='like_post'),

    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('registration/', auth_views.SignView.as_view(), name='registr'),

    path('logout/', auth_views.logout_view, name='logout'),

    path('profile/<int:user_id>/', auth_views.ProfileView.as_view(), name='profile'),

    path('password_reset/', PasswordResetView.as_view(
        success_url=reverse_lazy('password_reset_done'),
        template_name='my_auth/password_reset.html'
    ), name="password_reset"),
    path('password_reset/done', PasswordResetDoneView.as_view(

        template_name='my_auth/password_reset_done.html'
    ), name="password_reset_done"),

    path('password-reset/<str:uidb64>/<slug:token>', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),

    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]