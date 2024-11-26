from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from snippets.views import SnippetViewSet, UserSnippetList, ShareUnlistedSnippetView, LoginUserSnippet
snippetRouter = DefaultRouter()
snippetRouter.register(r'', SnippetViewSet, basename= 'snippet')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),

    #snippet endpoint
    path('api/v1/snippets/my/', LoginUserSnippet.as_view(), name='login-user-snippet'),
    path('api/v1/snippets/user/<str:username>/', UserSnippetList.as_view(), name='users-snippet'),
    path('api/v1/snippets/share/<token>/', ShareUnlistedSnippetView.as_view(), name='share-unlisted-snappet'),
    # Snippet CRUD routes from router
    path('api/v1/snippets/', include(snippetRouter.urls)),



    path('api/comments/', include('comments.urls')),
    path('api/users/', include('users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns