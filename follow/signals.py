from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Follow

@receiver(post_save, sender= Follow)
def increase_followers_and_following(sender, instance, created, **kwargs):
    if created:
        followed_user = instance.followed
        follower_user = instance.follower

        followed_user.followers = F('followers') + 1
        followed_user.save(update_fields=['followers'])

        follower_user.following = F('following') + 1
        follower_user.save(update_fields= ['following'])

@receiver(post_delete, sender= Follow)
def decrease_followers_and_following(sender, instance, **kwargs):
    followed_user = instance.followed
    follower_user = instance.follower

    followed_user.followers = F('followers') - 1
    followed_user.save(update_fields=['followers'])

    follower_user.following = F('following') - 1
    follower_user.save(update_fields= ['following'])