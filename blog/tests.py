from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


from .models import Post


class BlogTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create(
			username='test-user',
			password='harrypotter'
			)
		self.post = Post.objects.create(
			title = 'A good title',
			author = self.user,
			body = 'A nice body'
			)
	def test_string_representation(self):
		post = Post(title = 'A simple title')
		self.assertEqual(str(post), post.title)

	def test_post_content(self):
		self.assertEqual(f'{self.post.title}', 'A good title')
		self.assertEqual(f'{self.post.body}', 'A nice body')
		self.assertEqual(f'{self.post.author}', 'test-user')

	def test_post_list_view(self):
		resp = self.client.get(reverse('home'))
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'A nice body')
		self.assertTemplateUsed(resp, 'home.html')

	def test_post_detail_view(self):
		response = self.client.get('/post/1/')
		no_response = self.client.get('/post/100/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(no_response.status_code, 404)
		self.assertContains(response,'A good title')
		self.assertTemplateUsed(response, 'post_detail.html')

	def test_get_absolute_url(self):
		self.assertEqual(self.post.get_absolute_url(), '/post/1/')

	def test_post_creatview(self):
		response = self.client.post(reverse('post_new'),{
			'title': 'New title',
			'author': self.user,
			'body': 'A new body'
			})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'New title')
		self.assertContains(response, 'A new body')
	def test_post_updateview(self):
		response = self.client.post(reverse('post_edit', args='1'),{
			'title': 'edit title',
			'body': 'A edit body'
			})
		self.assertEqual(response.status_code, 302)

	def test_post_deleteview(self):
		response = self.client.get(reverse('post_delete', args='1'))
		self.assertEqual(response.status_code, 200)