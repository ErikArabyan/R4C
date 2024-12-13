# robots/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Robot
from orders.models import Order
from django.conf import settings

@receiver(post_save, sender=Robot)
def send_robot_availability_email(sender, instance, created, **kwargs):
    if created:
        # Получаем все заказы на роботов, которые еще не были выполнены
        orders = Order.objects.filter(robot_serial=instance.serial)
        for order in orders:
            send_mail(
                'Робот теперь в наличии!',
                f'Добрый день!\n\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}. Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.',
                settings.EMAIL_HOST_USER,
                [order.customer.email],
                fail_silently=False
            )
