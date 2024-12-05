from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Snippet

@receiver(signal= post_save, sender= Snippet)
def snippets_cache_delete(sender, instance, created, **kwarg):
    if not created:
        cache_key = f'snippet_id:{instance.id}'
        cache.delete(cache_key)

@receiver(signal= post_delete, sender= Snippet)
def snippets_cache_delete(sender, instance, **kwargs):
    cache_key = f'snippet_id:{instance.id}'
    cache.delete(cache_key)