from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name','profile_image', 'cover_image', 'bio', 'about', 'followers', 'following', 'total_post')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'joining_date', 'last_update')}),
    )

    ordering = ('email',)
    readonly_fields = ('last_login', 'joining_date', 'last_update', 'followers', 'following', 'total_post')

    add_fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
