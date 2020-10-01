from django.shortcuts import render, redirect, get_object_or_404#ф-я рендеер аналог лоадера, redirect - 
from django.http import HttpResponse, Http404#404 - позволяет явно вызвать ошибку 404
from .models import Post, Profile, Comment
from django.db.models import Sum, Count 
from django.template import loader
from .form import PostForm, CommentForm
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView, DetailView# ListView позволяет отдавать с помощью гет запроса список объектов из базы
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from .form import LoginForm, SignUpForm
from .exceptions import PermissionDenied


class IndexView(ListView):
    model = Post#имя модели
    template_name = 'core/index.html'#Имя шаблона
    context_object_name = 'posts'#имя контекста - то что в html

    def get_queryset(self):#логика получения данных
        return Post.objects.annotate(like_nums=Count('likes')).order_by('-like_nums')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title' : 'Главная страница',
        })
        return context


# def index(request):#Вьюха. Запрос.Главная страница чаще обозн-я index
#     '''
#     Вьюха для main страницы
#     '''
#     post_queryset = Post.objects.annotate(like_nums=Count('likes')).order_by('-like_nums')#[:3]#множество объектов
#     #Ф-я annotate создает дополнительное поле к полям объектов в БД order_by - сортирует; (-) - от большего к меньшему
#     output = ['id:{}|description:{}|likes\n:{}'.format(post.id, post.description, post.like_nums) for post in post_queryset]
#     # template = loader.get_template('core/index.html')#loader - используется для рендера штмл шаблона
#     context = {
#         'posts' : post_queryset,
#     }#данные на шаблон; context - некий словарь
#     # return HttpResponse(template.render(context))#можем так же в рендер заключать данные (контекст)
#     return render(request, "core/index.html", context)


class FeedView(View):
    template_name = 'core/feed.html'

    def get(self, request, *args, **kwargs):#метод/вьюха будет вызывать когда будет запрошен метод get
        if request.user.is_authenticated:
            posts = Post.objects.filter(
                author__in=request.user.user_profile.friends.all()
            ).order_by('-date_pub')[:10]# order_by - фильтр
            context = {
                'posts' : posts,
            }#данные которые мы передает в шаблон
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)


# def feed(request):
#     '''
#     Вьюха для страницы постов друзей
#     '''
#     feed_queryset = Post.objects.filter(author__in=request.user.user_profile.friends.all())
#     output = ['Author:{}|id:{}|description:{} '.format(post.author, post.id, post.description) for post in feed_queryset]
#     return HttpResponse(output)


class CreatePostView(CreateView):
    form_class = PostForm
    template_name = 'core/post_create.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):        
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            context['form'] = self.form_class
            context['post_was_created'] = True
            return render(request, self.template_name, context)
        else:
            context['post_was_created'] = False
            context['form'] = form
            return render(request, self.template_name, context)


# def post_create(request):
#     '''
#     Вьюха для создания публикации
#     '''
#     form = PostForm()
#     template_name = 'core/post_create.html'
#     context = {'form' : form}

#     if request.method == "GET":
#         return render(request, template_name, context)
#     elif request.method == "POST":
#         form = PostForm(request.POST, request.FILES)

#         if form.is_valid():#проверяет форму на ограничения указанные в моделях и выдаст Tru or False
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()логина
#         else:
#             context['post_was_created'] = False
#             context['form'] = form
#             return render(request, template_name, context)

    # response = 'Создание поста'
    # return HttpResponse(response)


class PostView(DetailView):
    model = Post
    comment_form = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_detail.html'

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comments'] = Comment.objects.filter(
            in_post__id=post_id
        ).order_by('-date_publish')#in_post__pk; in_post - поле; __pk ссылается на id/pk
        context['comment_form'] = None
        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form
        return self.render_to_response(context)

    def get_queryset(self):#логика получения данных
        return Post.objects.annotate(like_nums=Count('likes'))

    @method_decorator(login_required)#предоставляет доступ только авторизованым пользователям
    def post(self,request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.in_post = post
            comment.save()
            return render(request, self.template_name, context={
                'comment_form': self.comment_form,
                'post': post,
                'comments': post.comment_set.order_by('-date_publish')
            })
        else:
             return render(request, self.template_name, context={
                'comment_form': form,
                'post': post,
                'comments': post.comment_set.order_by('-date_publish')
            })


# def post_detail(request, post_id):
#     '''
#     Вьюха для детальной информации о публикации
#     '''
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         raise Http404("Post does not exist")
#     # response = 'Author:{}| id:{}|description:{}'.format(post.author, post.id, post.description)
#     context = {
#         'post' : post
#     }
#     # return HttpResponse(response)
#     return render(request, "core/post_detail.html", context)


class EditePostView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_edit.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):#переопределяем dispatch, 
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You are not author of this post')
        return super(EditePostView, self).dispatch(request, *args, **kwargs)#вызываем dispatch дефолтный

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('post_detail', args=(post_id, ))


# def post_edit(request, post_id):
#     '''
#     Вьюха для редактироpostвания публикации
#     '''
#     post = Post.objects.get(id=post_id)
#     response = 'Редактирование поста Author:{}| id:{}|description:{}'.format(post.author, post.id, post.description)
#     return HttpResponse(response)


class DeletePostView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_delete.html'

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('delete-post-success', args=(post_id, ))


# def post_delete(request, post_id):
#     '''
#     Вьюха для удаления публикации
#     '''
#     post = Post.objects.get(id=post_id)
#     response = 'Удаление поста поста Author:{}| id:{}|description:{}'.format(post.author, post.id, post.description)
#     return HttpResponse(response)


class LikePostView(View):
    def get(self, request, post_id, *args, **kwargs):
        return redirect(reverse('post_detail', args=(post_id, )))

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            like = post.likes.get(pk=request.user.id)
            post.likes.remove(like)
        else:
            post.likes.add(request.user)
            post.save()

        return redirect(request.META.get('HTTP_REFERER'), request)


# def like_post(request, post_id):
#     '''
#     Вьюха для обработки лайков
#     '''
#     post = Post.objects.get(id=post_id)
#     if request.user in post.likes.all():#проверяем лайкнул ли уже юзер наш пост
#         like = post.likes.get(pk=request.user.id)#из тех чуваков кто лайкнул запрашиваем пользователя
#         post.likes.remove(like)#и удаляем пользователя из лайков
#     else:
#         post.likes.add(request.user)
#         post.save()#после редакта сохраняем изменения
#     # response = 'Лайкнуть пост Author:{}| id:{}|description:{}'.format(post.author, post.id, post.description)
#     # return HttpResponse(response)
#     return redirect(request.META.get('HTTP_REFERER'), request)#redirect - что-то типо перенаправления


# class LoginView(LoginView):
#     template_name = 'my_auth/login.html'
#     form_class = LoginForm

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse('index'), request)
#             else:
#                 context = {
#                     'form' :form
#                 }
#                 return render(request, self.template_name, context)
#         else:
#             context = {
#                 'form' : form
#             }
#             return render(request, self.template_name, context)


# class SignView(View):
#     template_name = 'my_auth/signup.html'
#     registration_form =  SignUpForm

#     def get(self, request, *args, **kwargs):
#         context = {
#             'form' : self.registration_form
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         user_form = self.registration_form(data=request.POST)
#         registered = False
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.email = user_form.cleaned_data['email']
#             user.save
#             registered = True
#             return render(request, self.template_name, {'registered' : registered})
#         else:
#             return render(
#                 request, self.template_name, {
#                     'form' : user_form, 'registered' : registered
#                 }
#             )


# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect(reverse('index'))
