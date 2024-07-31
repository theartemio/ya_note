from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author one')
        cls.reader = User.objects.create(username='author two')
        cls.user = User.objects.create(username='testUser')
        cls.note = Note.objects.create(title='Заголовок', 
                                       text='Текст',
                                       slug='slug',
                                       author=cls.author,
                                       )

    def test_home_page(self):
        urls = ('notes:home', 'users:login', 'users:signup', 'users:logout')
        for url in urls:
            
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_list_and_add_pages(self):
        self.client.force_login(self.user)
        for name in ('notes:list',
                     'notes:add',
                     ):
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_detailed_view_editing_and_deleting_notes(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:detail',
                         'notes:edit',
                         'notes:delete',
                         ):
                with self.subTest(user=user, name=name):        
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    # Попробовать тут объединить два теста, используя кортеж
    def test_redirect_for_anonymous_client_note(self):
        login_url = reverse('users:login')
        for name in ('notes:delete',
                     'notes:edit',
                     ):
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_redirect_for_anonymous_client_pages(self):
        login_url = reverse('users:login')
        for name in (
                     'notes:success',
                     'notes:list',
                     ):
            with self.subTest(name=name):
                url = reverse(name)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)