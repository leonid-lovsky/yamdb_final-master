from api import views
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('categories', views.CategoryViewSet, basename='categories')
v1_router.register('genres', views.GenreViewSet, basename='genres')
v1_router.register('titles', views.TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments'
)
v1_router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
