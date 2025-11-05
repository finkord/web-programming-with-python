import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory

class DetailPostTests(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Створюємо тестові пости
        self.p1 = Post(title='Active Post Detail', content='...', is_active=True, category='tech')
        self.p2 = Post(title='Inactive Post Detail', content='...', is_active=False, category='news')
        db.session.add_all([self.p1, self.p2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_detail_post_active(self):
        """Тест: Чи можна переглянути активний пост?"""
        response = self.client.get(f'/post/{self.p1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Active Post Detail', response.data)

    def test_detail_post_inactive(self):
        """Тест: Чи повертає 404 при спробі перегляду неактивного поста?"""
        # Ваша функція detail_post використовує first_or_404(is_active=True)
        response = self.client.get(f'/post/{self.p2.id}')
        self.assertEqual(response.status_code, 404)
        
    def test_detail_post_non_existent(self):
        """Тест: Чи повертає 404, якщо поста не існує?"""
        response = self.client.get('/post/9999')
        self.assertEqual(response.status_code, 404)