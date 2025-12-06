import unittest
from datetime import datetime
from app import create_app, db
from app.posts.models import Post, PostCategory

class CreatePostTests(unittest.TestCase):
    
    def setUp(self):
        # Використовуємо конфігурацію 'testing'
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post_get_page(self):
        """Тест: Чи завантажується сторінка 'create' (GET)?"""
        response = self.client.get('/post/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn('творення поста'.encode(), response.data) # convert Unicode to bytes

    # def test_create_post_anonymous(self):
    #     """Тест: Чи створюється пост з автором 'Anonymous', якщо ніхто не залогінений?"""
    #     response = self.client.post('/post/create', data={
    #         'title': 'Test Post Anonymous',
    #         'content': 'Some content here.',
    #         'posted': datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
    #         'category': 'tech',
    #         'is_active': True
    #     }, follow_redirects=True)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Пост успішно створено'.encode(), response.data)
        
    #     post = Post.query.filter_by(title='Test Post Anonymous').first()
    #     self.assertIsNotNone(post)
    #     self.assertEqual(post.author, 'Anonymous')

    # def test_create_post_logged_in(self):
    #     """Тест: Чи створюється пост з автором 'testuser', якщо він у сесії?"""
    #     # Імітуємо логін користувача
    #     with self.client.session_transaction() as sess:
    #         sess['username'] = 'testuser'
            
    #     response = self.client.post('/post/create', data={
    #         'title': 'Test Post Logged In',
    #         'content': 'Some content here.',
    #         'posted': datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
    #         'category': 'news',
    #         'is_active': True
    #     }, follow_redirects=True)
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Пост успішно створено'.encode(), response.data)
        
    #     post = Post.query.filter_by(title='Test Post Logged In').first()
    #     self.assertIsNotNone(post)
    #     self.assertEqual(post.author, 'testuser')

    def test_create_post_invalid_data(self):
        """Тест: Чи залишається користувач на сторінці, якщо дані невалідні (немає title)?"""
        response = self.client.post('/post/create', data={
            'title': '', # Невалідні дані
            'content': 'Some content here.',
            'category': 'tech',
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('творення поста'.encode(), response.data)
        self.assertIn('This field is required'.encode(), response.data) # Повідомлення від WTForms