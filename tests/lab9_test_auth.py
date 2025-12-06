import unittest
from app import create_app, db
from app.users.models import User

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        """Налаштування перед кожним тестом"""
        # Використовуємо конфігурацію 'test', де WTF_CSRF_ENABLED = False
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Створюємо таблиці
        db.create_all()
        
        self.client = self.app.test_client()

    def tearDown(self):
        """Очищення після кожного тесту"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # ---------------------------------------------------------
    # 1. Перевірка завантаження сторінок (Views Tests)
    # ---------------------------------------------------------
    
    def test_register_page_loads(self):
        """Тест: сторінка реєстрації завантажується успішно (GET)"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        # Перевіряємо наявність тексту з шаблону register.html
        self.assertIn(b'Register', response.data)

    def test_login_page_loads(self):
        """Тест: сторінка входу завантажується успішно (GET)"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        # Перевіряємо наявність тексту з шаблону login.html
        self.assertIn(b'Login', response.data)

    # ---------------------------------------------------------
    # 2. Тестування реєстрації (Saving User to DB)
    # ---------------------------------------------------------

    def test_register_user_success(self):
        """Тест: успішна реєстрація користувача та збереження в БД"""
        # Дані для форми
        user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        }
        
        response = self.client.post('/register', data=user_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ваш акаунт створено'.encode('utf-8'), response.data)
        
        # ГОЛОВНЕ: Перевіряємо, чи з'явився юзер у базі даних
        user = User.query.filter_by(email='new@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')
        # Перевіряємо, що пароль захешовано (не дорівнює чистому тексту)
        self.assertNotEqual(user.password, 'pass123')

    def test_register_duplicate_email(self):
        """Тест: неможна зареєструватись з існуючим email"""
        # 1. Створюємо користувача вручну
        existing_user = User(username='olduser', email='exist@test.com', password='password')
        db.session.add(existing_user)
        db.session.commit()

        # 2. Пробуємо зареєструвати нового з тим самим email
        response = self.client.post('/register', data={
            'username': 'newuser2',
            'email': 'exist@test.com', # Той самий email
            'password': 'pass123',
            'confirm_password': 'pass123'
        }, follow_redirects=True)

        # Перевіряємо, що ми залишились на сторінці (або отримали помилку форми)
        # У forms.py є валідація: "Ця електронна пошта вже зареєстрована"
        self.assertIn('Ця електронна пошта вже зареєстрована'.encode('utf-8'), response.data)

    # ---------------------------------------------------------
    # 3. Тестування входу та виходу (Login & Logout)
    # ---------------------------------------------------------

    def test_login_success(self):
        """Тест: успішний вхід користувача"""
        # 1. Створюємо користувача (пароль треба хешувати, як у views.py)
        password = 'pass123'
        hashed_pwd = User.hash_password(password)
        user = User(username='loginuser', email='login@test.com', password=hashed_pwd)
        db.session.add(user)
        db.session.commit()

        # 2. Логінимось
        response = self.client.post('/login', data={
            'username': 'loginuser', # Форма приймає username або email
            'password': password
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        # Перевіряємо повідомлення про успішний вхід
        self.assertIn('Вхід успішно виконано'.encode('utf-8'), response.data)
        # Перевіряємо, що в сесії з'явився user_id (або ми на сторінці профілю)
        self.assertIn(b'Welcome, loginuser!', response.data) # Це є в profile.html

    def test_login_invalid_password(self):
        """Тест: помилка при неправильному паролі"""
        # Створюємо юзера
        user = User(username='user2', email='u2@test.com', password=User.hash_password('pass123'))
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data={
            'username': 'user2',
            'password': 'wrong12'
        }, follow_redirects=True)

        # Перевіряємо повідомлення про помилку (з views.py)
        self.assertIn("Неправильне ім&#39;я користувача або пароль".encode('utf-8'), response.data)

    def test_logout(self):
        """Тест: вихід із системи"""
        # 1. Спочатку логінимось (можна використати helper method, але розпишемо явно)
        password = 'pass'
        user = User(username='logoutuser', email='out@test.com', password=User.hash_password(password))
        db.session.add(user)
        db.session.commit()

        self.client.post('/login', data={'username': 'logoutuser', 'password': password}, follow_redirects=True)

        # 2. Робимо вихід
        response = self.client.get('/logout', follow_redirects=True)

        # 3. Перевіряємо редірект на логін і повідомлення
        self.assertIn('You have been logged out'.encode('utf-8'), response.data)
        # Перевіряємо, що ми знову бачимо форму логіну
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()