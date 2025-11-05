import unittest
from app import app

class PostBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_post_list_page(self):
        """
        Перевірка, чи сторінка зі списком постів завантажується (200 OK) 
        """
        # Виконуємо GET-запит до кореневого маршруту блюпринта постів (/)
        response = self.client.get("/posts/")
        
        # Перевіряємо, чи статус коду відповіді є 200 (OK)
        self.assertEqual(response.status_code, 200)

    # --- Тести для детальної сторінки поста (@post_bp.route('/<int:id>')) ---

    def test_detail_post_success(self):
        """
        Перевірка, чи детальна сторінка поста з ID=1 завантажується (200 OK) 
        та містить очікуваний контент.
        """
        # Виконуємо GET-запит до поста з ID 1
        response = self.client.get("/posts/1")
        
        self.assertEqual(response.status_code, 200)
        
        response_data = response.data.decode('utf-8')
        
        # Перевіряємо, чи відображається контент першого поста
        self.assertIn("This is the content of my first post.", response_data)
        self.assertIn("My First Post", response_data)
        
    def test_detail_post_404(self):
        """
        Перевірка, чи запит до неіснуючого поста (ID=99) повертає 404 Not Found.
        (Згідно з логікою блюпринта, id > 3 має викликати 404)
        """
        # Виконуємо GET-запит до поста з неіснуючим ID (4 або більше)
        response = self.client.get("/4")
        # Перевіряємо, чи статус коду відповіді є 404
        self.assertEqual(response.status_code, 404)
        # Опціонально: перевіряємо, чи тіло відповіді містить загальний текст помилки
        response_data = response.data.decode('utf-8')
        self.assertIn("Not Found", response_data)

if __name__ == "__main__":
    unittest.main()