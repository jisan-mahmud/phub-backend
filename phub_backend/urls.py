from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/snippets/', include('snippets.urls')),

    # Nested comment routes: include comment-related URLs under /snippets/<snippet_id>/comments/
    path('api/snippets/<int:snippet_id>/comments/', include('comments.urls')),

    # Nested vote routes: include vote-related URLs under /snippets/<snippet_id>/vote/
    path('api/snippets/<int:snippet_id>/vote/', include('votes.urls')),
    # Nested vote routes: include vote-related URLs under /comments/<comment_id>/vote/
    path('api/comments/<int:comment_id>/vote/', include('votes.urls')),
    
    path('api/users/', include('users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns