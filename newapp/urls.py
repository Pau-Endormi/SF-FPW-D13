from django.urls import path

from .views import PostsList, PostDetail, PostSearch, PostAdd, PostEdit, PostDelete, CategorySubscribe
from .views import subscribe_category, unsubscribe_category


urlpatterns = [
    path('', PostsList.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearch.as_view(), name='post_search'),
    path('add', PostAdd.as_view(), name='post_add'),
    path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('category/<int:pk>', CategorySubscribe.as_view(), name='post_category'),
    path('category/<int:pk>/subscribe', subscribe_category, name='subscribe_category'),
    path('category/<int:pk>/unsubscribe', unsubscribe_category, name='unsubscribe_category'),
]
