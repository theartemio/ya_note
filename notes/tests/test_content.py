from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note

User = get_user_model()


NOTE_NUMBER = 2

class TestHomePage(TestCase):
    
    
    @classmethod
    def setUpTestData(cls):
        
        cls.user_one = User.objects.create(username='UserOne')
        cls.user_two = User.objects.create(username='UserTwo')
        all_users_notes = []
        for user, multiplier in ((cls.user_one, 1), (cls.user_two, 2)):
            user_notes = [
                Note(title=f'Заголовок {index}',
                     text='Текст.', slug=f'slug_{index}',
                     author=cls.user_one)
                for index in range(multiplier*NOTE_NUMBER, 2*multiplier*NOTE_NUMBER)
                ]
            all_users_notes += user_notes
        Note.objects.bulk_create(all_users_notes)

    def test_user_note_list(self):
        self.client.force_login(self.user_one)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        authors = [note.author for note in object_list]
        for author in authors:
            with self.subTest(author=author):
                self.assertEqual(author, self.user_one)