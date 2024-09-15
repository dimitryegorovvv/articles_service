from django.urls import path, include
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_article/', views.create_article_page, name='create_article_page'),
    path('create_article_submit/', views.create_article, name='create_article'),
    path('save_text/', views.save_text, name='save_text'),
    path('article/<int:article_id>/', views.article, name='article'),
    path('send_comment/<int:article_id>/', views.send_comment, name='send_comment'),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('publish_article/<int:article_id>/', views.publish_article, name='publish_article'),
    path('del_article/<int:article_id>/', views.del_article, name='del_article'),
    path('edit_article/<int:article_id>/', views.edit_article, name='edit_article'),
]
