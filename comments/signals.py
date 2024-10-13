from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment

@receiver(post_save, sender=Comment)
def increase_reply_count(sender, instance, created, **kwargs):
    # If the comment is a reply, increase the reply count for the parent comment
    if created and instance.parent_comment:
        parent_comment = instance.parent_comment
        parent_comment.reply_count += 1  # increment
        parent_comment.save(update_fields=['reply_count'])

@receiver(post_delete, sender=Comment)
def decrease_reply_count(sender, instance, **kwargs):
    # If the comment is a reply, decrease the reply count for the parent comment
    if instance.parent_comment:
        parent_comment = instance.parent_comment
        parent_comment.reply_count -= 1  # decrement
        parent_comment.save(update_fields=['reply_count'])
