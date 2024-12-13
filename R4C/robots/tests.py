# robots/tests.py

from django.test import TestCase
from django.core import mail
from robots.models import Robot
from orders.models import Order
from customers.models import Customer

class RobotSignalTest(TestCase):

    def setUp(self):
        # Создаем клиента
        self.customer = Customer.objects.create(email="customer@example.com")
        
        # Создаем заказ для робота, которого пока нет в наличии
        self.order = Order.objects.create(customer=self.customer, robot_serial="R2-D2")

        # Создаем робота
        self.robot = Robot.objects.create(
            serial="R2-D2",
            model="R2",
            version="D2",
            created="2022-12-31 23:59:59"
        )

    def test_email_sent_on_robot_creation(self):
        # Проверяем, что нет отправленных писем до создания робота
        self.assertEqual(len(mail.outbox), 0)

        # Сохраняем робота (это должно вызвать сигнал)
        self.robot.save()

        # Теперь проверяем, что письмо было отправлено
        self.assertEqual(len(mail.outbox), 1)

        # Проверяем содержание письма
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Робот теперь в наличии!')
        self.assertIn("Робот модели R2, версии D2", email.body)
        self.assertEqual(email.to, ["customer@example.com"])

