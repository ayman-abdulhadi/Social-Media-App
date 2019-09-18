from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
    # path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    # path('comment/', views.image_comment, name='comment'),
    # path('ranking/', views.image_ranking, name='ranking'),
    path('', views.image_list, name='list'),
]
