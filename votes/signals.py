from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
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

        #save changes
        if instance.comment:
            # Save the updated comment
            instance.comment.save()
        else:
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
        
        # Save the updated vote counts for the related snippet or comment
        if instance.comment:
            instance.comment.save()
        else:
            instance.snippet.save()

# Triggered after a Vote is deleted
@receiver(post_delete, sender=Vote)
def handle_vote_delete(sender, instance, **kwargs):
    # Check if the deleted vote was an upvote
    if instance.vote_type == 'upvote':
        # If the vote is associated with a snippet, decrement its upvote count
        if instance.snippet:
            instance.snippet.upvotes -= 1
        # If the vote is associated with a comment, decrement its upvote count
        elif instance.comment:
            instance.comment.upvotes -= 1
        
    # Check if the deleted vote was a downvote
    elif instance.vote_type == 'downvote':
        # If the vote is associated with a snippet, decrement its downvote count
        if instance.snippet:
            instance.snippet.downvotes -= 1
        # If the vote is associated with a comment, decrement its downvote count
        elif instance.comment:
            instance.comment.downvotes -= 1
    
    # Save the updated vote counts for the related snippet or comment
    if instance.snippet:
        instance.snippet.save(update_fields=['upvotes', 'downvotes'])
    elif instance.comment:
        instance.comment.save(update_fields=['upvotes', 'downvotes'])


@receiver(post_save, sender= Vote)
def invalid_vote_cache(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.snippet and not instance.comment:
            cache_key = f'snippet_vote:{instance.snippet.id}'
            cache.delete(cache_key)
        elif instance.comment:
            cache_key = f'comment_vote:{instance.comment.id}'
            print(cache_key)
            cache.delete(cache_key)

@receiver(post_delete, sender= Vote)
def invalid_vote_cache(sender, instance, *args, **kwargs):
    if instance.snippet and not instance.comment:
            cache_key = f'snippet_vote:{instance.snippet.id}'
            cache.delete(cache_key)
    elif instance.comment:
        cache_key = f'comment_vote:{instance.comment.id}'
        print(cache_key)
        cache.delete(cache_key)