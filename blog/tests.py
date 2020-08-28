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