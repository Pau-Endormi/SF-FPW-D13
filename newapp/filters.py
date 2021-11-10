from django_filters import FilterSet

from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        #  fields = ('author__user', 'title', 'timeCreation')
        fields = {
            'author__user__username': ['icontains'],
            'title': ['icontains'],
            'timeCreation': ['lt'],
        }
