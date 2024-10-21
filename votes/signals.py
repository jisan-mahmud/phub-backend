from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Vote

@receiver(pre_save, sender=Vote)
def check_previous_vote(sender, instance, **kwargs):
    # This signal is triggered before saving a vote
    if instance.pk:
        previous_vote = Vote.objects.get(pk=instance.pk)
        print(f"Previous vote: {previous_vote.vote_type}")
        # Logic here if you want to check or compare the previous vote
    else:
        print("This is a new vote being created.")


@receiver(post_delete, sender=Vote)
def handle_vote_delete(sender, instance, **kwargs):
    # This signal is triggered after a vote is deleted
    print(f"Vote deleted: {instance.vote_type}")
    # Logic for decreasing the vote count when a vote is removed
