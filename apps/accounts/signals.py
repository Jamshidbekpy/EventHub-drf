from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@receiver(post_save, sender=User)
def send_email_when_organizer_confirmed(sender, instance, created, **kwargs):
    if created:
        return

    try:
        old_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    if not old_user.is_organizer_pending and instance.is_organizer_pending:
        send_mail(
            subject="Tashkilotchi sifatida tasdiqlandingiz",
            message="Siz endi tashkilotchi sifatida tasdiqlandingiz!",
            from_email="jamshidbekshodibekov2004@gmail.com",
            recipient_list=[instance.email],
        )
