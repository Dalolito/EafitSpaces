from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation, Notifications

@receiver(post_save, sender=Reservation)
def create_notification(sender, instance, created, **kwargs):
    if created:  # Esto asegura que solo se cree la notificación cuando se crea una nueva reserva
        Notifications.objects.create(
            user_id=instance.user_id,
            message=f'A new reservation has been created for the space {instance.space_id}.',
            reservation=instance
        )
