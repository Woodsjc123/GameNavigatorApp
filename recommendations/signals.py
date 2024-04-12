from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=UserProfile)
def update_user_recommendations(sender, instance, **kwargs):
    from recommendations import update_recommendations_for_user
    update_recommendations_for_user(instance.user)
