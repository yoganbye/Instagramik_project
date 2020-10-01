from django.db import models
from django.contrib.auth.models import User#auth содержит все модели пользователей
from django.utils import timezone#Модуль для работы со временем в Джанго


# Модель представление таблиц БД в виде классов; все модели наследуются от models.Model
# В БД создастся таблица по имени класса

def avatar_path(instance, filename):#Объект кому создаем аватар и имя файла\
    return 'user_{0}/avatars/{1}'.format(instance.user.id, filename)#путь куда картинка возвращается; пишем как строку; instance - равносильно селф класса Профиль

def posts_path(instance, filename):
    return 'user_{0}/posts/{1}'.format(instance.author.id, filename)


class Profile(models.Model):
    """
    Модель профиля
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile'#Релейтед для того чтобы обращаться к кнокретной модели через вью
    )#Отношение пользователя к БД?! Один пользователь - имеет одну БД  
    #Параметр on_delete удаляет какие либо данные связанные с пользователем
    # Cascade - все данные удалятся
    birth_date = models.DateField('Date of birth', null=True, blank=True)#Дата рождения; null - поле может быть нулевым; blank - поле может быть пустым
    about = models.TextField('About', max_length=500, blank=True)#Инфа о пользователе
    avatar = models.ImageField(upload_to=avatar_path, default=None)#Фото профиля; upload_to - папка куда будет сохраняться фотоl; default - если ничего не укахали то None
    friends = models.ManyToManyField(User, related_name='friends', blank=True)#Друзья профиля; между профилем и юзером

    def __str__(self):
        return str(self.user.username)


class Post(models.Model):
    """
    Пост пользователя с картинкой
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)#ForeignKey - указаывает отношение что у поста может быть один автор, но у автора несколько постов
    description = models.TextField(max_length=1000, blank=True)#Описание
    image = models.ImageField(upload_to=posts_path)#Картинка; папки создаются в корне
    likes = models.ManyToManyField(User, related_name='users_likes', blank=True)#ManyToMany - ещё один тип отношений; между постом и юзером
    date_pub = models.DateTimeField(default=timezone.now)#Дата публикации
    date_edit = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Author {}, date {}'.format(self.author.username, self.date_pub) 

    @property
    def get_likes(self):#не используется
        return self.likes.count()



class Comment(models.Model):  
    author = models.ForeignKey(User, on_delete=models.CASCADE)       
    text = models.TextField(max_length=700)
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Author {}: {}'.format(self.author.username, self.text[:10] + "...")                                     