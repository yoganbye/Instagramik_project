from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):#устанавливает начальные параметры, которые необходимы
        self.client = Client()
        self.user = User(
            username='test', first_name='test', 
            last_name='test', email='test@test.com'
        )
        self.user.save()

        self.user2 = User(
            username='test2', first_name='test2', 
            last_name='test2', email='test2@test2.com'
        )
        self.user2.save()

        Profile.objects.create(user=self.user)#можно пользователя создавать таким способом
        Profile.objects.create(user=self.user2)

    
    def test_check_user_profile(self):
        user = User.objects.first()
        profile = Profile.objects.first()

        self.assertEqual(user, profile.user)

    def test_profile_view(self):
        user = User.objects.first()
        response = self.client.get(
            reverse('profile', args=(user.id,))
        )
        self.assertEqual(200, response.status_code)
        
