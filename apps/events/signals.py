from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
import threading

from .models import Event

def send_email(participant, instance: Event):
    subject = "Tadbir ma'lumotlari o'zgardi"
    message = (
        f"Hurmatli {participant.get_full_name()},\n\n"
        f"{instance.title} nomli tadbir sanasi {instance.date} etib belgilandi.\n"
        f"Joylashuv: {instance.location}\n\n"
        f"Hurmat bilan,\nEventHub jamoasi"
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=instance.owner.email,
            recipient_list=[participant.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {participant.email} - {e}")


@receiver(post_save, sender=Event)
def event_updated(sender, instance, created, **kwargs):
    if created:
        return

    def notify_all():
        for participant in instance.participants.all():
            send_email(participant, instance)

    thread = threading.Thread(target=notify_all)
    thread.start()
    
