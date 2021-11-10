from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import make_me_author

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('upgrade/', make_me_author, name='make_me_author'),
]
