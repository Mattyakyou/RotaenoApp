from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User

@receiver(post_save, sender=UserSocialAuth)
def user_social_login(sender, instance, **kwargs):
    # Discordのログイン時にユーザーを切り替え
    if instance.provider == 'discord':
        user = instance.user
        user.email = instance.extra_data.get('email', '')
        user.save()

