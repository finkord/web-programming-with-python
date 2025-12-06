# import unittest
# from app import create_app, db
# from app.posts.models import Post, PostCategory

# class GetPostsTests(unittest.TestCase):
    
#     def setUp(self):
#         self.app = create_app('test')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         self.client = self.app.test_client()

#         # Створюємо тестові пости
#         p1 = Post(title='Active Post', content='...', is_active=True, category='tech')
#         p2 = Post(title='Inactive Post', content='...', is_active=False, category='news')
#         db.session.add_all([p1, p2])
#         db.session.commit()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     def test_get_posts_default(self):
#         """Тест: Чи 'get_posts' за замовчуванням показує ТІЛЬКИ активні пости?"""
#         response = self.client.get('/post/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Active Post', response.data)
#         self.assertNotIn(b'Inactive Post', response.data)

#     def test_get_posts_show_all(self):
#         """Тест: Чи 'get_posts' з ?show_all=true показує ВСІ пости?"""
#         response = self.client.get('/post/?show_all=true')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Active Post', response.data)
#         self.assertIn(b'Inactive Post', response.data)