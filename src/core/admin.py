from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from core.models import UserProfile


from django.contrib.admin import AdminSite


admin.site.site_url = "https://gsnap.ctagroup.org"


class UserProfileInline(admin.TabularInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.site_header = "SNAP Admin"
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.unregister(Token)
