from webSite.models import User, Order, Profile

from django.contrib import admin



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('personal_info', )

# admin.site.register(User, OrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)
