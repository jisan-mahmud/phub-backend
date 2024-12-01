from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Snippet

@receiver(signal= post_save, sender= Snippet)
def snippets_cache_delete(sender, instance, created, **kwarg):

    if not created:
        cache_key = f'snippet_id:{instance.id}'
        cache.delete(cache_key)

    total_pages = Snippet.objects.all().count() // 8
    cache_page_key = f'snippets_list_page:{None}'
    for i in range(1, total_pages + 2):
        cache.delete(cache_page_key)
        cache_page_key = f'snippets_list_page:{i}'

@receiver(signal= post_delete, sender= Snippet)
def snippets_cache_delete(sender, instance, **kwargs):

    ## snippets all pagination delete from cache
    total_pages = Snippet.objects.all().count() // 8
    cache_page_key = f'snippets_list_page:{None}'
    for i in range(1, total_pages + 2):
        cache.delete(cache_page_key)
        cache_page_key = f'snippets_list_page:{i}'

    #specific snippet delete from cache
    cache_key = f'snippet_id:{instance.id}'
    cache.delete(cache_key)