from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Vote

# Triggered before saving a Vote (update or create)
@receiver(pre_save, sender=Vote)
def check_previous_vote(sender, instance, **kwargs):
    # If updating an existing vote
    if instance.pk:
        if instance.vote_type == 'upvote':
            # Ensure it's related to a snippet (and not a comment) before updating counts
            if instance.snippet and not instance.comment:
                instance.snippet.downvotes -= 1
                instance.snippet.upvotes += 1

            # Ensure it's related to a comment before updating counts
            elif instance.comment:
                instance.comment.downvotes -= 1
                instance.comment.upvotes += 1

        elif instance.vote_type == 'downvote':
            # Ensure it's related to a snippet (and not a comment) before updating counts
            if instance.snippet and not instance.comment:
                instance.snippet.upvotes -= 1
                instance.snippet.downvotes += 1

            # Ensure it's related to a comment before updating counts
            elif instance.comment:
                instance.comment.upvotes -= 1
                instance.comment.downvotes += 1

        # Save the updated snippet
        instance.snippet.save()
    
    # If creating a new vote
    else:  
        if instance.vote_type == 'upvote':
            # Ensure it's related to a snippet (and not a comment) before updating counts
            if instance.snippet and not instance.comment:
                instance.snippet.upvotes += 1
            
            # Ensure it's related to a comment before updating counts
            elif instance.comment:
                instance.comment.upvotes += 1

        elif instance.vote_type == 'downvote':
            # Ensure it's related to a snippet (and not a comment) before updating counts
            if instance.snippet and not instance.comment:
                instance.snippet.downvotes += 1
            
            # Ensure it's related to a comment before updating counts
            elif instance.comment:
                instance.comment.downvotes += 1
        
        # Save the updated snippet
        instance.snippet.save()  

# Triggered after a Vote is deleted
@receiver(post_delete, sender=Vote)
def handle_vote_delete(sender, instance, **kwargs):
    print(f"Vote deleted: {instance.vote_type}")
