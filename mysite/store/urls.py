from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', PostListGreatAPIView.as_view(), name='post_list'),
    path('users/', UserProfileViewSet.as_view({'get': 'list'}), name='users_list'),
    path('follow/', FollowListCreateAPIView.as_view(), name='follow_list'),
    path('post_like/', PostLikeListAPIView.as_view(), name='post_like_list'),
    path('comment/', CommentViewSet.as_view({'get': 'list'}), name='comment_list'),
    path('comment_like/', CommentLikeListApiVIew.as_view(), name='comment_like_list'),
    path('story/', StoryListCreateAPIView.as_view(),name='story_list'),
    path('saved/', SavedListApiVIew.as_view(), name='saved_list'),
    path('save_item/', SaveItemViewSet.as_view({'get': 'list'}), name='save_item_list')
]
