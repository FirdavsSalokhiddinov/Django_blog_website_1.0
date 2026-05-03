from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post
# Create your tests here.

class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret',
        )

        self.post = Post.objects.create(
            title = 'New post',
            body = 'Post body',
            author = self.user,
        )

    def test_string_representation(self):
        post = Post(title='Post title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'New post')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Post body')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post body')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/1000000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'New post')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_create_view(self):
        response = self.client.post(
            reverse('post_new'),
            {
                'title': 'Another post',
                'body': 'Created in a test',
                'author': self.user.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Another post').exists())

    def test_post_update_view(self):
        response = self.client.post(
            reverse('post_edit', args=[self.post.pk]),
            {
                'title': 'Updated post',
                'body': 'Updated body',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated post')
        self.assertEqual(self.post.body, 'Updated body')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
