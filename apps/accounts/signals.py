from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

@receiver(pre_save, sender=User)
def store_old_is_organizer_pending(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_user = User.objects.get(pk=instance.pk)
            instance._old_is_organizer_pending = old_user.is_organizer_pending
        except User.DoesNotExist:
            instance._old_is_organizer_pending = None

@receiver(post_save, sender=User)
def send_email_when_organizer_confirmed(sender, instance, created, **kwargs):
    if created:
        return

    # Oldingi qiymat True emas edi, yangi qiymat True bo‘ldi
    if hasattr(instance, '_old_is_organizer_pending') and not instance._old_is_organizer_pending and instance.is_organizer_pending:
        send_mail(
            subject="Tashkilotchi sifatida tasdiqlandingiz",
            message="Siz endi tashkilotchi sifatida tasdiqlandingiz!",
            from_email="jamshidbekshodibekov2004@gmail.com",
            recipient_list=[instance.email],
        )
