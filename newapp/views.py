import logging
import datetime
import pytz

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.shortcuts import redirect

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm

logger = logging.getLogger(__name__)


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-timeCreation']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()
        context['posts_quantity'] = Post.objects.count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_of_post'] = list(Post.objects.filter(id=self.get_object().id).values('categories__name'))
        context['categories'] = Category.objects.all()
        return context


class CategorySubscribe(DetailView):
    model = Category
    template_name = 'post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscribers = Category.objects.filter(id=self.get_object().id).values('subscribers')
        for s in list(subscribers):
            for key, value in s.items():
                if self.request.user.pk == value:
                    context['is_subscribe'] = True
                else:
                    context['is_subscribe'] = False
        return context


@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    print('add user ----------')
    send_mail(
        subject=f'{category}',
        message=f'Вы «{request.user}» подписались на обновления категории: «{category}».',
        from_email='dr.knyaz-nerub@yandex.ru',
        recipient_list=['sphalerite.4@gmail.com', ],
    )
    return redirect('/news')


@login_required
def unsubscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    print('remove user ----------')
    send_mail(
        subject=f'{category}',
        message=f'Вы «{request.user}» отписались от обновлений категории: «{category}».',
        from_email='dr.knyaz-nerub@yandex.ru',
        recipient_list=['sphalerite.4@gmail.com', ],
    )
    return redirect('/news')


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAdd(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post_add.html'
    permission_required = ('newapp.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Getting the beginning of the current day
        current_date = datetime.datetime.now()
        start_of_day = datetime.datetime(current_date.year, current_date.month, current_date.day)
        start_of_day = start_of_day.replace(tzinfo=pytz.UTC)

        posts_of_current_day = list(Post.objects.filter(
                timeCreation__gt=start_of_day).filter(author__user=self.request.user.pk))

        # Restricting the publications of the author
        if len(posts_of_current_day) == 3:
            context['is_exceeded_limit_publications'] = True
        return context


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('newapp.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('newapp.delete_post',)
